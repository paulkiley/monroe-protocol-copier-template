#!/usr/bin/env python3
import os, json, subprocess, sys

BASE = os.path.dirname(os.path.abspath(__file__))
VAL = os.path.join(BASE, "validator.py")
TRUST = os.path.join(BASE, "keys.json")
TESTS = ["T1","T2","T3","T4"]

def run(name):
    log = os.path.join(BASE, "tests", name, "log.jsonl")
    expected = json.load(open(os.path.join(BASE, "tests", name, "expected.json"), "r", encoding="utf-8"))
    out = subprocess.check_output([sys.executable, VAL, log, "--trust", TRUST, "--require-signatures"]).decode("utf-8")
    result = json.loads(out)
    ok = (result.get("ok") == expected.get("ok"))
    if not expected.get("ok"):
        ok = ok and (result.get("reason") == expected.get("reason"))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        print('  result:  ', json.dumps(result, indent=2))
        print('  expected:', json.dumps(expected, indent=2))
    return ok

def main():
    failures = 0
    for t in TESTS:
        if not run(t):
            failures += 1
    if failures:
        sys.exit(1)

if __name__ == "__main__":
    main()
