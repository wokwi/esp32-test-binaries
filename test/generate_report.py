import glob
import json
import os
import re


def extract_test_results(report_file: str):
    counts = {}
    current_device = None
    with open(report_file, "r") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
            except json.JSONDecodeError:
                continue

            if data.get("$report_type") == "TestReport":
                location = data.get("location")
                if location:
                    current_device = location[-1].split("[")[1].split("]")[0]

            if (
                data.get("$report_type") == "TestReport"
                and data.get("when") == "teardown"
            ):
                sections = data.get("sections", [])
                stdout_section = next(
                    filter(lambda x: x[0] == "Captured stdout call", sections), None
                )
                if not stdout_section:
                    continue

                stdout = stdout_section[1]
                matches = re.findall(
                    r"\r\n(\d+) Tests (\d+) Failures (\d+) Ignored", stdout
                )
                if matches:
                    total = 0
                    fail = 0
                    skip = 0
                    passed = 0
                    for match in matches:
                        total += int(match[0])
                        fail += int(match[1])
                        skip += int(match[2])
                    passed = total - fail - skip
                else:
                    total = 1
                    fail = int(data.get("outcome") == "failed")
                    skip = int(data.get("outcome") == "skipped")
                    passed = int(data.get("outcome") == "passed")
                summary = []
                if passed:
                    summary.append(f"✅ {passed}")
                if fail:
                    summary.append(f"❌ {fail}")
                if skip:
                    summary.append(f"⏭️ {skip}")
                counts[current_device] = {
                    "total": total,
                    "fail": fail,
                    "skip": skip,
                    "summary": " ".join(summary),
                }
    return counts


if __name__ == "__main__":
    devices = set()
    reports = []
    total = 0
    failed = 0
    for file in glob.glob(f"{os.path.dirname(__file__)}/test_*.json"):
        if file.endswith(".json"):
            report = extract_test_results(file)
            devices.update(report.keys())
            test_name = os.path.basename(file).replace(".json", "")
            reports.append([test_name, report])
            total += max(
                [0] + [report.get(device, {}).get("total", 0) for device in devices]
            )
            failed += max(
                [0] + [report.get(device, {}).get("fail", 0) for device in devices]
            )

    devices = sorted(devices)
    print(f"# Wokwi ESP-IDF Test Report")
    print(f"")
    print(f"Total tests: {total}")
    print(f"Failed tests: {failed}")
    print(f"")
    print(f"| Test | {' | '.join(devices)} |")
    print(f"| ---- | {' | '.join(['---' for _ in devices])} |")

    # Sort reports by name
    reports.sort(key=lambda x: x[0])
    for name, report in reports:
        print(
            f"| {name} | {' | '.join([str(report.get(device, {}).get('summary', '')) for device in devices])} |"
        )
