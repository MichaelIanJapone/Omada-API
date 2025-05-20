from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=dotenv_path)


BASE_URL = "https://aps1-omada-northbound.tplinkcloud.com"
EMAIL = os.getenv("OMADA_EMAIL")
PASSWORD = os.getenv("OMADA_PASSWORD")

INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

PROVINCES = {
    "Kalinga": {
        "client_id": "ff6627381ec5450e9fed88af4fd595c1",
        "client_secret": "9e37c05e9cfd48d29dc893837331012c",
        "omadac_id": "f95dd45b8e5f1449c1687526c4453cd4"
    },
    "Quezon": {
        "client_id": "e907acde91d04704b1cedaffb8fb0ac3",
        "client_secret": "6d317c96764741f790fa7d61f4d35b79",
        "omadac_id": "478614c90c6e62e22fea04914c2ea139"
    },
    "Benguet": {
        "client_id": "1166ae0f282945f98704fe827e83145c",
        "client_secret": "4c886093e980467ebedc5ca6b69c3901",
        "omadac_id": "da057e6d95a57a9706e4881e6188b26b"
    },
    "Ifugao": {
        "client_id": "72f24fccf8aa4f16ba76457f141a9863",
        "client_secret": "4940c7a5b5244161aec417154d852911",
        "omadac_id": "f1205ddfdac34f6e3c6e2c96d8ba6f8a"
    },
    "Pangasinan": {
        "client_id": "723f4872a6684298b6a76ea12f8f064a",
        "client_secret": "ff23acc237744856aa990f4a9741c081",
        "omadac_id": "cdd0bd044d68004a269b1ad6dbeb0d71"
    },
    "Ilocos": {
        "client_id": "bb9c56e3efaf49168c62be6e5eaa8d90",
        "client_secret": "c22e2d25d8c54ae4b4500a1ab3324947",
        "omadac_id": "ebdc0e2ce38d013bedaf0cf08a9b7bf9"
    },
}
