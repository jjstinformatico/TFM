---

## Fase 8 - Consolidación de resultados, tablas, figuras y discusión

**Estado:** completada.  
**Objetivo:** consolidar los resultados de las fases 6 y 7, preparar tablas y figuras para la memoria, y redactar una primera discusión técnica de la comparación entre baseline heurístico y modelo de Machine Learning.

**Máquina utilizada:** LABWIN / entorno de análisis del TFM.  
**Dataset de entrada:** resultados de Fase 6 y Fase 7.  
**Ficheros principales de entrada:**

- `reports/ranking_baseline.csv`
- `reports/baseline_evaluation.json`
- `reports/ranking_ml.csv`
- `reports/ml_evaluation.json`
- `reports/comparison_baseline_ml.csv`
- `reports/comparison_baseline_ml.json`

**Acciones realizadas:**

1. Consolidación de métricas `Precision@K` y `Recall@K`.
2. Generación de tabla final comparativa entre baseline y modelo ML.
3. Extracción del Top 20 del baseline heurístico.
4. Extracción del Top 20 del ranking ML.
5. Identificación de posiciones de procesos `suspicious_simulated` en ambos rankings.
6. Generación de figuras comparativas para la memoria.
7. Redacción del resumen de discusión de resultados.
8. Redacción de conclusiones experimentales.
9. Preparación de borradores para el apartado de resultados y conclusiones de la memoria.
10. Cálculo de hashes SHA-256 de los artefactos generados.

**Ficheros generados:**

| Fichero | Descripción |
|---|---|
| `reports/tabla_metricas_final.csv` | Tabla final de métricas baseline frente a ML |
| `reports/top20_baseline_para_memoria.csv` | Top 20 del baseline heurístico |
| `reports/top20_ml_para_memoria.csv` | Top 20 del modelo ML |
| `reports/posiciones_procesos_sospechosos.csv` | Posiciones de procesos sospechosos simulados en ambos rankings |
| `reports/distribucion_etiquetas_top20.csv` | Distribución de etiquetas en los Top 20 |
| `reports/resumen_discusion_resultados.md` | Resumen técnico de discusión |
| `reports/conclusiones_experimentales.md` | Conclusiones experimentales |
| `reports/borrador_apartado_4_3_resultados.md` | Borrador de redacción para resultados |
| `reports/borrador_capitulo_5_conclusiones.md` | Borrador de conclusiones y trabajo futuro |
| `figures/comparacion_precision_recall.png` | Comparación visual de Precision@K y Recall@K |
| `figures/precision_at_k.png` | Comparación de Precision@K |
| `figures/recall_at_k.png` | Comparación de Recall@K |
| `figures/top20_baseline.png` | Visualización del Top 20 baseline |
| `figures/top20_ml.png` | Visualización del Top 20 ML |
| `figures/distribucion_etiquetas_top20.png` | Distribución de etiquetas en Top 20 |
| `hashes/hashes_fase8_reports.txt` | Hashes de reportes generados |
| `hashes/hashes_fase8_figures.txt` | Hashes de figuras generadas |

**Resumen comparativo de métricas:**

| K | Precision baseline | Recall baseline | Precision ML | Recall ML |
|---:|---:|---:|---:|---:|
| 5 | 0.4000 | 0.1429 | 0.2000 | 0.0714 |
| 10 | 0.5000 | 0.3571 | 0.1000 | 0.0714 |
| 15 | 0.5333 | 0.5714 | 0.1333 | 0.1429 |
| 20 | 0.6000 | 0.8571 | 0.1000 | 0.1429 |

**Resultado principal:**

El baseline heurístico supera al modelo `IsolationForest` en todos los valores de K evaluados. En el Top 20, el baseline recupera 12 de los 14 procesos `suspicious_simulated`, mientras que el modelo ML recupera 2 de 14.

**Interpretación:**

El resultado confirma que, en este laboratorio controlado y con dataset reducido, la formalización de conocimiento experto en reglas interpretables resulta más eficaz para priorización forense que un modelo no supervisado de anomalías. El modelo ML identifica rareza estadística, pero no necesariamente relevancia forense.

**Utilidad dentro del TFM:**

Esta fase proporciona las tablas, figuras y textos base necesarios para redactar el capítulo de resultados, la discusión, las conclusiones y las limitaciones metodológicas del trabajo.
