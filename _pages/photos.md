---
layout: page
title: Photo
permalink: /photos/
description: 학회 참석, MT, 회식 등 연구실 활동을 기념하는 사진첩입니다.
nav: true
nav_order: 5
---

<!-- pages/photos.md -->

<style>
.photo-year-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--global-text-color, #333);
  border-left: 4px solid var(--global-theme-color, #4285f4);
  padding-left: 0.8rem;
  margin-top: 2.5rem;
  margin-bottom: 1rem;
}

.photo-carousel-wrap {
  position: relative;
}

.photo-carousel {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  padding: 0.25rem 0.25rem 0.75rem;
  -webkit-overflow-scrolling: touch;
}

.photo-carousel::-webkit-scrollbar {
  height: 8px;
}

.photo-carousel::-webkit-scrollbar-thumb {
  background: var(--global-divider-color, #ddd);
  border-radius: 4px;
}

.photo-item {
  flex: 0 0 auto;
  width: 300px;
  margin: 0;
  scroll-snap-align: start;
}

.photo-item a {
  display: block;
  overflow: hidden;
  border-radius: 10px;
  border: 1px solid var(--global-divider-color, #f0f0f0);
  background: var(--global-card-bg-color, #fff);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.photo-item a:hover {
  box-shadow: 0 8px 25px rgba(0,0,0,0.08), 0 2px 10px rgba(0,0,0,0.04);
  transform: translateY(-2px);
}

.photo-item img {
  display: block;
  width: 100%;
  height: 210px;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.photo-item a:hover img {
  transform: scale(1.03);
}

.photo-item figcaption {
  text-align: center;
  margin-top: 0.5rem;
  line-height: 1.4;
}

.photo-item .photo-date {
  display: block;
  font-size: 0.85rem;
  color: var(--global-text-color-light, #666);
}

.photo-item .photo-event {
  display: block;
  font-size: 1rem;
  font-weight: 600;
  color: var(--global-text-color, #333);
}

.carousel-btn {
  position: absolute;
  top: 105px;
  transform: translateY(-50%);
  z-index: 2;
  width: 2.2rem;
  height: 2.2rem;
  border-radius: 50%;
  border: 1px solid var(--global-divider-color, #ddd);
  background: var(--global-card-bg-color, #fff);
  color: var(--global-text-color, #333);
  font-size: 1.2rem;
  line-height: 1;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.9;
}

.carousel-btn:hover {
  background: var(--global-theme-color, #4285f4);
  color: #fff;
}

.carousel-btn.prev { left: -0.6rem; }
.carousel-btn.next { right: -0.6rem; }

@media (max-width: 768px) {
  .photo-item { width: 240px; }
  .photo-item img { height: 170px; }
  .carousel-btn { top: 85px; }
}
</style>

{%- comment %}
사진 파일명 규칙: YYYY_M_행사명.확장자 (예: 2026_6_KCC.png → "2026년 6월 / KCC")
.webp 제외: jekyll-imagemagick이 생성하는 반응형 변환본(-480/-800/-1400.webp)이 중복 표시되는 것 방지
{%- endcomment %}
{%- assign photo_files = site.static_files | where_exp: "file", "file.path contains '/assets/img/photos/'" %}
{%- assign photo_files = photo_files | where_exp: "file", "file.extname == '.jpg' or file.extname == '.jpeg' or file.extname == '.png' or file.extname == '.gif' or file.extname == '.JPG' or file.extname == '.JPEG' or file.extname == '.PNG'" %}
{%- assign year_groups = photo_files | group_by_exp: "file", "file.basename | split: '_' | first" | sort: "name" | reverse %}
{%- assign months_desc = "12,11,10,9,8,7,6,5,4,3,2,1" | split: "," %}

{%- for year_group in year_groups %}
<h4 class="photo-year-title">{{ year_group.name }}</h4>
<div class="photo-carousel-wrap">
  <button class="carousel-btn prev" type="button" aria-label="이전 사진">‹</button>
  <div class="photo-carousel">
  {%- for m in months_desc %}
    {%- assign m_num = m | plus: 0 %}
    {%- for photo in year_group.items %}
      {%- assign parts = photo.basename | split: "_" %}
      {%- assign photo_month = parts[1] | plus: 0 %}
      {%- if photo_month == m_num %}
      {%- assign event_name = parts | slice: 2, 10 | join: " " %}
      <figure class="photo-item">
        <a href="{{ photo.path | relative_url }}" target="_blank" rel="noopener">
          <img src="{{ photo.path | relative_url }}" alt="{{ event_name | default: photo.basename }}" loading="lazy">
        </a>
        <figcaption>
          <span class="photo-date">{{ parts[0] }}년 {{ photo_month }}월</span>
          <span class="photo-event">{{ event_name | default: photo.basename }}</span>
        </figcaption>
      </figure>
      {%- endif %}
    {%- endfor %}
  {%- endfor %}
  {%- comment %} 파일명이 YYYY_M_행사명 규칙을 따르지 않는 사진은 마지막에 표시 {%- endcomment %}
  {%- for photo in year_group.items %}
    {%- assign parts = photo.basename | split: "_" %}
    {%- assign photo_month = parts[1] | plus: 0 %}
    {%- if photo_month < 1 or photo_month > 12 %}
      <figure class="photo-item">
        <a href="{{ photo.path | relative_url }}" target="_blank" rel="noopener">
          <img src="{{ photo.path | relative_url }}" alt="{{ photo.basename }}" loading="lazy">
        </a>
        <figcaption>
          <span class="photo-event">{{ photo.basename | replace: "_", " " }}</span>
        </figcaption>
      </figure>
    {%- endif %}
  {%- endfor %}
  </div>
  <button class="carousel-btn next" type="button" aria-label="다음 사진">›</button>
</div>
{%- endfor %}

<script>
  document.querySelectorAll('.photo-carousel-wrap .carousel-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var carousel = btn.closest('.photo-carousel-wrap').querySelector('.photo-carousel');
      var amount = Math.max(carousel.clientWidth * 0.8, 320);
      carousel.scrollBy({
        left: btn.classList.contains('next') ? amount : -amount,
        behavior: 'smooth'
      });
    });
  });
</script>
