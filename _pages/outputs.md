---
layout: page
permalink: /outputs/
title: Outputs Ledger
description: 2026년 이후 연구실적 × 사사 과제 관리 (내부용, 검색 제외)
nav: false
sitemap: false
noindex: true
---

<!-- _pages/outputs.md : 데이터는 _plugins/project_outputs.rb 가 생성 -->
<style>
.ledger { width: 100%; font-size: 0.82rem; border-collapse: collapse; margin-bottom: 2rem; }
.ledger th, .ledger td { border-bottom: 1px solid var(--global-divider-color); padding: 0.4rem 0.5rem; vertical-align: top; text-align: left; }
.ledger th { white-space: nowrap; }
.ledger .missing { color: #d9534f; font-weight: 700; }
.ledger .num { text-align: center; }
.ledger-tools { margin-bottom: 0.8rem; }
</style>

{%- assign ledger = site.data.outputs_ledger %}
{%- assign cats = "intl_journal,intl_conf,domestic_journal,domestic_conf,patent_applied,patent_granted" | split: "," %}

<h2>과제별 사사 정보 및 실적 수</h2>
<div style="overflow-x:auto">
<table class="ledger">
  <thead><tr>
    <th>과제</th><th>key</th><th>과제번호</th><th>사사문구</th>
    <th class="num">국제저널</th><th class="num">국제학회</th><th class="num">국내저널</th><th class="num">국내학회</th><th class="num">특허출원</th><th class="num">특허등록</th>
  </tr></thead>
  <tbody>
  {%- assign projects = site.research | sort: "importance" | sort: "category" | reverse %}
  {%- for p in projects %}
  <tr>
    <td><a href="{{ p.url | relative_url }}">{{ p.title }}</a> <small>({{ p.category }})</small></td>
    <td><code>{{ p.key }}</code></td>
    <td>{% if p.grant_no and p.grant_no != "" %}{{ p.grant_no }}{% else %}<span class="missing">미입력</span>{% endif %}</td>
    {%- capture ack %}{{ p.ack_ko }}{{ p.ack_en }}{% endcapture %}
    <td>{% if ack != "" %}입력됨{% else %}<span class="missing">미입력</span>{% endif %}</td>
    {%- for c in cats %}
    {%- assign n = ledger | where: "category", c | where_exp: "it", "it.project_keys contains p.key" | size %}
    <td class="num">{% if n > 0 %}{{ n }}{% else %}·{% endif %}</td>
    {%- endfor %}
  </tr>
  {%- endfor %}
  </tbody>
</table>
</div>

<h2>2026년 이후 실적 목록</h2>
<div class="ledger-tools"><button type="button" class="btn btn-sm z-depth-0" id="ledger-csv">CSV 다운로드</button></div>
<div style="overflow-x:auto">
<table class="ledger" id="ledger-table">
  <thead><tr><th>연도</th><th>구분</th><th>제목</th><th>저자</th><th>발표처</th><th>사사 과제</th></tr></thead>
  <tbody>
  {%- for it in ledger %}
  <tr>
    <td>{{ it.year }}</td>
    <td>{{ it.label }}</td>
    <td>{% if it.url != "" %}<a href="{{ it.url | relative_url }}">{{ it.title }}</a>{% else %}{{ it.title }}{% endif %}</td>
    <td>{{ it.authors }}</td>
    <td>{{ it.venue }}</td>
    <td>{%- if it.projects.size == 0 %}<span class="missing">미기재</span>{% else %}{% for pr in it.projects %}{% if pr.url %}<a href="{{ pr.url | relative_url }}">{{ pr.title }}</a>{% else %}<span class="missing">{{ pr.key }}?</span>{% endif %}{% unless forloop.last %}<br>{% endunless %}{% endfor %}{% endif -%}</td>
  </tr>
  {%- endfor %}
  </tbody>
</table>
</div>

<script>
  document.getElementById('ledger-csv').addEventListener('click', function () {
    var rows = document.querySelectorAll('#ledger-table tr');
    var csv = Array.prototype.map.call(rows, function (tr) {
      return Array.prototype.map.call(tr.children, function (td) {
        var cell = td.cloneNode(true);
        Array.prototype.forEach.call(cell.querySelectorAll('br'), function (br) { br.replaceWith(' / '); });
        return '"' + cell.textContent.replace(/\s+/g, ' ').trim().replace(/"/g, '""') + '"';
      }).join(',');
    }).join('\r\n');
    var blob = new Blob(['﻿' + csv], { type: 'text/csv;charset=utf-8' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'outputs-ledger.csv';
    a.click();
  });
</script>
