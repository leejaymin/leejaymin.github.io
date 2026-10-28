---
layout: page
permalink: /publications/
title: Publications
description: (*) denotes corresponding authors.<br>  
  (**) denotes equal contributors.   
nav: true
nav_order: 2
---

<!-- _pages/publications.md -->
{% assign s = site.data.pub_stats %}
{% if s %}
<div class="publication-stats" id="publication-stats" data-by-year='{{ s.by_year | jsonify }}'>
  <div class="pub-stat">
    <span class="pub-stat-num">{{ s.scie }}</span>
    <span class="pub-stat-label">SCIE 저널</span>
  </div>
  <div class="pub-stat">
    <span class="pub-stat-num">{{ s.bk }}</span>
    <span class="pub-stat-label">BK21 학회</span>
  </div>
  <div class="pub-stat">
    <span class="pub-stat-num">{{ s.kiise }}</span>
    <span class="pub-stat-label">KIISE-CS 학회</span>
  </div>
  <div class="pub-stat">
    <span class="pub-stat-num" id="pub-recent5">{{ s.recent5 }}</span>
    <span class="pub-stat-label">최근 5년 SCIE·BK21·KIISE-CS (<span id="pub-recent5-range">{{ s.recent5_from }}–{{ s.current_year }}</span>)</span>
  </div>
  <div class="pub-stat">
    <span class="pub-stat-num" id="pub-recent3">{{ s.recent3 }}</span>
    <span class="pub-stat-label">최근 3년 SCIE·BK21·KIISE-CS (<span id="pub-recent3-range">{{ s.recent3_from }}–{{ s.current_year }}</span>)</span>
  </div>
</div>
<script>
  (function () {
    var el = document.getElementById('publication-stats');
    if (!el) return;
    var byYear;
    try { byYear = JSON.parse(el.getAttribute('data-by-year')); } catch (e) { return; }
    var cy = new Date().getFullYear();
    var sumFrom = function (from) {
      var t = 0;
      for (var y in byYear) { if (+y >= from && +y <= cy) { t += byYear[y]; } }
      return t;
    };
    document.getElementById('pub-recent5').textContent = sumFrom(cy - 4);
    document.getElementById('pub-recent3').textContent = sumFrom(cy - 2);
    document.getElementById('pub-recent5-range').textContent = (cy - 4) + '–' + cy;
    document.getElementById('pub-recent3-range').textContent = (cy - 2) + '–' + cy;
  })();
</script>
{% endif %}

<h2>All Peer-reviewed Journals and Proceedings</h2>

<div class="publications">

{% bibliography -f {{ site.scholar.bibliography }} %}

</div>

<h2>ISSUED PATENTS</h2>
<hr>
{% include domestic_pubs.html type="patent" status="granted" %}

{%- assign applied = site.data.domestic_pubs | where: "type", "patent" | where: "status", "applied" %}
{%- if applied.size > 0 %}
<h2>PATENT APPLICATIONS</h2>
<hr>
{% include domestic_pubs.html type="patent" status="applied" %}
{%- endif %}

<h2>Peer-reviewed Domestic Journals</h2>
<hr>
{% include domestic_pubs.html type="domestic_journal" %}

<h2>Domestic Conference</h2>
<hr>
{% include domestic_pubs.html type="domestic_conf" %}
