# 团子翻译器 - 基于OCR的生肉翻译软件


[![最新版本](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC-Ver4.5.3-ff69b4)](https://github.com/PantsuDango/Dango-Translator)
[![更新时间](https://img.shields.io/badge/%E6%9B%B4%E6%96%B0%E6%97%B6%E9%97%B4-2023--06--18-ff69b4)]()
[![操作系统](https://img.shields.io/badge/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F-win7--10-ff69b4)]()
[![GitHubStars](https://img.shields.io/github/stars/PantsuDango/Dango-Translator)]()
[![GitHubForks](https://img.shields.io/github/forks/PantsuDango/Dango-Translator)]()
[![作者](https://img.shields.io/badge/QQ-%E8%83%96%E6%AC%A1%E5%9B%A2%E5%AD%90-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/%E4%BD%9C%E8%80%85.png)
[![群号](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E4%BA%A4%E6%B5%81%E7%BE%A4-19%E7%BE%A4691201730-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/19%E7%BE%A4.png)

  
## 简介

团子翻译器是一款生肉翻译软件，通过OCR识别屏幕特定范围内的文字，然后将识别到的文字调取各种翻译源，并实时输出翻译结果。

+ 搭载了离线OCR，项目地址：[DangoOCR](https://github.com/PantsuDango/DangoOCR) 
+ 搭载了在线OCR，官网地址：[星河云OCR](https://cloud.stariver.org.cn/auth/login.html)
+ 实现自动模式，实时识别区域内的文本并翻译
+ 配置了11种翻译源
+ 账号系统，能够自动云端保存配置
+ 另有图片翻译功能, 实现对生肉漫画图片自动识别、翻译、消字、嵌字


## 使用教程

[翻译器使用文档教程](https://dango-docs.ap-sh.starivercs.cn/#/4.0/basic/dangotranslator)

  
## 安装版下载

- 群文件下载：[![群号](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E4%BA%A4%E6%B5%81%E7%BE%A4-19%E7%BE%A4691201730-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/19%E7%BE%A4.png)  
- 官网下载：[下载地址](https://translator.dango.cloud)
- Github Releases：[Ver4.5.2](https://github.com/PantsuDango/Dango-Translator/releases/tag/Ver4.5.2)

  
## 更新日志

#### 翻译器相关 

[![最新版本](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC-Ver4.5.3-ff69b4)]()
[![更新时间](https://img.shields.io/badge/%E6%9B%B4%E6%96%B0%E6%97%B6%E9%97%B4-2023--06--18-ff69b4)]()

版本号：4.5.0 - 4.5.3  
更新时间：2023/06/15 - 2023/06/18  
#### 新增 
+ 图片翻译, 支持webp格式的图片
+ 全新上线漫画图片翻译功能, 支持对生肉图片进行识别、抠字、翻译后回填
+ 私人翻译新增团子翻译, 目前完全免费, 可以随便使用
#### 修复
+ 修复在线OCR试用次数查询什么时候都是0
+ 修复开启在线OCR试用后点测试按钮仍然失败
+ 修复图片翻译, 识别文本框可能显示不全问题
+ 修复图片翻译, 导入图片时可能发生崩溃问题
+ 私人团子翻译改为默认关闭
#### 优化 
+ 在翻译框锁定时, 仍可以操作自动/手动模式切换按钮
+ 优化公共翻译失效问题、文字堆叠问题
+ 优化chatgpt翻译, 更新为0613模型

更多更新日志：[查看](https://docs1.ayano.top/#/4.0/develop/changelog)  

#### OCR相关

[![最新版本](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC-Ver4.3.6-ff69b4)]()
[![更新时间](https://img.shields.io/badge/%E6%9B%B4%E6%96%B0%E6%97%B6%E9%97%B4-2022--11--26-ff69b4)]()

+ 添加俄语识别;

+ 更多更新日志：[查看](https://docs1.ayano.top/#/4.0/develop/changelog)  


## 原理说明

![原理说明](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/%E6%B5%81%E7%A8%8B%E5%9B%BE.png)


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
![原图](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.5.0/%E5%8E%9F%E5%9B%BE.png)
![编辑](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.5.0/%E7%BC%96%E8%BE%91.png)
![译图](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.5.0/%E8%AF%91%E5%9B%BE.png)

#### 登录界面
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.3.6/%E7%99%BB%E5%BD%95.png" width="50%" height="50%">

#### 注册界面
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.3.6/%E6%B3%A8%E5%86%8C.png" width="50%" height="50%">

#### 主界面
![](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.3.6/%E7%BF%BB%E8%AF%91%E7%95%8C%E9%9D%A2.png)

#### 设置界面
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.3.6/%E8%AE%BE%E7%BD%AE-%E8%AF%86%E5%88%AB%E8%AE%BE%E5%AE%9A.png" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.3.6/%E8%AE%BE%E7%BD%AE-%E7%BF%BB%E8%AF%91%E8%AE%BE%E5%AE%9A.png" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.3.6/%E8%AE%BE%E7%BD%AE-%E6%98%BE%E7%A4%BA%E8%AE%BE%E5%AE%9A.png" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.3.6/%E8%AE%BE%E7%BD%AE-%E5%8A%9F%E8%83%BD%E8%AE%BE%E5%AE%9A.png" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.3.6/%E8%AE%BE%E7%BD%AE-%E5%85%B3%E4%BA%8E.png" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.3.6/%E5%A4%9A%E8%8C%83%E5%9B%B4%E5%88%87%E6%8D%A2.png" width="50%" height="50%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.3.6/%E5%B1%8F%E8%94%BD%E8%AF%8D.png" width="50%" height="50%">

#### 支持作者
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.3.6/%E8%AE%BE%E7%BD%AE-%E6%94%AF%E6%8C%81%E4%BD%9C%E8%80%85.png" width="100%" height="100%">

## 开源协议
本项目使用GNU LESSER GENERAL PUBLIC LICENSE(LGPL)开源协议
