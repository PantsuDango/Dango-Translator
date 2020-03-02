# Dango-Translator Ver1.0 —— 团子翻译器 Ver1.0


### 简单地说明：
个人兴趣制作的一款基于OCR技术的在线游戏翻译器能够实现固定区域截图并识别图片上的文字，然后进行翻译<br/>
主要用于未汉化的galgame游戏，也可用于未汉化的手游、页游甚至没有中文字幕的视频等一切出现在屏幕需要翻译的内容<br/>
OCR调用了百度AI的文字识别接口，翻译方面爬取有道翻译的网页版，百度翻译和腾讯翻译调用了API


### 为什么想制作这个：
本身是个vnr翻译软件的忠实用户，但是遇到某些游戏无法提取文本，并且没有找到有热心人公开发布的特殊码，于是某天<br/>
研究如何提取特殊码研究到了深夜还是失败了。然后发现有OCR（文字识别）技术的存在，下载了很多已经有的OCR翻译器，<br/>
但是使用体验都觉得很不方便，于是萌生了自己制作一个自己喜欢的翻译器的想法


### 目前有的功能：
+ 提取屏幕上指定位置的坐标参数；
+ 通过输入坐标参数实现固定区域截图；
+ 通过文字识别从截图中提取要翻译的游戏文本；
+ 翻译采用公共接口的有道翻译、私人接口的百度翻译和腾讯翻译；
+ 拥有手动和自动两种翻译模式；
+ 能自定义自动翻译时的刷新频率（3-10秒）；
+ 可以自定义是否显示提取到的原文.


### 吐槽：
+ 及其简陋的功能和UI；
+ 过多的本地配置文件；
+ 自动翻译时如果点击按键或拖动软件，会卡顿；
+ 电脑屏幕不是100%时截图会出现莫名其妙的黑边，导致无法识别；
+ 翻译框不可以拉长；
+ 翻译框最右边的文字显示不全；
+ 会出现莫名其妙的弹窗警告；
+ 自动模式下即使画面无变化也会重复调用翻译；
+ 仅支持64位系统和简中的系统区域。


### 效果截图：

![](https://raw.githubusercontent.com/PantsuDango/Dango-Translator/master/git_image/1.png)
![](https://raw.githubusercontent.com/PantsuDango/Dango-Translator/master/git_image/2.png)
![](https://raw.githubusercontent.com/PantsuDango/Dango-Translator/master/git_image/3.png)
![](https://raw.githubusercontent.com/PantsuDango/Dango-Translator/master/git_image/4.png)

