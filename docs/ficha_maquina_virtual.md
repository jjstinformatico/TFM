# Ficha técnica de la máquina virtual del laboratorio

## Identificación general

**Nombre de la máquina virtual:** Windows11-TFM  
**Rol en el laboratorio:** sistema objeto de análisis forense.  
**Sistema operativo verificado:** Microsoft Windows 11 Pro, versión 25H2, compilación 26200.8655.
**Observación:** algunos comandos de PowerShell muestran `WindowsProductName : Windows 10 Pro`, pero `winver`, `systeminfo` y `OsName` identifican el sistema como Windows 11 Pro.**Finalidad:** generar actividad normal y actividad sospechosa simulada para obtener registros EVTX y eventos Sysmon que serán utilizados en la validación experimental de la herramienta Python.

---

## Plataforma de virtualización

**Máquina anfitriona:** ST-RT.  
**Hipervisor utilizado:** Oracle Virtualbox.  
**Versión del hipervisor:** 7.2.4.  
**Tipo de virtualización:** máquina virtual local.  

---

## Recursos asignados a la VM

**CPU asignadas:** 5.  
**Memoria RAM asignada:** 8198 MB.  
**Disco virtual asignado:** 80 GB.  
**Tipo de disco:** Normal VDI.  
**Adaptador de red:** Intel Pro MT/1000 Desktop.  
**Modo de red:** NAT.  
**Aceleración/virtualización habilitada:** Si.

---

## Configuración de red

**Conectividad a Internet:** sí .  
**Modo de red utilizado durante la preparación:** NAT.  
**Modo de red utilizado durante las pruebas:** NAT.  
**Dirección IP de la VM:** 10.0.2.15  
**Puerta de enlace:** 10.0.2.2  
**DNS:** 10.100.15.20, 10.100.16.82

---

## Estado inicial

**Fecha de creación/preparación:** 29/06/2026.  
**Usuario utilizado en las pruebas:** jjstestal.  
**Privilegios del usuario:** el usuario `jjstestal` pertenece al grupo local Administradores. Las tareas sensibles del laboratorio se ejecutan mediante PowerShell con privilegios elevados.
**Snapshot inicial creado:** sí .  
**Nombre del snapshot inicial:** S01_Snapshot_Inicial.  
**Fecha del snapshot inicial:** 30/06/2026.
**Snapshot previo a Sysmon creado:** sí.
**Nombre del snapshot previo a Sysmon:** S02_PreSysmon_EntornoValidado.
**Fecha del snapshot previo a Sysmon:** 30/06/2026.
**Snapshot posterior a Sysmon creado:** sí.  
**Nombre del snapshot posterior a Sysmon:** S03_PostSysmon_Instalado.  
**Fecha del snapshot posterior a Sysmon:** 30/06/2026.
---

## Herramientas previstas

- Sysmon.
- PowerShell.
- Visor de eventos de Windows.
- Python.
- Scripts propios del TFM.
- Herramientas auxiliares de exportación y procesado de EVTX.

---

## Decisiones de seguridad

1. La máquina virtual será el único sistema usado para generar eventos del dataset.
2. No se ejecutará malware real.
3. Los escenarios sospechosos serán simulados mediante comandos benignos.
4. La máquina anfitriona no formará parte del dataset.
5. Las evidencias generadas se exportarán y se conservarán con hash SHA-256 cuando proceda.
6. Se mantendrá un diario de laboratorio y una transcripción de PowerShell para asegurar trazabilidad.

---

## Observaciones

La Fase 1 valida el estado previo a Sysmon. Se confirma que el canal Microsoft-Windows-Sysmon/Operational no existe antes de la instalación, que PowerShell Operational está activo y que la VM dispone de conectividad mediante NAT.