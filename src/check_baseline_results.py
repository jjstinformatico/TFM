import pandas as pd
import json

ranking_path = r"C:\TFM_Triage\reports\ranking_baseline.csv"
eval_path = r"C:\TFM_Triage\reports\baseline_evaluation.json"

df = pd.read_csv(ranking_path, dtype=str, encoding="utf-8-sig").fillna("")

print("Total procesos:", len(df))

print("\nProcesos por etiqueta:")
print(df["label"].value_counts())

print("\nProcesos por nivel de riesgo:")
print(df["risk_level"].value_counts())

print("\nTop 20 procesos priorizados:")
cols = [
    "rank", "baseline_score", "risk_level", "label", "scenario_ids",
    "process_name", "image", "main_reasons"
]
print(df[cols].head(20).to_string(index=False))

print("\nProcesos sospechosos simulados:")
print(df[df["label"].eq("suspicious_simulated")][cols].to_string(index=False))

print("\nEvaluación JSON:")
with open(eval_path, "r", encoding="utf-8") as f:
    evaluation = json.load(f)
print(json.dumps(evaluation, indent=2, ensure_ascii=False))