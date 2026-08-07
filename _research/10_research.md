---
layout: page
title: AI 반도체 지원을 위한 저수준 API 기반 연산 커널 개발
description: AI 반도체의 저수준 API에 직접 대응하는 연산 커널을 개발하는 과제이다. 가속기의 연산 유닛, 온칩 메모리, 데이터 이동 경로를 명시적으로 다루어 타일링·스케줄링·메모리 배치를 하드웨어에 맞게 최적화하고, 수치 정확성과 성능 검증을 거쳐 상위 런타임과 프레임워크에서 활용 가능한 커널을 제공한다.
img: assets/img/research_kernel_api.png
sponsor_logo: assets/img/logo/etri-logo.png
importance: 4
category: Present
period: "Aug. 2026 – Nov. 2026"
# funding: "TBD"
funded_by: "ETRI"
role: "과제책임자"
project_type: "용역"
---

<div class="col-sm mt-3 mt-md-0">
    {% include figure.html path="assets/img/research_kernel_api.png" title="Low-Level API-Based Operation Kernel Development" class="img-fluid rounded z-depth-1" %}
</div>

- This project is funded by ETRI (Electronics and Telecommunications Research Institute).
- Period: Aug. 2026 – Nov. 2026.

AI 반도체 지원을 위한 저수준 API 기반 연산 커널 개발

This project develops operation kernels written directly against the low-level API of AI semiconductors. Programming at this level exposes the accelerator's compute units, on-chip memory, and data movement paths explicitly, so kernel performance depends on how carefully tiling, scheduling, and memory placement are chosen for the target hardware.

The work covers the implementation of the core operators required by deep learning workloads, hardware-aware tuning of those kernels, and validation of both numerical correctness and performance against reference implementations, so that the resulting kernels can be adopted by higher-level runtimes and frameworks.
