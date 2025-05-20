from config import PROVINCES
from influx import get_influx_client
from omada.connection import get_all_past_connections

def main():
    influx_client = get_influx_client()
    write_api = influx_client.write_api()

    for province, creds in PROVINCES.items():
        print(f"📡 Processing province: {province}")
        get_all_past_connections(province, creds, write_api)

    influx_client.close()
    print("✅ All data saved to InfluxDB.")

if __name__ == "__main__":
    main()
