import os
import requests
import json
import time
import random
import logging

# 配置详细日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("sign.log"),
        logging.StreamHandler()
    ]
)

def get_juejin_cookie():
    """从 GitHub Secrets 获取 Cookie，并清理换行符"""
    cookie = os.getenv('JUEJIN_COOKIE')
    if not cookie:
        raise ValueError("JUEJIN_COOKIE 环境变量未设置")
    
    # 关键修复：移除Cookie中的换行符
    clean_cookie = cookie.replace('\n', '').replace('\r', '')
    
    logging.info("✅ Cookie 已加载 (清理后长度: %d 字节)", len(clean_cookie))
    return clean_cookie

def sign_in():
    """执行掘金签到（带超时和详细日志）"""
    # 随机延迟0-30分钟（0-1800秒）
    delay_seconds = random.randint(0, 180)
    logging.info("⏳ 正在等待 %d 秒后签到（避免固定时间触发）", delay_seconds)
    time.sleep(delay_seconds)
    
    url = "https://api.juejin.cn/growth_api/v1/check_in?aid=2608&spider=0"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Cookie": get_juejin_cookie(),
        "Content-Type": "application/json"
    }
    
    logging.info("🌐 正在请求: %s", url)
    logging.info("🔍 请求头: %s", headers)
    
    try:
        # 关键修复：添加超时（连接3秒，读取10秒）
        start_time = time.time()
        response = requests.post(
            url, 
            headers=headers, 
            data="", 
            timeout=(3, 10)  # (连接超时, 读取超时)
        )
        elapsed = time.time() - start_time
        logging.info("✅ API 响应成功 (耗时: %.2f秒)", elapsed)
        
        response.raise_for_status()
        result = response.json()
        
        if result.get('code') == 0:
            logging.info("✅ 签到成功！获得 %d 积分", result['data']['reward'])
            logging.info("📊 当前总积分: %d", result['data']['total'])
        else:
            logging.error("❌ 签到失败: %s (code: %d)", result.get('message', '未知错误'), result.get('code', -1))
            if result.get('code') == 401:
                logging.warning("⚠️ Cookie 可能已过期，请更新 GitHub Secrets")
                
    except requests.exceptions.Timeout as e:
        logging.error("🚨 请求超时: %s", str(e))
    except requests.exceptions.RequestException as e:
        logging.error("🚨 网络请求失败: %s", str(e))
    except Exception as e:
        logging.exception("🚨 未处理异常: %s", str(e))

if __name__ == "__main__":
    logging.info("🚀 掘金自动签到脚本启动 (北京时间: %s)", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    sign_in()
    logging.info("⏰ 脚本执行完成 (总耗时: %d 秒)", time.time() - time.time())
