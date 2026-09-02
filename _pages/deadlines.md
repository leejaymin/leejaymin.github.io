---
layout: page
title: Deadlines
permalink: /deadlines/
description: AI·NLP·컴퓨터 시스템 분야 주요 학회의 논문 마감일과 ACL Rolling Review(ARR) 사이클 일정을 모아 보여줍니다. 데이터는 매주 자동으로 갱신됩니다.
nav: true
nav_order: 6
---

<!-- pages/deadlines.md -->

<style>
.dl-controls {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.6rem;
  margin: 1.2rem 0 1.5rem;
}

.dl-filter {
  padding: 0.35rem 0.9rem;
  border-radius: 999px;
  border: 1px solid var(--global-divider-color, #ddd);
  background: var(--global-card-bg-color, #fff);
  color: var(--global-text-color, #333);
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dl-filter:hover { border-color: var(--global-theme-color, #4285f4); }

.dl-filter.active {
  background: var(--global-theme-color, #4285f4);
  border-color: var(--global-theme-color, #4285f4);
  color: #fff;
}

#dl-search {
  flex: 1 1 200px;
  min-width: 160px;
  padding: 0.4rem 0.8rem;
  border-radius: 8px;
  border: 1px solid var(--global-divider-color, #ddd);
  background: var(--global-card-bg-color, #fff);
  color: var(--global-text-color, #333);
  font-size: 0.85rem;
}

.dl-toggle {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.85rem;
  color: var(--global-text-color-light, #666);
  cursor: pointer;
}

.dl-card {
  display: flex;
  align-items: stretch;
  gap: 1.2rem;
  margin-bottom: 0.7rem;
  padding: 1rem 1.2rem;
  border-radius: 12px;
  background: var(--global-card-bg-color, #fff);
  border: 1px solid var(--global-divider-color, #f0f0f0);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  color: var(--global-text-color);
  text-decoration: none;
}

.dl-card:hover,
.dl-card:focus {
  box-shadow: 0 8px 25px rgba(0,0,0,0.08), 0 2px 10px rgba(0,0,0,0.04);
  transform: translateY(-2px);
  color: var(--global-text-color);
  text-decoration: none;
}

.dl-count {
  flex: 0 0 5.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  border-right: 1px solid var(--global-divider-color, #eee);
  padding-right: 1rem;
}

.dl-dday {
  font-size: 1.35rem;
  font-weight: 700;
  font-family: 'Roboto', monospace;
  line-height: 1.1;
  color: var(--global-theme-color, #4285f4);
}

.dl-dday.urgent { color: #d93025; }
.dl-dday.closed { color: var(--global-text-color-light, #999); font-size: 1rem; }

.dl-remain {
  font-size: 0.7rem;
  font-family: 'Roboto', monospace;
  color: var(--global-text-color-light, #888);
  margin-top: 0.2rem;
}

.dl-body { flex: 1 1 auto; min-width: 0; }

.dl-title {
  font-size: 1.05rem;
  font-weight: 600;
  margin: 0 0 0.25rem;
  color: var(--global-text-color);
}

.dl-card:hover .dl-title { color: var(--global-theme-color); }

.dl-year {
  font-family: 'Roboto', monospace;
  color: var(--global-text-color-light, #888);
  font-weight: 400;
}

.dl-badge {
  display: inline-block;
  font-size: 0.65rem;
  font-weight: 600;
  padding: 0.1rem 0.5rem;
  border-radius: 999px;
  margin-left: 0.35rem;
  vertical-align: middle;
}

.dl-badge.area-AI { background: var(--global-theme-color, #4285f4); color: #fff; }
.dl-badge.area-NLP { background: #673ab7; color: #fff; }
.dl-badge.area-Systems { background: #34a853; color: #fff; }
.dl-badge.area-Other { background: var(--global-divider-color, #e5e5e5); color: var(--global-text-color, #333); }
.dl-badge.tba { background: #fbbc04; color: #333; }
.dl-badge.approx { background: #e8710a; color: #fff; }

.dl-full {
  font-size: 0.78rem;
  color: var(--global-text-color-light, #777);
  margin: 0 0 0.3rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dl-meta {
  font-size: 0.75rem;
  font-family: 'Roboto', monospace;
  color: var(--global-text-color-light, #666);
  margin: 0;
}

.dl-meta .sep { color: var(--global-divider-color, #ccc); margin: 0 0.45rem; }
.dl-when { font-weight: 600; color: var(--global-text-color, #444); }
.dl-kind { color: var(--global-text-color-light, #888); margin-left: 0.3rem; }

.dl-empty {
  padding: 2rem 0;
  text-align: center;
  color: var(--global-text-color-light, #888);
  font-size: 0.9rem;
}

.dl-note {
  margin-top: 2.5rem;
  padding-top: 1rem;
  border-top: 1px solid var(--global-divider-color, #eee);
  font-size: 0.75rem;
  color: var(--global-text-color-light, #888);
}

@media (max-width: 768px) {
  .dl-card { flex-direction: column; gap: 0.6rem; }
  .dl-count {
    flex-direction: row;
    gap: 0.5rem;
    justify-content: flex-start;
    border-right: none;
    border-bottom: 1px solid var(--global-divider-color, #eee);
    padding: 0 0 0.5rem;
  }
  .dl-full { white-space: normal; }
}
</style>

<div class="dl-controls">
  <button class="dl-filter active" data-area="all" type="button">전체</button>
  <button class="dl-filter" data-area="AI" type="button">AI</button>
  <button class="dl-filter" data-area="NLP" type="button">NLP</button>
  <button class="dl-filter" data-area="Systems" type="button">Systems</button>
  <input type="search" id="dl-search" placeholder="학회 이름 검색 (예: NeurIPS, ISCA)" aria-label="학회 검색">
  <label class="dl-toggle">
    <input type="checkbox" id="dl-show-past"> 마감 지난 학회도 보기
  </label>
</div>

<div id="dl-list">
{%- assign conferences = site.data.conferences %}
{%- for conf in conferences %}
  {%- assign areas = conf.areas | join: " " %}
  {%- assign haystack = conf.title | append: " " | append: conf.full_name | append: " " | append: conf.place | append: " " | append: conf.year | downcase %}
  <a class="dl-card{% unless conf.next_deadline or conf.tba %} dl-past{% endunless %}"
     href="{{ conf.link | default: '#' }}"
     {% if conf.link %}target="_blank" rel="noopener"{% endif %}
     data-areas="{{ areas }}"
     data-search="{{ haystack | escape }}"
     {% if conf.next_deadline %}data-deadline="{{ conf.next_deadline }}"{% endif %}>
    <div class="dl-count">
      <span class="dl-dday">{% if conf.next_deadline %}—{% elsif conf.tba %}미정{% else %}마감 종료{% endif %}</span>
      {%- if conf.next_deadline %}<span class="dl-remain"></span>{% endif %}
    </div>
    <div class="dl-body">
      <p class="dl-title">
        {{ conf.title }} <span class="dl-year">{{ conf.year }}</span>
        {%- for area in conf.areas %}<span class="dl-badge area-{{ area }}">{{ area }}</span>{% endfor %}
        {%- if conf.tba %}<span class="dl-badge tba">CFP 미발표</span>{% endif %}
        {%- if conf.approx %}<span class="dl-badge approx">예상 마감</span>{% endif %}
      </p>
      {%- if conf.full_name %}
      <p class="dl-full">{{ conf.full_name }}</p>
      {%- endif %}
      <p class="dl-meta">
        {%- if conf.next_deadline %}
        {%- assign next_label = "" %}
        {%- for d in conf.deadlines %}{% if d.utc == conf.next_deadline %}{% assign next_label = d.label %}{% endif %}{% endfor %}
        <span class="dl-when" data-deadline="{{ conf.next_deadline }}"></span>
        {%- if next_label != "" %} <span class="dl-kind">{{ next_label }}</span>{% endif %}<span class="sep">|</span>
        {%- endif %}
        {%- if conf.date %}{{ conf.date }}{%- endif %}
        {%- if conf.date and conf.place %}<span class="sep">|</span>{% endif %}
        {%- if conf.place %}{{ conf.place }}{%- endif %}
      </p>
    </div>
  </a>
{%- endfor %}
</div>

<p class="dl-empty" id="dl-empty" hidden>조건에 맞는 학회가 없습니다.</p>

<p class="dl-note">
  마감일은 매주 자동으로 갱신되지만, 실제 마감 시각은 반드시 각 학회 공식 홈페이지에서 확인하시기 바랍니다.
  NLP 계열 학회(ACL, EMNLP, NAACL 등)는 <a href="https://aclrollingreview.org/dates" target="_blank" rel="noopener">ACL Rolling Review(ARR)</a> 사이클로 제출이 이뤄지므로, ARR 사이클 일정과 학회별 commitment 마감도 함께 표시합니다.
  <span class="dl-badge approx">예상 마감</span> 표시는 아직 공식 발표 전인 추정 일정입니다.
</p>

<script>
(function () {
  var MINUTE = 60000, HOUR = 3600000, DAY = 86400000;

  function renderCountdowns() {
    var now = Date.now();
    document.querySelectorAll('.dl-card[data-deadline]').forEach(function (card) {
      var target = new Date(card.getAttribute('data-deadline')).getTime();
      var diff = target - now;
      var dday = card.querySelector('.dl-dday');
      var remain = card.querySelector('.dl-remain');

      if (diff <= 0) {
        dday.textContent = '마감 종료';
        dday.classList.add('closed');
        if (remain) remain.textContent = '';
        card.classList.add('dl-past');
        return;
      }

      var days = Math.floor(diff / DAY);
      dday.textContent = 'D-' + days;
      dday.classList.toggle('urgent', days <= 7);
      if (remain) {
        var hours = Math.floor((diff % DAY) / HOUR);
        var mins = Math.floor((diff % HOUR) / MINUTE);
        remain.textContent = hours + '시간 ' + mins + '분';
      }
    });
  }

  // 마감 시각은 동기화 시점에 UTC로 변환해 두었으므로, 여기서는 보는 사람의
  // 현지 시간대로만 표시하면 된다.
  function renderLocalTimes() {
    document.querySelectorAll('.dl-when[data-deadline]').forEach(function (el) {
      var d = new Date(el.getAttribute('data-deadline'));
      el.textContent = d.toLocaleString(undefined, {
        year: 'numeric', month: 'short', day: 'numeric',
        hour: '2-digit', minute: '2-digit'
      });
      el.title = '내 시간대 기준 마감 시각';
    });
  }

  function applyFilters() {
    var area = document.querySelector('.dl-filter.active').getAttribute('data-area');
    var query = document.getElementById('dl-search').value.trim().toLowerCase();
    var showPast = document.getElementById('dl-show-past').checked;
    var visible = 0;

    document.querySelectorAll('.dl-card').forEach(function (card) {
      var matchArea = area === 'all' || card.getAttribute('data-areas').indexOf(area) !== -1;
      var matchQuery = !query || card.getAttribute('data-search').indexOf(query) !== -1;
      var matchPast = showPast || !card.classList.contains('dl-past');
      var show = matchArea && matchQuery && matchPast;
      card.hidden = !show;
      if (show) visible++;
    });

    document.getElementById('dl-empty').hidden = visible > 0;
  }

  document.querySelectorAll('.dl-filter').forEach(function (btn) {
    btn.addEventListener('click', function () {
      document.querySelectorAll('.dl-filter').forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      applyFilters();
    });
  });
  document.getElementById('dl-search').addEventListener('input', applyFilters);
  document.getElementById('dl-show-past').addEventListener('change', applyFilters);

  renderCountdowns();
  renderLocalTimes();
  applyFilters();
  setInterval(renderCountdowns, MINUTE);
})();
</script>
