---
title: arcfutil.aff.easing
language: zh-CN
---

# `arcfutil.aff.easing`

## `bezier()`

将百分比形式的变换进度映射到贝塞尔曲线。

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|percent||百分比进度（小数形式）|
|p1x|float|控制点1的x坐标|1/3|
|p1y|float|控制点1的y坐标|0|
|p2x|float|控制点2的x坐标|2/3|
|p2y|float|控制点2的y坐标|1|

### 返回值

`(float)`变换后的进度。

## `cosine()`

将百分比形式的变换进度映射到余弦曲线。

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|percent||百分比进度（小数形式）|

### 返回值

变换后的进度。

## `get_ease()`

将百分比形式的变换进度按照给定的曲线变换。

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|percent|float|百分比进度（小数形式）|
|type|str|变换类型，支持`s|si|so|b`以及easings.net中的easing，例如`ease_in_sine`|
|b_point|list|贝塞尔曲线控制点，参数`type`为`b`时生效|[1/3, 0, 2/3, 1]|

### 返回值

变换后的进度。

## `get_easing_func()`

给定一个字符串，返回对应的缓动函数。

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|type|str|变换类型，支持`s|si|so|b`以及easings.net中的easing，例如`ease_in_sine`|
|b_point|list|贝塞尔曲线控制点，参数`type`为`b`时生效|[1/3, 0, 2/3, 1]|

### 返回值

`(Callable)`返回的缓动函数。

## `linear()`

将百分比形式的变换进度映射到直线。这个函数会返回原值。

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|percent||百分比进度（小数形式）|

### 返回值

`(float)`变换后的进度。

## `slicer()`

获取曲线在特定时点下于某个方向上的取得的坐标。

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|time||切片时间点|
|fromtime||曲线起始时间点|
|totime||曲线终止时间点|
|fromposition||曲线起始位置|
|toposition||曲线终止位置|
|easingtype||缓动类型，支持`s|si|so|b`/缓动函数|s|

### 返回值

映射得到的坐标位置。

## `sine()`

将百分比形式的变换进度映射到正弦曲线。

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|percent||百分比进度（小数形式）|

### 返回值

变换后的进度。

# `arcfutil.aff.easing.cheatsheet`

预置缓动函数，提供t[0,1]->x[0,1]的映射，详见[easings.net](https://easings.net/)。
