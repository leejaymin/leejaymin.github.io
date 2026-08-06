---
layout: page
title: AI최고급신진연구자지원 (AI스타펠로우십, 지역주도형)
description: 진단 AI 에이전트의 경량화 및 추론 최적화를 담당하는 과제이다. 양자화, 프루닝·지식 증류, 컴파일러/커널 최적화, 서빙·런타임 최적화를 통해 대규모 멀티모달 에이전트를 실용적인 지연시간과 메모리 예산 내에서 서비스하는 것을 목표로 한다.
img: assets/img/research_ai_star_fellowship.png
sponsor_logo: assets/img/logo/iitp-logo.png
importance: 2
category: Present
period: "Jul. 2026 – Dec. 2031"
# funding: "TBD"
funded_by: "IITP"
---

<div class="col-sm mt-3 mt-md-0">
    {% include figure.html path="assets/img/research_ai_star_fellowship.png" title="Lightweighting and optimization for diagnostic AI agents" class="img-fluid rounded z-depth-1" %}
</div>

- This project is funded by IITP (Institute of Information & Communications Technology Planning & Evaluation), Korea, under the **AI Star Fellowship** program.
- Period: Jul. 1, 2026 – Dec. 31, 2031 (6 years).

Within this project, our lab is responsible for the **lightweighting and optimization** of the diagnostic AI agent.

Diagnostic agents combine multimodal perception, clinical language-model reasoning, and tool orchestration, which makes them large and latency-sensitive — precisely the regime where naive deployment becomes impractical. Our role is to close that gap:

- **Quantization** — low-precision weights and activations that preserve diagnostic accuracy.
- **Pruning and distillation** — smaller models at comparable quality.
- **Compiler and kernel optimization** — hardware-aware operator tuning for the target accelerators.
- **Serving and runtime optimization** — meeting throughput, memory, and latency budgets in real deployments.

The result is a diagnostic agent that can be served on-device or at the edge, so that inference stays fast and affordable at the point of care.
