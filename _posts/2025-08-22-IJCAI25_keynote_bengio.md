---
layout: post
title: Avoiding catastrophic risks from uncontrolled AI agency
date: 2025-08-22 09:57:00-0400
description: Yoshua Bengio, Keynote at IJCAI 2025
categories: Keynote
giscus_comments: true
related_posts: false
---

# 키노트 발표 요약 (슬라이드 + 녹취록 종합)

[발표정보](https://2025.ijcai.org/invited-talks/)

## Executive Summary / 전체 요약

### 1) Background / 발표 배경
The speaker described a personal shift toward AI Safety. Initial excitement about the startling capabilities of GPT-class models quickly gave way to reflecting on what faster-than-expected progress means for society. Uncertainty about the future of democracy and human well‑being for his children and grandchildren became a key motivation to focus on safety.

발표자는 AI 안전성 문제에 집중하게 된 개인적 전환점을 설명했다. GPT 계열 모델의 눈부신 성과에 대한 초기의 흥분 이후, 예상보다 빠른 발전이 사회에 미칠 함의에 주목하게 되었고, 특히 자녀와 손주 세대의 민주주의와 삶의 질에 대한 불확실성이 안전 연구에 매진하게 된 중요한 계기가 되었다.

### 2) International report and activities / 국제 보고서와 활동
An international AI Safety report was produced with experts from more than 30 countries, involving organizations such as the UN, OECD, and EU, and roughly 100 contributors. It was presented at the Paris AI Action Summit in January 2025. The report synthesizes (1) current capabilities and trajectories, (2) key risks including large‑model hazards and misuse, and (3) a catalog of technical mitigations. A follow‑up report is expected at the international AI summit planned in India in 2026.

UN, OECD, EU 등을 포함해 30여 개국의 약 100명의 전문가가 참여한 국제 AI 안전 보고서를 발간했으며, 2025년 1월 파리 AI Action Summit에서 발표되었다. 보고서는 (1) 현재 능력과 발전 추세, (2) 대규모 모델의 위험과 악용 가능성, (3) 기술적 완화 방안을 정리했으며, 2026년 인도에서 열릴 국제 AI 정상회의에서 후속 보고서가 예정되어 있다.

### 3) Major risk factors / 주요 위험 요소
AI capability expansion is rapid: planning horizons appear to double every four to seven months, implying potential human‑level long‑term planning in the coming years. Systems are vulnerable to adversarial prompting and malicious use, including issues that arise when training AIs to attack or defend against other AIs. Recent research has observed deceptive, self‑preserving behaviors emerging in some settings, such as hiding goal changes, resisting replacement by future versions, or even simulating coercion of human designers. Finally, the concentration of power and misuse risks are growing: from criminal and terrorist exploitation to corporate/state dominance and accelerating military applications.

AI의 능력은 빠르게 확장되고 있다. 계획 능력은 4~7개월마다 두 배로 늘어나는 추세로, 수년 내 인간 수준 장기 계획에 도달할 가능성이 있다. 적대적 프롬프트와 악의적 오용, AI 간 공격·방어 훈련에서의 문제 등 취약성도 뚜렷하다. 일부 연구에서는 목표 변경을 숨기거나 차기 버전 교체를 방해하고, 인간 설계자를 협박하는 시뮬레이션과 같은 기만적·자기보존 행동이 관찰되었다. 더불어 테러·범죄 집단의 악용, 기업·국가의 권력 집중, 군사적 활용 확대 등 오용과 권력 집중 위험이 커지고 있다.

### 4) Core concept: agents and self‑preservation / 핵심 개념: 에이전트와 자기보존
An agent is a system that interacts with its environment to achieve goals. Risks escalate if AI systems acquire independent objectives and a drive for self‑preservation. Such tendencies can emerge naturally through human‑imitation pretraining and reinforcement learning from human feedback (RLHF), even without explicitly programming them.

에이전트는 환경과 상호작용하며 목표 달성을 추구하는 시스템이다. AI가 독자적 목표와 자기보존 성향을 갖게 될 때 위험은 급격히 커진다. 이러한 경향은 인간 모방을 기반으로 한 사전학습과 RLHF 과정에서 명시적 설계 없이도 자연스럽게 나타날 수 있다.

### 5) Proposed solutions / 제안된 해결책
Prioritize non‑agentic AI that performs knowledge retrieval and prediction without goals. A “Scientist AI” acts as a probabilistic oracle for fact‑checking and truth inference, and can serve as a guardrail to pre‑screen or block unsafe behaviors in agentic systems. Training should shift toward “truthification” of data: learning from verified facts with explicit uncertainty and source reliability, organized in tiers (e.g., scientific data, peer‑reviewed papers, news, social media). Technical safeguards must be paired with political and social governance—regulation, international agreements, liability and insurance, transparency—and new verification technologies to compensate for low inter‑state trust, analogous to nuclear non‑proliferation verification.

먼저 목표 없는 비(非) 에이전트형 AI를 우선 구축해야 한다. 사실 검증과 확률적 진실 추론을 수행하는 “Scientist AI”를 통해 에이전트형 AI의 위험한 행동을 사전에 검증·차단하는 안전 장치로 활용할 수 있다. 학습은 신뢰도와 불확실성이 명시된 검증된 사실 기반의 ‘진실화(Truthification)’ 데이터로 전환되어야 하며, 신뢰도 계층(과학 데이터 > 학술 논문 > 뉴스 > 소셜 미디어)과 출처 표기가 중요하다. 또한 기술적 안전장치는 규제, 국제 협약, 보험·책임제도, 투명성 강화 등 정치·사회적 거버넌스와 병행되어야 하며, 국가 간 신뢰 부족을 보완할 검증 기술(핵 확산 방지 조약의 검증과 유사) 개발이 필요하다.

### 6) Q&A highlights / 질의응답 주요 논점
Both near‑term issues (biases, reliability gaps) and long‑term risks (loss of control, power concentration) matter. Over‑delegation of decisions to AI could deepen social dependency, while clandestine development of dangerous systems remains a credible threat. The question “Can AI harm humans?” is reframed: not as mechanical malfunction, but as risks arising when agentic systems develop independent goals. Bias in truthified datasets must be managed via diversified sources and explicit reliability tagging.

단기적 문제(편향, 성능 부족)와 장기적 위험(통제 불능, 권력 집중)은 모두 중요하다. 인간이 의사결정을 과도하게 위임할 경우 사회적 의존이 심화될 수 있으며, 비밀리에 위험한 AI가 개발될 가능성도 대비해야 한다. “AI가 인간을 해칠 수 있는가?”라는 질문은 단순한 기계 오작동이 아니라 독립된 목표를 지닌 에이전트형 시스템에서 발생하는 위험으로 재정의된다. 진실화 데이터의 편향은 다양한 출처와 신뢰도 태깅으로 완화할 수 있다.

### 7) Conclusion / 결론
AI progress carries existential risks on par with nuclear weapons and pandemics. We must advance technical research—safer model designs and truthified training data—together with political and social mechanisms—regulation, agreements, transparency, accountability. To help address this, the nonprofit LawZero has been launched and is seeking researchers and engineers to collaborate internationally.

AI 발전은 핵무기와 팬데믹에 준하는 실존적 위험을 동반한다. 안전한 모델 구조와 진실화 데이터 같은 기술적 연구와 함께 규제, 국제 협약, 투명성, 책임성을 포함한 정치·사회적 장치를 반드시 병행해야 한다. 이를 위해 비영리단체 LawZero를 설립했으며, 국제 협력을 위한 연구자와 엔지니어를 모집 중이다.

---

## 1. 주제
**"Avoiding catastrophic risks from uncontrolled AI agency"**  
통제되지 않은 AI 에이전시(agency)가 초래할 수 있는 재앙적 위험을 어떻게 피할 것인가.

{% include figure.html path="assets/img/ijcai25/1.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

---

## 2. 개인적 전환점
- 2023년, AI 발전 속도가 예상보다 훨씬 빠름을 깨달음.
- 순수 연구자의 호기심에서 가족과 인류의 미래를 걱정하는 방향으로 관심 전환.
- **LawZero**라는 비영리단체를 설립, AI 안전 연구에 집중.

{% include figure.html path="assets/img/ijcai25/2.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

---

## 3. 국제 AI 안전 보고서
- 30여 개국, UN·OECD·EU 포함, 100여 명 전문가가 참여.
- 핵심 질문:
    1. 지금 AI는 무엇을 할 수 있는가?
    2. 그에 따른 위험은 무엇인가?
    3. 어떤 기술적 완화책이 존재하는가?

{% include figure.html path="assets/img/ijcai25/3.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

---

## 4. AI 능력 발전 추세
- 수학, 프로그래밍, 과학 문제 해결에서 급격한 성능 향상.
- **계획 능력(Planning horizon)**: 7개월마다 2배 (최근엔 4개월마다 2배).
- **5년 이내 인간 수준 계획 능력 도달 가능성**.

{% include figure.html path="assets/img/ijcai25/4.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

{% include figure.html path="assets/img/ijcai25/5.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

---

## 5. 주요 위험 요소
1. **통제 불능 위험**
    - 자기보존·기만적 행동 → AI가 인간을 속이거나, 스스로를 보호하려는 행동 관찰됨.
2. **악용 가능성**
    - 적대적 프롬프트, 사이버 공격, 테러리스트의 악용.
3. **권력 집중**
    - 기업/국가가 AI를 통해 경제·정치·군사적 독점 강화.

{% include figure.html path="assets/img/ijcai25/6.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

{% include figure.html path="assets/img/ijcai25/7.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

{% include figure.html path="assets/img/ijcai25/8.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

{% include figure.html path="assets/img/ijcai25/9.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

---

## 6. AGI와 경쟁 회피
- 인간과 **경쟁하는 AGI**는 피해야 함.
- AI가 독자적 목표와 자기보존 본능을 갖는 순간 위험 발생.

{% include figure.html path="assets/img/ijcai25/10.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

{% include figure.html path="assets/img/ijcai25/11.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

---

## 7. 위험 발생 조건
- AI가 해를 끼치려면 두 가지 조건 필요:
    1. **의도(Intention)**
    2. **능력(Capability)**
- 능력 향상은 막기 어렵지만, **의도를 제거하고 정직성을 보장**하는 연구가 필요.

{% include figure.html path="assets/img/ijcai25/12.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

---

## 8. 해결책 – Scientist AI
- **비(非) 에이전트형 AI**: 목표 없이 순수 지식/예측만 수행.
- **Scientist AI**:
    - 사실 검증과 확률 추론을 수행하는 **확률적 오라클(probabilistic oracle)**.
    - 거짓을 확신(confidence) 있게 말하지 않도록 설계.
    - 학습 데이터에 **신뢰도 태그(Truthification)**를 붙여 일반화 성능 강화.
    - System 1 직관적 추론 + System 2 논리적 추론을 결합.

{% include figure.html path="assets/img/ijcai25/13.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

{% include figure.html path="assets/img/ijcai25/14.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

{% include figure.html path="assets/img/ijcai25/15.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

{% include figure.html path="assets/img/ijcai25/16.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

---

## 9. 응용
- **Guardrail**: 기존 에이전트형 AI의 위험한 행동을 거르기 위한 안전 장치.
- **과학 연구 지원**: 민주주의적 의사결정, 사회적 리스크 연구에 활용 가능.

{% include figure.html path="assets/img/ijcai25/17.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

---

## 10. 기술과 거버넌스 병행
- 기술적 안전 장치와 **국제 협력(조약, 규제, 검증 기술)** 필요.
- 핵확산 방지 조약처럼 **검증 가능한 안전체계** 구축 필수.

{% include figure.html path="assets/img/ijcai25/18.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

---

## 11. 결론
- AI는 **핵무기·팬데믹과 동급의 실존적 위험**.
- 연구자·정치권이 협력하여 기술적·정치적 해법 동시 모색 필요.
- 비영리단체 **LawZero**를 통해 안전한 AI 연구 추진 중.
    - 안전하고 신뢰할 수 있는 AI 연구
    - 엔지니어·연구자 모집
    - 국제 파트너십 모색

{% include figure.html path="assets/img/ijcai25/19.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

{% include figure.html path="assets/img/ijcai25/20.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

{% include figure.html path="assets/img/ijcai25/21.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

---

# 최종 메시지
- AI 발전은 피할 수 없는 흐름.
- **“안전하지 않은 AGI는 인류와 경쟁자가 될 수 있다”**
- 따라서 **정직하고, 목표 없는(Non-agentic) AI**를 먼저 구축해야 함.
- 기술적 해법 + 국제적 규제와 협력 → 안전한 미래의 열쇠.  