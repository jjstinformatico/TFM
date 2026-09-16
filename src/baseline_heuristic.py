import argparse
import json
import os

import pandas as pd


def as_int(value):
    try:
        return int(float(str(value)))
    except Exception:
        return 0


def risk_level(score):
    if score >= 70:
        return "alto"
    if score >= 40:
        return "medio"
    if score >= 20:
        return "bajo"
    return "informativo"


def score_row(row):
    score = 0
    reasons = []

    def add(points, reason):
        nonlocal score
        score += points
        reasons.append(f"+{points} {reason}")

    if as_int(row.get("runs_from_temp")):
        add(25, "ejecución o artefacto asociado a ruta temporal")

    if as_int(row.get("runs_from_user_profile")):
        add(10, "ejecución o artefacto asociado a perfil de usuario")

    if as_int(row.get("has_encoded_command")):
        add(25, "uso de PowerShell con EncodedCommand")

    if as_int(row.get("has_registry_run")):
        add(20, "modificación de clave Run asociada a persistencia")

    if as_int(row.get("has_scheduled_task")):
        add(18, "creación o uso de tarea programada")

    if as_int(row.get("has_service_creation")):
        add(18, "creación o gestión de servicio")

    if as_int(row.get("has_startup_folder")):
        add(18, "artefacto en carpeta Startup")

    if as_int(row.get("has_network_connection")):
        add(10, "conexión de red asociada al proceso")

    if as_int(row.get("external_destination_count")) > 0:
        add(8, "destinos de red externos")

    if as_int(row.get("is_lolbin")):
        add(8, "uso de binario legítimo de administración o LOLBin")

    if as_int(row.get("rare_parent_child")):
        add(6, "relación padre-hijo poco frecuente en el dataset")

    if as_int(row.get("commandline_length_max")) >= 120:
        add(5, "línea de comandos larga")

    suspicious_keywords = as_int(row.get("suspicious_keyword_count"))
    if suspicious_keywords >= 3:
        add(10, "varias palabras clave de interés forense")
    elif suspicious_keywords > 0:
        add(4, "palabras clave de interés forense")

    if as_int(row.get("registry_event_count")) > 0:
        add(8, "eventos de registro asociados al proceso")

    if as_int(row.get("file_creation_count")) >= 5:
        add(5, "múltiples creaciones de fichero")

    return score, "; ".join(reasons)


def precision_recall_at_k(df, k):
    top = df.head(k)
    tp = int((top["label"] == "suspicious_simulated").sum())
    total_suspicious = int((df["label"] == "suspicious_simulated").sum())

    precision = tp / k if k else 0
    recall = tp / total_suspicious if total_suspicious else 0

    return {
        "k": k,
        "true_positives_at_k": tp,
        "precision_at_k": precision,
        "recall_at_k": recall,
    }


def main():
    parser = argparse.ArgumentParser(description="Aplica baseline heurístico a process_features.csv.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--ranking", required=True)
    parser.add_argument("--evaluation", required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input, dtype=str, encoding="utf-8-sig").fillna("")

    scores = df.apply(score_row, axis=1)
    df["baseline_score"] = [s[0] for s in scores]
    df["main_reasons"] = [s[1] for s in scores]
    df["risk_level"] = df["baseline_score"].apply(risk_level)

    df = df.sort_values(
        by=["baseline_score", "event_count"],
        ascending=[False, False]
    ).reset_index(drop=True)

    df.insert(0, "rank", range(1, len(df) + 1))

    cols_first = [
        "rank", "baseline_score", "risk_level", "label", "scenario_ids",
        "process_name", "image", "command_line", "parent_image",
        "user", "event_count", "main_reasons"
    ]

    cols = cols_first + [c for c in df.columns if c not in cols_first]

    os.makedirs(os.path.dirname(args.ranking), exist_ok=True)
    os.makedirs(os.path.dirname(args.evaluation), exist_ok=True)

    df[cols].to_csv(args.ranking, index=False, encoding="utf-8-sig")

    evaluation = {
        "total_processes": int(len(df)),
        "suspicious_simulated_processes": int((df["label"] == "suspicious_simulated").sum()),
        "normal_processes": int((df["label"] == "normal").sum()),
        "background_processes": int((df["label"] == "background").sum()),
        "precision_recall": [
            precision_recall_at_k(df, 5),
            precision_recall_at_k(df, 10),
            precision_recall_at_k(df, 15),
            precision_recall_at_k(df, 20),
        ],
        "top_10": df.head(10)[
            ["rank", "baseline_score", "risk_level", "label", "scenario_ids", "process_name", "image", "main_reasons"]
        ].to_dict(orient="records"),
    }

    with open(args.evaluation, "w", encoding="utf-8") as f:
        json.dump(evaluation, f, indent=2, ensure_ascii=False)

    print(json.dumps(evaluation, indent=2, ensure_ascii=False))
    print(f"OK: ranking generado en {args.ranking}")
    print(f"OK: evaluación generada en {args.evaluation}")


if __name__ == "__main__":
    main()