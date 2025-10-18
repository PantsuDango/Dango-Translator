# 团子翻译器 - 基于OCR的生肉翻译软件


[![最新版本](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC-v6.1.2-ff69b4)](https://github.com/PantsuDango/Dango-Translator)
[![更新时间](https://img.shields.io/badge/%E6%9B%B4%E6%96%B0%E6%97%B6%E9%97%B4-2025--10--18-ff69b4)]()
[![操作系统](https://img.shields.io/badge/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F-win7--11-ff69b4)]()
[![GitHubStars](https://img.shields.io/github/stars/PantsuDango/Dango-Translator)]()
[![GitHubForks](https://img.shields.io/github/forks/PantsuDango/Dango-Translator)]()
[![作者](https://img.shields.io/badge/QQ-%E8%83%96%E6%AC%A1%E5%9B%A2%E5%AD%90-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/%E4%BD%9C%E8%80%85.png)
[![群号](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E4%BA%A4%E6%B5%81%E7%BE%A4-6%E7%BE%A4434137389-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/qrcode_1759602480385.jpg)


## 简介

团子翻译器是一款生肉翻译软件，通过OCR识别屏幕特定范围内的文字，然后将识别到的文字调取各种翻译源，并实时输出翻译结果。

+ 搭载了离线OCR, 项目地址: [DangoOCR](https://github.com/PantsuDango/DangoOCR) 
+ 搭载了在线OCR和漫画OCR, 官网地址: [星河云OCR](https://cloud.stariver.org.cn/auth/login.html)
+ 实现自动模式，实时识别区域内的文本并翻译
+ 配置有常规翻译、在线AI翻译、本地AI翻译
+ 账号系统, 能够自动云端保存配置
+ 另有图片翻译功能, 实现对生肉漫画图片自动识别、翻译、消字、嵌字



## 使用教程

[翻译器使用文档教程](https://dango-docs-v6.ap-sh.starivercs.cn/)

## 安装版下载

- 群文件下载: [![群号](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E4%BA%A4%E6%B5%81%E7%BE%A4-6%E7%BE%A4434137389-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/qrcode_1759602480385.jpg)  
- 官网下载: [下载地址](https://translator.dango.cloud)
- 网盘下载: [夸克网盘](https://pan.quark.cn/s/eb5663a0edf2)
- Github Releases: [v6.1.2](https://dango-static-cm.starivercs.cn/resources/translator/DangoTranslator-v6.1.2-%E7%AE%80%E6%98%93%E7%89%88.exe)

## 更新日志
[![最新版本](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC-v6.1.2-ff69b4)]()
[![更新时间](https://img.shields.io/badge/%E6%9B%B4%E6%96%B0%E6%97%B6%E9%97%B4-2025--10--18-ff69b4)]()

版本号：6.1.2
#### 更新时间 2025/10/18
1. 修复点击翻译框工具栏的分开/覆盖按钮会导致软件崩溃的问题;      

#### 版本号：6.1.1
#### 更新时间 2025/10/17

1. 在线OCR搭载了更强大的识别模型, 识别能力大大提升;
2. 移除了翻译框和范围框碰撞提示;
3. 优化了翻译框界面, 将语种选择和贴图模式放置翻译框界面;
4. 优化了贴图(覆盖)译文的各种效果;
5. 修复本地ocr、朗读等下载时会失败的问题;
6. 翻译框高度新增支持不自动随文本改变;
7. 漫画翻译新增高质量消除模型, 可在设置里开启;
8. 还优化修复各种已知问题; 


## 原理说明

### 实时翻译
![原理说明](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/%E6%B5%81%E7%A8%8B%E5%9B%BE.png)
### 图片翻译
![原理说明](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver6.0.0/manga.png)


## 特别鸣谢

[PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)  在线&本地OCR均基于此框架搭建

[QPT打包工具](https://github.com/GT-ZhangAcer/QPT)  本地OCR基于此工具打包

[GT-Zhang](https://github.com/GT-ZhangAcer) 在线&本地OCR开发过程给予了诸多帮助

[C4a15Wh](https://c4a15wh.cn) 在线OCR, 星河云架构开发

[Cypas_Nya](https://blog.ayano.top) 在线教程文档, 星河云开发

[艾梦](https://github.com/HighCWu) 漫画翻译/在线OCR, 星河云模型开发


## 软件预览

#### 使用效果
![游戏实时翻译](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.3.6/%E4%BD%BF%E7%94%A8%E6%95%88%E6%9E%9C.png)
![漫画翻译](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver6.0.0/manga3.jpg)

#### 快速上手
![实时翻译](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver6.0.3/%E5%AE%9E%E6%97%B6%E7%BF%BB%E8%AF%91.png)
![漫画翻译](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver6.0.3/%E6%BC%AB%E7%94%BB%E7%BF%BB%E8%AF%91.png)

#### 登录界面
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver6.0.0/login.jpg" width="50%" height="50%">
#### 主界面
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver6.0.0/mode.jpg" width="50%" height="50%">

#### 漫画翻译
![原图](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver6.0.0/manga1.jpg)
![编辑](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver6.0.0/manga2.jpg)
![译图](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver6.0.0/manga3.jpg)

#### 设置界面
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver6.0.0/setting1.jpg" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver6.0.0/setting2.jpg" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver6.0.0/setting3.png" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver6.0.0/setting4.png" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.3.6/%E5%A4%9A%E8%8C%83%E5%9B%B4%E5%88%87%E6%8D%A2.png" width="30%" height="30%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver5.2.2/text_lib.png" width="30%" height="30%">

## 开源协议
本项目使用GNU LESSER GENERAL PUBLIC LICENSE(LGPL)开源协议
