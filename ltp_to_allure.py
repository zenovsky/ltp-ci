#!/usr/bin/env python3
# License: MIT
# Copyright (c) 2025 Konstantin Zenovsky <https://github.com/zenovsky>
"""
This script converts JSON results from kirk to JSON-files for Allure
"""
import json
import uuid
from pathlib import Path
from time import time
from datetime import datetime

launch_label = datetime.now().strftime("LTP run %Y-%m-%d %H:%M:%S")

kirk_json_path = Path("results.json")
allure_output_dir = Path("allure-results")
allure_output_dir.mkdir(exist_ok=True)

with kirk_json_path.open(encoding="utf-8") as f:
    data = json.load(f)

results = data.get("results", data)
now_ms = int(time() * 1000)

status_map = {
    "pass": "passed",
    "fail": "failed",
    "skip": "skipped",
    "brok": "broken",
    "warn": "broken",
    "conf": "skipped",
}

for item in results:
    test_name = item.get("test_fqn", "unknown")
    test = item.get("test", {})
    status = (
        "fail" if test.get("failed", 0) > 0 else
        "brok" if test.get("broken", 0) > 0 else
        "warn" if test.get("warnings", 0) > 0 else
        "skip" if test.get("skipped", 0) > 0 else
        "pass"
    )

    allure_status = status_map.get(status, "unknown")
    duration_ms = int(float(test.get("duration", 0)) * 1000)
    start = int(time() * 1000)
    stop = start + duration_ms

    message = ""
    for line in test.get("log", "").splitlines():
        if any(x in line for x in ["TFAIL", "TCONF", "TBROK", "TSKIP", "XFAIL", "XPASS"]):
            message = line
            break
     
    test_uuid = str(uuid.uuid4())

    allure_result = {
        "uuid": test_uuid,
        "type": "testResult",
        "name": test_name,
        "fullName": test_name,
        "historyId": test_name,
        "status": allure_status,
        "statusDetails": {
            "message": message
        },
        "stage": "finished",
        "start": start,
        "stop": stop,
        "labels": [
            {"name": "suite", "value": "LTP"},
            {"name": "host", "value": "debian"},
            {"name": "framework", "value": "ltp"},
            {"name": "launch", "value": launch_label}
        ],
        "steps": [],
        "attachments": [],
        "parameters": []
    }

    out_path = allure_output_dir / f"{test_uuid}-result.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(allure_result, f, indent=2)

print("JSON-files with full keys generated")