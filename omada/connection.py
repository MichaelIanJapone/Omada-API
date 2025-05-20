import time
import requests
from datetime import datetime, timedelta, timezone
from influxdb_client import Point, WritePrecision
from config import BASE_URL, INFLUX_BUCKET, INFLUX_ORG
from .auth import get_access_token
from .site import get_sites
from influx import write_points

def get_all_past_connections(province_name, creds, influx_writer):
    try:
        access_token = get_access_token(creds)
        sites = get_sites(creds["omadac_id"], access_token)
        headers = {"Authorization": f"AccessToken={access_token}"}

        unique_macs = set()

        
        tz = timezone(timedelta(hours=8))
        
        
        start_date = datetime(2025, 1, 1, tzinfo=tz) 
        end_date = datetime.now(tz)  

        
        current_start = start_date

        while current_start < end_date:
            
            current_end = min(current_start + timedelta(days=31), end_date)

            
            start_ms = int(current_start.timestamp() * 1000)
            end_ms = int(current_end.timestamp() * 1000)

            print(f"📅 Fetching data from {current_start.date()} to {current_end.date()}")

            
            for site in sites:
                site_id = site["siteId"]
                site_name = site["name"]
                page = 1

                while True:
                    url = (
                        f"{BASE_URL}/openapi/v1/{creds['omadac_id']}/sites/{site_id}/insight/past-connection"
                        f"?pageSize=1000&page={page}&filters.timeStart={start_ms}&filters.timeEnd={end_ms}"
                    )
                    res = requests.get(url, headers=headers, timeout=15).json()
                    data = res.get("result", {}).get("data", [])
                    if not data:
                        break

                    points = []
                    for conn in data:
                        mac = conn.get("mac")
                        name = conn.get("name", "")
                        device_name = conn.get("deviceName", "")
                        ssid = conn.get("ssid", "")
                        first_seen = conn.get("firstSeen")
                        last_seen = conn.get("lastSeen")
                        download = conn.get("download", 0)
                        upload = conn.get("upload", 0)

                        if not (mac and first_seen and last_seen):
                            continue

                        unique_macs.add(mac)

                        traffic_mb = round((download + upload) / (1024 * 1024), 2)
                        session = f"{mac}_{first_seen}_{last_seen}"
                        tags = {
                            "province": province_name,
                            "site": site_name,
                            "mac": mac,
                            "device": name,
                            "ssid": ssid,
                            "ap_name": device_name,
                            "session_id": session
                        }


                        first_dt = datetime.fromtimestamp(first_seen / 1000, tz=tz)
                        last_dt = datetime.fromtimestamp(last_seen / 1000, tz=tz)


                        mid_dt = first_dt + (last_dt - first_dt) / 2
                        point = Point("connection_traffic").time(mid_dt, WritePrecision.MS).field("total_traffic_MB", traffic_mb)
                        for k, v in tags.items():
                            point.tag(k, v)
                        points.append(point)


                    if points:
                        write_points(influx_writer, INFLUX_BUCKET, INFLUX_ORG, points)

                    if len(data) < 1000:
                        break

                    page += 1
                    time.sleep(0.5)

            current_start = current_end

        print(f"✅ Province {province_name}: {len(unique_macs)} unique MAC addresses")

    except Exception as e:
        print(f"❌ Error fetching data for {province_name}: {e}")
