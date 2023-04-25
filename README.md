# 团子翻译器 - 基于OCR的生肉翻译软件


[![最新版本](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC-Ver4.4.4-ff69b4)](https://github.com/PantsuDango/Dango-Translator)
[![更新时间](https://img.shields.io/badge/%E6%9B%B4%E6%96%B0%E6%97%B6%E9%97%B4-2023--04--25-ff69b4)]()
[![操作系统](https://img.shields.io/badge/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F-win7--10-ff69b4)]()
[![GitHubStars](https://img.shields.io/github/stars/PantsuDango/Dango-Translator)]()
[![GitHubForks](https://img.shields.io/github/forks/PantsuDango/Dango-Translator)]()
[![作者](https://img.shields.io/badge/QQ-%E8%83%96%E6%AC%A1%E5%9B%A2%E5%AD%90-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/%E4%BD%9C%E8%80%85.png)
[![群号](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E4%BA%A4%E6%B5%81%E7%BE%A4-1%E7%BE%A4651351974-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/8%E7%BE%A4.png)

  
## 简介
> 因安装包文件过大，软件下载请前往[团子翻译器官网](https://translator.dango.cloud)进行下载，新版本不再发布github Releases


团子翻译器是一款生肉翻译软件，通过OCR识别屏幕特定范围内的文字，然后将识别到的文字调取各大厂的翻译，并输出翻译结果。

+ 搭载了离线OCR，项目地址：[DangoOCR](https://github.com/PantsuDango/DangoOCR) 
+ 搭载了在线OCR，官网地址：[星河云OCR](https://cloud.stariver.org/auth/login.html)
+ 实现自动模式，循环识别区域内的文本并翻译
+ 配置了10种翻译源
+ 账号系统，能够自动云端保存配置


## 使用教程

[翻译器使用文档教程](https://docs2.ayano.top/#/4.0/basic/start)

  
## 安装版下载

- 群文件下载：[![群号](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E4%BA%A4%E6%B5%81%E7%BE%A4-1%E7%BE%A4651351974-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/8%E7%BE%A4.png)  
- 官网下载：[下载地址](https://translator.dango.cloud)

  
## 更新日志

#### 翻译器相关 

[![最新版本](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC-Ver4.4.4-ff69b4)]()
[![更新时间](https://img.shields.io/badge/%E6%9B%B4%E6%96%B0%E6%97%B6%E9%97%B4-2023--04--25-ff69b4)]()

新增:
+ 私人翻译新增ChatGPT, 需要密钥+代理才可使用;
+ 新增可手动修改原文并刷新翻译功能, 位于翻译框的翻译键右侧新图标使用;
+ 新增翻译框自动记录上一次退出的位置和大小;
+ 在设置页面字体选择时下拉框可预览字体样式, 并且修改字体大小和样式后退出设置会立即生效;
+ 软件启动时范围框也会一起和翻译框显示;      

优化:
+ 修复自动翻译时前后截图相似度对比失效, 该问题会导致不停刷新翻译从而出现'闪烁'现象;
+ 修复公共有道翻译失效问题;
+ 自动登录失败会返回登录界面而不是失败死循环;
+ 一些提示窗口的文本优化;
+ 一些已知问题的优化;       
+ 修复网络错误时翻译器异常报错打不开的问题
 
更多更新日志：[查看](https://docs1.ayano.top/#/4.0/develop/changelog)  

#### OCR相关

[![最新版本](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC-Ver4.3.6-ff69b4)]()
[![更新时间](https://img.shields.io/badge/%E6%9B%B4%E6%96%B0%E6%97%B6%E9%97%B4-2022--11--26-ff69b4)]()

+ 添加俄语识别;

+ 更多更新日志：[查看](https://docs1.ayano.top/#/4.0/develop/changelog)  


## 原理说明

![](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/%E6%B5%81%E7%A8%8B%E5%9B%BE.png)


## 特别鸣谢

[PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)  在线&本地OCR均基于此框架搭建

[QPT打包工具](https://github.com/GT-ZhangAcer/QPT)  本地OCR基于此工具打包

[GT-Zhang](https://github.com/GT-ZhangAcer) 在线&本地OCR开发过程给予了诸多帮助

[C4a15Wh](https://c4a15wh.cn) 在线OCR, 星河云架构开发

[Cypas_Nya](https://blog.ayano.top) 在线教程文档, 星河云开发

  
## 软件预览

#### 使用效果
![](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.3.6/%E4%BD%BF%E7%94%A8%E6%95%88%E6%9E%9C.png)

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
