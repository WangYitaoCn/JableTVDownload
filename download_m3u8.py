import urllib.request
import ssl
import os

# 创建一个自定义的 SSL 上下文，忽略证书验证
ssl_context = ssl._create_unverified_context()

# 定义要下载的 m3u8 文件 URL 和保存路径
m3u8url = 'https://ao-block-ater.mushroomtrack.com/bcdn_token=KResNPKqWLju79uW2aBuPEWzj18fJKGalhwdXLXZjMM&expires=1720805783&token_path=%2Fvod%2F/vod/7000/7821/7821.m3u8'
m3u8file = '/Users/yitaowang/Downloads/7821.m3u8'  # 请将此路径替换为你的实际保存路径

# 创建保存目录（如果不存在）
os.makedirs(os.path.dirname(m3u8file), exist_ok=True)

# 使用自定义的 SSL 上下文打开 URL
with urllib.request.urlopen(m3u8url, context=ssl_context) as response:
    with open(m3u8file, 'wb') as out_file:
        out_file.write(response.read())

print(f"文件已成功下载到 {m3u8file}")