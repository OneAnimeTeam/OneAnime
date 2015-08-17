#什么是 OneAnime？

OneAnime 为 Qwe7002开发的一个随机头图（也可以随机任何图片）服务器。使用 Python 制作。初衷只是想让访客看到不一样的头图。本程序采用自建 Http 服务器的设计。

#如何安装

首先你需要安装Wand扩展，使用 JPG 格式可以节约流量带宽和提高加载速度。

pip install wand

您需要安装以下支持：

apt-get install libmagickwand-dev

接着，打开 Screen 或者其他终端,运行Python img.py,访问设定的端口即可。

#白名单
为了防止滥用,OneAnime 提供了白名单功能，您可以编辑 Whitelist.txt 文件来实现对访客的过滤（未在白名单的用户访问会被打上 OneAnime 的标志,您也可以修改代码的29行改成你喜欢的名字）
## 授权协议
采用MIT协议分发

>Copyright (C) <year> <copyright holders>

>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.