import requests

proxies_dict = {}

def request_with_proxy(method, url, patter=None, outputFile="proxies-validos",**kwargs):

    with open(outputFile, "r") as f:
        for line in f:
            proxy = line.strip()
            proxies_dict[proxy] = 0

    for proxy, score in sorted(proxies_dict.items(), key=lambda x: x[1], reverse=True):
        tipo, ip, port = proxy.split(":")
        proxy_url = f"{tipo}://{ip}:{port}"
        proxies = {"http": proxy_url, "https": proxy_url}
        
        try:
            response = requests.request(method, url, proxies=proxies, timeout=5, **kwargs)
            data = response.json()
            if patter != None and not patter in data:
                proxies_dict[proxy] -= 1
                raise requests.RequestException

            proxies_dict[proxy] += 1
            print(f"[OK] {proxy}: {data}")
            return response
        except requests.RequestException:
            print(f"[FAIL] {proxy}, probando siguiente...")
            proxies_dict[proxy] -= 1
            continue
    
    raise Exception("Ningún proxy funcionó para esta petición")


