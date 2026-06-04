# 团子翻译器 - 基于OCR的生肉翻译软件


[![最新版本](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC-v6.3.0-ff69b4)](https://github.com/PantsuDango/Dango-Translator)
[![更新时间](https://img.shields.io/badge/%E6%9B%B4%E6%96%B0%E6%97%B6%E9%97%B4-2026--06--04-ff69b4)]()
[![操作系统](https://img.shields.io/badge/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F-win7--11-ff69b4)]()
[![GitHubStars](https://img.shields.io/github/stars/PantsuDango/Dango-Translator)]()
[![GitHubForks](https://img.shields.io/github/forks/PantsuDango/Dango-Translator)]()
[![作者](https://img.shields.io/badge/QQ-%E8%83%96%E6%AC%A1%E5%9B%A2%E5%AD%90-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/%E4%BD%9C%E8%80%85.png)
[![群号](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E4%BA%A4%E6%B5%81%E7%BE%A4-6%E7%BE%A4434137389-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/qrcode_1759602480385.jpg)


## 简介

团子翻译器是一款生肉翻译软件，通过OCR识别屏幕特定范围内的文字，然后将识别到的文字调取各种翻译源，并实时输出翻译结果。

+ 搭载了离线OCR, 项目地址: [DangoOCR](https://github.com/PantsuDango/DangoOCR) 
+ 搭载了在线OCR和漫画OCR, 官网地址: [星河云OCR](https://dashboard.stariver.org.cn/)
+ 实现自动模式，实时识别区域内的文本并翻译
+ 配置有常规翻译、在线AI翻译、本地AI翻译
+ 账号系统, 能够自动云端保存配置
+ 另有图片翻译功能, 实现对生肉漫画图片自动识别、翻译、消字、嵌字


## 仓库代码维护说明

自 4.5.8 版本后, 团子翻译器换成了 Golang 完全重构了，因为完全换语言重写了，因此 Python 版本的代码不再更新。
为了方便大家下载最新版本，此仓库还是会正常在首页说明里更新版本信息。
如您有 Golang 版本的开发需求，可通过交流群直接与我沟通联系。


## 使用教程

[翻译器使用文档教程](https://dango-docs.ap-sh.starivercs.cn/)

## 安装版下载

- 群文件下载: [![群号](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E4%BA%A4%E6%B5%81%E7%BE%A4-6%E7%BE%A4434137389-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/qrcode_1759602480385.jpg)  
- 官网下载: [下载地址](https://translator.dango.cloud)
- 网盘下载: [夸克网盘](https://pan.quark.cn/s/eb5663a0edf2)
- Github Releases: [v6.3.0](https://github.com/PantsuDango/Dango-Translator/releases/tag/Ver6.3.0)

## 更新日志
[![最新版本](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC-v6.3.0-ff69b4)]()
[![更新时间](https://img.shields.io/badge/%E6%9B%B4%E6%96%B0%E6%97%B6%E9%97%B4-2026--06--04-ff69b4)]()

版本号：6.3.0
#### 更新时间 2026/06/04
##### 实时翻译
- 优化在全屏独占游戏下的置顶翻译器的逻辑, 现在更稳定了;
- 新增支持开启多个范围框, 同时识别和翻译;

##### 漫画翻译
- 样式模版最大数新增至100, 避免不够用;
- 手动添加文本块时, 空白文本块字体大小调整为基于全局样式里的字体大小;
- 搜索页面, 新增基于搜索结果的全部重新翻译, 可以用于替换原文后重新刷新翻译;
- 漫画识别和渲染的超时, 由180s调整为60s, 避免超时等待太长时间都不会退出;
- 词库界面, 每次新增屏蔽词后, 滚动条自动滑到最底部;
- 修复连点文本框样式页的重新贴字按钮会闪退的问题;
- 修复手动识别时, 如果框了一个很小的区域, 会错误贴图的问题;
- 修复通过系统托盘的退出键退出软件, 配置保存不全的问题;
- 导出译图现在自动记录上一次选择的导出目录;
- 修复在图片边缘粘贴文本块会失效的问题;
- 优化通过鼠标滚动缩放文本块大小的逻辑, 现在可以连续滚动至合适大小后再统一执行渲染, 不会再滚动一次执行一次;
- 原图导入和译图导出, 现在新支持了PDF文件;
- 修复手动擦除会重置笔刷填涂操作记录的问题;
- 优化了翻译进度条在折叠状态下显示的信息, 现在会把成功和失败也一并显示;
- 图片列表框、样式编辑框, 现在支持折叠了;
- 优化图片的缩放、拖拽交互;
- 笔刷填涂的交互方式改为了后触发, 和手动擦除类似;
- 全局、文本框编辑样式, 字体色和轮廓色新增最近颜色功能, 可以快速切换之前选过的颜色;
- 图片列表框新增支持, 切换图片列表的排序方式;
- 图片列表框支持快捷键全选、多选、快速选中部分图片;
- 复制和粘贴文本框支持快捷键;
- 优化文本框的自由缩放尺寸交互;
##### 全局
- 在线AI翻译源, 现在支持自定义翻译源显示名称;
- 词库支持导入和导出;


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
