# Matriz de control de resultados del laboratorio

## Fase 0 - Preparación inicial

**Estado:** completada.  
**Objetivo:** creación de estructura de laboratorio, diario técnico y transcript inicial.  
**Evidencias principales:**
- `docs/diario_laboratorio.md`
- `docs/ficha_maquina_virtual.md`
- `reports/transcript_laboratorio_fase0.txt`

---

## Fase 1 - Validación del entorno

**Estado:** completada.  
**Máquina virtual:** LABWIN.  
**Sistema operativo verificado:** Windows 11 Pro 25H2, build 26200.8655.  
**Hipervisor:** VirtualBox.  
**IP VM:** 10.0.2.15.  
**Gateway NAT:** 10.0.2.2.  
**DNS:** 10.100.15.20 y 10.100.16.82.  
**Sysmon previo:** no instalado.  
**PowerShell Operational:** activo.  
**Snapshot:** S02_PreSysmon_EntornoValidado.  

**Evidencias principales:**
- `reports/info_windows_detallada.txt`
- `reports/systeminfo_vm.txt`
- `reports/info_eventlogs_disponibles.txt`
- `reports/info_log_sysmon_preinstalacion.txt`
- `screenshots/fase1_winver.png`
- `screenshots/fase1_snapshot_presysmon.png`

---

## Fase 2 - Instalación y validación de Sysmon

**Estado:** completada.  
**Sysmon:** versión 15.21.  
**Firma:** válida, Microsoft Windows Publisher.  
**Servicio:** Sysmon64 activo.  
**Canal:** Microsoft-Windows-Sysmon/Operational activo.  
**Eventos Sysmon tras validación:** 12130.  
**EVTX validación:** `raw/fase2_sysmon_validacion.evtx`.  
**Hash SHA-256 EVTX validación:** A31A1E24FD17F53B0296374DEB9BACDDC0770E78C9A54886478FBAD215481A5B.  
**Snapshot:** S03_PostSysmon_Instalado.

**Incidencia documentada:**
PowerShell mostró `NativeCommandError` durante la instalación, pero la salida de Sysmon confirmó instalación correcta de `Sysmon64` y `SysmonDrv`. Una segunda ejecución confirmó que el servicio ya estaba registrado.

**Evidencias principales:**
- `tools/Config/sysmon_config_tfm.xml`
- `reports/sysmon_signature.txt`
- `reports/sysmon_version.txt`
- `reports/sysmon_install_output.txt`
- `reports/estado_servicio_sysmon_postinstalacion.txt`
- `reports/info_log_sysmon_postinstalacion.txt`
- `reports/sample_sysmon_events.txt`
- `raw/fase2_sysmon_validacion.evtx`
- `hashes/hash_fase2_sysmon_validacion_evtx.txt`


---

## Fase 3 - Generación de actividad normal y línea base legítima

**Estado:** completada.  
**Objetivo:** generar una línea base de actividad normal en Windows para comparar posteriormente con escenarios sospechosos simulados.  

**Máquina utilizada:** LABWIN.  
**Usuario utilizado:** labwin\jjstestal.  
**Sysmon:** activo durante la fase.  
**PowerShell Operational:** activo durante la fase.  

**Acción metodológica previa:**  
Antes de iniciar los escenarios normales se limpió de forma controlada el canal `Microsoft-Windows-Sysmon/Operational`, tras haber preservado previamente el EVTX de validación de la Fase 2. Esta limpieza se realizó para separar las evidencias de validación técnica de Sysmon de las evidencias utilizadas para construir la línea base normal.

**Escenarios ejecutados:**
- N1: actividad básica de usuario mediante `notepad.exe`, `calc.exe` y `explorer.exe`.
- N2: gestión legítima de ficheros dentro de `C:\TFM_Triage\lab_normal\N2`.
- N3: administración legítima de Windows mediante `cmd.exe`, `tasklist`, `schtasks`, `Get-Service` y `Get-Process`.
- N4: uso legítimo de PowerShell sin comandos codificados ni ofuscados.
- N5: conectividad legítima mediante DNS y HTTPS contra dominios de Microsoft y UNIR.

**Marcas temporales de escenarios:**
- N1: 2026-06-30 17:53:35.021 - 2026-06-30 17:53:50.273.
- N2: 2026-06-30 17:54:26.107 - 2026-06-30 17:54:26.289.
- N3: 2026-06-30 17:54:48.782 - 2026-06-30 17:54:49.786.
- N4: 2026-06-30 17:55:12.655 - 2026-06-30 17:55:15.998.
- N5: 2026-06-30 17:55:29.873 - 2026-06-30 17:55:33.120.

**Recuento de eventos:**
- Sysmon: 144 eventos.
- PowerShell Operational: 472 eventos.
- Security: 21762 eventos.
- System: 1616 eventos.

**Conectividad documentada:**
- `www.microsoft.com:443`: conexión correcta.
- `www.unir.net:443`: conexión correcta.

**EVTX generados:**
- `raw/fase3_sysmon_normal.evtx`
- `raw/fase3_powershell_normal.evtx`
- `raw/fase3_security_normal.evtx`
- `raw/fase3_system_normal.evtx`

**Hashes SHA-256:**
- `fase3_sysmon_normal.evtx`: 4CFAA001B2F8165CE121EC95480BBF59A1FEF0E33C65C49002F9AABAB0E1CB4C
- `fase3_powershell_normal.evtx`: 486FE6DEF5B24911F275A099D0B5F089EA3832EBCCCCA11DE44BB2FCF7EB1421
- `fase3_security_normal.evtx`: 29638E3020519B21C3876A834AC73DAB653E928DC8B2377C94917F7FE982EB4B
- `fase3_system_normal.evtx`: 70D774D47A37C6E0693D3E4EBF7A21DCF5D6CF0A6CF6FF287981544CA2C88415

**Evidencias principales:**
- `reports/transcript_laboratorio_fase3.txt`
- `reports/fase3_reset_log_sysmon.txt`
- `reports/fase3_scenarios_timestamps.csv`
- `reports/fase3_N1_usuario_basico.txt`
- `reports/fase3_N2_ofimatica_ficheros.txt`
- `reports/fase3_N3_administracion_windows.txt`
- `reports/fase3_N4_powershell_legitimo.txt`
- `reports/fase3_N5_red_legitima.txt`
- `reports/count_sysmon_fase3.txt`
- `reports/count_powershell_fase3.txt`
- `reports/sample_sysmon_events_fase3.txt`
- `reports/sample_powershell_events_fase3.txt`
- `screenshots/fase3_eventos_sysmon_normal.png`
- `screenshots/fase3_powershell_operational.png`
- `screenshots/fase3_carpeta_evidencias.png`
- `screenshots/fase3_timestamps_escenarios.png`
- `screenshots/fase3_evtx_exportados.png`

**Observaciones para la memoria:**
La Fase 3 permite justificar que procesos y acciones legítimas como `powershell.exe`, `cmd.exe`, consultas DNS, conexiones HTTPS, creación de ficheros o uso de `schtasks.exe` pueden aparecer en actividad normal. Por tanto, la herramienta no debe clasificar automáticamente estos comportamientos como maliciosos, sino priorizarlos según contexto, combinación de evidencias, ubicación, línea de comandos, relaciones padre-hijo y puntuación acumulada.

**Utilidad dentro del TFM:**
Esta fase aporta la línea base normal necesaria para comparar posteriormente los escenarios sospechosos simulados de la Fase 4. También servirá para discutir falsos positivos, ruido operativo y necesidad de una priorización interpretable.


---

## Fase 4 - Generación de actividad sospechosa simulada

**Estado:** completada.
**Objetivo:** generar actividad sospechosa simulada, benigna y controlada, para disponer de eventos de interés forense frente a la línea base normal de Fase 3.

**Máquina utilizada:** LABWIN.
**Usuario utilizado:** labwin\jjstestal.
**Sysmon:** activo durante la fase.
**PowerShell Operational:** activo durante la fase.

**Acción metodológica previa:**
Antes de iniciar los escenarios sospechosos simulados se limpiaron de forma controlada los canales `Microsoft-Windows-Sysmon/Operational` y `Microsoft-Windows-PowerShell/Operational`, tras haber preservado previamente los EVTX de la Fase 3. No se limpiaron los registros `Security` ni `System`; estos registros se analizarán mediante filtrado temporal.

**Escenarios ejecutados:**

* S1: ejecución de binario desde ruta temporal mediante copia benigna de `notepad.exe` como `svchost-test.exe`.
* S2: ejecución de PowerShell con `EncodedCommand` benigno.
* S3: modificación controlada de clave `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`.
* S4: creación y eliminación de tarea programada `TFMTestTask`.
* S5: creación y eliminación de servicio de prueba `TFMTestService`.
* S6: creación y eliminación de fichero benigno en carpeta Startup.
* S7: conexión de red desde PowerShell contra `www.example.com`.

**Marcas temporales de escenarios:**

* S1: 2026-07-01 09:32:33.982 - 2026-07-01 09:32:39.211.
* S2: 2026-07-01 09:33:26.457 - 2026-07-01 09:33:27.288.
* S3: 2026-07-01 09:33:42.244 - 2026-07-01 09:33:44.522.
* S3: 2026-07-01 09:35:16.537 - 2026-07-01 09:35:18.623.
* S4: 2026-07-01 09:38:14.147 - 2026-07-01 09:38:16.296.
* S5: 2026-07-01 09:39:53.365 - 2026-07-01 09:39:55.463.
* S6: 2026-07-01 09:41:35.408 - 2026-07-01 09:41:37.550.
* S7: 2026-07-01 09:41:57.630 - 2026-07-01 09:42:00.816.

**Observación sobre S3:**
El escenario S3 se ejecutó en dos ventanas temporales. Esta repetición no invalida la fase, ya que ambas ejecuciones representan la misma simulación controlada de modificación de clave `Run` y aportan evidencias adicionales sobre eventos de registro.

**Recuento de eventos:**

* Sysmon: 719 eventos.
* PowerShell Operational: 228 eventos.
* Security: 21838 eventos.
* System: 1729 eventos.

**Conectividad documentada:**

* `www.example.com:80`: conexión correcta.
* Resolución DNS de `www.example.com`: correcta.

**EVTX generados:**

* `raw/fase4_sysmon_sospechosa.evtx`
* `raw/fase4_powershell_sospechosa.evtx`
* `raw/fase4_security_sospechosa.evtx`
* `raw/fase4_system_sospechosa.evtx`

**Hashes SHA-256:**

* `fase4_sysmon_sospechosa.evtx`: A46B12CFCC2BC34DDC7B14890319C58C737E9E44939CB11BEAEF847FC34FC65E.
* `fase4_powershell_sospechosa.evtx`: DF06ACF17547627E0ADFD8204AB6661AA8CA4944864EB4D5C12F77C7F78E8144.
* `fase4_security_sospechosa.evtx`: AA9E6FDCCA54774974C0F18541420CB4F76A5CD357AFFBE2AF8B43D6CBDEBABC.
* `fase4_system_sospechosa.evtx`: F8789DD4847D8F35C38E6CA7D0C2957C362C59FF7D1572A723F29B99DAE5AA16.

**Evidencias principales:**

* `reports/transcript_laboratorio_fase4.txt`
* `reports/fase4_reset_logs.txt`
* `reports/fase4_scenarios_timestamps.csv`
* `reports/fase4_labels.csv`
* `reports/fase4_S1_temp_execution.txt`
* `reports/fase4_S2_powershell_encoded.txt`
* `reports/fase4_S2_encoded_string.txt`
* `reports/fase4_S3_registry_run.txt`
* `reports/fase4_S3_run_key_after_add.txt`
* `reports/fase4_S4_scheduled_task.txt`
* `reports/fase4_S4_scheduled_task_query.txt`
* `reports/fase4_S5_service_creation.txt`
* `reports/fase4_S5_service_query.txt`
* `reports/fase4_S6_startup_folder.txt`
* `reports/fase4_S6_startup_file_info.txt`
* `reports/fase4_S7_network_powershell.txt`
* `reports/fase4_S7_test_example_80.txt`
* `reports/fase4_S7_dns_example.txt`
* `reports/sample_sysmon_events_fase4.txt`
* `reports/sample_powershell_events_fase4.txt`
* `reports/fase4_eventos_interes_sysmon.txt`
* `screenshots/fase4_eventos_sysmon_sospechosos.png`
* `screenshots/fase4_eventos_sysmon_sospechosos2.png`
* `screenshots/fase4_powershell_encoded.png`
* `screenshots/fase4_registry_run.png`
* `screenshots/fase4_tarea_programada.png`
* `screenshots/fase4_servicio_prueba.png`
* `screenshots/fase4_evtx_exportados.png`

**Observaciones para la memoria:**
La Fase 4 no representa una infección real, sino una simulación controlada de patrones de interés forense. Esta decisión permite generar evidencias reproducibles y seguras, manteniendo el enfoque ético del laboratorio. Los escenarios permiten evaluar si el sistema de priorización es capaz de elevar procesos y comportamientos que, por contexto, ubicación, línea de comandos, uso de PowerShell, modificación de registro, creación de tareas, creación de servicios o ejecución desde rutas temporales, merecen revisión prioritaria por parte de un analista.

**Utilidad dentro del TFM:**
Esta fase aporta los casos positivos o de interés forense necesarios para comparar la priorización frente a la línea base normal de Fase 3. Será fundamental para calcular métricas como Precision@K, Recall@K, reducción de volumen revisado y comparación entre baseline heurístico y modelo de Machine Learning.

**Limitación metodológica:**
Los escenarios son benignos, controlados y reversibles. Por tanto, los resultados no deben interpretarse como detección de malware real, sino como evaluación experimental de priorización forense ante patrones representativos de interés.


---

## Fase 5 - Conversión de EVTX a dataset normalizado

**Estado:** completada.
**Objetivo:** transformar los registros EVTX generados en las fases 3 y 4 en ficheros CSV normalizados, integrando eventos normales y sospechosos simulados para construir el dataset base del prototipo.

**Máquina utilizada:** LABWIN.
**Usuario utilizado:** labwin\jjstestal.
**Entorno de ejecución:** Python en entorno virtual `.venv`.
**Versión de Python:** Python 3.14.6.

**Dependencias principales:**

| Paquete       | Versión |
| ------------- | ------: |
| `python-evtx` |   0.8.1 |
| `pandas`      |   2.3.3 |
| `numpy`       |   2.5.0 |

**Acciones realizadas:**

1. Creación de estructura `src` y `processed`.
2. Creación de entorno virtual Python.
3. Instalación de dependencias.
4. Corrección de `requirements.txt` para usar `pandas==2.3.3`.
5. Desarrollo del script `evtx_to_csv.py`.
6. Conversión de EVTX Sysmon y PowerShell a CSV.
7. Desarrollo y corrección del script `build_labeled_dataset.py`.
8. Integración de eventos normales y sospechosos simulados.
9. Etiquetado inicial por fase, escenario y ventana temporal.
10. Desarrollo y corrección de `quick_dataset_check.py`.
11. Generación de resumen del dataset.
12. Cálculo de hashes de scripts y datasets.

**EVTX convertidos a CSV:**

| EVTX origen                        | CSV generado                                  | Eventos |
| ---------------------------------- | --------------------------------------------- | ------: |
| `fase3_sysmon_normal.evtx`         | `processed/fase3/events_fase3_sysmon.csv`     |     155 |
| `fase3_powershell_normal.evtx`     | `processed/fase3/events_fase3_powershell.csv` |     472 |
| `fase4_sysmon_sospechosa.evtx`     | `processed/fase4/events_fase4_sysmon.csv`     |     750 |
| `fase4_powershell_sospechosa.evtx` | `processed/fase4/events_fase4_powershell.csv` |     228 |

**Dataset combinado:**

| Fichero                                   | Descripción                                 |
| ----------------------------------------- | ------------------------------------------- |
| `processed/combined/events_labeled.csv`   | Dataset combinado, normalizado y etiquetado |
| `processed/combined/dataset_summary.json` | Resumen cuantitativo del dataset            |

**Resumen del dataset:**

| Métrica                               | Valor |
| ------------------------------------- | ----: |
| Total de eventos integrados           |  1605 |
| Eventos de Fase 3 normal              |   627 |
| Eventos de Fase 4 sospechosa simulada |   978 |
| Eventos Sysmon                        |   905 |
| Eventos PowerShell Operational        |   700 |

**Eventos por etiqueta:**

| Etiqueta               | Eventos |
| ---------------------- | ------: |
| `normal`               |     627 |
| `suspicious_simulated` |      59 |
| `background`           |     919 |

**Eventos por escenario:**

| Escenario              | Eventos |
| ---------------------- | ------: |
| Sin escenario asignado |     847 |
| N5                     |     250 |
| S7                     |     236 |
| S2                     |     125 |
| N4                     |      35 |
| N3                     |      28 |
| N1                     |      22 |
| S3                     |      21 |
| S5                     |      18 |
| N2                     |       7 |
| S4                     |       7 |
| S1                     |       6 |
| S6                     |       3 |

**Eventos por Event ID:**

| Event ID | Eventos | Interpretación principal                    |
| -------- | ------: | ------------------------------------------- |
| 4104     |     671 | Script Block Logging de PowerShell          |
| 11       |     294 | Creación de fichero en Sysmon               |
| 3        |     230 | Conexión de red en Sysmon                   |
| 1        |     141 | Creación de proceso en Sysmon               |
| 5        |     138 | Finalización de proceso en Sysmon           |
| 22       |      79 | Consulta DNS en Sysmon                      |
| 7        |      15 | Carga de imagen en Sysmon                   |
| 12       |       6 | Evento de registro en Sysmon                |
| 13       |       2 | Modificación de valor de registro en Sysmon |

**Hashes SHA-256 de salidas principales:**

| Evidencia                                 | SHA-256                                                            |
| ----------------------------------------- | ------------------------------------------------------------------ |
| `processed/combined/events_labeled.csv`   | `4CEA6F473570B0984327E9F2A4C9E50D75423C0D5192601314C949BC585DB585` |
| `processed/combined/dataset_summary.json` | `EC7CF41E9D7E95E67C2904A886644A1CAB90FDEF5381F4C2F58CE1CEBBCAA158` |
| `src/evtx_to_csv.py`                      | `80FA34F203438F9EB41570E902FC553E5DCB219FC0DF0AC29FDCF826B59FC335` |
| `src/build_labeled_dataset.py`            | `6FA509C47A9D2B9555BB37B83ECD0C38B7D0739E1615CE3D8493D113F5C9658D` |
| `src/quick_dataset_check.py`              | `CC50BEF1F914E7C6187334930B87FA52C2A93A8DBC3525BA555284797FABC9F6` |

**Incidencias resueltas:**

1. La instalación inicial de `pandas==2.2.2` falló porque `pip` intentó compilar el paquete desde código fuente y no encontró componentes de Microsoft Visual Studio. Se corrigió actualizando a `pandas==2.3.3`, recreando el entorno virtual y forzando instalación desde ruedas binarias.
2. La primera versión de `build_labeled_dataset.py` falló al comparar fechas con y sin zona horaria. Se corrigió normalizando `local_time` y las marcas de escenario a fecha local sin zona horaria.
3. La primera versión de `quick_dataset_check.py` contenía una ruta errónea hacia `C:\FM_Triage`. Se corrigió a `C:\TFM_Triage`.

**Observaciones para la memoria:**

La Fase 5 constituye el paso de transformación de evidencias forenses a datos analizables. A partir de los EVTX preservados en fases anteriores se generaron ficheros CSV normalizados, conservando campos relevantes como marca temporal, proveedor, identificador de evento, proceso, línea de comandos, usuario, ruta de fichero, objeto de registro y consulta DNS. El dataset combinado integra eventos normales, eventos sospechosos simulados y eventos de contexto, lo que permitirá en fases posteriores extraer características por proceso, aplicar un baseline heurístico y comparar los resultados con técnicas de Machine Learning.

**Limitación metodológica:**

El etiquetado se realiza mediante una combinación de fase, ventana temporal y coincidencia de términos esperados. Por tanto, no debe interpretarse como etiquetado forense perfecto, sino como una aproximación experimental suficiente para evaluar la priorización de procesos en un laboratorio controlado.



---

## Fase 6 - Extracción de características por proceso y baseline heurístico

**Estado:** completada.
**Objetivo:** transformar los eventos normalizados en características agregadas por proceso y aplicar un baseline heurístico interpretable para generar un primer ranking de prioridad forense.

**Máquina utilizada:** LABWIN.
**Usuario utilizado:** labwin\jjstestal.
**Entorno de ejecución:** Python en entorno virtual `.venv`.
**Dataset de entrada:** `processed/combined/events_labeled.csv`.

**Acciones realizadas:**

1. Desarrollo del script `build_process_features.py`.
2. Carga del dataset normalizado `events_labeled.csv`.
3. Filtrado de eventos Sysmon como fuente principal para la agregación por proceso.
4. Construcción de claves de proceso mediante `ProcessGuid` o clave alternativa.
5. Extracción de características por proceso.
6. Generación de `process_features.csv`.
7. Desarrollo del script `baseline_heuristic.py`.
8. Definición de reglas y pesos heurísticos.
9. Generación de `ranking_baseline.csv`.
10. Evaluación inicial mediante `Precision@K` y `Recall@K`.
11. Desarrollo del script `check_baseline_results.py`.
12. Cálculo de hashes SHA-256 de scripts, datasets y reportes.

**Ficheros generados:**

| Fichero                                            | Descripción                                   |
| -------------------------------------------------- | --------------------------------------------- |
| `src/build_process_features.py`                    | Script de agregación de eventos por proceso   |
| `src/baseline_heuristic.py`                        | Script de scoring heurístico                  |
| `src/check_baseline_results.py`                    | Script de comprobación rápida del baseline    |
| `processed/combined/process_features.csv`          | Dataset agregado por proceso                  |
| `processed/combined/process_features_summary.json` | Resumen de características por proceso        |
| `reports/ranking_baseline.csv`                     | Ranking de procesos según baseline heurístico |
| `reports/baseline_evaluation.json`                 | Métricas de evaluación del baseline           |
| `reports/baseline_summary_fase6.txt`               | Salida de ejecución del baseline              |
| `reports/quick_baseline_check_fase6.txt`           | Comprobación textual del ranking              |

**Resumen de procesos agregados:**

| Métrica                                          | Valor |
| ------------------------------------------------ | ----: |
| Total de procesos agregados                      |   176 |
| Procesos etiquetados como `suspicious_simulated` |    14 |
| Procesos etiquetados como `normal`               |    41 |
| Procesos etiquetados como `background`           |   121 |

**Procesos por nivel de riesgo:**

| Nivel de riesgo | Procesos |
| --------------- | -------: |
| Alto            |        3 |
| Medio           |       12 |
| Bajo            |       21 |
| Informativo     |      140 |

**Métricas del baseline heurístico:**

| Métrica        |  Valor |
| -------------- | -----: |
| `Precision@5`  |   0,40 |
| `Recall@5`     | 0,1429 |
| `Precision@10` |   0,50 |
| `Recall@10`    | 0,3571 |
| `Precision@15` | 0,5333 |
| `Recall@15`    | 0,5714 |
| `Precision@20` |   0,60 |
| `Recall@20`    | 0,8571 |

**Top 10 del baseline heurístico:**

| Rank | Score | Riesgo | Etiqueta               | Escenario            | Proceso            |
| ---: | ----: | ------ | ---------------------- | -------------------- | ------------------ |
|    1 |   109 | Alto   | `suspicious_simulated` | S1;S2;S3;S4;S5;S6;S7 | `powershell.exe`   |
|    2 |    91 | Alto   | `suspicious_simulated` | S2                   | `powershell.exe`   |
|    3 |    81 | Alto   | `background`           | S2;S3                | `firefox.exe`      |
|    4 |    66 | Medio  | `normal`               | N4                   | `powershell.exe`   |
|    5 |    61 | Medio  | `normal`               | N4                   | `powershell.exe`   |
|    6 |    61 | Medio  | `normal`               | N4                   | `powershell.exe`   |
|    7 |    61 | Medio  | `normal`               | N4                   | `powershell.exe`   |
|    8 |    51 | Medio  | `suspicious_simulated` | S3                   | `reg.exe`          |
|    9 |    51 | Medio  | `suspicious_simulated` | S3                   | `reg.exe`          |
|   10 |    51 | Medio  | `suspicious_simulated` | S1                   | `svchost-test.exe` |

**Procesos sospechosos simulados priorizados:**

* `powershell.exe` asociado a `EncodedCommand`.
* `svchost-test.exe` ejecutado desde ruta temporal.
* `reg.exe` modificando clave `Run`.
* `schtasks.exe` creando tarea programada.
* `sc.exe` creando servicio de prueba.

**Falsos positivos relevantes:**

* `firefox.exe` aparece en posición alta como evento de contexto/background.
* Varios procesos `powershell.exe` del escenario normal N4 aparecen con puntuación media.

**Interpretación de resultados:**

El baseline heurístico consigue elevar procesos de interés forense dentro de las primeras posiciones del ranking. En el Top 20 se recuperan 12 de los 14 procesos etiquetados como `suspicious_simulated`, alcanzando un `Recall@20` de 0,8571. Sin embargo, también aparecen falsos positivos relevantes, especialmente actividad legítima de PowerShell y eventos de contexto asociados a Firefox. Este resultado es coherente con la naturaleza del triage: el objetivo no es clasificar de forma definitiva un proceso como malicioso, sino ordenar los procesos para que el analista revise primero aquellos con mayor acumulación de indicadores.

**Limitación metodológica:**

El baseline depende de reglas y pesos definidos manualmente. Aunque aporta interpretabilidad, también puede elevar actividad legítima que comparte rasgos con patrones sospechosos, como PowerShell, conexiones de red, rutas temporales o líneas de comandos largas. Esta limitación justifica la comparación posterior con un modelo de Machine Learning.

**Hashes SHA-256 de salidas principales:**

| Evidencia                                          | SHA-256                                                            |
| -------------------------------------------------- | ------------------------------------------------------------------ |
| `src/build_process_features.py`                    | `AE7D6B1FE5E1846990022D9967ECF4CE1272E85578C39D64025EF861588E9F72` |
| `src/baseline_heuristic.py`                        | `7010F170EACABE1FB289E3573C83DC2C5E2B005665009257C123612341E91CE4` |
| `src/check_baseline_results.py`                    | `F417AE7FF40ACDD212948FE9AB29B6EB68BF975B9B0B8FDC52C687385E0A40C0` |
| `processed/combined/process_features.csv`          | `802A64E068D1A0FEA72D0BF64EBA039D738431B4C3A57FEB9F493F605448DAA3` |
| `processed/combined/process_features_summary.json` | `5CD945692C57C682291440D6284381EB29E31B58F73CA68D965D045B66F02068` |
| `reports/ranking_baseline.csv`                     | `2EC54C1F3C237E02823B370B3AF16DCA428ABEB2B67110C70D58CF8529DDE1E0` |
| `reports/baseline_evaluation.json`                 | `B9326F23397205B3EF8D1203A03E0820333FE6EA0B53252EEA4D366CCF879DD2` |
| `reports/baseline_summary_fase6.txt`               | `240C681EA02B82E89ABC2375FB6D1DA7F81BF95FF336DE926153AC45915C271B` |
| `reports/quick_baseline_check_fase6.txt`           | `FFFDB93998F71C658BACA8EC6E4A858976EDA704D04CC7B6018D465485AC44F5` |

**Utilidad dentro del TFM:**

Esta fase proporciona una primera solución interpretable de priorización forense. Sus resultados servirán como punto de comparación frente al modelo de Machine Learning de la Fase 7 y como base para discutir ventajas, limitaciones, falsos positivos y utilidad práctica del sistema propuesto.


---

## Fase 7 - Modelo de Machine Learning y comparación con baseline

**Estado:** completada.  
**Objetivo:** aplicar un modelo de Machine Learning no supervisado sobre las características agregadas por proceso y comparar su capacidad de priorización con el baseline heurístico desarrollado en la Fase 6.

**Máquina utilizada:** LABWIN.  
**Usuario utilizado:** labwin\jjstestal.  
**Entorno de ejecución:** Python en entorno virtual `.venv`.  
**Dataset de entrada:** `processed/combined/process_features.csv`.  
**Modelo utilizado:** `IsolationForest`.  
**Librería principal:** `scikit-learn`.  
**Versión de scikit-learn:** 1.9.0.

**Estrategia de entrenamiento:**

El modelo se entrenó utilizando únicamente los procesos etiquetados como `normal`, con el objetivo de que identificara como más anómalos aquellos procesos que se alejan del comportamiento base observado en la línea normal de laboratorio.

**Parámetros principales del modelo:**

| Parámetro | Valor |
|---|---:|
| Modelo | `IsolationForest` |
| `n_estimators` | 200 |
| `contamination` | 0,10 |
| `random_state` | 42 |
| Procesos usados para entrenamiento | 41 |

**Distribución de procesos evaluados:**

| Tipo de proceso | Procesos |
|---|---:|
| Total de procesos | 176 |
| Procesos `normal` | 41 |
| Procesos `suspicious_simulated` | 14 |
| Procesos `background` | 121 |

**Acciones realizadas:**

1. Instalación de `scikit-learn`.
2. Verificación de importación y versión de `scikit-learn`.
3. Desarrollo del script `ml_isolation_forest.py`.
4. Carga de `process_features.csv`.
5. Selección de características numéricas.
6. Entrenamiento de `IsolationForest` con procesos normales.
7. Generación del ranking `ranking_ml.csv`.
8. Evaluación del ranking ML mediante `Precision@K`, `Recall@K` y `nDCG@K`.
9. Desarrollo del script `compare_baseline_ml.py`.
10. Comparación del ranking ML con el ranking heurístico.
11. Desarrollo del script `check_ml_results.py`.
12. Cálculo de hashes SHA-256 de scripts y reportes.

**Ficheros generados:**

| Fichero | Descripción |
|---|---|
| `src/ml_isolation_forest.py` | Script del modelo Isolation Forest |
| `src/compare_baseline_ml.py` | Script de comparación baseline frente a ML |
| `src/check_ml_results.py` | Script de comprobación rápida de resultados ML |
| `reports/ranking_ml.csv` | Ranking de procesos generado por el modelo ML |
| `reports/ml_evaluation.json` | Métricas del modelo ML |
| `reports/ml_summary_fase7.txt` | Salida textual de la ejecución ML |
| `reports/comparison_baseline_ml.csv` | Comparación tabular baseline frente a ML |
| `reports/comparison_baseline_ml.json` | Comparación detallada baseline frente a ML |
| `reports/comparison_baseline_ml_summary_fase7.txt` | Salida textual de comparación |
| `reports/quick_ml_check_fase7.txt` | Comprobación rápida del ranking ML |
| `reports/pip_install_sklearn_fase7.txt` | Evidencia de instalación de `scikit-learn` |
| `reports/pip_freeze_fase7.txt` | Dependencias instaladas tras Fase 7 |
| `reports/sklearn_import_test_fase7.txt` | Verificación de importación de `scikit-learn` |

**Métricas del modelo ML:**

| Métrica | Valor |
|---|---:|
| `Precision@5` | 0,20 |
| `Recall@5` | 0,0714 |
| `Precision@10` | 0,10 |
| `Recall@10` | 0,0714 |
| `Precision@15` | 0,1333 |
| `Recall@15` | 0,1429 |
| `Precision@20` | 0,10 |
| `Recall@20` | 0,1429 |

**nDCG del modelo ML:**

| Métrica | Valor |
|---|---:|
| `nDCG@5` | 0,1696 |
| `nDCG@10` | 0,1100 |
| `nDCG@15` | 0,1337 |
| `nDCG@20` | 0,1337 |

**Top 10 del modelo ML:**

| Rank ML | Anomaly score | Etiqueta | Escenario | Proceso |
|---:|---:|---|---|---|
| 1 | 0,2154 | `normal` | N1;N2;N3;N4;N5 | `powershell.exe` |
| 2 | 0,2077 | `background` | S2;S3 | `firefox.exe` |
| 3 | 0,1744 | `suspicious_simulated` | S1;S2;S3;S4;S5;S6;S7 | `powershell.exe` |
| 4 | 0,1352 | `background` | S2 | `svchost.exe` |
| 5 | 0,1292 | `background` | Sin escenario | `msedgewebview2.exe` |
| 6 | 0,1080 | `background` | Sin escenario | `systemsettings.exe` |
| 7 | 0,1032 | `background` | S2 | `taskhostw.exe` |
| 8 | 0,0969 | `background` | Sin escenario | `svchost.exe` |
| 9 | 0,0937 | `background` | S2;S3;S5;S7 | `svchost.exe` |
| 10 | 0,0889 | `background` | Sin escenario | `svchost.exe` |

**Procesos sospechosos simulados recuperados por el modelo ML:**

| Rank ML | Escenario | Proceso |
|---:|---|---|
| 3 | S1;S2;S3;S4;S5;S6;S7 | `powershell.exe` |
| 15 | S2 | `powershell.exe` |
| 28 | S1 | `svchost-test.exe` |
| 35 | S4 | `schtasks.exe` |
| 36 | S4 | `schtasks.exe` |
| 37 | S4 | `schtasks.exe` |
| 52 | S3 | `reg.exe` |
| 53 | S3 | `reg.exe` |
| 61 | S3 | `reg.exe` |
| 62 | S3 | `reg.exe` |
| 65 | S5 | `sc.exe` |
| 71 | S5 | `sc.exe` |
| 72 | S5 | `sc.exe` |
| 73 | S3 | `reg.exe` |

**Comparación baseline heurístico frente a ML:**

| K | Precision baseline | Recall baseline | Precision ML | Recall ML |
|---:|---:|---:|---:|---:|
| 5 | 0,40 | 0,1429 | 0,20 | 0,0714 |
| 10 | 0,50 | 0,3571 | 0,10 | 0,0714 |
| 15 | 0,5333 | 0,5714 | 0,1333 | 0,1429 |
| 20 | 0,60 | 0,8571 | 0,10 | 0,1429 |

**Solapamiento Top 10 entre baseline y ML:**

| Métrica | Valor |
|---|---:|
| Procesos comunes en ambos Top 10 | 2 |
| Etiquetas en Top 10 baseline | 5 `suspicious_simulated`, 4 `normal`, 1 `background` |
| Etiquetas en Top 10 ML | 1 `suspicious_simulated`, 1 `normal`, 8 `background` |

**Interpretación de resultados:**

El modelo Isolation Forest fue capaz de generar un ranking de anomalía, pero su rendimiento en este laboratorio fue inferior al baseline heurístico. En el Top 20, el modelo ML recuperó 2 de los 14 procesos etiquetados como `suspicious_simulated`, mientras que el baseline heurístico recuperó 12 de 14. Además, el Top 10 del modelo ML estuvo dominado por procesos `background`, como `firefox.exe`, `svchost.exe`, `msedgewebview2.exe`, `taskhostw.exe` y otros procesos del sistema o de aplicaciones legítimas.

Este resultado indica que el modelo no supervisado detecta anomalías estadísticas, pero no necesariamente prioriza mejor los patrones forenses de interés definidos en el laboratorio. En cambio, el baseline heurístico incorpora conocimiento experto explícito sobre rutas temporales, PowerShell codificado, modificación de claves Run, tareas programadas, servicios y otros indicadores, por lo que ofrece mejor rendimiento en este entorno controlado.

**Conclusión técnica de la fase:**

La Fase 7 demuestra que la incorporación de Machine Learning no garantiza automáticamente una mejora sobre un baseline experto interpretable. Para el caso concreto de este TFM, el enfoque heurístico obtiene mejores métricas de priorización y resulta más explicable para un analista. El modelo ML sigue siendo útil como comparación experimental y como evidencia de que los modelos no supervisados pueden verse afectados por ruido operativo, procesos de contexto y tamaño reducido del dataset.

**Limitación metodológica:**

El dataset contiene un número reducido de procesos y procede de un laboratorio controlado. Además, el modelo se entrenó solo con 41 procesos normales, lo que limita la capacidad de generalización. Por ello, los resultados no deben interpretarse como una evaluación universal de Isolation Forest, sino como una comparación experimental dentro del entorno diseñado para el TFM.

**Incidencias y observaciones técnicas:**

- La instalación de `scikit-learn` se completó correctamente mediante ruedas binarias.
- Durante la instalación apareció una salida de PowerShell catalogada como `NativeCommandError`, pero no impidió la instalación.
- La importación posterior confirmó `scikit-learn 1.9.0`.
- Algunos reportes generados mediante redirección de PowerShell quedaron codificados en UTF-16. No afecta a la validez de las evidencias, aunque para futuras fases se recomienda usar `Out-File -Encoding utf8`.

**Hashes SHA-256 de salidas principales:**

| Evidencia | SHA-256 |
|---|---|
| `src/ml_isolation_forest.py` | `DC49E323A7D37B957F188C378FE4159CA65F4890A6027BD9263766F95FE6C255` |
| `src/compare_baseline_ml.py` | `5D0DFAF7C79AD6BAEFD82B9E617754A35DEAD82E33A50605097C889EE2B620A5` |
| `src/check_ml_results.py` | `D08BDD7CF2B1145C999AC039A0A775A9FB059592E221CEA13E61E62317C7313F` |
| `reports/ranking_ml.csv` | `F25757909908C9FF6252DC72308839279C80CF2017778C092CFC6AE7125AA8C1` |
| `reports/ml_evaluation.json` | `4FD75769EFEE5AD0B5EE637DADC7EB37D5A415F2B3FB7C77EDD644A2CDA7B146` |
| `reports/comparison_baseline_ml.csv` | `B03A0339E4F4F39C7F4677FFD2E8CCB8B1DCB5640CBF96305AB398277C2FF632` |
| `reports/comparison_baseline_ml.json` | `1831D67E58459CA8231D2664F5BE44CDF2C296A8DA9749874BA13698894E631B` |
| `reports/quick_ml_check_fase7.txt` | `87D23782A0B7AB1789781F4419B66BFF37E5CAA0509F29BC7419621555B7D534` |

**Utilidad dentro del TFM:**

Esta fase aporta la comparación experimental entre un enfoque heurístico interpretable y un modelo de Machine Learning no supervisado. Los resultados permiten defender que, en un contexto de triage forense con dataset pequeño y escenarios controlados, la interpretabilidad y el conocimiento experto pueden ser más eficaces que un modelo automático de anomalías. Esta conclusión será especialmente relevante para la discusión de resultados, las limitaciones y las líneas futuras.


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







