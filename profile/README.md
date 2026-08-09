<a id="top"></a>

<p align="center">
  <img src="./assets/hero.svg" width="100%" alt="NANIM NO WORRY fertility AI research" />
</p>

<h1 align="center">난임걱정마삼조</h1>

<p align="center">
  <strong>난임 환자 대상 임신 성공 여부 예측 AI 프로젝트</strong><br />
  난임 시술 데이터의 구조를 분석하고 OOF 검증과 앙상블을 이용해 임신 성공 확률을 예측했습니다.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Task-Binary%20Classification-2563EB?style=flat-square" alt="Binary Classification" />
  <img src="https://img.shields.io/badge/Metric-ROC--AUC-7C3AED?style=flat-square" alt="ROC-AUC" />
  <img src="https://img.shields.io/badge/Models-CatBoost%20%7C%20LightGBM%20%7C%20XGBoost-059669?style=flat-square" alt="Models" />
  <img src="https://img.shields.io/badge/Final-Plan%203%20%C2%B7%200.74231-EA580C?style=flat-square" alt="Final model" />
</p>

---

## Project

연령, 시술 유형, 난자·배아·이식 정보, 과거 시술 이력 등을 이용한 ROC-AUC 기반 이진 분류 프로젝트입니다.

IVF와 DI처럼 시술 과정이 다른 경우에는 결측값의 의미도 달라질 수 있다고 보고, 배아·난자·이식 관련 값이 함께 비는 패턴을 구조적 결측으로 다뤘습니다. 모델링에서는 CatBoost, LightGBM, XGBoost를 중심으로 OOF 검증과 여러 앙상블 방식을 비교했습니다.

## Final Result

| 항목 | 결과 |
|---|---:|
| 1안 | OOF 기반 기초 모델 · 제출 `0.74213` |
| 2안 | Feature 확장 + Ensemble / Stacking · **제출 `0.74232`** |
| 3안 | OOF + Multi-Seed · 제출 `0.74231` |
| 최고 제출 점수 | **2안 · 0.74232** |
| 최종 채택 모델 | **3안 · 0.74231** |

2안의 제출 점수가 조금 더 높았지만, 최종 발표에서는 모델 복잡도와 검증 부담, seed 변동성, 추론 비용까지 고려해 3안을 최종 모델로 선택했습니다.

## Model Lineage

<p align="center">
  <a href="https://github.com/nanimnoworry/PSP/blob/main/docs/model_lineage.md">
    <img src="./assets/model-lineage.svg" width="100%" alt="Fertility PSP model lineage" />
  </a>
</p>

공식 모델 계보와 최종 제출 자료는 [`PSP`](https://github.com/nanimnoworry/PSP)에 정리되어 있습니다.

## Research

- **구조적 결측:** 시술 유형에 따라 원래 존재하지 않는 정보를 일반적인 결측과 구분했습니다.
- **Feature Engineering:** 연령 구간, 시술 유형, 난자·배아 수, 이식 시점, 기증자 정보, 과거 시술 이력과 상호작용을 검토했습니다.
- **OOF 검증:** 단일 hold-out보다 K-Fold OOF를 중심으로 모델과 앙상블을 비교했습니다.
- **앙상블:** Weighted, Rank, Multi-Seed, Stacking 계열을 실험했습니다.

## Public Repositories

| Repository | 내용 |
|---|---|
| **[`PSP`](https://github.com/nanimnoworry/PSP)** | 공식 프로젝트, 최종 제출·발표 결과, 모델 계보 |
| [`BS`](https://github.com/nanimnoworry/BS) | 3안과 연결된 모델 비교·OOF·Weighted/Rank Ensemble 연구 |

후속 실험 기록과 임상·문헌 근거 자료는 Organization 내부 저장소에 별도로 보존하고 있습니다.

---

<p align="center">
  <strong>Final adopted model: Plan 3 · Submission ROC-AUC 0.74231</strong><br />
  <sub>Highest submitted AUC: Plan 2 · 0.74232</sub>
</p>

연구 결과는 실제 의료 판단이나 임상 의사결정을 위한 모델이 아닙니다.
