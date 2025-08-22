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

{% include figure.html path="assets/img/ijcai25/9.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

---

## 6. AGI와 경쟁 회피
- 인간과 **경쟁하는 AGI**는 피해야 함.
- AI가 독자적 목표와 자기보존 본능을 갖는 순간 위험 발생.

{% include figure.html path="assets/img/ijcai25/11.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

{% include figure.html path="assets/img/ijcai25/10.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

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

{% include figure.html path="assets/img/ijcai25/8.jpeg" class="img-fluid rounded z-depth-1" zoomable=true %}

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