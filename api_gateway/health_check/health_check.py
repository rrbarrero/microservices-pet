import threading
import time
import requests
from config import API_PREFIX, SERVICE_NAME, log
from etcd_client.client import EtcdClient


def health_check_gateway(client: EtcdClient):
    """
    Function that performs the health check of all services from the API Gateway.
    """
    while True:
        services = client.get_services(SERVICE_NAME)
        for service in services:
            service_id = service['address']
            health_key = f"/health/{SERVICE_NAME}/{service_id}"
            try:
                url = f"http://{service['address']}:{service['port']}{API_PREFIX}health"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    client.put(health_key, "healthy")
                    log.debug(f"[HEALTH CHECK] {SERVICE_NAME} in {service['address']} is healthy.")
                else:
                    client.put(health_key, "unhealthy")
                    log.error(f"[HEALTH CHECK] {SERVICE_NAME} in {service['address']} is not healthy. Status code: {response.status_code}")
            except requests.RequestException as e:
                client.put(health_key, "unhealthy")
                log.error(f"[HEALTH CHECK] {SERVICE_NAME} in {service['address']} is not healthy")
                log.debug(f"[HEALTH CHECK] Error verifying {SERVICE_NAME} in {service['address']}: {e}")
        
        time.sleep(10)

def start(client: EtcdClient):
    health_thread = threading.Thread(target=health_check_gateway, args=[client], daemon=True)
    health_thread.start()