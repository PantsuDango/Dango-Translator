# 团子翻译器 - 基于OCR的生肉翻译软件


[![最新版本](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC-Ver6.0.1-ff69b4)](https://github.com/PantsuDango/Dango-Translator)
[![更新时间](https://img.shields.io/badge/%E6%9B%B4%E6%96%B0%E6%97%B6%E9%97%B4-2025--04--07-ff69b4)]()
[![操作系统](https://img.shields.io/badge/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F-win7--11-ff69b4)]()
[![GitHubStars](https://img.shields.io/github/stars/PantsuDango/Dango-Translator)]()
[![GitHubForks](https://img.shields.io/github/forks/PantsuDango/Dango-Translator)]()
[![作者](https://img.shields.io/badge/QQ-%E8%83%96%E6%AC%A1%E5%9B%A2%E5%AD%90-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/%E4%BD%9C%E8%80%85.png)
[![群号](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E4%BA%A4%E6%B5%81%E7%BE%A4-4%E7%BE%A41036831717-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/qrcode_1740921893259.jpg)


## 简介

团子翻译器是一款生肉翻译软件，通过OCR识别屏幕特定范围内的文字，然后将识别到的文字调取各种翻译源，并实时输出翻译结果。

+ 搭载了离线OCR, 项目地址: [DangoOCR](https://github.com/PantsuDango/DangoOCR) 
+ 搭载了在线OCR和漫画OCR, 官网地址: [星河云OCR](https://cloud.stariver.org.cn/auth/login.html)
+ 实现自动模式，实时识别区域内的文本并翻译
+ 配置了15种翻译源
+ 账号系统, 能够自动云端保存配置
+ 另有图片翻译功能, 实现对生肉漫画图片自动识别、翻译、消字、嵌字



## 使用教程

[翻译器使用文档教程](https://dango-docs.ap-sh.starivercs.cn/#/5.0/basic/dangotranslator)

## 安装版下载

- 群文件下载: [![群号](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E4%BA%A4%E6%B5%81%E7%BE%A4-4%E7%BE%A41036831717-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/qrcode_1740921893259.jpg)  
- 官网下载: [下载地址](https://translator.dango.cloud)
- 网盘系在: [夸克网盘](https://pan.quark.cn/s/eb5663a0edf2)
- Github Releases: [Ver6.0.1](https://nfd.ap-sh.starivercs.cn/ec/bc73f09f0474c59e5045125e3751fa071go)

## 更新日志
[![最新版本](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC-Ver6.0.0-ff69b4)]()
[![更新时间](https://img.shields.io/badge/%E6%9B%B4%E6%96%B0%E6%97%B6%E9%97%B4-2025--03--31-ff69b4)]()

#### 版本号：6.0.1
#### 更新时间 2025/04/07     

#### 全局:
+ 修复了各种可能导致软件闪退的问题
+ 修复词库界面编辑文本的时候, 如果最小化了界面, 会导致编辑的文本消失的问题
+ 修复翻译历史界面, 如果最小化了界面, 再放大需要重新加载数据导致卡顿的问题

#### 实时翻译:
+ 用户未配置就误打开chatgpt的开关, 导致整体翻译耗时过长, 现在加上了开启限制, 需要经过测试通过才可开启

#### 漫画翻译:
+ 界面原本默认全屏, 现在支持自定义缩放尺寸
+ 轮廓颜色样式新增可设置为, 和当前字体色相反
+ 调整了界面上滚动条的颜色, 并加粗
+ 点击译图上的文本块时, 现在滚轮会自动滑到译文编辑的区域, 避免小屏幕用户需要频繁滑动滚轮
+ 手动擦除和笔刷填涂现在笔头改为了圆形
+ 进一步优化了手动擦除和笔刷填涂后的图片质量
+ 修复样式模版操作的时候, 消息提示窗上的模版名称错误的问题
+ 原图和译图下方的缩放比例处, 新增了一组比例的下拉框, 可以快速切换比例的
+ 高级设置-其他一栏里, 新增了翻译环节出错后可设置最大重试次数的功能
+ 优化了原图和译图, 拖拽移动图片的速度, 使其移动更平滑
+ 更多更新日志: [查看](https://dango-docs.ap-sh.starivercs.cn/#/5.0/develop/changelog)  


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
