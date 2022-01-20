---
title: 命令行工具
language: zh-CN
---

# 命令行工具

本节将介绍arcfutil提供的几个使用的CLI工具，它们被设计用于批量处理Arcaea相关的文件。

您的包管理工具应当自动创建这些CLI工具的二进制文件并处理环境变量，使得您在安装了arcfutil的Python环境下能够直接使用这些工具。如果环境变量没有被正确配置，pip在安装完毕可能会产生以下提示：

```
WARNING: The scripts arcadeclean, arcfutil, songlist and sortassets are installed in '/home/direwolf/.local/bin' which is not on PATH.
Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```

此时需要您手动将引号内的路径添加进环境变量，具体方法根据您使用的操作系统而有所不同。

当然，通过`python3`命令直接运行这些工具对应的.py模块也是可行的。

## arcadeclean

`arcadeclean`命令用于清理Arcade（或者其衍生版本）在谱面文件夹下产生的自动保存文件和备份文件。

在默认情况下，arcadeclean扫描当前的工作目录。如果想指定一个目录，则将目录作为参数传入：

```bash
arcadeclean ~/path/to/your/charts/
```

## sortassets

如果您查看过Arcaea的下载资源文件，则应该会注意到它们不太方便被可视化制谱器读取。`sortassets`命令可以将这些文件整理成方便被读取的形式。这个命令接受一个`-d`参数，指向您想要整理的/dl/文件夹:

```bash
sortassets -d ~/arcaea_output/blahblah/dl/
```

## songlist

::: warning 注意
这是一个过时的模块。其中一些内容可能已经不再适用于当前版本的Arcaea。
:::

`songlist`命令提供在songlist和songconfig.txt之间互相转换的功能。songconfig.txt是一种不受官方支持的，描述曲目信息的配置文件。它接受Arcaea资源文件夹作为必选参数（通常，这个文件夹内包含song，img等文件夹）。

同时，这个命令还给出了几个开关：

- `-r`: 读取songlist，并为每个曲目创建songconfig.txt

- `-p`: 自动建立packlist文件

- `-b`: 自动检查并复制背景文件

- `-t`: 在songlist中追加id为tempestissimo的曲目

假设有以下的目录结构。

```
 .
 ├- assets
 |     ├- img
 |     |   ├- bg
 |     |   └- ...
 |     ├- song
 |     |   ├- song1
 |     |   ├- song2
 |     |   └- ...
 |     └- ...
 └- ...
```
要创建songlist及自动处理所有文件：

``` sh
songlist -pbt ./assets/
```

要从songlist创建songconfig.txt：

```sh
songlist -r ./assets/
```