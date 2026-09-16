import argparse
import csv
import os
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from Evtx.Evtx import Evtx

NS = {"e": "http://schemas.microsoft.com/win/2004/08/events/event"}

KNOWN_FIELDS = [
    "RuleName", "UtcTime", "ProcessGuid", "ProcessId", "Image", "FileVersion",
    "Description", "Product", "Company", "OriginalFileName", "CommandLine",
    "CurrentDirectory", "User", "LogonGuid", "LogonId", "TerminalSessionId",
    "IntegrityLevel", "Hashes", "ParentProcessGuid", "ParentProcessId",
    "ParentImage", "ParentCommandLine", "ParentUser", "Protocol", "Initiated",
    "SourceIp", "SourceHostname", "SourcePort", "DestinationIp",
    "DestinationHostname", "DestinationPort", "DestinationPortName",
    "QueryName", "QueryStatus", "QueryResults", "TargetObject",
    "Details", "NewName", "TargetFilename", "CreationUtcTime"
]

BASE_FIELDS = [
    "phase", "source_file", "record_number", "event_id", "provider",
    "channel", "computer", "utc_system_time", "local_time",
    "level", "task", "opcode", "keywords"
]

def parse_utc_to_local(system_time: str) -> str:
    if not system_time:
        return ""
    try:
        dt = datetime.fromisoformat(system_time.replace("Z", "+00:00"))
        return dt.astimezone().isoformat(sep=" ", timespec="milliseconds")
    except Exception:
        return ""

def get_text(elem, path):
    found = elem.find(path, NS)
    return found.text if found is not None and found.text is not None else ""

def convert_evtx(input_path, output_path, phase):
    rows = []

    with Evtx(input_path) as log:
        for record in log.records():
            xml = record.xml()
            try:
                root = ET.fromstring(xml)
            except ET.ParseError:
                continue

            system = root.find("e:System", NS)
            if system is None:
                continue

            provider_elem = system.find("e:Provider", NS)
            time_elem = system.find("e:TimeCreated", NS)

            provider = provider_elem.attrib.get("Name", "") if provider_elem is not None else ""
            utc_time = time_elem.attrib.get("SystemTime", "") if time_elem is not None else ""

            row = {
                "phase": phase,
                "source_file": os.path.basename(input_path),
                "record_number": str(record.record_num()),
                "event_id": get_text(system, "e:EventID"),
                "provider": provider,
                "channel": get_text(system, "e:Channel"),
                "computer": get_text(system, "e:Computer"),
                "utc_system_time": utc_time,
                "local_time": parse_utc_to_local(utc_time),
                "level": get_text(system, "e:Level"),
                "task": get_text(system, "e:Task"),
                "opcode": get_text(system, "e:Opcode"),
                "keywords": get_text(system, "e:Keywords"),
            }

            eventdata = root.find("e:EventData", NS)
            if eventdata is not None:
                unnamed_index = 0
                for data in eventdata.findall("e:Data", NS):
                    name = data.attrib.get("Name")
                    if not name:
                        name = f"Data_{unnamed_index}"
                        unnamed_index += 1
                    row[name] = data.text if data.text is not None else ""

            userdata = root.find("e:UserData", NS)
            if userdata is not None:
                row["UserData_raw"] = ET.tostring(userdata, encoding="unicode", method="xml")

            rows.append(row)

    fieldnames = list(BASE_FIELDS)
    for f in KNOWN_FIELDS:
        if f not in fieldnames:
            fieldnames.append(f)

    extra_fields = sorted({k for row in rows for k in row.keys()} - set(fieldnames))
    fieldnames.extend(extra_fields)

    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"OK: {input_path} -> {output_path} ({len(rows)} eventos)")

def main():
    parser = argparse.ArgumentParser(description="Convierte EVTX a CSV normalizado.")
    parser.add_argument("--input", required=True, help="Ruta del EVTX de entrada")
    parser.add_argument("--output", required=True, help="Ruta del CSV de salida")
    parser.add_argument("--phase", required=True, help="Fase o etiqueta de origen")
    args = parser.parse_args()

    convert_evtx(args.input, args.output, args.phase)

if __name__ == "__main__":
    main()