import requests
from dataclasses import dataclass

@dataclass
class Auth():
    KEY: str
    SECRET: str
    AUTH_HAEDER: str

@dataclass
class AccessToken():
    access_token: str
    api_product_list: list
    api_product_list_json: str
    application_name: str
    client_id: str
    expires_in: str
    issued_at: str
    organization_name: str
    refresh_count: str
    refresh_token_expires_in: str
    scope: str
    status: str
    token_type: str


FUEL_AUTH = Auth(
    "d1AN4ASrGs6Km7roGUHSZqR63d3GSXgN",
    "wLOkawX7hWU7VREm",
    "Basic ZDFBTjRBU3JHczZLbTdyb0dVSFNacVI2M2QzR1NYZ046d0xPa2F3WDdoV1U3VlJFbQ==",
)


class OneGovAPI():

    _endpoints = {
        "oauth": "/oauth/client_credential/accesstoken"
    }

    def __init__(self, AUTH:Auth, BASE_URL:str="https://api.onegov.nsw.gov.au"):
        self.BASE_URL = BASE_URL

    def get_oauth_token(self):

        # Make request to retrieve access token.
        _raw = requests.get(
            url     = self.BASE_URL + "/oauth/client_credential/accesstoken",
            params  = {"grant_type":"client_credentials"},
            headers = {"Authorization": FUEL_AUTH.AUTH_HAEDER}
        )

        # Get JSON response
        jsonResp = _raw.json()
        jsonResp.pop("developer.email")

        # Store in dataclass
        self.TOKEN = AccessToken(**jsonResp)

        return self.TOKEN
        

class FuelAPI(OneGovAPI):

    def __init__(self, AUTH:Auth, BASE_URL:str="https://api.onegov.nsw.gov.au"):
        super().__init__(AUTH, BASE_URL)


fapi = FuelAPI(FUEL_AUTH)
token = fapi.get_oauth_token()