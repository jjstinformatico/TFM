import json
import os

import pandas as pd


baseline_path = r"C:\TFM_Triage\reports\ranking_baseline.csv"
ml_path = r"C:\TFM_Triage\reports\ranking_ml.csv"
baseline_eval_path = r"C:\TFM_Triage\reports\baseline_evaluation.json"
ml_eval_path = r"C:\TFM_Triage\reports\ml_evaluation.json"
output_csv = r"C:\TFM_Triage\reports\comparison_baseline_ml.csv"
output_json = r"C:\TFM_Triage\reports\comparison_baseline_ml.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def metric_dict(evaluation):
    result = {}
    for item in evaluation.get("precision_recall", []):
        k = item["k"]
        result[f"precision_at_{k}"] = item["precision_at_k"]
        result[f"recall_at_{k}"] = item["recall_at_k"]
    return result


def main():
    baseline = pd.read_csv(baseline_path, dtype=str, encoding="utf-8-sig").fillna("")
    ml = pd.read_csv(ml_path, dtype=str, encoding="utf-8-sig").fillna("")

    baseline_eval = load_json(baseline_eval_path)
    ml_eval = load_json(ml_eval_path)

    baseline_metrics = metric_dict(baseline_eval)
    ml_metrics = metric_dict(ml_eval)

    rows = []

    for k in [5, 10, 15, 20]:
        rows.append({
            "k": k,
            "baseline_precision": baseline_metrics.get(f"precision_at_{k}", 0),
            "baseline_recall": baseline_metrics.get(f"recall_at_{k}", 0),
            "ml_precision": ml_metrics.get(f"precision_at_{k}", 0),
            "ml_recall": ml_metrics.get(f"recall_at_{k}", 0),
        })

    comparison_df = pd.DataFrame(rows)

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    comparison_df.to_csv(output_csv, index=False, encoding="utf-8-sig")

    baseline_top10 = baseline.head(10)
    ml_top10 = ml.head(10)

    baseline_top10_keys = set(baseline_top10["process_key"].tolist()) if "process_key" in baseline_top10.columns else set()
    ml_top10_keys = set(ml_top10["process_key"].tolist()) if "process_key" in ml_top10.columns else set()

    comparison = {
        "baseline_total_processes": int(len(baseline)),
        "ml_total_processes": int(len(ml)),
        "baseline_metrics": baseline_metrics,
        "ml_metrics": ml_metrics,
        "top10_overlap_count": len(baseline_top10_keys & ml_top10_keys),
        "top10_overlap_process_keys": sorted(list(baseline_top10_keys & ml_top10_keys)),
        "baseline_top10_labels": baseline_top10["label"].value_counts().to_dict(),
        "ml_top10_labels": ml_top10["label"].value_counts().to_dict(),
        "baseline_top10": baseline_top10[
            ["rank", "baseline_score", "risk_level", "label", "scenario_ids", "process_name", "image", "main_reasons"]
        ].to_dict(orient="records"),
        "ml_top10": ml_top10[
            ["ml_rank", "ml_anomaly_score", "label", "scenario_ids", "process_name", "image", "event_count"]
        ].to_dict(orient="records"),
    }

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(comparison, f, indent=2, ensure_ascii=False)

    print(json.dumps(comparison, indent=2, ensure_ascii=False))
    print(f"OK: comparación CSV generada en {output_csv}")
    print(f"OK: comparación JSON generada en {output_json}")


if __name__ == "__main__":
    main()