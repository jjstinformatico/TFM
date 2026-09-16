# Conclusiones experimentales - Fase 8

## Conclusión 1. El pipeline completo es funcional

El laboratorio ha permitido construir un flujo completo desde la generación de eventos Windows hasta la priorización de procesos. El pipeline incluye instalación y validación de Sysmon, generación de actividad normal, generación de actividad sospechosa simulada, conversión EVTX a CSV, etiquetado experimental, agregación por proceso, baseline heurístico y comparación con un modelo de Machine Learning.

## Conclusión 2. La línea base normal es necesaria

Los escenarios normales de Fase 3 muestran que procesos como `powershell.exe`, `cmd.exe`, conexiones DNS/HTTPS, creación de ficheros y consultas administrativas pueden aparecer en actividad legítima. Por ello, no basta con detectar la presencia de una herramienta o comando; es necesario valorar contexto, relación padre-hijo, ruta, línea de comandos y combinación de indicadores.

## Conclusión 3. Los escenarios sospechosos simulados son adecuados para evaluar priorización

La Fase 4 generó patrones representativos de interés forense sin ejecutar malware real: ruta temporal, PowerShell codificado, clave `Run`, tarea programada, servicio, carpeta Startup y conexión de red desde PowerShell. Estos escenarios son suficientes para validar un prototipo de priorización, aunque no equivalen a una infección real.

## Conclusión 4. El baseline heurístico obtiene mejor rendimiento en este laboratorio

El baseline recupera 12 de los 14 procesos `suspicious_simulated` en el Top 20, con `Precision@20` de 0,60 y `Recall@20` de 0,8571. Esto demuestra que una aproximación interpretable basada en conocimiento experto puede ser muy útil para triage forense inicial.

## Conclusión 5. El modelo Isolation Forest no mejora al baseline

El modelo `IsolationForest` recupera solo 2 de los 14 procesos `suspicious_simulated` en el Top 20. Su Top 10 queda dominado por procesos `background`. La anomalía estadística no equivale necesariamente a relevancia forense, especialmente cuando el dataset es pequeño y contiene ruido operativo.

## Conclusión 6. La interpretabilidad es clave para el analista

El baseline ofrece razones explícitas para cada puntuación: ruta temporal, `EncodedCommand`, clave `Run`, tarea programada, creación de servicio, carpeta Startup, conexión de red, LOLBins o relación padre-hijo poco frecuente. Esta trazabilidad favorece su uso como herramienta de apoyo al analista.

## Conclusión 7. El resultado justifica enfoques híbridos futuros

Una línea futura razonable sería combinar reglas expertas con modelos supervisados o semisupervisados entrenados con datasets más amplios. También sería conveniente incorporar más familias de eventos, más escenarios, validación cruzada temporal y comparación con datasets públicos.
