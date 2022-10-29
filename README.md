# 团子翻译器 - 基于OCR的生肉翻译软件


[![最新版本](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC-Ver4.3.2-ff69b4)](https://github.com/PantsuDango/Dango-Translator)
[![更新时间](https://img.shields.io/badge/%E6%9B%B4%E6%96%B0%E6%97%B6%E9%97%B4-2022--10--30-ff69b4)]()
[![更新时间](https://img.shields.io/badge/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F-win7--10-ff69b4)]()
[![GitHubStars](https://img.shields.io/github/stars/PantsuDango/Dango-Translator)]()
[![GitHubForks](https://img.shields.io/github/forks/PantsuDango/Dango-Translator)]()
[![作者](https://img.shields.io/badge/QQ-%E8%83%96%E6%AC%A1%E5%9B%A2%E5%AD%90-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/%E4%BD%9C%E8%80%85.png)
[![群号](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E4%BA%A4%E6%B5%81%E7%BE%A4-16%E7%BE%A432523865-ff69b4)](https://l2.drive.c4a15wh.cn/api/v3/slave/source/0/dXBsb2Fkcy8yMDIyLzEwLzI4L0VkWWVtZUdKX-WbouWtkOe_u-ivkeWZqDE2576k576k6IGK5LqM57u056CBLnBuZw/%E5%9B%A2%E5%AD%90%E7%BF%BB%E8%AF%91%E5%99%A816%E7%BE%A4%E7%BE%A4%E8%81%8A%E4%BA%8C%E7%BB%B4%E7%A0%81.png?sign=bxQ3shRTcsdgTs91-5vEnrVMJI-ryZWEeZNAN7rzPC0%3D%3A0)

  
## 简介
> 因安装包文件过大，软件下载请前往[团子翻译器官网](https://translator.dango.cloud)进行下载，新版本不再发布github Releases


团子翻译器是一款生肉翻译软件，通过OCR识别屏幕特定范围内的文字，然后将识别到的文字调取各大厂的翻译，并输出翻译结果。

+ 搭载了离线OCR，项目地址：[DangoOCR](https://github.com/PantsuDango/DangoOCR) 
+ 搭载了在线OCR，官网地址：[星河云OCR](https://cloud.stariver.org/auth/login.html)
+ 实现自动模式，循环识别区域内的文本并翻译
+ 配置了9种翻译源
+ 账号系统，能够自动云端保存配置


  
## 安装版下载

- 群文件下载：[![群号](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E4%BA%A4%E6%B5%81%E7%BE%A4-16%E7%BE%A432523865-ff69b4)](https://l2.drive.c4a15wh.cn/api/v3/slave/source/0/dXBsb2Fkcy8yMDIyLzEwLzI4L0VkWWVtZUdKX-WbouWtkOe_u-ivkeWZqDE2576k576k6IGK5LqM57u056CBLnBuZw/%E5%9B%A2%E5%AD%90%E7%BF%BB%E8%AF%91%E5%99%A816%E7%BE%A4%E7%BE%A4%E8%81%8A%E4%BA%8C%E7%BB%B4%E7%A0%81.png?sign=bxQ3shRTcsdgTs91-5vEnrVMJI-ryZWEeZNAN7rzPC0%3D%3A0)  
- 官网下载：[下载地址](https://translator.dango.cloud)

  
## 更新日志

#### 翻译器相关 

[![最新版本](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC-Ver4.3.2-ff69b4)]()
[![更新时间](https://img.shields.io/badge/%E6%9B%B4%E6%96%B0%E6%97%B6%E9%97%B4-2022--10--30-ff69b4)]()

发现新版本，版本号：4.3.2
2022/10/30  更新内容:

+ 修复了公共翻译的各种问题, 优化其使用  
+ 删除了公共goole翻译, 添加公共bing翻译  
+ 截取范围功能现在支持多屏操作了  
+ 新增了程序启动图标  
+ 修复设置页面侧边栏高度不齐  
+ 文字方向开关在所有ocr页签下都显示    
+ 更多更新日志：[查看](https://docs1.ayano.top/#/4.0/develop/changelog)  

#### OCR相关

[![最新版本](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC-Ver1.2-ff69b4)]()
[![更新时间](https://img.shields.io/badge/%E6%9B%B4%E6%96%B0%E6%97%B6%E9%97%B4-2021--08--19-ff69b4)]()

+ 优化了识别速度和识别质量;
+ 优化了对个别环境的适配问题

+ 更多更新日志：[查看](https://docs1.ayano.top/#/4.0/develop/changelog)  

  
## 使用教程

[翻译器使用文档教程](https://docs1.ayano.top)

  
## 原理说明

![](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/%E6%B5%81%E7%A8%8B%E5%9B%BE.png)


  
## 更新计划

#### 新增项

- [x] 升级Ver4.0，全新的界面设计，更舒服的交互
- [x] 加入DeepL 翻译
- [ ] 离线OCR加入GPU模式
- [x] 加入云服务在线OCR（收费）
- [ ] 加入自定义OCR API接口功能，可以自由添加想要的OCR API接口（需要略懂开发）

#### 优化项

- [x] 优化公共翻译和网页翻译，提高翻译质量，降低抽风率
- [ ] 离线OCR取消黑窗，加入简单的GUI界面，最小化从任务栏改为系统托盘
- [x] 对屏幕缩放比例175%以上做适配
- [x] 离线OCR加入竖排文本检测模式用于翻译生肉本

#### 修复项

- [x] 修复快捷键会失效的问题
- [x] 修复手动模式下，程序概率卡死的问题
- [x] 修复多屏模式下，副屏幕无法截图的问题

  
 ## 特别鸣谢

[PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)  离线OCR基于此框架搭建

[QPT打包工具](https://github.com/GT-ZhangAcer/QPT)  离线OCR基于此工具打包

[GT-Zhang](https://github.com/GT-ZhangAcer) 离线OCR开发过程给予了诸多帮助的大佬

[C4a15Wh](https://c4a15wh.cn) 星团云在线OCR主力开发

[Cypas_Nya](https://blog.ayano.top) 在线教程文档、团子云盘搭建者

  
## 软件预览

#### 使用效果

![](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/%E4%BD%BF%E7%94%A8%E6%95%88%E6%9E%9C.png)

#### 登录界面
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.0/%E7%99%BB%E5%BD%95.png" width="50%" height="50%">

#### 主界面

![](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.0/%E4%B8%BB%E7%95%8C%E9%9D%A2.png)

#### 设置界面
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.0/OCR%E8%AE%BE%E5%AE%9A.png" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.0/%E7%BF%BB%E8%AF%91%E6%BA%90%E8%AE%BE%E5%AE%9A.png" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.0/%E5%85%B6%E4%BB%96%E8%AE%BE%E5%AE%9A.png" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.0/%E5%85%B3%E4%BA%8E.png" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.0/%E5%B1%8F%E8%94%BD%E8%AF%8D%E8%AE%BE%E7%BD%AE.png" width="50%" height="50%">

#### 支持作者
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.0/%E6%94%AF%E6%8C%81%E4%BD%9C%E8%80%85.png" width="100%" height="100%">


## 开源协议

本项目使用GNU LESSER GENERAL PUBLIC LICENSE(LGPL)开源协议
