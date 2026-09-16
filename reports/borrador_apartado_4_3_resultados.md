# Borrador para memoria - Apartado 4.3 Resultados experimentales

## 4.3.X Evaluación del baseline heurístico

El baseline heurístico se aplicó sobre el fichero `process_features.csv`, que contiene 176 procesos agregados a partir de eventos Sysmon. De ellos, 14 procesos estaban etiquetados como `suspicious_simulated`, 41 como `normal` y 121 como `background`.

El ranking heurístico asignó puntuaciones a cada proceso en función de indicadores interpretables: ejecución desde ruta temporal, uso de PowerShell, presencia de `EncodedCommand`, modificación de claves `Run`, creación de tareas programadas, creación de servicios, artefactos en carpeta Startup, conexiones de red, uso de binarios administrativos y presencia de palabras clave de interés.

El baseline alcanzó los siguientes resultados:

|   k |   baseline_precision |   baseline_recall |
|----:|---------------------:|------------------:|
|   5 |               0.4    |            0.1429 |
|  10 |               0.5    |            0.3571 |
|  15 |               0.5333 |            0.5714 |
|  20 |               0.6    |            0.8571 |

En el Top 20, el baseline recuperó 12 de los 14 procesos de interés, con un `Recall@20` de 0,8571. Este comportamiento indica que el enfoque heurístico es adecuado para reducir el volumen de revisión inicial, ya que concentra la mayoría de procesos sospechosos simulados en las primeras posiciones.

## 4.3.X Evaluación del modelo Machine Learning

El modelo `IsolationForest` se entrenó únicamente con los 41 procesos etiquetados como normales. El objetivo fue modelar el comportamiento base y ordenar el resto de procesos por anomalía. El modelo produjo un ranking completo, pero sus resultados fueron inferiores a los del baseline:

|   k |   ml_precision |   ml_recall |
|----:|---------------:|------------:|
|   5 |         0.2    |      0.0714 |
|  10 |         0.1    |      0.0714 |
|  15 |         0.1333 |      0.1429 |
|  20 |         0.1    |      0.1429 |

En el Top 20, el modelo recuperó 2 de los 14 procesos `suspicious_simulated`, con un `Recall@20` de 0,1429. El Top 10 quedó dominado por eventos `background`, lo que indica que el modelo identificó procesos estadísticamente anómalos, pero no necesariamente los más relevantes desde el punto de vista forense.

## 4.3.X Comparación de enfoques

La comparación directa muestra que el baseline supera al modelo ML en todos los valores de K evaluados:

|   k |   baseline_precision |   baseline_recall |   ml_precision |   ml_recall |   precision_advantage_baseline |   recall_advantage_baseline |
|----:|---------------------:|------------------:|---------------:|------------:|-------------------------------:|----------------------------:|
|   5 |               0.4    |            0.1429 |         0.2    |      0.0714 |                            0.2 |                      0.0714 |
|  10 |               0.5    |            0.3571 |         0.1    |      0.0714 |                            0.4 |                      0.2857 |
|  15 |               0.5333 |            0.5714 |         0.1333 |      0.1429 |                            0.4 |                      0.4286 |
|  20 |               0.6    |            0.8571 |         0.1    |      0.1429 |                            0.5 |                      0.7143 |

El resultado es coherente con las condiciones del experimento. El dataset es pequeño, procede de un laboratorio controlado y los escenarios sospechosos fueron diseñados a partir de patrones forenses concretos. En este contexto, las reglas expertas capturan mejor la relevancia forense que un modelo no supervisado de anomalías.

## 4.3.X Discusión

Los resultados no implican que Machine Learning sea inadecuado para triage forense, sino que su utilidad depende de la calidad, tamaño y representatividad del dataset. En este laboratorio, el modelo no supervisado se ve afectado por ruido operativo y por procesos legítimos poco frecuentes, mientras que el baseline incorpora conocimiento explícito sobre técnicas simuladas.

Por tanto, el prototipo demuestra dos ideas relevantes: primero, que es posible automatizar una priorización inicial de procesos a partir de eventos Windows; segundo, que la interpretabilidad y el conocimiento experto siguen siendo factores clave en entornos forenses.
