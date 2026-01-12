import os
import requests
import json
import sys
import time

# 从环境变量获取配置
APP_ID = os.environ.get('WECHAT_APP_ID')
APP_SECRET = os.environ.get('WECHAT_APP_SECRET')

# 文件列表，预计通过命令行参数传入，空格分隔
# 例如: python sync_to_wechat.py "blog/2026-01/image1.jpg blog/2026-01/image2.png"
if len(sys.argv) > 1:
    IMAGES_LIST = sys.argv[1].split()
else:
    IMAGES_LIST = []

def get_access_token():
    """
    获取微信 Access Token
    简单实现：不持久化缓存，每次运行获取一次（GitHub Action 频率不高，通常不会超限）
    如果需要更严谨，可以将 token 写入本地文件并判断过期时间
    """
    if not APP_ID or not APP_SECRET:
        print("❌ 错误：未配置 WECHAT_APP_ID 或 WECHAT_APP_SECRET")
        return None

    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    try:
        res = requests.get(url, timeout=10)
        data = res.json()
        if 'access_token' in data:
            return data['access_token']
        else:
            print(f"❌ 获取 Access Token 失败: {data}")
            return None
    except Exception as e:
        print(f"❌ 网络请求异常: {e}")
        return None

def upload_image(token, file_path):
    """
    上传图片到微信永久素材库
    """
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    
    # 微信接口限制
    # 1. 2M 以内
    # 2. bmp/png/jpeg/jpg/gif
    
    file_name = os.path.basename(file_path)
    # 使用完整路径作为 Title，方便后续搜索识别 (微信可能不支持斜杠，替换为下划线)
    title = file_path.replace("/", "_")
    
    try:
        with open(file_path, 'rb') as f:
            files = {'media': (file_name, f)}
            # 永久素材不需要 ID (临时素材需要)，但永久图文素材需要。
            # add_material 对于 image 类型，不需要 description。但为了保险或者如果接口变动，
            # 我们可以尝试传，或者对于非 video 类型不传 description 参数通常也可以。
            # 官方文档：如果是图片（image）、语音（voice）、视频（video）类型，参数不同。
            # 图片仅需 access_token, type, media.
            # 视频需要 description.
            
            # 这里是上传图片作为“永久素材”，通常不需要 description，直接 POST 即可
            res = requests.post(url, files=files, timeout=30)
            return res.json()
    except Exception as e:
        return {"errcode": -1, "errmsg": str(e)}

def main():
    print(">>> [WeChat Sync] 开始同步图片到微信公众号...")
    
    if not IMAGES_LIST:
        print(">>> [WeChat Sync] 没有接收到需要同步的文件列表，退出。")
        return

    token = get_access_token()
    if not token:
        sys.exit(1)

    success_count = 0
    fail_count = 0

    for img_path in IMAGES_LIST:
        if not os.path.exists(img_path):
            print(f"⚠️ 文件不存在，跳过: {img_path}")
            continue

        print(f">>> 正在同步: {img_path}")
        result = upload_image(token, img_path)
        
        if 'media_id' in result:
            print(f"✅ 同步成功! MediaID: {result['media_id']} (URL: {result.get('url', 'N/A')})")
            success_count += 1
        else:
            print(f"❌ 同步失败: {result}")
            fail_count += 1
        
        # 简单限流，防止触发频率限制
        time.sleep(1)

    print(f">>> [WeChat Sync] 完成。成功: {success_count}, 失败: {fail_count}")

if __name__ == "__main__":
    main()
