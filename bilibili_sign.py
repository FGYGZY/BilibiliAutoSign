from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_cookies(driver):
    """加载 Cookie 并跳转到签到页面"""
    try:
        cookies_json = os.getenv("BILIBILI_COOKIES")
        cookies = json.loads(cookies_json)
        
        # 先访问目标域名以设置 Cookie
        driver.get("https://account.bilibili.com")
        time.sleep(2)
        
        # 添加 Cookie（需覆盖到 account.bilibili.com）
        for cookie in cookies:
            # 强制修改 domain 确保匹配
            cookie["domain"] = ".bilibili.com"  # 使用主域名覆盖
            driver.add_cookie(cookie)
        logger.info("Cookie 加载完成")
    except Exception as e:
        logger.error(f"Cookie 加载失败: {str(e)}")
        raise

def click_sign_button(driver):
    """点击签到按钮"""
    try:
        # 跳转到实际签到页面
        driver.get("https://account.bilibili.com/big")
        time.sleep(3)
        
        # 使用你提供的 XPath 定位按钮
        sign_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[7]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]'))
        )
        sign_button.click()
        logger.info("签到按钮点击成功")
        
        # 验证签到结果（根据实际页面提示调整）
        time.sleep(2)
        success_text = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[contains(text(), "签到成功")]'))
        )
        logger.info(f"签到成功: {success_text.text}")
    except Exception as e:
        logger.error(f"签到失败: {str(e)}")
        raise

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    # 修复 Chromium 路径问题（GitHub Actions 环境）
    options.binary_location = "/usr/bin/chromium-browser"
    
    driver = webdriver.Chrome(options=options)
    try:
        load_cookies(driver)
        click_sign_button(driver)
    except Exception as e:
        logger.error(f"脚本执行失败: {str(e)}")
        exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()