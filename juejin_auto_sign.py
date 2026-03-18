import os
import requests
import json
import time
import random

def get_juejin_cookie():
    """从 GitHub Secrets 获取 Cookie"""
    cookie = os.getenv('JUEJIN_COOKIE')
    if not cookie:
        raise ValueError("JUEJIN_COOKIE 环境变量未设置")
    return cookie

def sign_in():
    """执行掘金签到（随机延迟0-30分钟）"""
    # 随机延迟0-30分钟（0-1800秒）
    delay_seconds = random.randint(0, 1800)
    print(f"⏳ 正在等待 {delay_seconds // 60} 分钟 {delay_seconds % 60} 秒后签到（避免固定时间触发）")
    time.sleep(delay_seconds)
    
    url = "https://api.juejin.cn/growth_api/v1/check_in?aid=2608&spider=0"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Cookie": get_juejin_cookie(),
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, data="")
        response.raise_for_status()
        result = response.json()
        
        if result.get('code') == 0:
            print(f"✅ 签到成功！获得 {result['data']['reward']} 积分")
            print(f"当前总积分: {result['data']['total']}")
        else:
            print(f"❌ 签到失败: {result.get('message', '未知错误')}")
            if result.get('code') == 401:
                print("⚠️ 请检查 Cookie 是否过期（需更新 GitHub Secrets）")
                
    except Exception as e:
        print(f"🚨 请求异常: {str(e)}")

if __name__ == "__main__":
    print("🚀 掘金自动签到脚本启动...")
    print("⏰ 当前时间: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    sign_in()
    print("⏰ 脚本执行完成（GitHub Actions 将自动记录日志）")
