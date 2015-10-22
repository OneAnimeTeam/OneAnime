# OneAnime

OneAnime 是 qwe7002 与 deluxghost 开发的一个随机头图（或者其他任何图片）服务器，最初只是为了让访问者看到不一样的博客头图。

## 特性

* 将 `.png` 格式转换为 `.jpg` 格式以节约带宽，提高速度
* 可选的白名单功能，不在白名单上的用户请求会被打上水印

## 安装

OneAnime 由 Python 编写，依赖于 Wand 图像处理库。如果您是在 Ubuntu 操作系统上部署，可以用如下命令安装依赖：

    sudo apt-get install -y python-wand libmagickwand-dev
    
之后，你可以将 OneAnime 克隆到本地：

    git clone https://github.com/qwe7002/OneAnime.git
    
## 设置与运行

您需要编辑 `img.py` 进行一些设置：

    server_info = ('0.0.0.0', 8000) # 服务器的 IP 与端口
    font = './Inconsolata.otf' # 水印字体文件的路径
    watermark = 'OneAnime' # 水印文字
    wl_enable = True # 是否启用白名单

白名单文件是 `whitelist.txt`，每行一个域名，不会自动允许子域名（子域名需要单独列出），例如：

    qwe7002.com
    deluxghost.com
    test.deluxghost.me

配置完成后，启动 Python 解释器即可启动 OneAnime 服务器：

    python img.py
