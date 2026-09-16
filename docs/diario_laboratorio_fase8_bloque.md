---

## Sesión 8 - Consolidación de resultados, tablas, figuras y discusión

**Fecha:** 05/08/2026.

**Objetivo de la sesión:** consolidar los resultados de las fases 6 y 7, preparar tablas y figuras para la memoria del TFM, y redactar una primera discusión técnica de la comparación entre baseline heurístico y modelo de Machine Learning.

**Acciones realizadas:**

1. Revisión de los rankings `ranking_baseline.csv` y `ranking_ml.csv`.
2. Consolidación de métricas `Precision@K` y `Recall@K`.
3. Generación de tablas comparativas.
4. Extracción de Top 20 para baseline y ML.
5. Identificación de posiciones de procesos sospechosos simulados.
6. Generación de figuras para la memoria.
7. Redacción de resumen de discusión.
8. Redacción de conclusiones experimentales.
9. Preparación de borradores para los capítulos de resultados y conclusiones.
10. Cálculo de hashes de evidencias generadas.

**Evidencias generadas:**

- `reports\tabla_metricas_final.csv`
- `reports\top20_baseline_para_memoria.csv`
- `reports\top20_ml_para_memoria.csv`
- `reports\posiciones_procesos_sospechosos.csv`
- `reports\distribucion_etiquetas_top20.csv`
- `reports\resumen_discusion_resultados.md`
- `reports\conclusiones_experimentales.md`
- `reports\borrador_apartado_4_3_resultados.md`
- `reports\borrador_capitulo_5_conclusiones.md`
- `figures\comparacion_precision_recall.png`
- `figures\precision_at_k.png`
- `figures\recall_at_k.png`
- `figures\top20_baseline.png`
- `figures\top20_ml.png`
- `figures\distribucion_etiquetas_top20.png`

**Observaciones:**

La comparación muestra que el baseline heurístico obtiene mejores resultados que el modelo `IsolationForest` en este laboratorio. Esta conclusión es relevante para la memoria, ya que permite defender la utilidad de enfoques interpretables y basados en conocimiento experto en contextos de triage forense con dataset reducido.

**Pendientes para la siguiente fase:**

1. Integrar estos resultados en la memoria.
2. Redactar de forma definitiva el capítulo 4.
3. Redactar conclusiones finales.
4. Preparar anexos técnicos con scripts, hashes y evidencias.
