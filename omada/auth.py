import requests
from config import BASE_URL, EMAIL, PASSWORD

def get_access_token(creds):
    login_url = f"{BASE_URL}/openapi/authorize/login?client_id={creds['client_id']}&omadac_id={creds['omadac_id']}"
    login_payload = {"username": EMAIL, "password": PASSWORD}
    login_res = requests.post(login_url, json=login_payload, timeout=15).json()
    csrf_token = login_res["result"]["csrfToken"]
    session_id = login_res["result"]["sessionId"]

    auth_code_url = f"{BASE_URL}/openapi/authorize/code?client_id={creds['client_id']}&omadac_id={creds['omadac_id']}&response_type=code"
    auth_headers = {"Csrf-Token": csrf_token, "Cookie": f"TPOMADA_SESSIONID={session_id}"}
    auth_code = requests.post(auth_code_url, headers=auth_headers, timeout=15).json()["result"]

    token_url = f"{BASE_URL}/openapi/authorize/token?grant_type=authorization_code&code={auth_code}"
    token_payload = {"client_id": creds["client_id"], "client_secret": creds["client_secret"]}
    token_res = requests.post(token_url, json=token_payload, timeout=15).json()

    return token_res["result"]["accessToken"]
