import ubinascii as binascii
import wifi

from database import database_set

DATABASE_KEY = "current-location"
BSSIDS_CSV = "apps/gumshoe/bssids.csv"

def add_locations(aps):
    with open(BSSIDS_CSV, "rb") as f:
        for bssid, loc in (l.split(b",") for l in f):
            for ap in aps:
                if bssid == binascii.hexlify(ap['bssid']):
                    ap['location'] = loc.strip()

def get_location():
    aps = wifi.nic().list_aps()
    nearest_aps = sorted(aps, key=lambda ap: ap['rssi'], reverse=True)[:5]
    print("whereami external got aps")
    add_locations(nearest_aps)
    print("whereami external added ap locations")
    print("nearest APs:")
    for ap in nearest_aps:
        print("{} ({})".format(ap.get('location', "Unknown"), ap['rssi']))
    return nearest_aps[0].get('location', "Unknown")

def store_location():
    database_set(DATABASE_KEY, get_location())
