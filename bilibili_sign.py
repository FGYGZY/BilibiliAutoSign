from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_cookies(driver):
    """从环境变量加载 Cookie"""
    cookies_json = os.getenv("BILIBILI_COOKIES")
    cookies = json.loads(cookies_json)
    driver.get("https://account.bilibili.com/big")  # 必须访问域名以加载 Cookie
    time.sleep(5)
    for cookie in cookies:
        # 修正 Cookie 格式（确保包含 'domain' 字段）
        if 'domain' not in cookie:
            cookie['domain'] = ".bilibili.com"
        driver.add_cookie(cookie)
    logger.info("Cookie 加载完成")

def click_sign_button(driver):
    """点击签到按钮"""
    # 示例：B站主站每日签到按钮（需根据实际页面调整！）
    driver.get("https://account.bilibili.com/big")
    time.sleep(3)
    try:
        # 通过 XPath 定位按钮（核心修改点）
        sign_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[7]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]'))
        )
        sign_button.click()
        logger.info("签到按钮点击成功")
        time.sleep(2)
        # 检查签到成功提示
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[contains(text(), "签到成功")]'))
        )
        logger.info("签到成功")
    except Exception as e:
        logger.error(f"签到失败: {str(e)}")
        raise

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(options=options)
    try:
        load_cookies(driver)
        click_sign_button(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()