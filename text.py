# -*- coding: UTF-8 -*-#
import zipfile

import pywget as wget
import shutil
import os

url = 'http://182.92.66.60:45015/down/aV9E2zTCj2oS?fname=/ErBaDao_Tool_Maya.zip'
scriptPath = r"C:\Users\Alan\Downloads\ls\haha"
filePath = r"C:\Users\Alan\Downloads\ls"
fileName = filePath + r'\ErBaDao_Tool_Maya.zip'
if os.path.exists(fileName):
    os.remove(fileName)
    print ('正在下载中请稍等')
    wget.download(url, filePath)
    print('下载完成')
    print(fileName)
else:
    print ('正在下载中请稍等')
    wget.download(url, filePath)
    print('下载完成')
    print(fileName)

if os.path.exists(scriptPath + r"\ErBaDao_Tool_Maya"):
    shutil.rmtree(scriptPath + r"\ErBaDao_Tool_Maya")
    zip = zipfile.ZipFile(fileName)
    zip.extractall(scriptPath)
    zip.close()
    print ("插件更新完成")

