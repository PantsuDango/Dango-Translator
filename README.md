# 团子翻译器 - 基于OCR的生肉翻译软件


[![最新版本](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC-Ver4.5.6-ff69b4)](https://github.com/PantsuDango/Dango-Translator)
[![更新时间](https://img.shields.io/badge/%E6%9B%B4%E6%96%B0%E6%97%B6%E9%97%B4-2023--07--13-ff69b4)]()
[![操作系统](https://img.shields.io/badge/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F-win7--11-ff69b4)]()
[![GitHubStars](https://img.shields.io/github/stars/PantsuDango/Dango-Translator)]()
[![GitHubForks](https://img.shields.io/github/forks/PantsuDango/Dango-Translator)]()
[![作者](https://img.shields.io/badge/QQ-%E8%83%96%E6%AC%A1%E5%9B%A2%E5%AD%90-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/%E4%BD%9C%E8%80%85.png)
[![群号](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E4%BA%A4%E6%B5%81%E7%BE%A4-19%E7%BE%A4691201730-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/19%E7%BE%A4.png)

  
## 简介

团子翻译器是一款生肉翻译软件，通过OCR识别屏幕特定范围内的文字，然后将识别到的文字调取各种翻译源，并实时输出翻译结果。

+ 搭载了离线OCR, 项目地址: [DangoOCR](https://github.com/PantsuDango/DangoOCR) 
+ 搭载了在线OCR和漫画OCR, 官网地址: [星河云OCR](https://cloud.stariver.org.cn/auth/login.html)
+ 实现自动模式，实时识别区域内的文本并翻译
+ 配置了12种翻译源
+ 账号系统, 能够自动云端保存配置
+ 另有图片翻译功能, 实现对生肉漫画图片自动识别、翻译、消字、嵌字


## 使用教程
[翻译器使用文档教程](https://dango-docs.ap-sh.starivercs.cn/#/4.0/basic/dangotranslator)

  
## 安装版下载
- 群文件下载: [![群号](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E4%BA%A4%E6%B5%81%E7%BE%A4-19%E7%BE%A4691201730-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/19%E7%BE%A4.png)  
- 官网下载: [下载地址](https://translator.dango.cloud)
- Github Releases: [Ver4.5.6](https://github.com/PantsuDango/Dango-Translator/releases/tag/Ver4.5.6)

  
## 更新日志
### 翻译器相关
[![最新版本](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC-Ver4.5.6-ff69b4)]()
[![更新时间](https://img.shields.io/badge/%E6%9B%B4%E6%96%B0%E6%97%B6%E9%97%B4-2023--07--13-ff69b4)]()

#### 版本号：4.5.6
#### 更新时间 2023/07/13
#### 新增
+ 图片翻译, 高级设置新增文本气泡框合并间隔参数, 可解决不同的文本气泡框错误合并在一起的问题;      
+ 翻译框在锁定状态时, 会应用鼠标穿透效果, 解决游玩游戏时出现误触翻译框问题;      
#### 优化
+ 修复初始化启动时, 设置的字体大小和样式不会生效的问题;      
+ 图片翻译, 修复删除文本框可能出现报错的问题;      
+ 图片翻译, 修复编辑文本框处, 重新翻译时屏蔽词不会生效的问题;      
+  图片翻译, 修复重新翻译后, 编辑/译图列表框的略缩图不会刷新的问题;      
+ 优化了图片翻译-高级设置的UI布局, 优化了设置登录、设置页面的背景图;
+ 
更多更新日志: [查看](https://github.com/PantsuDango/Dango-Translator/releases)  

## 原理说明
### 实时翻译
![原理说明](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/%E6%B5%81%E7%A8%8B%E5%9B%BE.png)
### 图片翻译
![原理说明](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.5.4/%E6%BC%AB%E7%94%BB%E7%BF%BB%E8%AF%91%E8%AF%B4%E6%98%8E.png)

## 特别鸣谢
[PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)  在线&本地OCR均基于此框架搭建

[QPT打包工具](https://github.com/GT-ZhangAcer/QPT)  本地OCR基于此工具打包

[GT-Zhang](https://github.com/GT-ZhangAcer) 在线&本地OCR开发过程给予了诸多帮助

[C4a15Wh](https://c4a15wh.cn) 在线OCR, 星河云架构开发

[Cypas_Nya](https://blog.ayano.top) 在线教程文档, 星河云开发

  
## 软件预览

#### 使用效果
![](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.3.6/%E4%BD%BF%E7%94%A8%E6%95%88%E6%9E%9C.png)

#### 漫画翻译
![原图](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.5.6/manga1.png)
![编辑](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.5.6/manga2.png)
![译图](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.5.6/manga3.png)

#### 登录界面
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.5.6/login1.png" width="50%" height="50%">

#### 注册界面
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.3.6/%E6%B3%A8%E5%86%8C.png" width="50%" height="50%">

#### 主界面
![](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.5.6/translation.png)

#### 设置界面
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.5.6/setting1.png" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.5.6/setting2.png" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.5.6/setting3.png" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.5.6/setting4.png" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.5.6/setting5.png" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.3.6/%E5%A4%9A%E8%8C%83%E5%9B%B4%E5%88%87%E6%8D%A2.png" width="30%" height="30%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.5.6/filter.png" width="30%" height="30%">

#### 支持作者
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.5.6/setting6.png" width="100%" height="100%">

## 开源协议
本项目使用GNU LESSER GENERAL PUBLIC LICENSE(LGPL)开源协议
