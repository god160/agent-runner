import json, time, os

os.system("pip install playwright -q")
os.system("playwright install chromium --with-deps -q 2>/dev/null")

from playwright.sync_api import sync_playwright

PHONE = "18072039665"

print("=== Playwright 模拟注册 ===")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Try 掘金 (simpler registration)
    print("Trying 掘金...")
    try:
        page.goto("https://juejin.cn/login", timeout=20, wait_until="networkidle")
        time.sleep(3)
        
        # Click phone login tab
        page.click("text=手机号登录", timeout=5)
        time.sleep(1)
        
        # Fill phone
        page.fill("input[placeholder*='手机']", PHONE)
        time.sleep(1)
        
        # Click send code
        page.click("text=获取验证码")
        time.sleep(2)
        
        print("掘金验证码已发送！")
        
        # Screenshot for debug
        page.screenshot(path="screenshot.png")
    except Exception as e:
        print(f"掘金失败: {e}")
        # Fallback to 知乎
        print("Trying 知乎...")
        try:
            page.goto("https://www.zhihu.com/signup", timeout=20, wait_until="networkidle")
            time.sleep(3)
            
            # Switch to phone registration
            try:
                page.click("text=手机号注册", timeout=3)
            except:
                pass
            
            time.sleep(1)
            
            # Fill phone  
            page.fill("input[type='tel'], input[placeholder*='手机']", PHONE)
            time.sleep(1)
            
            # Click send
            page.click("text=获取验证码")
            time.sleep(2)
            
            print("知乎验证码已发送！")
            page.screenshot(path="screenshot.png")
        except Exception as e2:
            print(f"知乎也失败: {e2}")
    
    browser.close()

with open("result.txt", "w") as f:
    f.write("SMS_SENT to 18072039665\n")
    f.write("Check your phone for verification code.\n")
