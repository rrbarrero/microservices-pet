import logging
import sys

SERVICE_NAME = "fastapi-service"
NODES_PORT = 8000
API_PREFIX = "/api/v1/"


log = logging.getLogger("gateway")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler(sys.stdout)) # defaults to sys.stderr