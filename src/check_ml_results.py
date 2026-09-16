import json
import pandas as pd

ml_path = r"C:\TFM_Triage\reports\ranking_ml.csv"
eval_path = r"C:\TFM_Triage\reports\ml_evaluation.json"
comparison_path = r"C:\TFM_Triage\reports\comparison_baseline_ml.csv"

df = pd.read_csv(ml_path, dtype=str, encoding="utf-8-sig").fillna("")

print("Total procesos ranking ML:", len(df))

print("\nTop 20 ML:")
cols = [
    "ml_rank", "ml_anomaly_score", "label", "scenario_ids",
    "process_name", "image", "event_count",
    "has_encoded_command", "has_registry_run", "has_scheduled_task",
    "has_service_creation", "runs_from_temp", "has_network_connection"
]
cols = [c for c in cols if c in df.columns]
print(df[cols].head(20).to_string(index=False))

print("\nProcesos suspicious_simulated en ranking ML:")
print(df[df["label"].eq("suspicious_simulated")][cols].to_string(index=False))

print("\nEvaluación ML:")
with open(eval_path, "r", encoding="utf-8") as f:
    print(json.dumps(json.load(f), indent=2, ensure_ascii=False))

print("\nComparación baseline vs ML:")
comparison = pd.read_csv(comparison_path, dtype=str, encoding="utf-8-sig").fillna("")
print(comparison.to_string(index=False))