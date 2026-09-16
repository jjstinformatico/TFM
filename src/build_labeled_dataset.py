import argparse
import json
import os
import re
from datetime import timedelta

import pandas as pd


def load_csv(path):
    """Carga un CSV como texto. Si no existe, devuelve DataFrame vacío."""
    if not os.path.exists(path):
        print(f"AVISO: no existe el fichero {path}")
        return pd.DataFrame()

    try:
        return pd.read_csv(path, dtype=str, encoding="utf-8-sig").fillna("")
    except Exception as exc:
        print(f"ERROR leyendo {path}: {exc}")
        return pd.DataFrame()


def parse_local_naive_series(series):
    """
    Convierte una serie de fechas a datetime sin zona horaria.

    Los CSV generados por evtx_to_csv.py incluyen local_time con offset,
    por ejemplo:
        2026-06-30 17:53:35.123+02:00

    Las marcas de escenario no tienen offset:
        2026-06-30 17:53:35.123

    Para comparar correctamente, se elimina el offset manteniendo la hora local
    visible del laboratorio.
    """
    s = series.astype(str).str.strip()

    # Elimina sufijos de zona horaria del tipo +02:00, -05:00 o Z
    s = s.str.replace(r"(Z|[+-]\d{2}:\d{2})$", "", regex=True)

    return pd.to_datetime(s, errors="coerce")


def parse_local_naive_value(value):
    """
    Convierte una fecha individual a Timestamp sin zona horaria.
    """
    if value is None:
        return pd.NaT

    text = str(value).strip()
    text = re.sub(r"(Z|[+-]\d{2}:\d{2})$", "", text)

    return pd.to_datetime(text, errors="coerce")


def row_text(row):
    """Concatena toda la fila en texto para búsquedas simples."""
    return " ".join(str(v) for v in row.values if str(v).strip())


def ensure_columns(df, columns):
    """Garantiza que existan columnas necesarias."""
    for col in columns:
        if col not in df.columns:
            df[col] = ""
    return df


def assign_phase3_scenarios(events, timestamps):
    """
    Etiqueta eventos de Fase 3 como normal según ventanas temporales.
    """
    if events.empty or timestamps.empty:
        return events

    events = events.copy()
    events["event_dt"] = parse_local_naive_series(events["local_time"])

    for _, sc in timestamps.iterrows():
        sid = sc.get("scenario_id", "")
        stype = sc.get("scenario_type", "")
        desc = sc.get("description", "")

        start = parse_local_naive_value(sc.get("start_time", "")) - timedelta(seconds=3)
        end = parse_local_naive_value(sc.get("end_time", "")) + timedelta(seconds=3)

        if pd.isna(start) or pd.isna(end):
            continue

        mask = (events["event_dt"] >= start) & (events["event_dt"] <= end)

        events.loc[mask, "scenario_id"] = sid
        events.loc[mask, "scenario_type"] = stype
        events.loc[mask, "scenario_description"] = desc
        events.loc[mask, "label"] = "normal"

    return events


def assign_phase4_scenarios(events, timestamps, labels):
    """
    Etiqueta eventos de Fase 4.

    Los eventos que coinciden temporalmente y además contienen términos esperados
    del escenario se etiquetan como suspicious_simulated.

    Los eventos que caen dentro de la ventana temporal, pero no contienen los
    términos esperados, se etiquetan como background.
    """
    if events.empty:
        return events

    events = events.copy()
    events["event_dt"] = parse_local_naive_series(events["local_time"])
    events["row_text"] = events.apply(row_text, axis=1)

    for _, sc in timestamps.iterrows():
        sid = sc.get("scenario_id", "")
        stype = sc.get("scenario_type", "")
        desc = sc.get("description", "")
        expected_processes = sc.get("expected_processes", "")
        notes = sc.get("notes", "")

        start = parse_local_naive_value(sc.get("start_time", "")) - timedelta(seconds=5)
        end = parse_local_naive_value(sc.get("end_time", "")) + timedelta(seconds=5)

        if pd.isna(start) or pd.isna(end):
            continue

        label_row = labels[labels["scenario_id"] == sid] if not labels.empty and "scenario_id" in labels.columns else pd.DataFrame()

        expected_artifacts = ""
        if not label_row.empty:
            expected_artifacts = label_row.iloc[0].get("expected_artifacts", "")

        terms = []

        base_terms = [
            expected_processes,
            expected_artifacts,
            notes,
            sid,
        ]

        scenario_terms = {
            "S1": ["svchost-test.exe", "TFMTest"],
            "S2": ["EncodedCommand", "powershell.exe", "fase4_S2_encoded_output.txt"],
            "S3": ["reg.exe", "CurrentVersion\\Run", "TFMTest"],
            "S4": ["schtasks.exe", "TFMTestTask"],
            "S5": ["sc.exe", "TFMTestService"],
            "S6": ["Startup", "tfm_startup_test.bat"],
            "S7": ["www.example.com", "Test-NetConnection", "Resolve-DnsName"],
        }

        base_terms.extend(scenario_terms.get(sid, []))

        for value in base_terms:
            if value:
                for part in str(value).replace(";", ",").split(","):
                    part = part.strip()
                    if part and part not in terms:
                        terms.append(part)

        time_mask = (events["event_dt"] >= start) & (events["event_dt"] <= end)

        def contains_any_term(text):
            text_l = str(text).lower()
            return any(term.lower() in text_l for term in terms)

        text_mask = events["row_text"].apply(contains_any_term)

        suspicious_mask = time_mask & text_mask

        events.loc[suspicious_mask, "scenario_id"] = sid
        events.loc[suspicious_mask, "scenario_type"] = stype
        events.loc[suspicious_mask, "scenario_description"] = desc
        events.loc[suspicious_mask, "label"] = "suspicious_simulated"

        background_mask = time_mask & (~text_mask) & events["label"].eq("")

        events.loc[background_mask, "scenario_id"] = sid
        events.loc[background_mask, "scenario_type"] = "background_in_suspicious_window"
        events.loc[background_mask, "scenario_description"] = "Evento de contexto dentro de ventana sospechosa simulada"
        events.loc[background_mask, "label"] = "background"

    return events


def main():
    parser = argparse.ArgumentParser(
        description="Combina eventos normalizados y asigna etiquetas por fase y escenario."
    )
    parser.add_argument("--output", required=True, help="CSV de salida etiquetado")
    parser.add_argument("--summary", required=True, help="JSON resumen del dataset")
    args = parser.parse_args()

    files = [
        r"C:\TFM_Triage\processed\fase3\events_fase3_sysmon.csv",
        r"C:\TFM_Triage\processed\fase3\events_fase3_powershell.csv",
        r"C:\TFM_Triage\processed\fase4\events_fase4_sysmon.csv",
        r"C:\TFM_Triage\processed\fase4\events_fase4_powershell.csv",
    ]

    dfs = [load_csv(f) for f in files]
    dfs = [df for df in dfs if not df.empty]

    if not dfs:
        raise RuntimeError("No se ha cargado ningún CSV de eventos. Revisa la conversión EVTX a CSV.")

    events = pd.concat(dfs, ignore_index=True).fillna("")

    events = ensure_columns(
        events,
        [
            "phase",
            "provider",
            "event_id",
            "source_file",
            "local_time",
            "Image",
            "CommandLine",
            "TargetObject",
            "TargetFilename",
            "QueryName",
        ],
    )

    events["scenario_id"] = ""
    events["scenario_type"] = ""
    events["scenario_description"] = ""
    events["label"] = ""

    ts3 = load_csv(r"C:\TFM_Triage\reports\fase3_scenarios_timestamps.csv")
    ts4 = load_csv(r"C:\TFM_Triage\reports\fase4_scenarios_timestamps.csv")
    labels4 = load_csv(r"C:\TFM_Triage\reports\fase4_labels.csv")

    phase3_mask = events["phase"].eq("fase3_normal")
    phase4_mask = events["phase"].eq("fase4_suspicious_simulated")

    events_phase3 = assign_phase3_scenarios(events[phase3_mask].copy(), ts3)
    events_phase4 = assign_phase4_scenarios(events[phase4_mask].copy(), ts4, labels4)

    final = pd.concat([events_phase3, events_phase4], ignore_index=True).fillna("")

    final.drop(columns=["event_dt", "row_text"], errors="ignore", inplace=True)

    unlabeled_mask = final["label"].eq("")

    final.loc[unlabeled_mask & final["phase"].eq("fase3_normal"), "label"] = "normal"
    final.loc[unlabeled_mask & final["phase"].eq("fase4_suspicious_simulated"), "label"] = "background"

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    os.makedirs(os.path.dirname(args.summary), exist_ok=True)

    final.to_csv(args.output, index=False, encoding="utf-8-sig")

    summary = {
        "total_events": int(len(final)),
        "events_by_phase": final["phase"].value_counts().to_dict(),
        "events_by_provider": final["provider"].value_counts().to_dict(),
        "events_by_event_id": final["event_id"].value_counts().to_dict(),
        "events_by_label": final["label"].value_counts().to_dict(),
        "events_by_scenario": final["scenario_id"].value_counts().to_dict(),
        "source_files": final["source_file"].value_counts().to_dict(),
    }

    with open(args.summary, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"\nOK: dataset generado en {args.output}")
    print(f"OK: resumen generado en {args.summary}")


if __name__ == "__main__":
    main()
