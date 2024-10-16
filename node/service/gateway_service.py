import socket
import etcd3
from config import ETCD, ETCD_PORT, SERVICE_NAME


class GatewayService:
    def __init__(self):
        self.client = etcd3.client(host=ETCD, port=ETCD_PORT)

    def register(self):
        service_id = socket.gethostbyname(socket.gethostname())
        health_key = f"/health/{SERVICE_NAME}/{service_id}"
        self.client.put(health_key, "healthy")
