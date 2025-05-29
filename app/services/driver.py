import requests
from app.models.driver import Driver
from app.services.database import Database
from datetime import datetime, timedelta, UTC

DRIVER_CACHE_KEY = "last_driver_fetch"
CACHE_EXPIRY = timedelta(hours=6)

def get_all_drivers() -> list[Driver]:
    db = Database()
    last_fetch = db.get_last_fetch_time(DRIVER_CACHE_KEY)
    now = datetime.now(UTC)

    if last_fetch and now - last_fetch < CACHE_EXPIRY:
        print("Loaded drivers from DB cache")
        driver_dicts = db.load_drivers()
    else:
        print("Fetching drivers from API")
        resp = requests.get("https://api.openf1.org/v1/drivers", timeout=10)
        driver_dicts = resp.json()
        db.save_drivers(driver_dicts)
        db.update_last_fetch_time(DRIVER_CACHE_KEY, now)

    return [Driver(**d) for d in driver_dicts]

def get_driver(driver_number: int) -> Driver | None:
    drivers = get_all_drivers()
    for driver in drivers:
        if driver.driver_number == int(driver_number):
            return driver
    return None

def get_id_driver_dict() -> dict[int, Driver]:
    drivers = get_all_drivers()
    return {driver.driver_number: driver for driver in drivers}
