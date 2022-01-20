---
title: arcfutil.cv
language: zh-CN
---

# `arcfutil.cv`

::: tip 提示
`arcfutil.cv`不包含在`arcfutil`包中。要使用这些函数，请安装`arcfutil-cvkit`包。
:::

与图像相关的一些工具函数。

## `image_to_arc()`

将图像转换为黑线。

### 原型

`arcfutil.cv.image_to_arc(...) -> NoteGroup`

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|path|str|图片路径|
|time|int|生成黑线的时间点|
|size|list|接收一个带有4个浮点数的列表，控制图片映射的坐标范围（以原点为基准`[上,右,下,左]`）|`[1,1.5,-0.2,-0.5]`|
|max_gap|float|Hough变换中线之间的最大间隔，过大会导致线之间相连，过小会导致线之间缝隙增大|10|

### 返回值

`(NoteGroup)` 生成的Note。
