# Dango Translator - OCR-Based Raw Translation Software

[![Latest Version](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC-Ver5.4.0-ff69b4)](https://github.com/PantsuDango/Dango-Translator)
[![Last Updated](https://img.shields.io/badge/%E6%9B%B4%E6%96%B0%E6%97%B6%E9%97%B4-2024--09--30-ff69b4)]()
[![Operating System](https://img.shields.io/badge/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F-win7--11-ff69b4)]()
[![GitHub Stars](https://img.shields.io/github/stars/PantsuDango/Dango-Translator)]()
[![GitHub Forks](https://img.shields.io/github/forks/PantsuDango/Dango-Translator)]()
[![Author](https://img.shields.io/badge/QQ-%E8%83%96%E6%AC%A1%E5%9B%A2%E5%AD%90-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/%E4%BD%9C%E8%80%85.png)
[![Group Number](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E4%BA%A4%E6%B5%81%E7%BE%A4-4%E7%BE%A4939840254-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/qrcode_1727856269396.jpg)

## Introduction

Dango Translator is a raw translation software that uses OCR to recognize text within a specific screen area and retrieves translations from various sources, outputting results in real-time.

+ Features offline OCR, project address: [DangoOCR](https://github.com/PantsuDango/DangoOCR) 
+ Offers online OCR and comic OCR, official website: [Star River Cloud OCR](https://cloud.stariver.org.cn/auth/login.html)
+ Implements an automatic mode for real-time text recognition and translation
+ Configured with 15 translation sources
+ Account system for automatically saving configurations to the cloud
+ Includes an image translation feature that automatically recognizes, translates, and edits raw manga images

## User Guide

[Translator User Documentation](https://dango-docs.ap-sh.starivercs.cn/#/5.0/basic/dangotranslator)

## Download

- Group file download: [![Group Number](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E4%BA%A4%E6%B5%81%E7%BE%A4-4%E7%BE%A4939840254-ff69b4)](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/qrcode_1727856269396.jpg)  
- Official website download: [Download Address](https://translator.dango.cloud)
- GitHub Releases: [Ver5.4.0](https://nfd.ap-sh.starivercs.cn/ec/c6c78893701d10a96f9d7f723f078765wXFwpLll)

## Changelog
[![Latest Version](https://img.shields.io/badge/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC-Ver5.4.0-ff69b4)]()
[![Last Updated](https://img.shields.io/badge/%E6%9B%B4%E6%96%B0%E6%97%B6%E9%97%B4-2024--09--30-ff69b4)]()

#### Version: 5.4.0
#### Last Updated: 2024/09/30     

#### Global:
+ Supports phone number registration, login, and password modification;      
+ Optimized icon for modifying translation source colors;      
+ Fixed various known issues...

#### Real-Time Translation:
+ Selected area will be highlighted when capturing range;      
+ Local OCR uses dynamic ports to avoid port conflicts and failures;      

#### Comic Translation:
+ Optimized comic UI aspect ratio issues;      
+ Added super-resolution feature to enhance blurry images before translation;      
+ Added support for batch dragging and importing image files and multiple folders;      
+ Added support for importing images from .txt documents containing image directories;      
+ Added automatic export of translated images upon completion;      
+ Added support for customizing the image format and compression ratio for exported translated images;      
+ Right-click menu in image list supports quick export of single translated images;      
+ Added support for Traditional Chinese as the source language, allowing conversion to Simplified Chinese;      
+ More update logs: [View](https://dango-docs.ap-sh.starivercs.cn/#/5.0/develop/changelog)  

## Principle Explanation

### Real-Time Translation
![Principle Explanation](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/public/%E6%B5%81%E7%A8%8B%E5%9B%BE.png)
### Image Translation
![Principle Explanation](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.5.4/%E6%BC%AB%E7%94%BB%E7%BF%BB%E8%AF%91%E8%AF%B4%E6%98%8E.png)

## Special Thanks

[PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)  Both online and local OCR are built on this framework.

[QPT Packing Tool](https://github.com/GT-ZhangAcer/QPT)  Local OCR is packaged using this tool.

[GT-Zhang](https://github.com/GT-ZhangAcer) Provided substantial help during the development of online and local OCR.

[C4a15Wh](https://c4a15wh.cn) Online OCR, developed under the Star River Cloud framework.

[Cypas_Nya](https://blog.ayano.top) Online tutorial documentation, development of Star River Cloud.

[艾梦](https://github.com/HighCWu) Comic translation/online OCR, development of Star River Cloud models.

## Software Preview

#### Usage Effect
![](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.3.6/%E4%BD%BF%E7%94%A8%E6%95%88%E6%9E%9C.png)

#### Comic Translation
![Initial Interface](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver5.2.2/manga.png)
![Original Image](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver5.2.2/manga1.png)
![Editing](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver5.2.2/manga2.png)
![Translated Image](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver5.2.2/manga3.png)

#### Login Interface
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver5.2.2/login.png" width="50%" height="50%">

#### Main Interface
![](https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver5.2.2/translation.png)

#### Settings Interface
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver5.2.2/setting1.png" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver5.2.2/setting2.png" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver5.2.2/setting3.png" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver5.2.2/setting4.png" width="100%" height="100%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver4.3.6/%E5%A4%9A%E8%8C%83%E5%9B%B4%E5%88%87%E6%8D%A2.png" width="30%" height="30%">
<img src="https://github.com/PantsuDango/ImageHub/blob/master/DangoTranslate/Ver5.2.2/text_lib.png" width="30%" height="30%">

## Open Source License

This project is licensed under the GNU Lesser General Public License (LGPL).