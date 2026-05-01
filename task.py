import json, os, requests, time, random

RESULTS = {}

# ========= LINE A: FAUCET FARMING =========
print("=== FAUCET FARMING ===")

faucets = [
    ("FreeBitco.in", "https://freebitco.in/?op=api&key=FAKE_KEY"),
    ("FaucetPay", "https://faucetpay.io/api/v1/faucetlist"),
    ("PipeFlare", "https://pipeflare.io/api/claim"),
]

# Test which faucets are accessible
for name, url in faucets:
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        RESULTS[name] = f"HTTP {r.status_code}"
        print(f"  {name}: HTTP {r.status_code}")
    except Exception as e:
        RESULTS[name] = f"FAIL: {str(e)[:50]}"

# ========= LINE B: TEST CHINESE PLATFORMS =========
print("\n=== LINE B: CHINESE PLATFORM ACCESS ===")

platforms = {
    "猪八戒": "https://www.zbj.com",
    "CSDN": "https://www.csdn.net",
    "掘金": "https://juejin.cn",
    "知乎": "https://www.zhihu.com",
    "闲鱼": "https://www.goofish.com",
    "百度知道": "https://zhidao.baidu.com",
    "豆瓣": "https://www.douban.com",
    "B站": "https://www.bilibili.com",
}

for name, url in platforms.items():
    try:
        r = requests.get(url, timeout=10, 
                        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                                "Accept-Language": "zh-CN,zh;q=0.9"})
        title = ""
        if '<title>' in r.text:
            title = r.text.split('<title>')[1].split('</title>')[0][:60]
        print(f"  {name}: HTTP {r.status_code} | {title}")
        RESULTS[name] = f"OK ({r.status_code})"
    except Exception as e:
        print(f"  {name}: FAIL - {str(e)[:50]}")
        RESULTS[name] = f"FAIL: {str(e)[:40]}"

# ========= LINE C: TEST EMAIL-ONLY REGISTRATION =========
print("\n=== LINE C: EMAIL-ONLY PLATFORMS ===")

email_platforms = {
    "GitLab": "https://gitlab.com/users/sign_up",
    "Notion": "https://www.notion.so/signup",
    "Medium": "https://medium.com/m/signin",
    "Dev.to": "https://dev.to/enter",
    "Hashnode": "https://hashnode.com/onboard",
    "Substack": "https://substack.com/sign-in",
    "Mirror.xyz": "https://mirror.xyz/dashboard",
    "ProductHunt": "https://www.producthunt.com/signup",
}

for name, url in email_platforms.items():
    try:
        r = requests.get(url, timeout=10,
                        headers={"User-Agent": "Mozilla/5.0"})
        print(f"  {name}: HTTP {r.status_code}")
        RESULTS[name] = f"OK ({r.status_code})"
    except Exception as e:
        RESULTS[name] = f"FAIL"

# Save
with open("result.txt", "w") as f:
    json.dump(RESULTS, f, indent=2)
    print(f"\n=== ALL DONE ===")
    print(json.dumps(RESULTS, indent=2))
