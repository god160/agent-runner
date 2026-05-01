import requests, json

print("=== NETWORK TEST ===")
# Test connectivity
tests = {
    "google": "https://www.google.com",
    "binance": "https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT",
    "bsc_rpc": "https://1rpc.io/bsc",
    "solana_rpc": "https://api.devnet.solana.com",
    "coingecko": "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
    "bountycaster": "https://www.bountycaster.xyz/api/bounties?status=open&limit=5",
    "dework": "https://api.dework.xyz/v1/tasks?limit=5",
    "onlydust": "https://app.onlydust.com/api/projects",
    "gitcoin": "https://api.gitcoin.co/v2/grants",
}

for name, url in tests.items():
    try:
        r = requests.get(url, timeout=10)
        print(f"✅ {name}: HTTP {r.status_code}")
        if r.status_code == 200:
            try:
                data = r.json()
                preview = json.dumps(data)[:200]
                print(f"   Data: {preview}")
            except:
                print(f"   Text: {r.text[:100]}")
    except Exception as e:
        print(f"❌ {name}: {str(e)[:80]}")

# Search for bounties on Bountycaster
print("\n=== BOUNTYCASTER BOUNTIES ===")
try:
    r = requests.get("https://www.bountycaster.xyz/api/bounties?status=open&limit=10", timeout=10)
    if r.status_code == 200:
        bounties = r.json()
        for b in bounties[:10]:
            print(f"💰 {b.get('reward','?')} {b.get('token','USDC')} - {str(b.get('title',''))[:80]}")
except Exception as e:
    print(f"Failed: {e}")

# Search OnlyDust
print("\n=== ONLYDUST PROJECTS ===")
try:
    r = requests.get("https://app.onlydust.com/api/projects?sort=contributors_count", timeout=10)
    if r.status_code == 200:
        projects = r.json()
        for p in projects[:5]:
            print(f"📦 {p.get('name','?')} - {p.get('description','')[:80]}")
except Exception as e:
    print(f"Failed: {e}")

print("\n=== DONE ===")
