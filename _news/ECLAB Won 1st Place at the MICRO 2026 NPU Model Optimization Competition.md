---
layout: post
title: "ECLAB Won 1st Place at the MICRO 2026 NPU Model Optimization Competition (FuriosaAI RNGD)"
date: 2026-10-29 09:00:00+0900
inline: false
related_posts: false
---

전북대학교 컴퓨터인공지능학부 효율적 컴퓨팅 연구실(ECLAB, 지도교수 이제민)의 오세현 박사과정 학생과 이제민 교수가 참가한 ECLAB 팀이 `IEEE/ACM MICRO 2026`과 연계해 열린 **NPU Model Optimization Competition**에서 **최종 1위**를 차지했습니다:tada:

{% include figure.html path="assets/img/micro2026_moa_winners.png" class="img-fluid rounded z-depth-1" zoomable=true %}


ECLAB 팀은 최종 라운드에서 **870.0 tokens/s**의 추론 처리량을 기록해 `1위`에 올랐습니다(2위 RTOSLab 821.1 tokens/s, 3위 Monkey 630.2 tokens/s). 이번 성과는 단순히 모델 크기를 줄이는 데 그치지 않고, 특정 NPU 하드웨어에 맞춘 컴파일러·커널 수준 최적화와 멀티모달 처리 전략을 결합해 실제 AI 추론 효율을 높였다는 데 의미가 있습니다.

1위 상금은 `5,000유로` (2026년 10월 28일 환율 1유로당 1,492.98원 기준 약 746만 원)이며, 시상식은 11월 1일 그리스 아테네에서 열리는 MICRO 2026 MOA 워크숍에서 진행됩니다. 


<div class="caption">
Model Optimization Round 최종 순위 (출처: <a href="https://micro2026-moa.github.io/index.html#winners">MICRO 2026 MOA Competition</a>)
</div>

이번 경진대회는 컴퓨터 구조 분야의 대표 국제학술대회인 제59회 `IEEE/ACM International Symposium on Microarchitecture (MICRO 2026)`의 MOA(Measuring and Optimizing Heterogeneous AI Architectures) 워크숍과 함께 진행되었으며, 서울대학교와 퓨리오사AI(FuriosaAI)가 공동 주최했습니다. 참가팀은 퓨리오사AI의 AI 반도체 **RNGD**에서 구동되는 멀티모달 대규모 언어모델 **Gemma 4 12B**의 추론 성능을 furiosa-opt 툴체인으로 높이는 과제를 수행했습니다.
{% include figure.html path="assets/img/micro_26.png" class="img-fluid rounded z-depth-1" zoomable=true %}


대회는 2단계로 진행되었습니다.

- **1라운드 – Kernel Optimization Round** (2026.9.1–9.30): QKV 투영, 어텐션 출력 투영, 피드포워드 블록 등 디코더 레이어의 주요 커널을 최적화했습니다. 성능과 정확도 검증을 거쳐 64개 팀이 2라운드에 진출했습니다.
- **2라운드 – Model Optimization Round** (2026.10.2–10.25): 전체 모델의 종단 간(end-to-end) 추론을 최적화했습니다. 정확성 검증을 통과한 제출물을 처리량(generated tokens/s)으로 순위를 매겼습니다.

ECLAB 팀은 RNGD NPU의 실행 특성에 맞춘 커널 설계와 연산 흐름 최적화에 집중했습니다. 핵심 기법은 다음 두 가지입니다.

**① Mega-kernel과 Chunked Prefill: 모든 요청을 함께, 여러 층을 한 번에**

- **Mega-kernel**: 커널 하나가 디코더 6개 층을 이어서 처리하도록 여러 연산을 하나의 큰 실행 단위로 묶었습니다. 48개 층 전체를 커널 8번 실행으로 계산하므로, 층마다 커널을 실행할 때 생기던 불필요한 실행 및 메모리 접근 비용이 줄어듭니다.
- **Chunked Prefill**: 처리 중인 모든 요청의 토큰을 한 번에 함께 계산합니다. 어떤 요청이 끝나면 그 자리에 새 요청(E, F)의 prefill이 곧바로 들어오므로, 이미지·텍스트·음성이 섞인 멀티모달 요청이 계속 들어와도 NPU가 쉬지 않고 연산을 이어 갑니다.

{% include figure.html path="assets/img/moa_chucked_prefill_mega_kernel.png" class="img-fluid rounded z-depth-1" zoomable=true %}

**② 8비트 양자화와 Hadamard 회전: 정확도를 지키며 행렬곱 입력을 8비트로**

- 기본 구현(baseline)에서는 가중치 정밀도가 FFN 4비트, attention 8비트, lm_head 16비트로 제각각이었고, 행렬곱 입력과 KV 캐시는 16비트였습니다. 이를 **행렬곱 입력(가중치, 활성값, KV 캐시) 모두 8비트**로 통일하고, 행렬곱 결과는 넓게 누적해 16비트로 받도록 했습니다.
- Query와 Key에는 소수의 큰 이상치(outlier)가 있어 그대로 8비트로 줄이면 정확도가 떨어집니다. 그래서 **Query와 Key를 같은 Hadamard 행렬로 회전**했습니다. 같은 행렬로 회전하므로 Q·K 값은 그대로 유지되고, 값은 고르게 퍼져 8비트로 양자화해도 대회의 정확도 검증 조건을 충족합니다.

{% include figure.html path="assets/img/moa_quantization.png" class="img-fluid rounded z-depth-1" zoomable=true %}

이번 수상은 국산 AI 반도체를 활용한 대규모 멀티모달 모델 추론 최적화 역량을 국제 무대에서 보여준 사례로, 향후 온디바이스 AI와 고효율 AI 시스템 연구로 이어질 것으로 기대됩니다.


---------

The ECLAB team, Ph.D. student Sehyeon Oh and Prof. Jemin Lee of the Efficient Computing Lab (ECLAB), Division of Computer Science and Artificial Intelligence, Jeonbuk National University, won **1st place** in the **NPU Model Optimization Competition** held with `IEEE/ACM MICRO 2026`:tada:

The competition was part of the MOA (Measuring and Optimizing Heterogeneous AI Architectures) Workshop at the 59th IEEE/ACM International Symposium on Microarchitecture (MICRO 2026), co-organized by Seoul National University and FuriosaAI. Participants optimized inference of **Gemma 4 12B**, a multimodal large language model, on FuriosaAI's **RNGD** AI accelerator using the furiosa-opt toolchain.

The competition ran in two rounds:

- **Round 1 – Kernel Optimization Round** (Sep. 1–30, 2026): optimize key decoder-layer kernels, namely the QKV projection, attention output projection, and feed-forward block. After performance and accuracy verification, 64 teams advanced to Round 2.
- **Round 2 – Model Optimization Round** (Oct. 2–25, 2026): optimize end-to-end inference of the full model. Submissions that pass the correctness check are ranked by throughput (generated tokens/s).

The team focused on kernel design and dataflow optimization tailored to the execution characteristics of the RNGD NPU. Two techniques were key:

**① Mega-kernel and chunked prefill: all requests together, many layers at once**

- **Mega-kernel**: multiple operations are fused into one large execution unit, so a single kernel processes six decoder layers back to back. All 48 layers are computed in just eight kernel launches, which removes the launch and memory-access overhead of running one kernel per layer.
- **Chunked prefill**: tokens from all in-flight requests are computed together in one pass. When a request finishes, the prefill of a new request (E, F) fills its slot immediately, so the NPU keeps computing without idle time even as multimodal requests (image, text, and audio) keep arriving.

**② 8-bit quantization with Hadamard rotation: 8-bit matmul inputs without losing accuracy**

- In the baseline, weight precision was mixed (4-bit FFN, 8-bit attention, 16-bit lm_head), and matmul inputs and the KV cache were 16-bit. The team unified **all matmul inputs (weights, activations, and KV cache) to 8-bit**, while accumulating results at wider precision and outputting 16-bit.
- Query and Key contain a few large outliers that hurt accuracy when quantized directly to 8-bit. The team therefore **rotated Query and Key with the same Hadamard matrix**: because both are rotated by the same matrix, Q·K is preserved, while values are spread evenly so they can be quantized to 8-bit and still pass the competition's accuracy check.

As a result, ECLAB achieved **870.0 tokens/s** in the final round and took first place (2nd: RTOSLab, 821.1 tokens/s; 3rd: Monkey, 630.2 tokens/s). Beyond simply shrinking the model, this result shows how compiler- and kernel-level optimization for a specific NPU, combined with a multimodal processing strategy, improves real-world AI inference efficiency.

The 1st-place prize is €5,000, and the award ceremony will take place at the MOA Workshop of MICRO 2026 in Athens, Greece, on November 1, 2026. This award demonstrates, on the international stage, the lab's expertise in optimizing large multimodal model inference on Korean AI accelerators, and the work is expected to carry forward into research on on-device AI and highly efficient AI systems.

- Competition website: <https://micro2026-moa.github.io/>
