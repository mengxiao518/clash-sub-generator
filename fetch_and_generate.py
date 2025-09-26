import requests, base64, re, yaml, os

OUT_CLASH = "docs/clash.yaml"
os.makedirs("docs", exist_ok=True)

def fetch_sources(file="sources.txt"):
    with open(file) as f:
        return [l.strip() for l in f if l.strip() and not l.startswith("#")]

def fetch_content(url):
    try:
        r = requests.get(url, timeout=15)
        if r.ok:
            return r.text
    except:
        return ""
    return ""

def parse_links(data):
    try:
        decoded = base64.b64decode(data).decode("utf-8", errors="ignore")
        return re.findall(r"(vmess://[^\s]+|ss://[^\s]+|trojan://[^\s]+)", decoded)
    except:
        return re.findall(r"(vmess://[^\s]+|ss://[^\s]+|trojan://[^\s]+)", data)

def convert_to_clash(links):
    return {
        "proxies": [{"name": f"Node-{i}", "type": "vmess", "server": "example.com",
                     "port": 443, "uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                     "alterId": 0, "cipher": "auto", "tls": True}
                    for i, _ in enumerate(links[:30])],
        "proxy-groups": [{
            "name": "Auto",
            "type": "select",
            "proxies": [f"Node-{i}" for i in range(min(30, len(links)))]
        }],
        "rules": ["MATCH,Auto"]
    }

def main():
    links = []
    for url in fetch_sources():
        data = fetch_content(url)
        if data:
            links.extend(parse_links(data))
    clash_conf = convert_to_clash(links)
    with open(OUT_CLASH, "w", encoding="utf-8") as f:
        yaml.dump(clash_conf, f, allow_unicode=True)
    print(f"✅ 生成完成: {OUT_CLASH}")

if __name__ == "__main__":
    main()
