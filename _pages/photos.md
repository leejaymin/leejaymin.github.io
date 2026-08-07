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
.photo-board {
  columns: 2 380px;
  column-gap: 1.2rem;
  margin-top: 1rem;
}

.photo-item {
  display: inline-block;
  width: 100%;
  margin: 0 0 1rem;
  break-inside: avoid;
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
  height: auto;
  transition: transform 0.4s ease;
}

.photo-item a:hover img {
  transform: scale(1.03);
}

.photo-item figcaption {
  font-size: 0.75rem;
  font-family: 'Roboto', monospace;
  color: var(--global-text-color-light, #555);
  text-align: center;
  margin-top: 0.35rem;
}
</style>

{% assign photo_files = site.static_files | where_exp: "file", "file.path contains '/assets/img/photos/'" | sort: "path" | reverse %}
<div class="photo-board">
{%- for photo in photo_files %}
  {%- assign ext = photo.extname | downcase %}
  {%- comment %} .webp 제외: jekyll-imagemagick이 생성하는 반응형 변환본(-480/-800/-1400.webp)이 중복 표시되는 것 방지 {%- endcomment %}
  {%- if ext == ".jpg" or ext == ".jpeg" or ext == ".png" or ext == ".gif" %}
  <figure class="photo-item">
    <a href="{{ photo.path | relative_url }}" target="_blank" rel="noopener">
      <img src="{{ photo.path | relative_url }}" alt="{{ photo.basename }}" loading="lazy">
    </a>
    <figcaption>{{ photo.basename | replace: "_", " " }}</figcaption>
  </figure>
  {%- endif %}
{%- endfor %}
</div>
