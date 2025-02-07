import random
from typing import Optional

class ProxyManager:
    def __init__(self):
        # Lista estática de proxies públicos
        self.proxies = [
            "http://165.227.71.60:80",
            "http://165.227.81.188:80",
            "http://159.65.77.168:80",
            "http://206.189.145.178:80",
            "http://157.245.222.183:80",
            "http://138.68.60.8:8080",
            "http://143.198.182.218:80"
        ]
    
    def get_random_proxy(self) -> Optional[str]:
        """Obtener un proxy aleatorio"""
        return random.choice(self.proxies) if self.proxies else None 