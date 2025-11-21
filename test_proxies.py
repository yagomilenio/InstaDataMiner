import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

INPUT_FOLDER = "proxies-to-test"
OUTPUT_FILE = "proxies-validos"
MAX_THREADS = 20  

file_lock = Lock()  


def load_proxies():
    proxies = []
    for file in os.listdir(INPUT_FOLDER):
        path = os.path.join(INPUT_FOLDER, file)
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(":")
                if len(parts) == 3:
                    tipo, ip, port = parts
                    proxies.append((tipo.lower(), ip, port))
    return proxies


def test_proxy(proxy):
    tipo, ip, port = proxy
    proxy_url = f"{tipo}://{ip}:{port}"
    proxies = {"http": proxy_url, "https": proxy_url}

    try:
        r = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=5)
        if r.status_code == 200:
            return proxy
    except Exception:
        pass

    return None


def write_valid_proxy(proxy):
    tipo, ip, port = proxy
    line = f"{tipo}:{ip}:{port}\n"

    with file_lock:
        with open(OUTPUT_FILE, "a") as f:
            f.write(line)


def main():
    proxies = load_proxies()
    print(f"Proxies cargados: {len(proxies)}")

    open(OUTPUT_FILE, "w").close()

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_proxy = {executor.submit(test_proxy, p): p for p in proxies}

        for future in as_completed(future_to_proxy):
            proxy = future_to_proxy[future]
            tipo, ip, port = proxy

            result = future.result()
            if result:
                print(f"{tipo}:{ip}:{port} OK")
                write_valid_proxy(proxy)
            else:
                print(f"{tipo}:{ip}:{port} FAIL")

    print(f"\nTodos los proxies procesados.")
    print(f"Resultados guardados en {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
