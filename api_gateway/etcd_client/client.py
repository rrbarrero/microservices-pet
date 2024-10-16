import etcd3

from config import NODES_PORT


class EtcdClient:
    def __init__(self):
        self.client = etcd3.client(host='etcd', port=2379)

    def get_services(self, service_name: str):
        services = []
        prefix = f"/health/{service_name}/"
        for value, metadata in self.client.get_prefix(prefix):
            if value == b"healthy":
                address = metadata.key.decode('utf-8').split("/")[-1]
                services.append({"address": address, "port": NODES_PORT})
        return services
    
    def put(self, key, value):
        self.client.put(key, value)