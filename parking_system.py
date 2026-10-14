"""Parking permit management for zones A, B and C."""
import json
import secrets
from datetime import datetime, timedelta

permits = {}
ZONES = ["A", "B", "C"]
DATE_FORMAT = "%Y-%m-%d"


def register_permit(vehicle_plate, zone_id, zone_records=None):
    """Register a permit and return its number, or None if invalid."""
    if not vehicle_plate or zone_id not in ZONES:
        return None
    if zone_records is None:
        zone_records = []
    permit_no = "P" + str(secrets.randbelow(90000) + 10000)
    expiry = datetime.now() + timedelta(days=180)
    permits[vehicle_plate] = {
        "zone": zone_id,
        "permit": permit_no,
        "expiry": expiry.strftime(DATE_FORMAT),
    }
    zone_records.append((vehicle_plate, zone_id))
    return permit_no


def revoke_permit(vehicle_plate):
    """Remove a permit if it exists."""
    permits.pop(vehicle_plate, None)


def is_expired(vehicle_plate):
    """Return True if the permit is missing, invalid or past expiry."""
    permit = permits.get(vehicle_plate)
    if permit is None:
        return True
    try:
        expiry = datetime.strptime(permit["expiry"], DATE_FORMAT)
    except (KeyError, ValueError):
        return True
    return expiry < datetime.now()


def scan_zone(zone_id, plates_seen):
    """Return plates without a valid permit for this zone."""
    flagged = []
    for plate in plates_seen:
        permit = permits.get(plate)
        if permit is None or permit["zone"] != zone_id or is_expired(plate):
            flagged.append(plate)
    return flagged


def load_permit_database(file="permits.json"):
    """Load permits from a JSON file, or start empty on failure."""
    try:
        with open(file, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        data = {}
    permits.clear()
    permits.update(data)


def save_permit_database(file="permits.json"):
    """Save permits to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(permits, handle)


def set_expiry(vehicle_plate, date_text):
    """Set a permit's expiry (YYYY-MM-DD). Return True on success."""
    if vehicle_plate not in permits:
        return False
    try:
        datetime.strptime(date_text, DATE_FORMAT)
    except ValueError:
        return False
    permits[vehicle_plate]["expiry"] = date_text
    return True


def main():
    """Run a demo of the permit system."""
    load_permit_database()
    register_permit("KA01AB1234", "A")
    register_permit("KA05XY9999", "Z")
    register_permit("", "B")
    register_permit(None, "C")
    set_expiry("KA01AB1234", "2020-01-01")
    revoke_permit("MH12ZZ0000")
    print("Flagged in zone A:",
          scan_zone("A", ["KA01AB1234", "KA05XY9999", "TN09QQ1111"]))
    plate = input("Plate to revoke (Enter to skip): ")
    revoke_permit(plate)
    save_permit_database()
    print("Permits on file:", len(permits))


if __name__ == "__main__":
    main()
