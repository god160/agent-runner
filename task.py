import requests, json, re, time

PHONE = "18072039665"
s = requests.Session()
h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
     "Accept-Language": "zh-CN,zh;q=0.9",
     "Accept": "application/json, text/plain, */*"}

# Try multiple platforms
platforms = [
    ("掘金", "https://juejin.cn", "/passport/web/user/login"),
    ("简书", "https://www.jianshu.com", "/users/sms"), 
    ("CSDN", "https://passport.csdn.net", "/v1/service/mobiles/"),
    ("豆瓣", "https://accounts.douban.com", "/j/mobile/sms/send"),
]

for name, base, path in platforms:
    print(f"\n=== {name} ===")
    try:
        # Get homepage for cookies
        r = s.get(base, headers=h, timeout=15)
        print(f"  Home: {r.status_code}")
        
        # Try common SMS endpoints
        endpoints = [
            f"{base}/api/v1/sms/send",
            f"{base}/api/sms/code",
            f"{base}/api/send-sms",
            f"{base}/passport/send_code",
            f"{base}/api/v3/oauth/sms",  
        ]
        
        for ep in endpoints:
            try:
                data = {"phone": PHONE, "mobile": PHONE, "phone_no": PHONE, "type": "register"}
                r2 = s.post(ep, json=data, headers=h, timeout=10)
                if r2.status_code != 404:
                    print(f"  {ep}: {r2.status_code} - {r2.text[:150]}")
            except:
                pass
                
    except Exception as e:
        print(f"  {name}: {e}")

with open("result.txt", "w") as f:
    f.write("DONE - checking APIs\n")
