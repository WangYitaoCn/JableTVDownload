# author: hcjohn463
#!/usr/bin/env python
# coding: utf-8
import requests

from args import *
from download import download
from movies import movieLinks
# In[2]:

parser = get_parser()
args = parser.parse_args()
if(len(args.url) != 0):
    url = args.url
    download(url)
elif(args.random == True):
    url = av_recommand()
    download(url)
elif(args.all_urls != ""):
    all_urls = args.all_urls
    urls = movieLinks(all_urls)
    for url in urls:
        download(url)
else:
    # 使用者輸入Jable網址
    url = input('輸入jable網址:')

    output_folder = input('輸入輸出資料夾:')
    if output_folder == "":
        output_folder = '/Users/yitaowang/Downloads/film'

    success = False
    while not success:
        try:
            download(url, output_folder)
            success = True
        except Exception as e:
            print(f"下载 {url} 时遇到意外错误: {e}，重试中...")