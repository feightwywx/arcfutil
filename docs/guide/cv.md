---
title: 图像处理
language: zh-CN
next: false
---

# 图像处理

arcfutil的`cvkit`拓展包提供了一些与图像处理有关的功能。

## 安装

要使用以下功能，需要安装`arcfutil-cvkit`包。

```bash
pip install arcfutil-cvkit
```

如果您还没有安装`arcfutil`或者版本低于0.7.0，这个操作会同时自动安装最新版本的arcfutil。通过源码安装的方法与安装本体相同。

## 图片转黑线

`image_to_arc()`函数可以提取图片中的轮廓，并转换成黑线，只需传入图片路径和时间点。

```python
from arcfutil.cv import image_to_arc as i2a

arcs = i2a(image_path, time)
```
同时，该函数还可以接收两个可选参数：

- `size`: 接收一个带有4个浮点数的列表，控制图片映射的坐标范围（以原点为基准`[上,右,下,左]`）。

- `max_gap`: 指定Hough变换中线之间的最大间隔。过大会导致线之间相连，过小会导致线之间缝隙增大。
