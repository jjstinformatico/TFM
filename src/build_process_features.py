import argparse
import os
import re
import json
import ipaddress
from collections import Counter

import pandas as pd


def load_events(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No existe el dataset de eventos: {path}")
    return pd.read_csv(path, dtype=str, encoding="utf-8-sig").fillna("")


def basename(path):
    if not path:
        return ""
    p = str(path).replace("/", "\\")
    return p.split("\\")[-1].lower()


def text_contains_any(text, terms):
    text_l = str(text).lower()
    return any(t.lower() in text_l for t in terms)


def is_private_ip(ip):
    try:
        if not ip:
            return False
        obj = ipaddress.ip_address(str(ip))
        return obj.is_private or obj.is_loopback or obj.is_link_local
    except Exception:
        return False


def safe_int(value):
    try:
        return int(float(str(value)))
    except Exception:
        return 0


def build_process_key(row):
    pguid = str(row.get("ProcessGuid", "")).strip()
    if pguid:
        return f"guid:{pguid}"

    image = str(row.get("Image", "")).strip()
    pid = str(row.get("ProcessId", "")).strip()
    phase = str(row.get("phase", "")).strip()
    command = str(row.get("CommandLine", "")).strip()

    if image or pid:
        return f"fallback:{phase}:{image}:{pid}:{command[:120]}"

    return ""


def main():
    parser = argparse.ArgumentParser(description="Agrupa eventos Sysmon por proceso y extrae características.")
    parser.add_argument("--input", required=True, help="events_labeled.csv")
    parser.add_argument("--output", required=True, help="process_features.csv")
    parser.add_argument("--summary", required=True, help="process_features_summary.json")
    args = parser.parse_args()

    df = load_events(args.input)

    for col in [
        "provider", "event_id", "phase", "label", "scenario_id", "ProcessGuid",
        "ProcessId", "Image", "CommandLine", "User", "ParentImage",
        "ParentCommandLine", "TargetObject", "TargetFilename", "DestinationIp",
        "DestinationHostname", "DestinationPort", "QueryName", "Hashes",
        "local_time"
    ]:
        if col not in df.columns:
            df[col] = ""

    # La unidad principal de análisis será el proceso a partir de eventos Sysmon.
    sysmon = df[df["provider"].str.contains("Sysmon", case=False, na=False)].copy()
    sysmon["process_key"] = sysmon.apply(build_process_key, axis=1)
    sysmon = sysmon[sysmon["process_key"].ne("")].copy()

    # Pares padre-hijo para rareza básica
    sysmon["process_name"] = sysmon["Image"].apply(basename)
    sysmon["parent_name"] = sysmon["ParentImage"].apply(basename)
    sysmon["parent_child_pair"] = sysmon["parent_name"] + "->" + sysmon["process_name"]
    pair_counts = Counter(sysmon["parent_child_pair"].tolist())

    rows = []

    suspicious_terms = [
        "encodedcommand", "-enc", "frombase64string", "currentversion\\run",
        "tfmtest", "tfmtesttask", "tfmtestservice", "startup",
        "svchost-test.exe", "\\temp\\", "\\appdata\\", "schtasks", "sc.exe",
        "reg add", "powershell"
    ]

    lolbins = {
        "powershell.exe", "cmd.exe", "reg.exe", "schtasks.exe", "sc.exe",
        "wscript.exe", "cscript.exe", "mshta.exe", "rundll32.exe",
        "regsvr32.exe", "certutil.exe", "bitsadmin.exe"
    }

    for process_key, g in sysmon.groupby("process_key"):
        g = g.copy()

        image_values = [v for v in g["Image"].tolist() if str(v).strip()]
        image = image_values[0] if image_values else ""
        process_name = basename(image)

        command_values = [v for v in g["CommandLine"].tolist() if str(v).strip()]
        command_line = max(command_values, key=len) if command_values else ""

        parent_values = [v for v in g["ParentImage"].tolist() if str(v).strip()]
        parent_image = parent_values[0] if parent_values else ""

        user_values = [v for v in g["User"].tolist() if str(v).strip()]
        user = user_values[0] if user_values else ""

        text_blob = " ".join(str(x) for x in g.astype(str).fillna("").values.flatten())
        text_l = text_blob.lower()

        event_ids = g["event_id"].astype(str).tolist()

        scenario_ids = sorted(set([s for s in g["scenario_id"].tolist() if str(s).strip()]))
        labels = set([l for l in g["label"].tolist() if str(l).strip()])

        label = "suspicious_simulated" if "suspicious_simulated" in labels else (
            "normal" if "normal" in labels else "background"
        )

        phase_values = sorted(set([p for p in g["phase"].tolist() if str(p).strip()]))

        destination_ips = sorted(set([ip for ip in g["DestinationIp"].tolist() if str(ip).strip()]))
        external_ips = [ip for ip in destination_ips if not is_private_ip(ip)]

        target_objects = " ".join(g["TargetObject"].astype(str).tolist()).lower()
        target_files = " ".join(g["TargetFilename"].astype(str).tolist()).lower()

        has_registry_run = "currentversion\\run" in target_objects or "currentversion\\run" in text_l
        has_scheduled_task = "tfmtesttask" in text_l or process_name == "schtasks.exe"
        has_service_creation = "tfmtestservice" in text_l or process_name == "sc.exe"
        has_startup_folder = "startup" in target_files or "startup" in text_l
        has_encoded_command = "encodedcommand" in command_line.lower() or "encodedcommand" in text_l

        runs_from_temp = (
            "\\temp\\" in image.lower()
            or "\\temp\\" in command_line.lower()
            or "\\temp\\" in target_files
        )

        runs_from_user_profile = (
            "\\users\\" in image.lower()
            or "\\appdata\\" in image.lower()
            or "\\users\\" in command_line.lower()
            or "\\appdata\\" in command_line.lower()
        )

        commandline_length_max = max([len(c) for c in command_values], default=0)
        suspicious_keyword_count = sum(1 for term in suspicious_terms if term in text_l)

        pair = (basename(parent_image) + "->" + process_name) if process_name else ""
        rare_parent_child = 1 if pair and pair_counts.get(pair, 0) == 1 else 0

        row = {
            "process_key": process_key,
            "process_guid": g["ProcessGuid"].iloc[0] if "ProcessGuid" in g else "",
            "process_id": g["ProcessId"].iloc[0] if "ProcessId" in g else "",
            "image": image,
            "process_name": process_name,
            "command_line": command_line,
            "user": user,
            "parent_image": parent_image,
            "parent_name": basename(parent_image),
            "phase": ";".join(phase_values),
            "label": label,
            "scenario_ids": ";".join(scenario_ids),
            "first_seen": g["local_time"].min(),
            "last_seen": g["local_time"].max(),
            "event_count": len(g),
            "unique_event_ids": len(set(event_ids)),
            "event_id_1_process_create": event_ids.count("1"),
            "event_id_3_network": event_ids.count("3"),
            "event_id_5_process_terminate": event_ids.count("5"),
            "event_id_7_image_load": event_ids.count("7"),
            "event_id_11_file_create": event_ids.count("11"),
            "event_id_12_registry_create": event_ids.count("12"),
            "event_id_13_registry_set": event_ids.count("13"),
            "event_id_14_registry_rename": event_ids.count("14"),
            "event_id_22_dns": event_ids.count("22"),
            "has_network_connection": 1 if event_ids.count("3") > 0 else 0,
            "network_connection_count": event_ids.count("3"),
            "dns_query_count": event_ids.count("22"),
            "file_creation_count": event_ids.count("11"),
            "registry_event_count": event_ids.count("12") + event_ids.count("13") + event_ids.count("14"),
            "destination_ip_count": len(destination_ips),
            "external_destination_count": len(external_ips),
            "runs_from_temp": int(runs_from_temp),
            "runs_from_user_profile": int(runs_from_user_profile),
            "has_powershell": int(process_name == "powershell.exe" or "powershell.exe" in text_l),
            "has_encoded_command": int(has_encoded_command),
            "has_registry_run": int(has_registry_run),
            "has_scheduled_task": int(has_scheduled_task),
            "has_service_creation": int(has_service_creation),
            "has_startup_folder": int(has_startup_folder),
            "is_lolbin": int(process_name in lolbins),
            "rare_parent_child": int(rare_parent_child),
            "commandline_length_max": commandline_length_max,
            "suspicious_keyword_count": suspicious_keyword_count,
        }

        rows.append(row)

    features = pd.DataFrame(rows).fillna("")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    os.makedirs(os.path.dirname(args.summary), exist_ok=True)

    features.to_csv(args.output, index=False, encoding="utf-8-sig")

    summary = {
        "total_processes": int(len(features)),
        "processes_by_label": features["label"].value_counts().to_dict() if not features.empty else {},
        "processes_by_phase": features["phase"].value_counts().to_dict() if not features.empty else {},
        "processes_by_scenario": features["scenario_ids"].value_counts().to_dict() if not features.empty else {},
        "top_process_names": features["process_name"].value_counts().head(20).to_dict() if not features.empty else {},
    }

    with open(args.summary, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"OK: características por proceso generadas en {args.output}")


if __name__ == "__main__":
    main()