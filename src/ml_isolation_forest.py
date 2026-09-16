import argparse
import json
import os

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


NUMERIC_FEATURES = [
    "event_count",
    "unique_event_ids",
    "event_id_1_process_create",
    "event_id_3_network",
    "event_id_5_process_terminate",
    "event_id_7_image_load",
    "event_id_11_file_create",
    "event_id_12_registry_create",
    "event_id_13_registry_set",
    "event_id_14_registry_rename",
    "event_id_22_dns",
    "has_network_connection",
    "network_connection_count",
    "dns_query_count",
    "file_creation_count",
    "registry_event_count",
    "destination_ip_count",
    "external_destination_count",
    "runs_from_temp",
    "runs_from_user_profile",
    "has_powershell",
    "has_encoded_command",
    "has_registry_run",
    "has_scheduled_task",
    "has_service_creation",
    "has_startup_folder",
    "is_lolbin",
    "rare_parent_child",
    "commandline_length_max",
    "suspicious_keyword_count",
]


def load_features(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No existe el fichero de características: {path}")

    df = pd.read_csv(path, dtype=str, encoding="utf-8-sig").fillna("")

    for col in NUMERIC_FEATURES:
        if col not in df.columns:
            df[col] = "0"

    for col in NUMERIC_FEATURES:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


def precision_recall_at_k(df, k):
    top = df.head(k)
    tp = int((top["label"] == "suspicious_simulated").sum())
    total_suspicious = int((df["label"] == "suspicious_simulated").sum())

    return {
        "k": k,
        "true_positives_at_k": tp,
        "precision_at_k": tp / k if k else 0,
        "recall_at_k": tp / total_suspicious if total_suspicious else 0,
    }


def ndcg_at_k(df, k):
    import math

    top = df.head(k)
    gains = [1 if label == "suspicious_simulated" else 0 for label in top["label"].tolist()]

    dcg = 0.0
    for i, rel in enumerate(gains, start=1):
        dcg += rel / math.log2(i + 1)

    total_relevant = int((df["label"] == "suspicious_simulated").sum())
    ideal_rels = [1] * min(total_relevant, k)

    idcg = 0.0
    for i, rel in enumerate(ideal_rels, start=1):
        idcg += rel / math.log2(i + 1)

    return dcg / idcg if idcg > 0 else 0.0


def main():
    parser = argparse.ArgumentParser(description="Modelo Isolation Forest para priorización de procesos.")
    parser.add_argument("--input", required=True, help="process_features.csv")
    parser.add_argument("--ranking", required=True, help="ranking_ml.csv")
    parser.add_argument("--evaluation", required=True, help="ml_evaluation.json")
    args = parser.parse_args()

    df = load_features(args.input)

    # Entrenamiento no supervisado con procesos normales como aproximación de comportamiento base.
    train_df = df[df["label"] == "normal"].copy()

    if train_df.empty:
        raise RuntimeError("No hay procesos normales para entrenar el modelo.")

    scaler = StandardScaler()
    x_train = scaler.fit_transform(train_df[NUMERIC_FEATURES])
    x_all = scaler.transform(df[NUMERIC_FEATURES])

    model = IsolationForest(
        n_estimators=200,
        contamination=0.10,
        random_state=42,
    )

    model.fit(x_train)

    # decision_function: valores más bajos indican mayor anomalía.
    decision = model.decision_function(x_all)

    df["ml_decision_function"] = decision
    df["ml_anomaly_score"] = -decision

    df = df.sort_values(
        by=["ml_anomaly_score", "event_count"],
        ascending=[False, False],
    ).reset_index(drop=True)

    df.insert(0, "ml_rank", range(1, len(df) + 1))

    cols_first = [
        "ml_rank",
        "ml_anomaly_score",
        "ml_decision_function",
        "label",
        "scenario_ids",
        "process_name",
        "image",
        "command_line",
        "parent_image",
        "event_count",
        "has_encoded_command",
        "has_registry_run",
        "has_scheduled_task",
        "has_service_creation",
        "has_startup_folder",
        "runs_from_temp",
        "has_network_connection",
        "external_destination_count",
        "suspicious_keyword_count",
    ]

    cols = cols_first + [c for c in df.columns if c not in cols_first]

    os.makedirs(os.path.dirname(args.ranking), exist_ok=True)
    os.makedirs(os.path.dirname(args.evaluation), exist_ok=True)

    df[cols].to_csv(args.ranking, index=False, encoding="utf-8-sig")

    evaluation = {
        "model": "IsolationForest",
        "training_strategy": "Entrenamiento con procesos etiquetados como normal",
        "random_state": 42,
        "n_estimators": 200,
        "contamination": 0.10,
        "total_processes": int(len(df)),
        "training_processes_normal": int(len(train_df)),
        "suspicious_simulated_processes": int((df["label"] == "suspicious_simulated").sum()),
        "normal_processes": int((df["label"] == "normal").sum()),
        "background_processes": int((df["label"] == "background").sum()),
        "precision_recall": [
            precision_recall_at_k(df, 5),
            precision_recall_at_k(df, 10),
            precision_recall_at_k(df, 15),
            precision_recall_at_k(df, 20),
        ],
        "ndcg": {
            "ndcg_at_5": ndcg_at_k(df, 5),
            "ndcg_at_10": ndcg_at_k(df, 10),
            "ndcg_at_15": ndcg_at_k(df, 15),
            "ndcg_at_20": ndcg_at_k(df, 20),
        },
        "top_10": df.head(10)[
            [
                "ml_rank",
                "ml_anomaly_score",
                "label",
                "scenario_ids",
                "process_name",
                "image",
                "event_count",
                "has_encoded_command",
                "has_registry_run",
                "has_scheduled_task",
                "has_service_creation",
                "runs_from_temp",
                "has_network_connection",
            ]
        ].to_dict(orient="records"),
    }

    with open(args.evaluation, "w", encoding="utf-8") as f:
        json.dump(evaluation, f, indent=2, ensure_ascii=False)

    print(json.dumps(evaluation, indent=2, ensure_ascii=False))
    print(f"OK: ranking ML generado en {args.ranking}")
    print(f"OK: evaluación ML generada en {args.evaluation}")


if __name__ == "__main__":
    main()