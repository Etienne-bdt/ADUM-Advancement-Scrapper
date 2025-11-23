import os

import dotenv
from gotify import Gotify

from adum import adum

dotenv.load_dotenv(".env")

if os.getenv("ADUM_EMAIL") is None or os.getenv("ADUM_PASSWORD") is None:
    print("Missing ADUM_EMAIL or ADUM_PASSWORD env vars")
    exit(1)

dotenv.load_dotenv(".env")
adum_client = adum(
    email=os.getenv("ADUM_EMAIL"),
    password=os.getenv("ADUM_PASSWORD")
)

if os.getenv("GOTIFY_BASEURL") is None or os.getenv("GOTIFY_TOKEN") is None:
    use_gotify = False
    print("Skipping Gotify notification, missing env vars")
else:
    use_gotify = True
    gotify = Gotify(
        base_url=os.getenv("GOTIFY_BASEURL"),
        app_token=os.getenv("GOTIFY_TOKEN"))
    

status = adum_client.get_status()
ical = adum_client.get_icalendar()
icalendar_path = os.getenv("ICAL_OUTPUT_PATH", "./output/advancements.ics")
with open(icalendar_path, "wb") as f:
    f.write(ical.to_ical())
print(f"iCalendar saved to {icalendar_path}")
#Read the last status from the file (handle missing file)
try:
    with open("status.txt", "r") as f:
        last_status = f.read().strip()
except FileNotFoundError:
    last_status = ""

if last_status != status:
    with open("status.txt", "w") as f:
        f.write(status)
    print(f"Status changed: {status}")
    if use_gotify:
        gotify.create_message(
            message=status,
            title="Status ADUM modifié"
        )
