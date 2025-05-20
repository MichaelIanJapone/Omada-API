import requests
from config import BASE_URL

def get_sites(omadac_id, access_token):
    url = f"{BASE_URL}/openapi/v1/{omadac_id}/sites?pageSize=80&page=1"
    headers = {"Authorization": f"AccessToken={access_token}"}
    response = requests.get(url, headers=headers, timeout=15)
    return response.json()["result"]["data"]
