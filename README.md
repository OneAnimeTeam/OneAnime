# OneAnime

OneAnime is a random picture server, the original purpose is to allow visitors to see different blog headlines.

## Why use OneAnime

* Convert the `jeg` `png` format to`.webp` format, save bandwidth and your disk space.
* Single file design, more compact and lightweight. Out of the box to use.

## Install the required environment

OneAnime is written in Python3 and relies on the PIL image processing library.

You can clone OneAnime to local:

```shell
git clone https://github.com/qwe7002/OneAnime.git
```

After that, install the graphics support library:

```shell
pip3 install Pillow
```

## Configure your server

You need to write your `config.json` according to `config.example.json` . Remember, json does not allow the presence of annotations!

```
{
  "server": "0.0.0.0", #Server listening address, 0.0.0.0 to accept all requests received by native IP
  "port": 8080, #Server listening port
  "location": "./image" #Image file storage location, it is recommended that you save the image folder to upgrade when the normal `git pull`
}
```

You can place the image in the directory you specified, only need to access the correct address when requested. For example, if you put the image in the `image / photos` directory, you can request` / photos' directly.

Once the configuration is complete, start your interpreter to start the OneAnime server:
```shell
python3 oneanime.py
```

## Keep running and monitor your blog

In order to avoid each update, the program error to bring you the trouble. SmartBlog strongly recommends that you use NodeJS-based monitoring programs: PM2

For more information about PM2 installation, please see [How To Install Node.js on Ubuntu 16.04 | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-16-04) and [PM2 - Quick Start](http://pm2.keymetrics.io/docs/usage/quick-start/)

Then you just need to run

```shell
pm2 start oneanime.py
```

It can be achieved in the update file or program error, automatically restart SmartBlog.

You can also use it

```shell
pm2 startup
pm2 save
```

So that your SmartBlog can start automatically when the system is powered on