# OneAnime

OneAnime 是 @qwe7002 与 @deluxghost 开发的一个随机头图（或者其他任何图片）服务器，最初只是为了让访问者看到不一样的博客头图。

## 特性

* 将 `.png` 格式转换为 `.jpg` 格式以节约带宽，提高速度
* 可选的白名单功能，不在白名单上的用户请求会被打上水印

## 安装

OneAnime 由 Python 编写，依赖于 PIL 图像处理库。你可以将 OneAnime 克隆到本地：

    git clone https://github.com/qwe7002/OneAnime.git

之后，
    
## 设置与运行

您需要编辑 `img.py` 进行一些设置：

    server_info = ('0.0.0.0', 8000) # 服务器的 IP 与端口
    font = './Inconsolata.otf' # 水印字体文件的路径
    watermark = 'OneAnime' # 水印文字
    wl_enable = True # 是否启用白名单

您可以将图片放在当前目录或者子目录，只需要在请求时访问正确的地址。例如，如果您将图片放在 `photos` 目录下，就需要请求 `http://example.com:8000/photos`。

配置完成后，启动 Python 解释器即可启动 OneAnime 服务器：

    python3 img.py
