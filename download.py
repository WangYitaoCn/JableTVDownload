import requests
import os
import re
import urllib.request
import m3u8
from Crypto.Cipher import AES
from selenium.webdriver.common.by import By

from config import headers
from crawler import prepareCrawl
from merge import mergeMp4
from delete import deleteM3u8, deleteMp4
from cover import getCover
from encode import ffmpegEncode
from args import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import ssl


def download(url, output_folder, _encode=1, _action='y'):
    # 创建一个自定义的 SSL 上下文，忽略证书验证
    ssl_context = ssl._create_unverified_context()
    # encode = 0  # 不转档
    # action = input('要转档吗?[y/n]')
    encode = _encode
    action = _action
    # if action.lower() == 'y':
    #     # action = input('选择转档方案[1:仅转换格式(默认,推荐) 2:NVIDIA GPU 转档 3:CPU 转档]')
    #     if action == '2':
    #         encode = 2  # GPU 转档
    #     elif action == '3':
    #         encode = 3  # CPU 转档
    #     else:
    #         encode = 1  # 快速无损转档

    print('正在下载影片: ' + url)
    # 建立番号资料夹
    urlSplit = url.split('/')
    dirName = urlSplit[-2]
    if os.path.exists(f'{output_folder}/{dirName}/{dirName}.mp4'):
        print('番号资料夹已存在, 跳过...')
        return
    if not os.path.exists(f'{output_folder}/{dirName}'):
        os.makedirs(f'{output_folder}/{dirName}')
    folderPath = os.path.join(output_folder, dirName)

    # 配置 Selenium 参数
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--headless')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")

    # 创建 webdriver 实例
    dr = webdriver.Chrome(options=options)
    dr.get(url)
    # 使用 BeautifulSoup 解析网页内容
    soup = BeautifulSoup(dr.page_source, 'html.parser')
    # 查找所有 <h4> 标签
    h4_tags = soup.find_all('h4')
    title = h4_tags[0].text
    print(title)


    result = re.search("https://.+m3u8", dr.page_source)
    print(f'result: {result}')
    m3u8url = result[0]
    print(f'm3u8url: {m3u8url}')

    # 得到 m3u8 地址
    m3u8urlList = m3u8url.split('/')
    m3u8urlList.pop(-1)
    downloadurl = '/'.join(m3u8urlList)

    # 保存 m3u8 文件至资料夹
    m3u8file = os.path.join(folderPath, dirName + '.m3u8')
    with urllib.request.urlopen(m3u8url, context=ssl_context) as response:
        with open(m3u8file, 'wb') as out_file:
            out_file.write(response.read())

    # 得到 m3u8 文件中的 URI 和 IV
    m3u8obj = m3u8.load(m3u8file)
    m3u8uri = ''
    m3u8iv = ''

    for key in m3u8obj.keys:
        if key:
            m3u8uri = key.uri
            m3u8iv = key.iv

    # 保存 ts 地址到 tsList
    tsList = []
    for seg in m3u8obj.segments:
        tsUrl = downloadurl + '/' + seg.uri
        tsList.append(tsUrl)

    # 有加密
    if m3u8uri:
        m3u8keyurl = downloadurl + '/' + m3u8uri  # 得到 key 的地址
        # 得到 key 的内容
        response = requests.get(m3u8keyurl, headers=headers, timeout=10)
        contentKey = response.content

        vt = m3u8iv.replace("0x", "")[:16].encode()  # IV 取前 16 位

        ci = AES.new(contentKey, AES.MODE_CBC, vt)  # 构造解码器
    else:
        ci = ''

    # 删除 m3u8 文件
    deleteM3u8(folderPath)

    # 开始爬虫并下载 mp4 片段至资料夹
    prepareCrawl(ci, folderPath, tsList)

    # 合成 mp4
    mergeMp4(folderPath, tsList)

    # 删除子 mp4
    deleteMp4(folderPath)

    # 获取封面
    getCover(html_file=dr.page_source, folder_path=folderPath)

    # 转档
    ffmpegEncode(folderPath, dirName, title ,encode)