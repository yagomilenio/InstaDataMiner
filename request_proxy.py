import requests


with open("proxies-validos", "r") as f:
    proxies_list = [line.strip() for line in f]

def request_with_proxy(method, url, **kwargs):

    for p in proxies_list:
        tipo, ip, port = p.split(":")
        proxy_url = f"{tipo}://{ip}:{port}"
        proxies = {"http": proxy_url, "https": proxy_url}
        
        try:
            response = requests.request(method, url, proxies=proxies, timeout=5, **kwargs)
            print(f"[OK] {p}")
            return response
        except requests.RequestException:
            print(f"[FAIL] {p}, probando siguiente...")
            continue
    
    raise Exception("Ningún proxy funcionó para esta petición")


resp = request_with_proxy("get", "https://httpbin.org/ip")
print(resp.json())
