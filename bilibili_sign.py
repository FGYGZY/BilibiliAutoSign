from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
import time
import logging
import smtplib
from email.mime.text import MIMEText
from email.header import Header

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

def send_email(status):
    """发送邮件通知"""
    # 从环境变量读取邮件配置
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT"))
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    # 构造邮件内容
    subject = "[DS]B站大会员积分领取状态通知"
    body = f"领取状态：{status}（时间：{time.strftime('%Y-%m-%d %H:%M:%S')}）"

    message = MIMEText(body, 'plain', 'utf-8')
    message['From'] = Header(sender_email)
    message['To'] = Header(receiver_email)
    message['Subject'] = Header(subject)

    try:
        # 使用 SSL 加密
        logger.info("连接到 SMTP 服务器")
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(sender_email, sender_password)
            logger.info("登录 SMTP 服务器")
            server.sendmail(sender_email, [receiver_email], message.as_string())
            logger.info("邮件发送成功")
            server.quit()
    except smtplib.SMTPException as e:
        logger.error(f"SMTP 错误: {str(e)}")
    except Exception as e:
        logger.error(f"邮件发送失败: {str(e)}")


def click_sign_button(driver, sign_button):
    button_text = sign_button.text.strip()
    logger.info(f"领取按钮文本: {button_text}")

    if button_text == "已领取":
        logger.info("今日已正常领取")
        return "[Success]今日已领取"
    elif button_text == "去领取":
        sign_button.click()
        logger.info("点击领取按钮")

        try:
            # 检查领取成功提示
            WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, '//*[contains(text(), "已领取")]'))
            )
            logger.info("点击领取成功")
            return "[Success]领取成功"
        except:
            # 检查是否有确认按钮
            try:
                confirm_button = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "确认")]'))
                )
                status_text = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[7]/div[2]/div[2]/div[1]/div[1]/div[3]/div/div/p[2]').text.strip()
                logger.info(f"确认弹窗状态文本: {status_text}")
                if "领取过" in status_text:
                    return "[Success]今日已领取"
                elif "网路繁忙" in status_text:
                    return "[Fail]网络异常"
                else:
                    return f"[Fail]未知状态: {status_text}"
            except:
                logger.info("未找到确认按钮")
                return "[Fail]未找到确认按钮"
    else:
        return f"[Fail]未知状态: {button_text}"

def check_sign_status(driver):
    # 检查领取状态
    try:
        logger.info("访问领取页面")
        driver.get("https://account.bilibili.com/big")
        time.sleep(3)
        
        logger.info("等待领取按钮出现")
        # 定位按钮元素（根据实际页面调整选择器）
        sign_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[7]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]'))
        )
        button_text = sign_button.text.strip()
        logger.info(f"按钮文本: {button_text}")

        # 点击领取按钮
        status = click_sign_button(driver, sign_button)
        if "网络异常" in status:
            logger.info("网络异常，重试一次")
            driver.refresh()
            time.sleep(3)
            sign_button = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[7]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]'))
            )
            logger.info(f"按钮文本: {button_text}")
            status = click_sign_button(driver, sign_button)

        return status
    except Exception as e:
        logger.error(f"状态检查失败: {str(e)}")
        return f"错误: {str(e)}"

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.binary_location = "/usr/bin/chromium-browser"
    
    driver = webdriver.Chrome(options=options)
    try:
        # 加载 Cookie（参考之前的代码）
        load_cookies(driver)
        
        # 检查领取状态并执行
        status = check_sign_status(driver)
        logger.info(status)
        
        # 如果已领取或失败，发送邮件
        if "[Success]" in status or "[Fail]" in status:
            send_email(status)
            
    except Exception as e:
        logger.error(f"主流程错误: {str(e)}")
        send_email(f"脚本运行异常: {str(e)}")
        exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()