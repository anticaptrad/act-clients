from urllib.request import Request, urlopen
import json
class ActClient:
    def __init__(self, base_url: str): self.base_url = base_url.rstrip('/')
    def _get(self, path: str):
        req = Request(self.base_url + path, headers={'Accept':'application/json'})
        with urlopen(req, timeout=10) as res: return json.load(res)
    def health(self): return self._get('/health')
    def ready(self): return self._get('/ready')
