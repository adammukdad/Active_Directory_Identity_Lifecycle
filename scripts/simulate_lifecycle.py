import csv
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
USERS_CSV = DATA / "users.csv"
GROUPS_CSV = DATA / "groups.csv"
MAP_JSON = DATA / "mapping.json"

def parse_date(s):
    s = (s or "").strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    return None

def split_groups(s):
    if not s:
        return set()
    # allow either ";" or "," separators inside CSV field
    parts = [p.strip() for p in s.replace(",", ";").split(";") if p.strip()]
    return set(parts)

def load_mapping():
    if MAP_JSON.exists():
        try:
            return json.loads(MAP_JSON.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def load_users():
    rows = []
    with USERS_CSV.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            # derive an event date for sorting: change > end > start
            ev = parse_date(row.get("change_date")) or parse_date(row.get("end_date")) or parse_date(row.get("start_date"))
            row["_event_date"] = ev or datetime.min
            row["_groups_set"] = split_groups(row.get("groups", ""))
            rows.append(row)
    return rows

def events_by_user(rows):
    by_id = {}
    for row in rows:
        uid = row.get("user_id") or row.get("username")
        by_id.setdefault(uid, []).append(row)
    # sort each user's events by event date
    for uid in by_id:
        by_id[uid].sort(key=lambda r: r["_event_date"])
    return by_id

def main():
    mapping = load_mapping()
    term_groups = set(mapping.get("termination_groups", []))
    print("=== IAM Lifecycle Plan (dry-run) ===")
    print(f"Users file : {USERS_CSV}")
    print(f"Groups file: {GROUPS_CSV}")
    print(f"Mapping    : {MAP_JSON if MAP_JSON.exists() else '(none)'}")
    print("")

    rows = load_users()
    users = events_by_user(rows)

    for uid, events in users.items():
        prev_groups = set()
        prev_status = None
        print(f"\n--- User {uid} ({events[0].get('username')}) ---")
        for ev in events:
            status = (ev.get("status") or "").strip()
            dept = (ev.get("department") or "").strip()
            title = (ev.get("title") or "").strip()
            when = ev["_event_date"]
            when_s = when.strftime("%Y-%m-%d") if when else "N/A"
            curr_groups = set(ev["_groups_set"])

            # If mapping.json exists, augment with department/title groups (idempotent)
            dept_map = mapping.get("department_to_groups", {}).get(dept, [])
            title_map = mapping.get("title_to_groups", {}).get(title, [])
            curr_groups |= set(dept_map) | set(title_map)

            if prev_status is None:
                # First event for this user → treat as hire
                print(f"[{when_s}] HIRE -> CREATE account for {ev.get('first_name')} {ev.get('last_name')} ({ev.get('email')})")
                if curr_groups:
                    print(f"           ADD groups: {', '.join(sorted(curr_groups))}")
                prev_groups = curr_groups
                prev_status = status or "Active"
                continue

            # Role/department change if change_date present
            if ev.get("change_date"):
                adds = sorted(curr_groups - prev_groups)
                rems = sorted(prev_groups - curr_groups)
                print(f"[{when_s}] CHANGE -> UPDATE attributes (dept='{dept}', title='{title}')")
                if adds:
                    print(f"           ADD groups: {', '.join(adds)}")
                if rems:
                    print(f"           REMOVE groups: {', '.join(rems)}")
                prev_groups = curr_groups
                prev_status = status or prev_status
                continue

            # Termination if status says terminated or end_date exists
            if status.lower() == "terminated" or ev.get("end_date"):
                print(f"[{when_s}] TERMINATE -> DISABLE account")
                # remove all previous groups, then add termination group(s)
                if prev_groups:
                    print(f"           REMOVE groups: {', '.join(sorted(prev_groups))}")
                if term_groups:
                    print(f"           ADD groups: {', '.join(sorted(term_groups))}")
                prev_groups = set()
                prev_status = "Terminated"
                continue

            # Fallback: unknown event
            print(f"[{when_s}] NOTE -> Unrecognized event row for user {uid}")

    print("\nDone (no changes applied).")

if __name__ == "__main__":
    main()
