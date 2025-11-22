import requests
from bs4 import BeautifulSoup as bs


class adum(requests.Session):
    def __init__(self, email: str, password: str):
        super().__init__()
        self.email = email
        self.password = password
        self.login_url = "https://adum.fr/index.pl"
        self.landing = self.login()

    def login(self):
        """Logs into the ADUM platform using provided credentials.
        Returns the response object after login.

        Raises:
            ValueError: If email or password is not provided.
        """

        if not self.email or not self.password:
            raise ValueError("Email and password must be provided")

        data = {
            "action": "login",
            "email": self.email,
            "password": self.password,
            "matFormation": "",
        }

        _ = self.get(self.login_url)
        # This sets the CGESID cookie
        response = self.post(self.login_url, data=data)

        return response

    def get_status(self):
        """Fetches the current status from the ADUM platform.

        Returns:
            str: The current status text.
        """
        soup = bs(self.landing.text, "html.parser")
        procedures = soup.find(id="zone_procedures")
        status = procedures.find_all("b")[-1].text
        return status

    def get_formations(self):
        """Fetches the list of formations that the user is enrolled in.
        It fetches formations that the user is :
            - Trying to enroll in
            - Currently enrolled in
            - Completed
        """
        formation_url = "https://adum.fr/phd/formation/formation_encours.pl"
        response = self.get(formation_url)
        soup = bs(response.text, "html.parser")
        formations = soup.find(id="zone_formulaire")
        tables = formations.find_all("table")
        formations_list = [
            tables[i].find_all("a", href=True) for i in range(len(tables))
        ]
        formations_href = [a["href"] for sublist in formations_list for a in sublist]
        
