# Resumen de discusión de resultados - Fase 8

## Objetivo

La Fase 8 consolida los resultados generados en las fases anteriores y prepara el material que se utilizará en la memoria del TFM para presentar la comparación entre el baseline heurístico y el modelo de Machine Learning no supervisado.

El análisis se basa en los ficheros generados en las fases 6 y 7:

- `reports/ranking_baseline.csv`
- `reports/baseline_evaluation.json`
- `reports/ranking_ml.csv`
- `reports/ml_evaluation.json`
- `reports/comparison_baseline_ml.csv`
- `reports/comparison_baseline_ml.json`

## Resultado principal

El baseline heurístico ofrece mejores resultados de priorización que el modelo `IsolationForest` en este laboratorio controlado.

| K | Precision baseline | Recall baseline | Precision ML | Recall ML |
|---:|---:|---:|---:|---:|
| 5 | 0.4000 | 0.1429 | 0.2000 | 0.0714 |
| 10 | 0.5000 | 0.3571 | 0.1000 | 0.0714 |
| 15 | 0.5333 | 0.5714 | 0.1333 | 0.1429 |
| 20 | 0.6000 | 0.8571 | 0.1000 | 0.1429 |

## Interpretación

El baseline heurístico recupera una mayor proporción de procesos `suspicious_simulated` en las primeras posiciones del ranking. En el Top 20 alcanza un `Recall@20` de 0,8571, mientras que el modelo `IsolationForest` alcanza 0,1429. Este resultado indica que, en un dataset pequeño y controlado, la incorporación explícita de conocimiento experto sobre indicadores forenses resulta más eficaz que una aproximación no supervisada basada exclusivamente en anomalía estadística.

## Top 10 baseline heurístico

|   rank |   baseline_score | risk_level   | label                | scenario_ids         | process_name     |
|-------:|-----------------:|:-------------|:---------------------|:---------------------|:-----------------|
|      1 |              109 | alto         | suspicious_simulated | S1;S2;S3;S4;S5;S6;S7 | powershell.exe   |
|      2 |               91 | alto         | suspicious_simulated | S2                   | powershell.exe   |
|      3 |               81 | alto         | background           | S2;S3                | firefox.exe      |
|      4 |               66 | medio        | normal               | N4                   | powershell.exe   |
|      5 |               61 | medio        | normal               | N4                   | powershell.exe   |
|      6 |               61 | medio        | normal               | N4                   | powershell.exe   |
|      7 |               61 | medio        | normal               | N4                   | powershell.exe   |
|      8 |               51 | medio        | suspicious_simulated | S3                   | reg.exe          |
|      9 |               51 | medio        | suspicious_simulated | S3                   | reg.exe          |
|     10 |               51 | medio        | suspicious_simulated | S1                   | svchost-test.exe |

## Top 10 modelo ML

|   ml_rank |   ml_anomaly_score | label                | scenario_ids         | process_name       |
|----------:|-------------------:|:---------------------|:---------------------|:-------------------|
|         1 |          0.215356  | normal               | N1;N2;N3;N4;N5       | powershell.exe     |
|         2 |          0.207656  | background           | S2;S3                | firefox.exe        |
|         3 |          0.174434  | suspicious_simulated | S1;S2;S3;S4;S5;S6;S7 | powershell.exe     |
|         4 |          0.135223  | background           | S2                   | svchost.exe        |
|         5 |          0.129195  | background           |                      | msedgewebview2.exe |
|         6 |          0.108042  | background           |                      | systemsettings.exe |
|         7 |          0.103208  | background           | S2                   | taskhostw.exe      |
|         8 |          0.0968645 | background           |                      | svchost.exe        |
|         9 |          0.0937236 | background           | S2;S3;S5;S7          | svchost.exe        |
|        10 |          0.0889131 | background           |                      | svchost.exe        |

## Falsos positivos y ruido operativo

El baseline heurístico sitúa en posiciones altas algunos procesos normales o de contexto, especialmente `powershell.exe` normal del escenario N4 y `firefox.exe` como proceso `background`. Esto demuestra que las reglas heurísticas son interpretables, pero pueden elevar actividad legítima cuando comparte rasgos con patrones de interés forense.

El modelo `IsolationForest`, por su parte, sitúa numerosos procesos `background` en el Top 10, como `firefox.exe`, `svchost.exe`, `msedgewebview2.exe` o `taskhostw.exe`. Esto sugiere que el modelo detecta rareza estadística, pero no necesariamente prioriza los artefactos forenses más relevantes del experimento.

## Conclusión de la comparación

La comparación no debe interpretarse como un rechazo general del Machine Learning en triage forense, sino como una evidencia experimental limitada al laboratorio diseñado. En este contexto, el baseline heurístico resulta más eficaz y más explicable. El modelo ML aporta una referencia comparativa útil y permite justificar que la aplicación de ML requiere datasets mayores, mejor balanceados, validación externa y posiblemente enfoques híbridos.
