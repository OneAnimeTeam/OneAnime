# OneAnime

OneAnime 是一个随机图片服务器，最初目的是为了让访问者看到不一样的博客头图。

## 为什么使用OneAnime

* 将 `jeg` `png` 格式转换为 `.webp` 格式,节约带宽以及您的磁盘空间。
* 单文件设计，更小巧和轻便。开箱即可使用。

## 安装所需要的环境

OneAnime 使用 Python3 编写，依赖于 PIL 图像处理库。

你可以将 OneAnime 克隆到本地：

```shell
git clone https://github.com/qwe7002/OneAnime.git
```

之后，安装图形支持库:

```shell
pip3 install Pillow
```
    
## 配置您的服务器

您需要根据 `config.example.json` 来编写您的 `config.json`。记得，json 并不允许注释的存在！

```
{
  "server":"0.0.0.0", #服务器监听地址，0.0.0.0为接受所有本机IP收到的请求
  "port":8080, #服务器监听端口
  "location":"./image" #图片文件存放地点,建议您存放在image文件夹下以便升级的时候能够正常 `git pull`
}
```

您可以将图片放在您指定的目录下，只需要在请求时访问正确的地址。例如，如果您将图片放在 `image/photos` 目录下，那么直接请求 `/photos` 即可。

配置完成后，启动您的解释器即可启动 OneAnime 服务器：
```shell
    python3 oneanime.py
```

## 持续运行并监控您的 OneAnime

为了避免每次更新，程序错误给您带来的困扰。 OneAnime 强烈推荐您使用基于 NodeJS 的监控程序： PM2

有关PM2的安装请查看 [How To Install Node.js on Ubuntu 16.04 | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-16-04) 和 [PM2 - Quick Start](http://pm2.keymetrics.io/docs/usage/quick-start/)

然后，您只需要运行

```shell
pm2 start oneanime.py
```

就可以实现在更新文件或者程序错误之后，自动重启 OneAnime。

您还可以使用

```shell
pm2 startup
pm2 save
```

使得您的 OneAnime 能够在系统开机的时候，自动启动