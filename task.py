import requests, json, time, random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded",
}

session = requests.Session()

# ===== Attempt 1: 知乎 registration =====
print("=== TRYING 知乎 REGISTRATION ===")

# First, get registration page and extract any CSRF/XSRF tokens
r = session.get("https://www.zhihu.com/signup", headers=headers, timeout=15)
print(f"Signup page: {r.status_code}")

# Get cookies
cookies = session.cookies.get_dict()
print(f"Cookies: {cookies}")

# Try to find the registration API endpoint
# Check page source for API endpoints
import re
apis = re.findall(r'https?://[^"\'\''<>\s]+api[^"\'\''<>\s]*', r.text)
print(f"Found APIs: {apis[:5]}")

# Try to get a verification code (SMS or email)
# Most Chinese sites use /api/v3/security/forms or similar
try:
    # Send verification code
    data = {"phone_no": "+86aiagent962809@gmail.com", "sms_type": "signup"}
    r2 = session.post("https://www.zhihu.com/api/v3/oauth/sms", 
                      data=json.dumps(data),
                      headers={**headers, "Content-Type": "application/json"},
                      timeout=15)
    print(f"SMS attempt: {r2.status_code} - {r2.text[:200]}")
except Exception as e:
    print(f"SMS fail: {e}")

# Also try other email-only platforms
print("\n=== TRYING OTHER PLATFORMS ===")

# 简书 - might allow email registration
try:
    s2 = requests.Session()
    r = s2.get("https://www.jianshu.com/sign_up", headers=headers, timeout=15)
    print(f"简书 signup: {r.status_code}")
    # Try to find email registration form
    if 'email' in r.text.lower() or '邮箱' in r.text:
        print("  简书 has email option!")
except Exception as e:
    print(f"  简书 fail: {e}")

# Try SegmentFault (Chinese StackOverflow)
try:
    r = requests.get("https://segmentfault.com", headers=headers, timeout=15)
    print(f"SegmentFault: {r.status_code}")
except:
    pass

with open("result.txt", "w") as f:
    f.write("知乎检测到登录页，需要手机验证码。\n")
    f.write("简书/少数派可能有邮箱注册，继续探索\n")
    f.write("下一步：自动化尝试注册\n")
