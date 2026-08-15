<a id="top"></a>

<p align="center">
  <a href="#_" aria-label="NANIM NO WORRY fertility AI research visual"><img src="./assets/hero.svg" width="100%" alt="NANIM NO WORRY fertility AI research" /></a>
</p>

<h1 align="center">난임걱정마삼조</h1>

<p align="center">
  <strong>난임 환자 대상 임신 성공 여부 예측 AI 프로젝트</strong><br />
  구조적 결측 · OOF 검증 · CatBoost/LightGBM/XGBoost · Ensemble
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Task-Binary%20Classification-2563EB?style=flat-square" alt="Binary Classification" />
  <img src="https://img.shields.io/badge/Metric-ROC--AUC-7C3AED?style=flat-square" alt="ROC-AUC" />
  <img src="https://img.shields.io/badge/Models-CatBoost%20%7C%20LightGBM%20%7C%20XGBoost-059669?style=flat-square" alt="Models" />
  <img src="https://img.shields.io/badge/Final-Plan%203%20%C2%B7%200.74231-EA580C?style=flat-square" alt="Final model" />
</p>

---

## Project

**Task:** 난임 시술 데이터 기반 임신 성공 여부 이진 분류  
**Metric:** ROC-AUC  
**Clinical axes:** 연령 · 시술 유형 · 난자/배아/이식 정보 · 과거 시술 이력

**결측 처리:** IVF/DI 시술 구조 차이 반영. 배아·난자·이식 관련 동시 결측은 비해당 구조와 일반 결측을 분리.

## Final Result

| 항목 | 결과 |
|---|---:|
| 1안 | OOF 기반 기초 모델 · 제출 `0.74213` |
| 2안 | Feature 확장 + Ensemble / Stacking · **제출 `0.74232`** |
| 3안 | OOF + Multi-Seed · 제출 `0.74231` |
| 최고 제출 점수 | **2안 · 0.74232** |
| 최종 채택 모델 | **3안 · 0.74231** |

**채택 기준:** 제출 점수 단독 최적화 제외 · 모델 복잡도 · 검증 부담 · seed 변동성 · 추론 비용

## Model Lineage

<p align="center">
  <a href="#_" aria-label="Fertility PSP model lineage visual"><img src="./assets/model-lineage.svg" width="100%" alt="Fertility PSP model lineage" /></a>
</p>

공식 계보·제출 artifact: [`PSP`](https://github.com/nanimnoworry/PSP)

## Research

- **Structural missingness** — 시술별 비해당 구조 / 일반 결측 분리
- **Feature Engineering** — 연령 구간 · 시술 유형 · 난자/배아 수 · 이식 시점 · 기증자 정보 · 과거 시술 이력 · 상호작용
- **OOF validation** — K-Fold OOF 중심
- **Ensemble** — Weighted · Rank · Multi-Seed · Stacking

## Public Repositories

| Repository | 범위 |
|---|---|
| **[`PSP`](https://github.com/nanimnoworry/PSP)** | 공식 프로젝트 · 최종 제출/발표 · 모델 계보 |
| [`BS`](https://github.com/nanimnoworry/BS) | 3안 연계 모델 비교 · OOF · Weighted/Rank Ensemble |

후속 실험·임상/문헌 근거 — Organization 내부 저장소.

---

<p align="center">
  <strong>Final adopted model: Plan 3 · Submission ROC-AUC 0.74231</strong><br />
  <sub>Highest submitted AUC: Plan 2 · 0.74232</sub>
</p>

**용도 제한:** 임상 의사결정용 모델 아님.

---

## License and Rights

**Public view · no public reuse license.**  
Organization 소개·시각 자산은 별도 허가 없는 재사용/재배포 불가.

[LICENSE](../LICENSE) · [RIGHTS.md](../RIGHTS.md) · [CONTRIBUTORS.md](../CONTRIBUTORS.md)
