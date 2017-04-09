# OneAnime

OneAnime 是一个随机图片服务器，最初目的是为了让访问者看到不一样的博客头图。

## 为什么使用OneAnime

* 将 `jeg` `png` 格式转换为 `.webp` 格式,节约带宽以及您的磁盘空间。
* 单文件设计，更小巧和轻便。开箱即可使用。

## 安装所需要的环境

OneAnime 由 Python 编写，依赖于 PIL 图像处理库。

你可以将 OneAnime 克隆到本地：

    git clone https://github.com/qwe7002/OneAnime.git

之后，安装图形支持库:

    pip3 install Pillow
    
## 配置您的服务器

您需要根据 `config.example.json` 来编写您的 `config.json`。记得，json并不允许注释的存在！

{
  "server":"0.0.0.0", #服务器监听地址，0.0.0.0为接受所有本机IP收到的请求
  "port":8080, #服务器监听端口
  "location":"./image" #图片文件存放地点,建议您存放在image文件夹下以便升级的时候能够正常 `git pull`
}

您可以将图片放在您指定的目录下，只需要在请求时访问正确的地址。例如，如果您将图片放在 `image/photos` 目录下，那么直接请求 `/photos` 即可。

配置完成后，启动 Python 解释器即可启动 OneAnime 服务器：

    python3 oneanime.py
    （您也可以使用 ./oneanime.py 来启动服务器）
