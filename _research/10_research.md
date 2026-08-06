---
layout: page
title: Low-Level API-Based Operation Kernel Development for AI Semiconductors
description: Development of operation kernels directly on the low-level API of AI semiconductors, targeting maximum utilization of the accelerator's compute and memory hierarchy.
img: assets/img/research_kernel_api.png
importance: 4
category: Present
period: "Aug. 2026 – Nov. 2026"
# funding: "TBD"
funded_by: "ETRI"
---

<div class="col-sm mt-3 mt-md-0">
    {% include figure.html path="assets/img/research_kernel_api.png" title="Low-Level API-Based Operation Kernel Development" class="img-fluid rounded z-depth-1" %}
</div>

- This project is funded by ETRI (Electronics and Telecommunications Research Institute).
- Period: Aug. 2026 – Nov. 2026.

AI 반도체 지원을 위한 저수준 API 기반 연산 커널 개발

This project develops operation kernels written directly against the low-level API of AI semiconductors. Programming at this level exposes the accelerator's compute units, on-chip memory, and data movement paths explicitly, so kernel performance depends on how carefully tiling, scheduling, and memory placement are chosen for the target hardware.

The work covers the implementation of the core operators required by deep learning workloads, hardware-aware tuning of those kernels, and validation of both numerical correctness and performance against reference implementations, so that the resulting kernels can be adopted by higher-level runtimes and frameworks.
