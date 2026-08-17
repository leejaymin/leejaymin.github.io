#!/usr/bin/env python3
"""학회 논문 마감일 데이터를 상류 저장소에서 가져와 _data/conferences.yml 로 동기화한다.

상류 두 곳을 합친다.

- huggingface/ai-deadlines            : AI 학회 (에이전트가 주기적으로 갱신)
- casys-kaist/casys-kaist.github.io   : 컴퓨터 시스템/아키텍처 학회 (KAIST CASYS 관리)

두 상류는 스키마가 다르므로 하나의 형태로 정규화하고, 마감 시각을 UTC로 미리
변환해 둔다. 브라우저에서 타임존을 다시 계산할 필요 없이 Date 하나로 카운트다운
할 수 있도록 하기 위함이다.

사용법:

    python3 bin/sync_deadlines.py                    # 상류를 임시 디렉터리에 clone
    python3 bin/sync_deadlines.py --hf-dir DIR ...   # 이미 받아둔 clone 재사용
"""

import argparse
import datetime as dt
import glob
import os
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import yaml

HF_REPO = "https://github.com/huggingface/ai-deadlines"
HF_DATA_PATH = "src/data/conferences"
CASYS_REPO = "https://github.com/casys-kaist/casys-kaist.github.io"
CASYS_DATA_PATH = "_data/conferences"

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(REPO_ROOT, "_data", "conferences.yml")

DATE_FORMATS = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d")
TBA_WORDS = {"tba", "tbd", "n/a", "none", ""}

# CASYS 의 sub 코드를 상위 분류로 매핑한다. HF 쪽은 전부 AI 로 본다.
CASYS_AREA = {"ARCH": "Systems", "SYS": "Systems", "ML": "AI", "OTHER": "Other"}
CASYS_TAG = {
    "ARCH": "computer-architecture",
    "SYS": "systems",
    "ML": "machine-learning",
    "OTHER": "other",
}


def sparse_clone(repo, data_path, dest):
    """상류 저장소에서 데이터 디렉터리만 얇게 받아온다."""
    subprocess.run(
        ["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse", repo, dest],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        ["git", "-C", dest, "sparse-checkout", "set", data_path],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return os.path.join(dest, data_path)


def load_yaml_dir(path):
    entries = []
    for f in sorted(glob.glob(os.path.join(path, "*.yml"))):
        with open(f, encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or []
        if isinstance(data, list):
            entries.extend(x for x in data if isinstance(x, dict))
    return entries


def resolve_timezone(tz):
    """상류에서 쓰는 여러 타임존 표기를 tzinfo 로 변환한다."""
    if not tz:
        return dt.timezone.utc
    tz = str(tz).strip()

    # Anywhere on Earth = UTC-12. 가장 늦게 마감되는 기준시.
    if tz.upper() == "AOE":
        return dt.timezone(dt.timedelta(hours=-12))
    fixed = {"PST": -8, "PDT": -7, "EST": -5, "EDT": -4, "CET": 1, "CEST": 2, "KST": 9}
    if tz.upper() in fixed:
        return dt.timezone(dt.timedelta(hours=fixed[tz.upper()]))

    m = re.fullmatch(r"(?:UTC|GMT)\s*([+-])\s*(\d{1,2})(?::?(\d{2}))?", tz, re.I)
    if m:
        sign = 1 if m.group(1) == "+" else -1
        hours, minutes = int(m.group(2)), int(m.group(3) or 0)
        return dt.timezone(sign * dt.timedelta(hours=hours, minutes=minutes))
    if tz.upper() in ("UTC", "GMT"):
        return dt.timezone.utc

    try:
        return ZoneInfo(tz)
    except (ZoneInfoNotFoundError, ValueError):
        return dt.timezone.utc


def to_utc(date_str, tz):
    """'2026-08-28 11:00:00' + 타임존 → UTC ISO 문자열. 실패하면 None."""
    if not date_str:
        return None
    s = str(date_str).strip().strip("'\"")
    if s.lower() in TBA_WORDS:
        return None
    for fmt in DATE_FORMATS:
        try:
            naive = dt.datetime.strptime(s, fmt)
            break
        except ValueError:
            continue
    else:
        return None
    aware = naive.replace(tzinfo=resolve_timezone(tz))
    return aware.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_day(value):
    if not value:
        return None
    s = str(value).strip().strip("'\"")
    try:
        return dt.date.fromisoformat(s[:10])
    except ValueError:
        return None


def normalize_tag(tag):
    return re.sub(r"\s+", "-", str(tag).strip().lower())


def base_title(title):
    """'ASPLOS (Fall)' → 'ASPLOS'. 같은 학회의 여러 라운드를 묶기 위한 키."""
    return re.sub(r"\s*\(.*?\)\s*", " ", str(title or "")).strip().upper()


def round_label(title):
    m = re.search(r"\((.*?)\)", str(title or ""))
    return m.group(1).strip().lower() if m else ""


def build_deadlines(entry, source):
    """상류 두 스키마를 공통 deadlines 배열로 정규화한다."""
    default_tz = entry.get("timezone")
    out = []
    seen = set()

    for d in entry.get("deadlines") or []:
        if not isinstance(d, dict):
            continue
        kind = str(d.get("type") or "submission")
        utc = to_utc(d.get("date"), d.get("timezone") or default_tz)
        out.append(
            {
                "type": kind,
                "label": d.get("label") or kind.replace("_", " ").title(),
                "date": str(d.get("date") or "").strip("'\""),
                "timezone": d.get("timezone") or default_tz or "UTC",
                "utc": utc,
            }
        )
        seen.add(kind)

    # CASYS 및 HF 구버전은 마감일이 평평한 필드로 들어 있다.
    legacy = [
        ("abstract", "Abstract Deadline", entry.get("abstract_deadline")),
        ("submission", "Paper Submission", entry.get("deadline")),
        ("commitment", "Commitment", entry.get("commitment_deadline")),
    ]
    for kind, label, value in legacy:
        if kind in seen or not value:
            continue
        utc = to_utc(value, default_tz)
        if utc is None:
            continue
        out.append(
            {
                "type": kind,
                "label": label,
                "date": str(value).strip("'\""),
                "timezone": default_tz or "UTC",
                "utc": utc,
            }
        )
        seen.add(kind)

    out = [d for d in out if d["utc"]]
    out.sort(key=lambda d: d["utc"])
    return out


def normalize(entry, source):
    title = str(entry.get("title") or "").strip()
    year = entry.get("year")
    if not title or not year:
        return None

    deadlines = build_deadlines(entry, source)

    if source == "casys":
        subs = entry.get("sub") or []
        if isinstance(subs, str):
            subs = [s.strip() for s in subs.split(",") if s.strip()]
        subs = [str(s).strip().upper() for s in subs]
        areas = sorted({CASYS_AREA[s] for s in subs if s in CASYS_AREA}) or ["Systems"]
        tags = sorted({CASYS_TAG[s] for s in subs if s in CASYS_TAG})
        tba = bool(entry.get("tba")) or "TBD" in subs
        place = entry.get("place")
    else:
        areas = ["AI"]
        tags = sorted({normalize_tag(t) for t in (entry.get("tags") or [])})
        tba = bool(entry.get("tba"))
        place = entry.get("place") or ", ".join(
            x for x in (entry.get("city"), entry.get("country")) if x
        )

    record = {
        "id": str(entry.get("id") or f"{base_title(title).lower()}{str(year)[-2:]}"),
        "title": title,
        "year": int(year),
        "areas": areas,
        "tags": tags,
        "deadlines": deadlines,
        "source": source,
    }
    for key, value in (
        ("full_name", entry.get("full_name")),
        ("link", entry.get("link")),
        ("place", place),
        ("date", entry.get("date")),
        ("start", entry.get("start")),
        ("end", entry.get("end")),
        ("note", entry.get("note")),
        ("hindex", entry.get("hindex")),
    ):
        if value not in (None, ""):
            record[key] = str(value).strip("'\"") if key in ("start", "end") else value
    if tba:
        record["tba"] = True
    return record


def dedupe(records):
    """두 상류에 함께 있는 학회를 정리한다.

    같은 (학회, 연도)에 대해 라운드를 더 많이 관리하는 쪽을 채택한다.
    ASPLOS 처럼 연 2~3회 마감이 있는 학회는 CASYS 가, 나머지는 대체로
    자동 갱신되는 HF 가 더 정확하기 때문이다.
    """
    groups = defaultdict(lambda: defaultdict(list))
    for r in records:
        groups[(base_title(r["title"]), r["year"])][r["source"]].append(r)

    merged = []
    for buckets in groups.values():
        hf, casys = buckets.get("ai-deadlines", []), buckets.get("casys", [])
        if not hf:
            chosen = casys
        elif not casys:
            chosen = hf
        elif len(casys) > len(hf):
            chosen = casys
        elif len(hf) > len(casys):
            chosen = hf
        else:
            # 1:1 이면 마감 정보가 더 충실한 쪽. 동률이면 HF.
            chosen = hf if len(hf[0]["deadlines"]) >= len(casys[0]["deadlines"]) else casys

        # 채택되지 않은 쪽의 분류는 살려 둔다 (예: ICML 은 AI 이면서 Systems 목록에도 있음).
        others = [r for r in hf + casys if r not in chosen]
        if others and len(chosen) == 1:
            extra_areas = {a for r in others for a in r["areas"]}
            chosen[0]["areas"] = sorted(set(chosen[0]["areas"]) | extra_areas)
        merged.extend(chosen)
    return merged


def prune_and_sort(records, today):
    """지난 학회는 버리고, 다가오는 마감 순으로 정렬한다."""
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    kept = []
    for r in records:
        upcoming = [d["utc"] for d in r["deadlines"] if d["utc"] > now]
        end = parse_day(r.get("end")) or parse_day(r.get("start"))
        if end is not None:
            alive = end >= today
        else:
            # 개최 일정이 아직 공지되지 않은 학회는 연도로만 판단한다.
            alive = r["year"] >= today.year
        if not upcoming and not alive:
            continue
        if upcoming:
            r["next_deadline"] = min(upcoming)
        kept.append(r)

    far_future = "9999"
    kept.sort(key=lambda r: (r.get("next_deadline", far_future), r["title"], r["year"]))
    return kept


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf-dir", help="이미 받아둔 ai-deadlines clone 경로")
    ap.add_argument("--casys-dir", help="이미 받아둔 casys-kaist.github.io clone 경로")
    ap.add_argument("--output", default=OUTPUT)
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        if args.hf_dir:
            hf_path = os.path.join(args.hf_dir, HF_DATA_PATH)
        else:
            hf_path = sparse_clone(HF_REPO, HF_DATA_PATH, os.path.join(tmp, "hf"))
        if args.casys_dir:
            casys_path = os.path.join(args.casys_dir, CASYS_DATA_PATH)
        else:
            casys_path = sparse_clone(
                CASYS_REPO, CASYS_DATA_PATH, os.path.join(tmp, "casys")
            )

        raw = [(e, "ai-deadlines") for e in load_yaml_dir(hf_path)]
        raw += [(e, "casys") for e in load_yaml_dir(casys_path)]

    records = [n for n in (normalize(e, s) for e, s in raw) if n]
    records = dedupe(records)
    records = prune_and_sort(records, dt.date.today())

    if not records:
        print("동기화 결과가 비어 있어 기존 파일을 유지한다.", file=sys.stderr)
        return 1

    header = (
        "# 이 파일은 bin/sync_deadlines.py 가 생성한다. 직접 수정하지 말 것.\n"
        "#\n"
        "# 출처:\n"
        f"#   - {HF_REPO} (MIT License)\n"
        f"#   - {CASYS_REPO}\n"
        "#\n"
        "# 갱신: .github/workflows/sync-deadlines.yml 이 매주 실행하며,\n"
        "#       수동 실행은 `python3 bin/sync_deadlines.py`.\n"
    )
    body = yaml.safe_dump(
        records, allow_unicode=True, sort_keys=False, default_flow_style=False, width=100
    )
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(header + "\n" + body)

    by_area = defaultdict(int)
    for r in records:
        for a in r["areas"]:
            by_area[a] += 1
    summary = ", ".join(f"{a} {n}건" for a, n in sorted(by_area.items()))
    print(f"학회 {len(records)}건 기록 ({summary}) → {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
