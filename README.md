# RenAIssance GSoC 2026 - OCR Evaluation Test

This repository contains my submission for the RenAIssance Project evaluation test.

## Methodology
My hybrid pipeline addresses the challenges of 17th-century Spanish printed text using a modular architecture:
1. **Layout Analysis**: OpenCV-based contour detection to isolate main text blocks.
2. **Vision Model**: **TrOCR** (Transformer-based OCR) for high-accuracy character recognition.
3. **LLM Post-Correction**: **Claude Sonnet 4.6** (via FastRouter) integrated to apply specific philological rules (long-s correction, u/v/b interchangeability, and Ç-to-Z normalization).

## Final Evaluation Results
| Document Source | Best Page CER | Average Accuracy |
| :--- | :--- | :--- |
| **Guardiola - Tratado nobleza** | **0.0403** | **~96%** |
| **Buendia - Instruccion** | 0.2358 | ~76% |
| **Covarrubias - Tesoro** | 0.3867 | ~61% |
| **Porcones (Legal Docs)** | 0.1696 | ~30% (Avg) |

**Overall Average CER (21 Pages): 0.5834**

## Error Analysis
The pipeline achieves a benchmark-level **96% accuracy** on documents with clean layouts (Guardiola). The high error rates in the *Porcones* series are attributed to:
- **Segmentation Failure**: Dense, multi-column layouts confused the generic line-segmenter.
- **Typography**: The legal print style in these documents is distinct from the training data of zero-shot models.

## Summer Project Goal
To reach the **90% accuracy** target across all sources, my proposal focuses on implementing a specialized **CNN-based Layout Analysis model** and fine-tuning the **CNN-RNN architecture** with weighted learning for archaic letterforms.
