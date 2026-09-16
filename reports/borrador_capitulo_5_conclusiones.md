# Borrador para memoria - Capítulo 5 Conclusiones y trabajo futuro

## Conclusiones

El trabajo ha desarrollado y validado experimentalmente un prototipo de triage forense asistido por análisis de datos sobre eventos Windows. El sistema parte de evidencias EVTX generadas con Sysmon y PowerShell Operational, las transforma a un formato tabular, agrega eventos por proceso y genera rankings de prioridad mediante dos enfoques: un baseline heurístico interpretable y un modelo no supervisado basado en `IsolationForest`.

La principal conclusión experimental es que, en el laboratorio diseñado, el baseline heurístico obtiene mejores resultados que el modelo de Machine Learning. El baseline recupera 12 de 14 procesos sospechosos simulados en el Top 20, mientras que el modelo ML recupera 2 de 14. Este resultado pone de manifiesto que el conocimiento experto, cuando se formaliza en reglas transparentes, puede resultar especialmente eficaz en escenarios de triage con datasets reducidos y técnicas simuladas bien definidas.

El prototipo no pretende sustituir el criterio de un analista, sino reducir el volumen inicial de revisión y ordenar los procesos de acuerdo con su interés forense. La salida del sistema es interpretable, ya que el baseline proporciona razones asociadas a cada puntuación, como rutas temporales, comandos codificados, modificaciones de persistencia o actividad de red.

## Limitaciones

La validación se ha realizado en una única máquina virtual y con escenarios controlados. No se ha ejecutado malware real y el etiquetado se basa en ventanas temporales y coincidencias de artefactos esperados. Por tanto, los resultados no deben generalizarse como capacidad de detección universal.

El dataset es reducido, especialmente en procesos normales de entrenamiento. Además, la actividad de fondo del sistema introduce ruido operativo que puede afectar tanto al baseline como al modelo ML. En el caso de `IsolationForest`, el tamaño limitado del conjunto normal y la presencia de procesos legítimos poco frecuentes reducen la calidad del ranking.

## Trabajo futuro

Como líneas futuras se propone ampliar el laboratorio con más máquinas, más perfiles de usuario y escenarios adicionales. También sería recomendable incorporar datasets públicos, comparar otros modelos supervisados y semisupervisados, integrar eventos de Security y System en la agregación por proceso y desarrollar una interfaz de analista que permita revisar los rankings con explicación de indicadores.

Otra línea relevante sería diseñar un enfoque híbrido, donde reglas expertas generen características interpretables y modelos ML aprendan patrones a partir de datasets más amplios. Este enfoque podría combinar la explicabilidad del baseline con la capacidad de generalización de modelos entrenados con más datos.
