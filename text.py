# -*- coding: UTF-8 -*-#
import wget
import os


url = 'https://codeload.github.com/dongpingyao/ErBaDao_Tool_UE5/zip/refs/heads/main'
scriptPath = r"C:\Users\Alan\Downloads\ls\haha"
filePath = r"C:\Users\Alan\Downloads\ls"
fileName = filePath + r'\ErBaDao_Tool_Maya.zip'
wget.download(url , filePath , (1024,1920,20))




