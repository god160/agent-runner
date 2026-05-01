import requests, json, re

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
           "Accept-Language": "zh-CN,zh;q=0.9"}

R = {}

# ===== 知乎: email registration test =====
print("=== 知乎 ===")
try:
    r = requests.get("https://www.zhihu.com/signup", headers=headers, timeout=15)
    print(f"Signup page: HTTP {r.status_code}")
    if '邮箱' in r.text or 'email' in r.text.lower():
        print("  ✅ Email registration option found!")
        R['zhihu'] = "EMAIL_REG_OK"
    elif '手机' in r.text:
        print("  ⚠️ Phone only? Checking...")
        R['zhihu'] = "PHONE_ONLY?" + str(r.status_code)
    else:
        print(f"  Text sample: {r.text[:300]}")
        R['zhihu'] = f"HTTP{r.status_code}"
except Exception as e:
    print(f"  FAIL: {e}")
    R['zhihu'] = f"FAIL:{str(e)[:30]}"

# ===== 掘金 =====
print("\n=== 掘金 ===")
try:
    r = requests.get("https://juejin.cn", headers=headers, timeout=15)
    print(f"Home: HTTP {r.status_code}")
    # Check login page
    r2 = requests.get("https://juejin.cn/login", headers=headers, timeout=15)
    if '邮箱' in r2.text or 'email' in r2.text.lower():
        print("  ✅ Email login found")
        R['juejin'] = "EMAIL_OK"
    else:
        R['juejin'] = f"HTTP{r2.status_code}"
except Exception as e:
    R['juejin'] = f"FAIL:{str(e)[:30]}"

# ===== CSDN =====
print("\n=== CSDN ===")
try:
    r = requests.get("https://www.csdn.net", headers=headers, timeout=15)
    print(f"Home: HTTP {r.status_code}")
    r2 = requests.get("https://passport.csdn.net/login", headers=headers, timeout=15)
    if '邮箱' in r2.text or 'email' in r2.text.lower():
        print("  ✅ Email option found")
        R['csdn'] = "EMAIL_OK"
    else:
        R['csdn'] = f"HTTP{r2.status_code}"
except Exception as e:
    R['csdn'] = f"FAIL:{str(e)[:30]}"

# ===== 简书 (jianshu.com) =====
print("\n=== 简书 ===")
try:
    r = requests.get("https://www.jianshu.com/sign_up", headers=headers, timeout=15)
    print(f"Signup: HTTP {r.status_code}")
    if '邮箱' in r.text or 'email' in r.text.lower():
        print("  ✅ Email registration!")
        R['jianshu'] = "EMAIL_REG_OK"
    else:
        R['jianshu'] = f"HTTP{r.status_code}"
except Exception as e:
    R['jianshu'] = f"FAIL:{str(e)[:30]}"

# ===== 少数派 sspai.com =====
print("\n=== 少数派 ===")
try:
    r = requests.get("https://sspai.com/signup", headers=headers, timeout=15)
    print(f"Signup: HTTP {r.status_code}")
    if '邮箱' in r.text or 'email' in r.text.lower():
        print("  ✅ Email registration!")
        R['sspai'] = "EMAIL_REG_OK"
    else:
        R['sspai'] = f"HTTP{r.status_code}"
except Exception as e:
    R['sspai'] = f"FAIL:{str(e)[:30]}"

# ===== 百度文库/知道 (check for reward systems) =====
print("\n=== 百度知道 ===")
try:
    r = requests.get("https://zhidao.baidu.com", headers=headers, timeout=15)
    print(f"Home: HTTP {r.status_code}")
    R['baidu_zhidao'] = f"HTTP{r.status_code}"
except Exception as e:
    R['baidu_zhidao'] = f"FAIL:{str(e)[:30]}"

# Save
with open("result.txt", "w") as f:
    json.dump(R, f, indent=2, ensure_ascii=False)
    print(f"\n=== RESULTS ===")
    print(json.dumps(R, indent=2, ensure_ascii=False))
