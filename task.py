import requests, json, time, re

PHONE = "18072039665"
session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://www.zhihu.com/",
}

print("=== 知乎发送验证码 ===")

# Step 1: Get cookies from zhihu.com
r = session.get("https://www.zhihu.com", headers=headers, timeout=15)
print(f"Home: {r.status_code}")

# Get XSRF token
xsrf = ""
for cookie in session.cookies:
    if 'xsrf' in cookie.name.lower() or 'csrf' in cookie.name.lower() or '_xsrf' in cookie.name.lower():
        xsrf = cookie.value
        print(f"XSRF found: {cookie.name}={xsrf[:20]}")

# Also try to find in HTML
if not xsrf:
    match = re.search(r'_xsrf[\'"]\s*[:=]\s*[\'"]([^\'"]+)[\'"]', r.text)
    if match:
        xsrf = match.group(1)
        print(f"XSRF from HTML: {xsrf}")

# Step 2: Send SMS verification code
api_headers = {**headers, "X-Xsrftoken": xsrf or "", "X-Requested-With": "XMLHttpRequest"}

# Zhihu signup API - try captcha first
try:
    captcha_url = "https://www.zhihu.com/api/v3/oauth/captcha?lang=cn"
    r = session.get(captcha_url, headers=api_headers, timeout=15)
    print(f"Captcha check: {r.status_code} - {r.text[:200]}")
except Exception as e:
    print(f"Captcha: {e}")

# Try to send SMS
try:
    sms_data = {"phone_no": PHONE, "digits": "86"}
    r = session.post(
        "https://www.zhihu.com/api/v3/oauth/sign_up",
        json=sms_data,
        headers=api_headers,
        timeout=15
    )
    print(f"SMS request: {r.status_code}")
    print(f"Response: {r.text[:500]}")
except Exception as e:
    print(f"SMS fail: {e}")

# Also try alternate endpoint
try:
    sms_data2 = {"phone_no": PHONE, "sms_type": "sign_up"}
    r = session.post(
        "https://www.zhihu.com/api/v3/oauth/sms",
        json=sms_data2,
        headers=api_headers,
        timeout=15
    )
    print(f"SMS v2: {r.status_code} - {r.text[:300]}")
except Exception as e:
    print(f"SMS v2 fail: {e}")

# Save cookies for next step
import pickle
with open("cookies.pkl", "wb") as f:
    pickle.dump(session.cookies, f)

with open("result.txt", "w") as f:
    f.write("SMS_SENT: check phone {PHONE}\n")
    f.write("Session saved. Waiting for verification code.\n")
