import requests
import os
import dotenv
from bs4 import BeautifulSoup as bs
from gotify import Gotify


dotenv.load_dotenv(".env")
s = requests.Session()

login_url = "https://adum.fr/index.pl"

gotify = Gotify(
    base_url=os.getenv("GOTIFY_BASEURL"),
    app_token=os.getenv("GOTIFY_TOKEN")
)
data = {
    "action": "login",
    "email": os.getenv("ADUM_EMAIL"),
    "password": os.getenv("ADUM_PASSWORD"),
    "matFormation": ""
}

get = s.get(login_url)
#This sets the CGESID cookie
response = s.post(login_url, data=data)

soup = bs(response.text, "html.parser")
procedures = soup.find(id="zone_procedures")
status = procedures.find_all("b")[-1].text

#Read the last status from the file
with open("status.txt", "r") as f:
    last_status = f.read()
if last_status != status:
    with open("status.txt", "w") as f:
        f.write(status)
    print(f"Status changed: {status}")
    gotify.create_message(
        message=status,
        title="Status ADUM modifié"
    )
    