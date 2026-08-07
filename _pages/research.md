---
layout: page
title: Projects
permalink: /projects/
description: What we have doing and done.
nav: true
nav_order: 3
display_categories: [Present, Past]
horizontal: false
---

<!-- pages/research.md -->

<style>
a.project-block {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 0.8rem;
  flex-wrap: wrap;
  padding: 1.2rem;
  border-radius: 12px;
  background: var(--global-card-bg-color, #fff);
  border: 1px solid var(--global-divider-color, #f0f0f0);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  color: var(--global-text-color);
  text-decoration: none;
}

a.project-block:hover,
a.project-block:focus {
  box-shadow: 0 8px 25px rgba(0,0,0,0.08), 0 2px 10px rgba(0,0,0,0.04);
  transform: translateY(-2px);
  color: var(--global-text-color);
  text-decoration: none;
}

.project-block .img-col {
  flex: 1 1 35%;
  max-width: 280px;
  overflow: hidden;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #fff;
  padding: 0.8rem;
}

.project-block .text-col {
  flex: 1 1 60%;
}

.project-block .img-col img {
  width: 100%;
  max-height: 120px;
  height: auto;
  border-radius: 8px;
  transition: transform 0.4s ease;
  object-fit: contain;
}

.project-block:hover .img-col img {
  transform: scale(1.03);
}

.project-block h3 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  color: var(--global-text-color);
}

.project-block h3 .project-contract {
  font-weight: 600;
  color: var(--global-text-color-light, #666);
}

.project-block .project-badge {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.15rem 0.55rem;
  border-radius: 999px;
  vertical-align: middle;
  margin-left: 0.45rem;
  white-space: nowrap;
}

.project-block .badge-pi {
  background: var(--global-theme-color, #4285f4);
  color: #fff;
}

.project-block .badge-copi {
  background: var(--global-divider-color, #e5e5e5);
  color: var(--global-text-color, #333);
}

a.project-block:hover h3 {
  color: var(--global-theme-color);
}

.project-block .project-desc {
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
  color: var(--global-text-color);
}

.project-block .project-meta {
  font-size: 0.75rem;
  font-family: 'Roboto', monospace;
  color: var(--global-text-color-light, #555);
  margin-bottom: 0;
}

.project-block .project-meta .meta-divider {
  color: var(--global-divider-color, #ccc);
  margin: 0 0.4rem;
}

.section-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--global-text-color, #333);
  border-left: 4px solid var(--global-theme-color, #4285f4);
  padding-left: 0.8rem;
  margin-top: 2.5rem;
  margin-bottom: 1rem;
}

/* 모바일: 이미지 위, 텍스트 아래 */
@media (max-width: 768px) {
  .project-block {
    flex-direction: column;
    padding: 0.8rem;
  }

  .project-block .img-col,
  .project-block .text-col {
    flex: 1 1 100%;
    max-width: 100%;
  }
}
</style>

<div class="projects research">
{%- for category in page.display_categories %}
  <h4 class="section-title">{{ category }}</h4>
  {%- assign categorized_projects = site.research | where: "category", category -%}
  {%- assign sorted_projects = categorized_projects | sort: "importance" %}
  {%- for project in sorted_projects %}
  <a class="project-block" href="{{ project.url | relative_url }}">
    <div class="img-col">
      {%- if project.sponsor_logo %}
      <img src="{{ project.sponsor_logo | relative_url }}" alt="{{ project.funded_by | default: project.title }}">
      {%- elsif project.img %}
      <img src="{{ project.img | relative_url }}" alt="{{ project.title }}">
      {%- endif %}
    </div>
    <div class="text-col">
      <h3>{{ project.title }}{%- if project.project_type %} <span class="project-contract">({{ project.project_type }})</span>{%- endif %}{%- if project.role %}<span class="project-badge {% if project.role == '과제책임자' %}badge-pi{% else %}badge-copi{% endif %}">{{ project.role }}</span>{%- endif %}</h3>
      <p class="project-desc">{{ project.description }}</p>
      {%- if project.period or project.funded_by %}
      <p class="project-meta">
        {%- if project.period %}Duration: {{ project.period }}{%- endif %}
        {%- if project.period and project.funded_by %}<span class="meta-divider">|</span>{%- endif %}
        {%- if project.funded_by %}Funded by {{ project.funded_by }}{%- endif %}
      </p>
      {%- endif %}
    </div>
  </a>
  {%- endfor %}
{%- endfor %}
</div>
