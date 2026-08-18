#!/usr/bin/env python3
"""학회 논문 마감일 데이터를 공개 저장소에서 가져와 _data/conferences.yml 로 동기화한다.

AI 학회 목록과 컴퓨터 시스템/아키텍처 학회 목록을 각각 유지하는 공개 저장소 두 곳을
읽어 하나로 합친다. 두 곳은 스키마가 다르므로 공통 형태로 정규화하고, 마감 시각을
UTC로 미리 변환해 둔다. 브라우저에서 타임존을 다시 계산할 필요 없이 Date 하나로
카운트다운할 수 있도록 하기 위함이다.

HF_REPO 의 데이터는 MIT License 로 배포된다 (Copyright (c) 2025 Hugging Face).

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
import urllib.request
from collections import defaultdict
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import yaml

HF_REPO = "https://github.com/huggingface/ai-deadlines"
HF_DATA_PATH = "src/data/conferences"
CASYS_REPO = "https://github.com/casys-kaist/casys-kaist.github.io"
CASYS_DATA_PATH = "_data/conferences"
IDSL_URL = "https://idsl.seoultech.ac.kr/js/conference-board-data.js"

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(REPO_ROOT, "_data", "conferences.yml")

DATE_FORMATS = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d")
TBA_WORDS = {"tba", "tbd", "n/a", "none", ""}

# 같은 학회를 다르게 부르는 경우를 묶어 준다. 중복 판정에만 쓴다.
TITLE_ALIASES = {"MM": "ACM MM", "IJCAI-ECAI": "IJCAI", "ACM-MM": "ACM MM"}

# CASYS 의 sub 코드를 상위 분류로 매핑한다. HF 쪽은 전부 AI 로 본다.
CASYS_AREA = {"ARCH": "Systems", "SYS": "Systems", "ML": "AI", "OTHER": "Other"}
CASYS_TAG = {
    "ARCH": "computer-architecture",
    "SYS": "systems",
    "ML": "machine-learning",
    "OTHER": "other",
}

# IDSL 데이터에는 분야 정보가 없어 약어로 분류한다. 목록에 없는 약어는 Other 로
# 두고 실행 시 경고를 남기므로, 새 학회가 추가되면 여기에 넣어 주면 된다.
IDSL_AI = {
    "AAAI", "ACCV", "ACL", "ACM MM", "AISTATS", "BMVC", "COLING", "CVPR", "ECAI",
    "ECCV", "EMNLP", "ICASSP", "ICCV", "ICLR", "ICML", "ICPR", "IJCAI",
    "INTERSPEECH", "NAACL", "NEURIPS", "SIGIR", "UAI",
}
IDSL_SYSTEMS = {
    "ASPLOS", "ASSCC", "CGO", "DAC", "DATE", "EUROSYS", "FPGA", "FPT", "HIPC",
    "HPCA", "HPDC", "ICCAD", "ICPP", "IISWC", "ISCA", "ISCAS", "ISICAS",
    "ISLPED", "ISPASS", "MASCOTS", "MICRO", "PACT", "PPOPP", "VLSI",
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


def fetch_idsl(url):
    """세 번째 출처의 데이터 파일을 받아 온다. 실패해도 동기화 전체를 막지는 않는다."""
    request = urllib.request.Request(url, headers={"User-Agent": "sync-deadlines/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=60) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as exc:  # 네트워크/서버 문제로 나머지 출처까지 잃지 않도록 한다.
        print(f"경고: 추가 출처를 가져오지 못했다 ({exc}). 나머지 출처로만 진행한다.",
              file=sys.stderr)
        return None


def parse_idsl(text):
    """`window.conferenceBoardData = [...]` 형태의 JS 객체 배열을 읽는다.

    키가 따옴표 없이 쓰인 JS 리터럴이라 JSON 으로 바로 읽을 수 없어, 항목 단위로
    끊은 뒤 필요한 필드만 뽑는다. 항목이 추가돼도 깨지지 않는다.
    """
    if not text:
        return []

    def field(block, key):
        m = re.search(key + r'\s*:\s*"([^"]*)"', block)
        return m.group(1).strip() if m else None

    entries = []
    for block in re.findall(r"\{\s*id\s*:.*?\n\s*\}", text, re.S):
        acronym = field(block, "acronym")
        if not acronym:
            continue

        conf_day = parse_day(field(block, "confDate"))
        year = conf_day.year if conf_day else None
        if year is None:
            m = re.search(r"-(\d{4})\b", field(block, "id") or "")
            year = int(m.group(1)) if m else None
        if year is None:
            continue

        due_block = re.search(r"submissionDue\s*:\s*\[([^\]]*)\]", block, re.S)
        dues = re.findall(r'"([^"]*)"', due_block.group(1)) if due_block else []
        dues = [d for d in dues if str(d).strip().lower() not in TBA_WORDS]

        deadlines = []
        for i, due in enumerate(dues, start=1):
            day = parse_day(due)
            if not day:
                continue
            label = "Paper Submission" if len(dues) == 1 else f"Paper Submission ({i})"
            deadlines.append(
                {
                    "type": "submission",
                    "label": label,
                    # 원본에 시각이 없어 이 분야에서 가장 흔한 마감 관례를 따른다.
                    "date": f"{day.isoformat()} 23:59:59",
                    "timezone": "AoE",
                }
            )

        entry = {
            "id": field(block, "id") or f"{acronym.lower()}{str(year)[-2:]}",
            "title": acronym,
            "year": year,
            "full_name": field(block, "name"),
            "link": field(block, "website"),
            "place": field(block, "location"),
            "deadlines": deadlines,
            "timezone": "AoE",
        }
        if conf_day:
            entry["start"] = conf_day.isoformat()
            entry["end"] = conf_day.isoformat()
            entry["date"] = conf_day.strftime("%B %d, %Y")
        if not deadlines:
            entry["tba"] = True
        entries.append(entry)
    return entries


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
    stripped = re.sub(r"\s*\(.*?\)\s*", " ", str(title or "")).strip().upper()
    return TITLE_ALIASES.get(stripped, stripped)


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

    if source == "idsl":
        acronym = base_title(title)
        if acronym in IDSL_AI:
            areas, tags = ["AI"], ["machine-learning"]
        elif acronym in IDSL_SYSTEMS:
            areas, tags = ["Systems"], ["systems"]
        else:
            areas, tags = ["Other"], []
            print(f"경고: '{title}' 은 분야를 알 수 없어 Other 로 둔다.", file=sys.stderr)
        tba = bool(entry.get("tba"))
        place = entry.get("place")
    elif source == "casys":
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


# 같은 학회가 여러 출처에 있을 때의 우선순위. 숫자가 작을수록 우선한다.
SOURCE_PRIORITY = {"ai-deadlines": 0, "casys": 1, "idsl": 2}


def dedupe(records):
    """여러 출처에 함께 있는 학회를 정리한다.

    같은 (학회, 연도)에 대해 라운드를 더 많이 관리하는 쪽을 채택하고, 라운드 수가
    같으면 마감 정보가 더 충실한 쪽을, 그마저 같으면 SOURCE_PRIORITY 순으로 고른다.
    ASPLOS 처럼 연 2~3회 마감이 있는 학회를 놓치지 않기 위함이다. 세 번째 출처는
    마감일이 날짜 단위라 정보량이 가장 적으므로, 사실상 다른 곳에 없는 학회를
    채워 넣는 역할만 한다.
    """
    groups = defaultdict(lambda: defaultdict(list))
    for r in records:
        groups[(base_title(r["title"]), r["year"])][r["source"]].append(r)

    merged = []
    for buckets in groups.values():
        def rank(item):
            source, group = item
            deadline_count = sum(len(r["deadlines"]) for r in group)
            return (len(group), deadline_count, -SOURCE_PRIORITY.get(source, 99))

        source, chosen = max(buckets.items(), key=rank)

        # 채택되지 않은 쪽의 분류는 살려 둔다 (예: ICML 은 AI 이면서 Systems 목록에도 있음).
        others = [r for s, g in buckets.items() if s != source for r in g]
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
    ap.add_argument("--idsl-file", help="이미 받아둔 추가 출처 데이터 파일 경로")
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

    if args.idsl_file:
        with open(args.idsl_file, encoding="utf-8") as fh:
            idsl_text = fh.read()
    else:
        idsl_text = fetch_idsl(IDSL_URL)
    idsl_entries = parse_idsl(idsl_text)
    raw += [(e, "idsl") for e in idsl_entries]

    records = [n for n in (normalize(e, s) for e, s in raw) if n]
    before = {r["source"]: 0 for r in records}
    for r in records:
        before[r["source"]] += 1
    records = dedupe(records)
    added = sum(1 for r in records if r["source"] == "idsl")
    print(f"추가 출처 {before.get('idsl', 0)}건 중 {added}건이 신규 (나머지는 중복)")
    records = prune_and_sort(records, dt.date.today())

    if not records:
        print("동기화 결과가 비어 있어 기존 파일을 유지한다.", file=sys.stderr)
        return 1

    # source 는 중복 제거 단계에서만 쓰이므로 출력에는 남기지 않는다.
    for r in records:
        r.pop("source", None)

    header = (
        "# 이 파일은 bin/sync_deadlines.py 가 생성한다. 직접 수정하지 말 것.\n"
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
