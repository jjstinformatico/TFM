# Diario de laboratorio del TFM

## Datos generales del trabajo

**Título provisional:** Triage forense asistido por Machine Learning: priorización automática de procesos y eventos en Windows mediante Sysmon y EVTX.

**Tipo de trabajo:** Desarrollo de software con validación experimental.

**Objetivo del laboratorio:** generar, conservar y analizar evidencias procedentes de una máquina Windows 11 mediante registros EVTX y Sysmon, con el fin de construir un dataset de laboratorio que permita evaluar una herramienta Python de priorización forense de procesos.

**Unidad principal de análisis:** proceso Windows, preferentemente identificado mediante ProcessGuid cuando esté disponible.

**Fuentes previstas de datos:**
- Microsoft-Windows-Sysmon/Operational.
- Security.evtx.
- Microsoft-Windows-PowerShell/Operational.evtx.
- System.evtx, si aporta valor complementario.

---

## Topología del laboratorio

El laboratorio se compone de dos sistemas:

### Máquina anfitriona

**Rol:** equipo de gestión del laboratorio, ejecución del hipervisor, almacenamiento de copias de seguridad de evidencias, edición de documentación y memoria.

**Sistema operativo:** Windows 11 pro.

**Hipervisor utilizado:** Oracle Virtualbox.

**Uso en el experimento:** la máquina anfitriona no será objeto de análisis forense y no se utilizará para generar eventos del dataset. Su función será únicamente de soporte y gestión.

### Máquina virtual Windows 11

**Rol:** sistema objeto de análisis forense y fuente principal de generación de eventos.

**Sistema operativo:** Windows 11.

**Uso en el experimento:** en esta máquina se instalará Sysmon, se generará actividad normal y actividad sospechosa simulada, se exportarán los registros EVTX y se ejecutarán los scripts de procesamiento.

**Estado inicial:** estructura de laboratorio creada, diario iniciado, transcript de PowerShell generado y snapshot inicial registrado como `S01_Snapshot_Inicial`. La validación técnica detallada se realizará en Fase 1.

---

## Decisiones iniciales de alcance

1. El laboratorio se limita a sistemas Windows.
2. No se utilizará malware real.
3. Los escenarios sospechosos serán simulados, benignos y controlados.
4. El objetivo no es atribuir ataques ni sustituir al analista forense.
5. El objetivo es generar un ranking de procesos priorizados para apoyar el triage inicial.
6. La herramienta se desarrollará en Python y funcionará mediante línea de comandos.
7. La evaluación se realizará sobre datos generados en laboratorio.
8. Todas las evidencias relevantes se conservarán junto con sus hashes cuando proceda.

---

## Estructura inicial de carpetas

La carpeta principal del laboratorio en la máquina virtual será:

`C:\TFM_Triage`

Subcarpetas previstas:

- `docs`: documentación del laboratorio.
- `reports`: salidas, informes y transcripciones.
- `raw`: evidencias EVTX originales.
- `processed`: datasets CSV/JSON procesados.
- `scripts`: scripts auxiliares.
- `hashes`: hashes SHA-256 de evidencias.
- `screenshots`: capturas de pantalla.
- `tools`: herramientas utilizadas.

---

## Sesión 0 - Preparación inicial

**Fecha:** 30/06/2026.

**Máquina utilizada:** máquina virtual LABWIN.

**Usuario utilizado:** labwin\jjstestal.

**Objetivo de la sesión:** preparar la estructura inicial del laboratorio, crear el diario técnico y activar la trazabilidad mediante transcripción de PowerShell.

**Acciones realizadas:**
1. Creación de la carpeta `C:\TFM_Triage`.
2. Creación de subcarpetas de trabajo.
3. Creación del archivo `diario_laboratorio.md`.
4. Preparación del archivo de transcripción automática de PowerShell.
5. Definición de la separación entre máquina anfitriona y máquina virtual.

**Evidencias generadas:**
- `C:\TFM_Triage\docs\diario_laboratorio.md`
- `C:\TFM_Triage\reports\transcript_laboratorio_fase0.txt`

**Observaciones:**
En esta fase todavía no se han generado eventos forenses, no se ha instalado Sysmon y no se han exportado registros EVTX. La finalidad ha sido únicamente preparar el entorno de trabajo y establecer la trazabilidad del laboratorio.

---

## Sesión 1 - Validación del entorno previo a Sysmon

**Fecha:** 30/06/2026.

**Máquina utilizada:** máquina virtual LABWIN.

**Usuario utilizado:** labwin\jjstestal.

**Objetivo de la sesión:** validar la configuración inicial del laboratorio antes de instalar Sysmon, documentando sistema operativo, usuario, privilegios, red, registros de eventos disponibles y estado previo del sistema.

**Acciones realizadas:**
1. Validación de la versión del sistema operativo mediante PowerShell, `systeminfo` y `winver`.
2. Verificación del usuario utilizado y sus privilegios.
3. Documentación de la configuración de red real.
4. Enumeración de registros de eventos disponibles.
5. Comprobación del estado previo del canal Sysmon.
6. Comprobación del estado de PowerShell Operational.
7. Creación del snapshot previo a Sysmon.
8. Preparación de carpetas para herramientas.
9. Generación de hashes de la documentación y reportes.

**Evidencias generadas:**
- `reports\transcript_laboratorio_fase1.txt`
- `reports\info_windows_detallada.txt`
- `reports\systeminfo_vm.txt`
- `reports\info_usuario_privilegios.txt`
- `reports\info_red_detallada.txt`
- `reports\info_eventlogs_disponibles.txt`
- `reports\info_log_powershell_operational.txt`
- `reports\info_log_sysmon_preinstalacion.txt`
- `reports\estado_sysmon_preinstalacion.txt`
- `reports\count_powershell_prepruebas.txt`
- `reports\count_security_prepruebas.txt`
- `reports\count_system_prepruebas.txt`
- `hashes\hashes_fase1_documentacion.txt`
- `hashes\hashes_fase1_reports.txt`
- `screenshots\fase1_winver.png`
- `screenshots\fase1_snapshot_presysmon.png`

**Observaciones:**
Esta fase no incluye generación de actividad normal ni sospechosa. Su finalidad es dejar documentado el estado previo del sistema antes de instalar Sysmon y antes de generar el dataset experimental.

**Pendientes para la Fase 2:**
1. Descargar Sysmon desde fuente oficial.
2. Seleccionar o crear configuración Sysmon.
3. Instalar Sysmon.
4. Verificar el servicio Sysmon.
5. Verificar el canal `Microsoft-Windows-Sysmon/Operational`.
6. Generar hash de la configuración Sysmon.
7. Crear snapshot posterior a instalación de Sysmon.


---

## Sesión 2 - Instalación y validación de Sysmon

**Fecha:** 30/06/2026.

**Máquina utilizada:** máquina virtual LABWIN.

**Usuario utilizado:** labwin\jjstestal con PowerShell elevado.

**Objetivo de la sesión:** instalar Sysmon, aplicar una configuración controlada para el TFM, verificar la creación del servicio y del canal de eventos, y generar eventos mínimos de validación.

**Acciones realizadas:**
1. Descarga de Sysmon desde Microsoft Sysinternals.
2. Cálculo del hash SHA-256 del paquete descargado.
3. Extracción del paquete Sysmon.
4. Verificación de firma digital del binario `Sysmon64.exe`.
5. Creación del archivo de configuración `sysmon_config_tfm.xml`.
6. Cálculo del hash SHA-256 de la configuración.
7. Instalación de Sysmon con la configuración definida.
8. Verificación del servicio `Sysmon64`.
9. Verificación del canal `Microsoft-Windows-Sysmon/Operational`.
10. Generación de eventos mínimos de validación.
11. Exportación del EVTX de validación.
12. Cálculo del hash SHA-256 del EVTX exportado.

**Evidencias generadas:**
- `tools\Sysmon\Sysmon.zip`
- `tools\Sysmon\Sysmon64.exe`
- `tools\Config\sysmon_config_tfm.xml`
- `reports\sysmon_signature.txt`
- `reports\sysmon_version.txt`
- `reports\sysmon_install_output.txt`
- `reports\estado_servicio_sysmon_postinstalacion.txt`
- `reports\info_log_sysmon_postinstalacion.txt`
- `reports\active_sysmon_config.txt`
- `reports\count_sysmon_postinstalacion.txt`
- `reports\sample_sysmon_events.txt`
- `raw\fase2_sysmon_validacion.evtx`
- `hashes\hash_sysmon_zip.txt`
- `hashes\hash_sysmon_binaries.txt`
- `hashes\hash_sysmon_config.txt`
- `hashes\hash_fase2_sysmon_validacion_evtx.txt`

**Observaciones:**
Los eventos generados en esta fase tienen finalidad exclusiva de validación técnica de Sysmon. No constituyen todavía el dataset experimental principal. El dataset será generado en fases posteriores mediante escenarios normales y sospechosos simulados, debidamente documentados.

**Incidencia durante la instalación:**
Durante la ejecución inicial de `Sysmon64.exe -accepteula -i`, PowerShell mostró un mensaje `NativeCommandError`. No obstante, la salida del propio ejecutable confirmó que la configuración XML fue validada correctamente, que `Sysmon64` y `SysmonDrv` fueron instalados y que ambos componentes se iniciaron correctamente. Una segunda ejecución con configuración mínima devolvió que el servicio `Sysmon64` ya estaba registrado, confirmando que la instalación inicial se había completado.


**Pendientes para la Fase 3:**
1. Snapshot posterior a la instalación de Sysmon creado como `S03_PostSysmon_Instalado`.
2. Generar actividad normal de usuario.
3. Generar actividad administrativa legítima.
4. Registrar marcas temporales de cada escenario.
5. Exportar registros EVTX para el dataset.


---

## Sesión 3 - Generación de actividad normal y línea base legítima

**Fecha:** 30/06/2026.

**Máquina utilizada:** máquina virtual LABWIN.

**Usuario utilizado:** labwin\jjstestal con PowerShell elevado.

**Objetivo de la sesión:** generar actividad normal y legítima en Windows para construir una línea base de comportamiento no malicioso, que servirá como comparación frente a los escenarios sospechosos simulados de fases posteriores.

**Acciones realizadas:**
1. Preservación previa del EVTX de validación de Fase 2.
2. Limpieza controlada del canal `Microsoft-Windows-Sysmon/Operational` para aislar el dataset normal.
3. Registro de marcas temporales por escenario.
4. Ejecución del escenario N1: actividad básica de usuario.
5. Ejecución del escenario N2: gestión normal de ficheros.
6. Ejecución del escenario N3: administración legítima de Windows.
7. Ejecución del escenario N4: uso legítimo de PowerShell.
8. Ejecución del escenario N5: conectividad de red legítima.
9. Recuento de eventos generados.
10. Extracción de muestras de eventos.
11. Exportación de registros EVTX.
12. Cálculo de hashes SHA-256.

**Escenarios ejecutados:**
- N1: actividad básica de usuario.
- N2: gestión normal de ficheros.
- N3: administración legítima de Windows.
- N4: uso legítimo de PowerShell.
- N5: conectividad de red legítima.

**Evidencias generadas:**
- `reports\fase3_scenarios_timestamps.csv`
- `reports\count_sysmon_fase3.txt`
- `reports\sample_sysmon_events_fase3.txt`
- `reports\sample_powershell_events_fase3.txt`
- `raw\fase3_sysmon_normal.evtx`
- `raw\fase3_powershell_normal.evtx`
- `raw\fase3_security_normal.evtx`
- `raw\fase3_system_normal.evtx`
- `hashes\hash_fase3_sysmon_normal.evtx.txt`
- `hashes\hash_fase3_powershell_normal.evtx.txt`
- `hashes\hash_fase3_security_normal.evtx.txt`
- `hashes\hash_fase3_system_normal.evtx.txt`

**Observaciones:**
Los eventos generados representan actividad legítima de usuario y administración básica. Esta fase no incluye actividad sospechosa simulada. Su finalidad es proporcionar una línea base normal para evaluar posteriormente la capacidad de priorización de la herramienta.

**Pendientes para la Fase 4:**
1. Generar escenarios sospechosos simulados y benignos.
2. Registrar marcas temporales por escenario.
3. Exportar EVTX de actividad sospechosa simulada.
4. Comparar eventos normales frente a eventos de interés forense.


---

## Sesión 4 - Generación de actividad sospechosa simulada

**Fecha:** 30/06/2026.

**Máquina utilizada:** máquina virtual LABWIN.

**Usuario utilizado:** labwin\jjstestal con PowerShell elevado.

**Objetivo de la sesión:** generar actividad sospechosa simulada, benigna y controlada, con el fin de disponer de eventos de interés forense que permitan evaluar posteriormente la priorización automática de procesos.

**Acciones realizadas:**
1. Verificación de que los EVTX de Fase 3 estaban preservados.
2. Limpieza controlada de los canales `Microsoft-Windows-Sysmon/Operational` y `Microsoft-Windows-PowerShell/Operational`.
3. Creación del fichero de marcas temporales de escenarios.
4. Creación del fichero de etiquetas `fase4_labels.csv`.
5. Ejecución del escenario S1: binario desde ruta temporal.
6. Ejecución del escenario S2: PowerShell con comando codificado benigno.
7. Ejecución del escenario S3: modificación de clave Run.
8. Ejecución del escenario S4: tarea programada benigna.
9. Ejecución del escenario S5: creación de servicio de prueba.
10. Ejecución del escenario S6: fichero en carpeta Startup.
11. Ejecución del escenario S7: conexión de red desde PowerShell.
12. Recuento de eventos.
13. Extracción de muestras.
14. Exportación de EVTX.
15. Cálculo de hashes SHA-256.

**Escenarios ejecutados:**
- S1: ejecución desde ruta temporal.
- S2: PowerShell con `EncodedCommand`.
- S3: modificación de clave Run.
- S4: creación de tarea programada.
- S5: creación de servicio de prueba.
- S6: creación de fichero en carpeta Startup.
- S7: conexión de red desde PowerShell.

**Evidencias generadas:**
- `reports\fase4_scenarios_timestamps.csv`
- `reports\fase4_labels.csv`
- `reports\fase4_S1_temp_execution.txt`
- `reports\fase4_S2_powershell_encoded.txt`
- `reports\fase4_S3_registry_run.txt`
- `reports\fase4_S4_scheduled_task.txt`
- `reports\fase4_S5_service_creation.txt`
- `reports\fase4_S6_startup_folder.txt`
- `reports\fase4_S7_network_powershell.txt`
- `raw\fase4_sysmon_sospechosa.evtx`
- `raw\fase4_powershell_sospechosa.evtx`
- `raw\fase4_security_sospechosa.evtx`
- `raw\fase4_system_sospechosa.evtx`

**Observaciones:**
Todos los escenarios de esta fase son simulaciones benignas, reversibles y controladas. No se ha utilizado malware real. La finalidad es generar patrones de interés forense que puedan ser priorizados posteriormente por la herramienta Python.

**Pendientes para la Fase 5:**
1. Integrar los EVTX normales de Fase 3 y sospechosos de Fase 4.
2. Crear el dataset normalizado.
3. Extraer eventos Sysmon y PowerShell.
4. Etiquetar eventos por escenario.
5. Preparar la base de datos para extracción de características por proceso.


---

## Sesión 5 - Conversión de EVTX a dataset normalizado

**Fecha:** 01/07/2026.

**Máquina utilizada:** máquina virtual LABWIN.

**Usuario utilizado:** labwin\jjstestal con PowerShell elevado.

**Objetivo de la sesión:** convertir los registros EVTX generados en las fases 3 y 4 en ficheros CSV normalizados, integrando eventos normales y sospechosos simulados para construir el dataset base del prototipo.

**Acciones realizadas:**
1. Creación de estructura `src` y `processed`.
2. Creación de entorno virtual Python.
3. Instalación de dependencias.
4. Desarrollo del script `evtx_to_csv.py`.
5. Conversión de EVTX Sysmon y PowerShell a CSV.
6. Desarrollo del script `build_labeled_dataset.py`.
7. Integración de eventos normales y sospechosos simulados.
8. Etiquetado inicial por fase, escenario y ventana temporal.
9. Generación de resumen del dataset.
10. Cálculo de hashes de scripts y datasets.

**Evidencias generadas:**
- `src\evtx_to_csv.py`
- `src\build_labeled_dataset.py`
- `src\quick_dataset_check.py`
- `processed\fase3\events_fase3_sysmon.csv`
- `processed\fase3\events_fase3_powershell.csv`
- `processed\fase4\events_fase4_sysmon.csv`
- `processed\fase4\events_fase4_powershell.csv`
- `processed\combined\events_labeled.csv`
- `processed\combined\dataset_summary.json`
- `reports\quick_dataset_check_fase5.txt`
- `reports\dataset_summary_fase5.txt`

**Observaciones:**
Esta fase no realiza todavía extracción de características por proceso ni entrenamiento de modelos. Su finalidad es transformar evidencias EVTX en datos tabulares normalizados y etiquetados, aptos para las fases posteriores de agregación, baseline heurístico y Machine Learning.


**Incidencia durante la instalación de dependencias:**
Durante la instalación inicial de dependencias se produjo un error al instalar `pandas==2.2.2`. `pip` intentó compilar pandas desde código fuente y falló al no encontrar componentes de Microsoft Visual Studio (`vswhere.exe`). Para evitar incorporar herramientas de compilación innecesarias al laboratorio y mejorar la reproducibilidad, se actualizó `requirements.txt` sustituyendo `pandas==2.2.2` por `pandas==2.3.3`, versión con wheel compatible para Windows x86-64 y versiones recientes de Python. Tras recrear el entorno virtual, la instalación se realizó usando `--only-binary=:all:` para impedir compilaciones desde fuente.
**Incidencia resuelta:** la instalación inicial de `pandas==2.2.2` falló porque `pip` intentó compilar el paquete desde código fuente. Se corrigió actualizando a `pandas==2.3.3`, recreando el entorno virtual y forzando instalación desde ruedas binarias con `--only-binary=:all:`.
**Incidencia durante el etiquetado del dataset:**  
Durante la primera ejecución de `build_labeled_dataset.py` se produjo un error de comparación de fechas en pandas (`Cannot compare tz-naive and tz-aware datetime-like objects`). La causa fue que los eventos normalizados contenían el campo `local_time` con zona horaria (`+02:00`), mientras que las marcas temporales de los escenarios estaban expresadas como hora local sin zona horaria. Se corrigió el script para normalizar todas las fechas a hora local sin zona horaria antes de realizar las comparaciones temporales. Tras la corrección, el dataset pudo generarse correctamente.
**Incidencia resuelta:**  
La primera versión de `build_labeled_dataset.py` falló al comparar fechas con y sin zona horaria. Se corrigió el tratamiento temporal normalizando `local_time` y las marcas de escenario a fecha local sin zona horaria. Esta corrección permitió etiquetar los eventos por ventanas temporales de forma consistente.


**Pendientes para la Fase 6:**
1. Agrupar eventos por proceso.
2. Extraer características por proceso.
3. Generar `process_features.csv`.
4. Definir reglas del baseline heurístico.
5. Crear primer ranking de procesos.


---

## Sesión 6 - Extracción de características por proceso y baseline heurístico

**Fecha:** 01/07/2026.

**Máquina utilizada:** máquina virtual LABWIN.

**Usuario utilizado:** labwin\jjstestal con PowerShell elevado.

**Objetivo de la sesión:** transformar los eventos normalizados en características agregadas por proceso y aplicar un baseline heurístico interpretable para generar un primer ranking de prioridad forense.

**Acciones realizadas:**
1. Desarrollo del script `build_process_features.py`.
2. Carga de `events_labeled.csv`.
3. Filtrado de eventos Sysmon como fuente principal de agregación por proceso.
4. Construcción de claves de proceso mediante `ProcessGuid` o clave alternativa.
5. Extracción de características por proceso.
6. Generación de `process_features.csv`.
7. Desarrollo del script `baseline_heuristic.py`.
8. Definición de reglas y pesos heurísticos.
9. Generación de `ranking_baseline.csv`.
10. Evaluación inicial mediante Precision@K y Recall@K.
11. Desarrollo de `check_baseline_results.py`.
12. Cálculo de hashes de scripts, datasets y reportes.

**Evidencias generadas:**
- `src\build_process_features.py`
- `src\baseline_heuristic.py`
- `src\check_baseline_results.py`
- `processed\combined\process_features.csv`
- `processed\combined\process_features_summary.json`
- `reports\ranking_baseline.csv`
- `reports\baseline_evaluation.json`
- `reports\baseline_summary_fase6.txt`
- `reports\quick_baseline_check_fase6.txt`

**Observaciones:**
La agregación se realiza principalmente sobre eventos Sysmon, ya que estos contienen campos como `ProcessGuid`, `Image`, `CommandLine`, `ParentImage`, `DestinationIp`, `TargetObject` y `TargetFilename`. Los eventos PowerShell Operational se mantienen en el dataset normalizado como contexto, pero el primer baseline por proceso se construye sobre la telemetría Sysmon por ser más adecuada para identificar procesos y relaciones padre-hijo.

**Pendientes para la Fase 7:**
1. Revisar el ranking generado.
2. Ajustar pesos del baseline si fuera necesario.
3. Preparar modelo de Machine Learning.
4. Comparar baseline heurístico frente a modelo ML.



---

## Sesión 7 - Modelo de Machine Learning y comparación con baseline

**Fecha:** 05/08/2026.

**Máquina utilizada:** máquina virtual LABWIN.

**Usuario utilizado:** labwin\jjstestal con PowerShell elevado.

**Objetivo de la sesión:** aplicar un modelo de Machine Learning no supervisado sobre las características por proceso y comparar su ranking con el baseline heurístico.

**Acciones realizadas:**
1. Instalación de `scikit-learn`.
2. Verificación de importación y versión de `scikit-learn`.
3. Desarrollo del script `ml_isolation_forest.py`.
4. Entrenamiento de un modelo Isolation Forest usando procesos etiquetados como normales.
5. Generación del ranking `ranking_ml.csv`.
6. Evaluación del ranking ML mediante Precision@K, Recall@K y nDCG@K.
7. Desarrollo del script `compare_baseline_ml.py`.
8. Comparación entre ranking heurístico y ranking ML.
9. Desarrollo del script `check_ml_results.py`.
10. Cálculo de hashes de scripts y reportes.

**Evidencias generadas:**
- `src\ml_isolation_forest.py`
- `src\compare_baseline_ml.py`
- `src\check_ml_results.py`
- `reports\ranking_ml.csv`
- `reports\ml_evaluation.json`
- `reports\comparison_baseline_ml.csv`
- `reports\comparison_baseline_ml.json`
- `reports\quick_ml_check_fase7.txt`
- `hashes\hashes_fase7_scripts.txt`
- `hashes\hashes_fase7_reports.txt`

**Observaciones:**
El modelo se utiliza como mecanismo de priorización/anomalía, no como detector definitivo de malware. Su resultado deberá compararse con el baseline heurístico considerando tanto métricas cuantitativas como interpretabilidad para el analista.

**Pendientes para la Fase 8:**
1. Analizar resultados comparativos.
2. Seleccionar tablas y figuras para la memoria.
3. Redactar discusión de resultados.
4. Preparar conclusiones técnicas del experimento.


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


