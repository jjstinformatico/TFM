import pandas as pd

path = r"C:\TFM_Triage\processed\combined\events_labeled.csv"
df = pd.read_csv(path, dtype=str, encoding="utf-8-sig").fillna("")

print("Total eventos:", len(df))
print("\nEventos por fase:")
print(df["phase"].value_counts())

print("\nEventos por etiqueta:")
print(df["label"].value_counts())

print("\nEventos por escenario:")
print(df["scenario_id"].value_counts())

print("\nEventos Sysmon ID:")
print(df[df["provider"].str.contains("Sysmon", case=False, na=False)]["event_id"].value_counts().head(20))

print("\nTop procesos Image:")
if "Image" in df.columns:
    print(df["Image"].value_counts().head(30))

print("\nEventos sospechosos simulados:")
cols = [c for c in ["local_time", "event_id", "Image", "CommandLine", "TargetObject", "QueryName", "scenario_id", "label"] if c in df.columns]
print(df[df["label"].eq("suspicious_simulated")][cols].head(50).to_string(index=False))