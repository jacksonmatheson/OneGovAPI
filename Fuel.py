import requests
from datetime import datetime, timezone
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
        self.AUTH = AUTH

    def get_oauth_token(self):

        # Make request to retrieve access token.
        _raw = requests.get(
            url     = self.BASE_URL + "/oauth/client_credential/accesstoken",
            params  = {"grant_type":"client_credentials"},
            headers = {"Authorization": self.AUTH.AUTH_HAEDER}
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


    def getJSON(self, path:str, params:dict={}, additional_headers:dict={}):
        
        # Get current time in their requested fucked up format.
        utc_timestamp = datetime.now(timezone.utc).strftime('%d/%m/%Y %I:%M:%S %p')

        _raw = requests.get(
            url         =   self.BASE_URL + path,
            params      =   params,
            headers     =   {
                "Authorization"     :   f"Bearer {self.TOKEN.access_token}",
                "apikey"            :   self.AUTH.KEY,
                "requesttimestamp"  :   utc_timestamp,
                **additional_headers
                }
        )
        return _raw

    def getFuelPrices(self):
        ret = fapi.getJSON(
            "/FuelPriceCheck/v1/fuel/prices",
            additional_headers={
                "transactionid"     : "5023"

            }
        )
        return ret


fapi = FuelAPI(FUEL_AUTH)
token = fapi.get_oauth_token()
ret = fapi.getFuelPrices()
