import subprocess, sys, time

subprocess.run([sys.executable, "-m", "pip", "install", "selenium"], capture_output=True)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

PHONE = "18072039665"
DEBUG = []

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--window-size=1920,1080")
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

driver = webdriver.Chrome(options=opts)

# Try zhihu first - simpler signup
print("=== Trying Zhihu ===")
driver.get("https://www.zhihu.com/signup")
time.sleep(4)
driver.save_screenshot("zhihu_1.png")
DEBUG.append(f"Zhihu URL: {driver.current_url[:80]}")

# Switch to phone reg
try:
    # Look for phone tab
    tabs = driver.find_elements(By.XPATH, "//*[contains(text(),'手机') or contains(text(),'phone')]")
    for t in tabs:
        try:
            if t.is_displayed():
                t.click()
                DEBUG.append(f"Clicked: {t.text[:30]}")
                time.sleep(1)
                break
        except:
            pass
except Exception as e:
    DEBUG.append(f"Tab fail: {e}")

# Find and fill phone input
try:
    inputs = driver.find_elements(By.TAG_NAME, "input")
    for inp in inputs:
        tp = inp.get_attribute("type") or ""
        ph = inp.get_attribute("placeholder") or ""
        if tp in ["tel", "text", "number"] and ("手机" in ph or "phone" in ph.lower() or "mobile" in ph.lower() or not ph):
            inp.click()
            inp.clear()
            inp.send_keys(PHONE)
            DEBUG.append(f"Filled: type={tp} placeholder={ph[:30]}")
            time.sleep(1)
            break
except Exception as e:
    DEBUG.append(f"Fill fail: {e}")

# Try to find and click send code button
driver.save_screenshot("zhihu_2.png")
try:
    btns = driver.find_elements(By.XPATH, "//*[contains(text(),'获取验证码') or contains(text(),'发送') or contains(text(),'验证码') or contains(text(),'Send')]")
    for btn in btns:
        try:
            if btn.is_displayed() and btn.is_enabled():
                DEBUG.append(f"Clicking: {btn.text[:30]}")
                btn.click()
                time.sleep(3)
                break
        except:
            pass
except Exception as e:
    DEBUG.append(f"Btn fail: {e}")

driver.save_screenshot("zhihu_3.png")

# Check for captcha
page_text = driver.page_source
if "captcha" in page_text.lower() or "滑块" in page_text or "验证" in page_text:
    DEBUG.append("⚠️ CAPTCHA detected!")
if "发送成功" in page_text or "已发送" in page_text:
    DEBUG.append("✅ SMS sent confirmation found!")
if "频繁" in page_text or "稍后再试" in page_text:
    DEBUG.append("⚠️ Rate limited!")

driver.quit()

result_text = "\n".join(DEBUG)
print(result_text)

with open("result.txt", "w") as f:
    f.write(f"PHONE: {PHONE}\n")
    f.write(result_text)
    f.write("\n\n如果没收到验证码，请查看截图：\n")
    f.write("https://github.com/god160/agent-runner (查看 zhihu_*.png)\n")
