from config import SERVICE_NAME
from etcd_client.client import EtcdClient


class TestEtcd:
    @classmethod
    def setup_class(cls):
        cls.client = EtcdClient()

    def setup_method(self, method):
        self.client.client.delete_prefix(f"/health/{SERVICE_NAME}")

    def teardown_method(self, method):
        self.client.client.delete_prefix(f"/health/{SERVICE_NAME}")

    def test_register_client(self):
        service_id = "192.168.13.1"
        health_key = f"/health/{SERVICE_NAME}/{service_id}"

        self.client.put(health_key, "healthy")

        actual = self.client.get_services(SERVICE_NAME)

        assert actual == [{"address": "192.168.13.1", "port": 8000}]
