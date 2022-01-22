---
title: arcfutil.aff.note
language: zh-CN
---

# `arcfutil.aff.note`

# 类

Note相关类。

::: tip 提示
在目前版本的arcfutil中，引入`arcfutil.aff`时就默认引入了用于表示Note的各种类。
:::

## `AffList`

### 原型

`arcfutil.aff.note.common_note.NoteGroup(list)`

--`arcfutil.aff.note.notegroup.AffList(NoteGroup)`

### 构造函数

|参数名|类型|说明|默认值|
|--|--|--|--|
|notes||接收可迭代对象，或者多个Note对象|
|offset|int|控制AudioOffset|0|
|desnity|float|控制TimingPointDesnityFactor|1|

### 方法

#### `__str__()`

##### 参数

无。

##### 返回值

Note容器内所有Note的Note语句形式字符串。如果`desnity`属性为`1`，则不输出TimingPointDesnityFactor。

#### `align()`

将Note容器内部所有Note对象时间对齐。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|bpm|float|基准bpm|
|error|int|允许的误差|3|
|lcd||需要对齐的细分的最小公倍数|96|

##### 返回值

时间对齐的Note容器。

#### `append()`

向容器中追加Note对象或NoteGroup对象。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|__objects||接收Note或NoteGroup对象|

##### 返回值

`None`

#### `extend()`

将一个Note容器与一个可迭代对象拼接。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|__iterable||接收可迭代对象|

##### 返回值

`None`

#### `mirror()`

将Note容器内部所有Note镜像。

##### 参数

无。

##### 返回值

镜像后的Note容器。

#### `moveto()`

将Note容器整体偏移到一个时间点。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|dest|int|偏移到的时间点|

##### 返回值

偏移后的Note对象。

#### `offsetto()`

将Note容器整体偏移一个毫秒数。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|value|int|偏移的毫秒数|

##### 返回值

偏移后的Note容器。

## `Arc`

### 原型

`arcfutil.aff.note.common_note.Note`

--`arcfutil.aff.note.tap.Tap(Note)`

----`arcfutil.aff.note.tap.Hold(Tap)`

------`arcfutil.aff.note.arc.Arc(Hold)`

### 构造函数

|参数名|类型|说明|默认值|
|--|--|--|--|
|time|int|Note时间点|
|totime|int|Note结束时间点|
|fromx|float|起始点x坐标|
|fromy|float|起始点y坐标|
|tox|float|终点x坐标|
|toy|float|终点y坐标|
|slideeasing|str,Callable, List[Callable]|缓动类型，支持`s|b|si|so`两两组合/缓动函数/两个缓动函数组成的列表|
|color|int|`0`~`2`，分别为蓝，红，绿|
|isskyline|bool|是否为黑线|
|skynote|list|天键时间点列表|`None`|
|fx|str|FX，支持值见`note.validstrings.fxlist`|`None`|


### 方法

##### 返回值

Note的Note语句形式字符串。

#### `__getitem__()`

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|item||数值或切片对象|

##### 返回值

Note容器（切片结果有多个对象）或Note（切片结果仅有一个对象）。

#### `__len__()`

##### 参数

无。

##### 返回值

Note的持续时长。

#### `__str__()`

##### 参数

无。

##### 返回值

Note的Note语句形式字符串。**注意，**只有`slideeasing`值为`note.validstrings.slideeasinglist`中的规定值时才允许返回。

#### `align()`

将Note时间对齐。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|bpm|float|基准bpm|
|error|int|允许的误差|3|
|lcd||需要对齐的细分的最小公倍数|96|

##### 返回值

时间对齐的Note对象。

#### `copy()`

返回Note对象的深拷贝。

##### 参数

无。

##### 返回值

Note对象的深拷贝。

#### `copyto()`

返回移动到某个时间点Note对象的深拷贝。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|dest|int|偏移到的时间点|

##### 返回值

偏移后Note的深拷贝。

#### `mirror()`

将Note镜像。

##### 参数

无。

##### 返回值

镜像后的Note对象。

#### `moveto()`

将Note移动到某个时间点。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|dest|int|偏移到的时间点|

##### 返回值

偏移后的Note对象。

#### `offsetto()`

偏移Note指定的毫秒数。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|value|int|偏移的毫秒数|

##### 返回值

偏移后的Note对象。

#### `transfer()`

##### 参数
|参数名|类型|说明|默认值|
|--|--|--|--|
|x_value|float|x轴偏移量|
|y_value|float|y轴偏移量|

##### 返回值

偏移后的Note对象。

#### `vmirror()`

将Note垂直镜像。

##### 参数

无。

##### 返回值

垂直镜像后的Note对象。

## `Camera`

### 原型

`arcfutil.aff.note.common_note.Note`

--`arcfutil.aff.note.camera.Camera(Note)`

### 构造函数

|参数名|类型|说明|默认值|
|--|--|--|--|
|time|int|Note时间点|
|transverse|float|
|bottomzoom|float|
|linezoom|float|
|steadyangle|float|
|topzoom|float|
|angle|float|
|easing|str|
|lastingtime|int|

### 方法

#### `__str__()`

##### 参数

无。

##### 返回值

Note的Note语句形式字符串。

#### `align()`

将Note时间对齐。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|bpm|float|基准bpm|
|error|int|允许的误差|3|
|lcd||需要对齐的细分的最小公倍数|96|

##### 返回值

时间对齐的Note对象。

#### `copy()`

返回Note对象的深拷贝。

##### 参数

无。

##### 返回值

Note对象的深拷贝。

#### `copyto()`

返回移动到某个时间点Note对象的深拷贝。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|dest|int|偏移到的时间点|

##### 返回值

偏移后Note的深拷贝。

#### `mirror()`

无实际作用。

#### `moveto()`

将Note移动到某个时间点。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|dest|int|偏移到的时间点|

##### 返回值

偏移后的Note对象。

#### `offsetto()`

偏移Note指定的毫秒数。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|value|int|偏移的毫秒数|

##### 返回值

偏移后的Note对象。

## `Flick`

:::warning 注意
这是一个过时的模块。其中一些内容可能已经不再适用于当前版本的Arcaea。
:::

### 原型

`arcfutil.aff.note.common_note.Note`

--`arcfutil.aff.note.flick.Flick(Note)`

### 构造函数

|参数名|类型|说明|默认值|
|--|--|--|--|
|time|int|Note时间点|
|x|float|
|y|float|
|dx|float|
|dy|float|

### 方法

#### `__str__()`

##### 参数

无。

##### 返回值

Note的Note语句形式字符串。

#### `align()`

将Note时间对齐。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|bpm|float|基准bpm|
|error|int|允许的误差|3|
|lcd||需要对齐的细分的最小公倍数|96|

##### 返回值

时间对齐的Note对象。

#### `copy()`

返回Note对象的深拷贝。

##### 参数

无。

##### 返回值

Note对象的深拷贝。

#### `copyto()`

返回移动到某个时间点Note对象的深拷贝。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|dest|int|偏移到的时间点|

##### 返回值

偏移后Note的深拷贝。

#### `mirror()`

无实际作用。

#### `moveto()`

将Note移动到某个时间点。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|dest|int|偏移到的时间点|

##### 返回值

偏移后的Note对象。

#### `offsetto()`

偏移Note指定的毫秒数。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|value|int|偏移的毫秒数|

##### 返回值

偏移后的Note对象。

## `Hold`

### 原型

`arcfutil.aff.note.common_note.Note`

--`arcfutil.aff.note.tap.Tap(Note)`

----`arcfutil.aff.note.tap.Hold(Tap)`

### 构造函数

|参数名|类型|说明|默认值|
|--|--|--|--|
|time|int|Note时间点|
|totime|int|Note结束时间点|
|lane|int|Note轨道，范围`0`~`3`|

### 方法

##### 返回值

Note的Note语句形式字符串。

#### `__getitem__()`

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|item||切片对象|

##### 返回值

Note容器（切片结果有多个对象）或Note（切片结果仅有一个对象）。

#### `__len__()`

##### 参数

无。

##### 返回值

Note的持续时长。

#### `__str__()`

##### 参数

无。

#### `align()`

将Note时间对齐。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|bpm|float|基准bpm|
|error|int|允许的误差|3|
|lcd||需要对齐的细分的最小公倍数|96|

##### 返回值

时间对齐的Note对象。

#### `copy()`

返回Note对象的深拷贝。

##### 参数

无。

##### 返回值

Note对象的深拷贝。

#### `copyto()`

返回移动到某个时间点Note对象的深拷贝。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|dest|int|偏移到的时间点|

##### 返回值

偏移后Note的深拷贝。

#### `mirror()`

将Note镜像。

##### 参数

无。

##### 返回值

镜像后的Note对象。

#### `moveto()`

将Note移动到某个时间点。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|dest|int|偏移到的时间点|

##### 返回值

偏移后的Note对象。

#### `offsetto()`

偏移Note指定的毫秒数。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|value|int|偏移的毫秒数|

##### 返回值

偏移后的Note对象。



## `Note`

所有Note的基类。

### 原型

`arcfutil.aff.note.common_note.Note`

### 构造函数

|参数名|类型|说明|默认值|
|--|--|--|--|
|time|int|Note时间点|

### 方法

#### `align()`

将Note时间对齐。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|bpm|float|基准bpm|
|error|int|允许的误差|3|
|lcd||需要对齐的细分的最小公倍数|96|

##### 返回值

时间对齐的Note对象。

#### `copy()`

返回Note对象的深拷贝。

##### 参数

无。

##### 返回值

Note对象的深拷贝。

#### `copyto()`

返回移动到某个时间点Note对象的深拷贝。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|dest|int|偏移到的时间点|

##### 返回值

偏移后Note的深拷贝。

#### `mirror()`

无实际作用。

#### `moveto()`

将Note移动到某个时间点。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|dest|int|偏移到的时间点|

##### 返回值

偏移后的Note对象。

#### `offsetto()`

偏移Note指定的毫秒数。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|value|int|偏移的毫秒数|

##### 返回值

偏移后的Note对象。

## `NoteGroup`

### 原型

`arcfutil.aff.note.common_note.NoteGroup(list)`

### 构造函数

|参数名|类型|说明|默认值|
|--|--|--|--|
|notes||接收可迭代对象，或者多个Note对象|

### 方法

#### `__str__()`

##### 参数

无。

##### 返回值

Note容器内所有Note的Note语句形式字符串。

#### `align()`

将Note容器内部所有Note对象时间对齐。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|bpm|float|基准bpm|
|error|int|允许的误差|3|
|lcd||需要对齐的细分的最小公倍数|96|

##### 返回值

时间对齐的Note容器。

#### `append()`

向容器中追加Note对象或NoteGroup对象。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|__objects||接收Note或NoteGroup对象|

##### 返回值

`None`

#### `extend()`

将一个Note容器与一个可迭代对象拼接。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|__iterable||接收可迭代对象|

##### 返回值

`None`

#### `mirror()`

将Note容器内部所有Note镜像。

##### 参数

无。

##### 返回值

镜像后的Note容器。

#### `moveto()`

将Note容器整体偏移到一个时间点。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|dest|int|偏移到的时间点|

##### 返回值

偏移后的Note对象。

## `SceneControl`

### 原型

`arcfutil.aff.note.common_note.Note`

--`arcfutil.aff.note.scenecontrol.SceneControl(Note)`

### 构造函数

|参数名|类型|说明|默认值|
|--|--|--|--|
|time|int|Note时间点|
|scenetype|str|scenecontrol类型，支持值见`note.validstrings.scenetypelist`|
|x|float|
|y|int|

### 方法

#### `__str__()`

##### 参数

无。

##### 返回值

Note的Note语句形式字符串。

#### `align()`

将Note时间对齐。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|bpm|float|基准bpm|
|error|int|允许的误差|3|
|lcd||需要对齐的细分的最小公倍数|96|

##### 返回值

时间对齐的Note对象。

#### `copy()`

返回Note对象的深拷贝。

##### 参数

无。

##### 返回值

Note对象的深拷贝。

#### `copyto()`

返回移动到某个时间点Note对象的深拷贝。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|dest|int|偏移到的时间点|

##### 返回值

偏移后Note的深拷贝。

#### `mirror()`

无实际作用。

#### `moveto()`

将Note移动到某个时间点。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|dest|int|偏移到的时间点|

##### 返回值

偏移后的Note对象。

#### `offsetto()`

偏移Note指定的毫秒数。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|value|int|偏移的毫秒数|

##### 返回值

偏移后的Note对象。

## `Tap`

### 原型

`arcfutil.aff.note.common_note.Note`

--`arcfutil.aff.note.tap.Tap(Note)`

### 构造函数

|参数名|类型|说明|默认值|
|--|--|--|--|
|time|int|Note时间点|
|lane|int|Note轨道，范围`0`~`3`|

### 方法

#### `__str__()`

##### 参数

无。

##### 返回值

Note的Note语句形式字符串。

#### `align()`

将Note时间对齐。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|bpm|float|基准bpm|
|error|int|允许的误差|3|
|lcd||需要对齐的细分的最小公倍数|96|

##### 返回值

时间对齐的Note对象。

#### `copy()`

返回Note对象的深拷贝。

##### 参数

无。

##### 返回值

Note对象的深拷贝。

#### `copyto()`

返回移动到某个时间点Note对象的深拷贝。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|dest|int|偏移到的时间点|

##### 返回值

偏移后Note的深拷贝。

#### `mirror()`

将Note镜像。

##### 参数

无。

##### 返回值

镜像后的Note对象。

#### `moveto()`

将Note移动到某个时间点。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|dest|int|偏移到的时间点|

##### 返回值

偏移后的Note对象。

#### `offsetto()`

偏移Note指定的毫秒数。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|value|int|偏移的毫秒数|

##### 返回值

偏移后的Note对象。

## `Timing`

### 原型

`arcfutil.aff.note.common_note.Note`

--`arcfutil.aff.note.timing.Timing(Note)`

### 构造函数

|参数名|类型|说明|默认值|
|--|--|--|--|
|time|int|Note时间点|
|bpm|float|BPM值|
|bar|float|小节线数值|4.00|

### 方法

#### `__str__()`

##### 参数

无。

##### 返回值

Note的Note语句形式字符串。

#### `align()`

将Note时间对齐。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|bpm|float|基准bpm|
|error|int|允许的误差|3|
|lcd||需要对齐的细分的最小公倍数|96|

##### 返回值

时间对齐的Note对象。

#### `copy()`

返回Note对象的深拷贝。

##### 参数

无。

##### 返回值

Note对象的深拷贝。

#### `copyto()`

返回移动到某个时间点Note对象的深拷贝。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|dest|int|偏移到的时间点|

##### 返回值

偏移后Note的深拷贝。

#### `mirror()`

无实际作用。

#### `moveto()`

将Note移动到某个时间点。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|dest|int|偏移到的时间点|

##### 返回值

偏移后的Note对象。

#### `offsetto()`

偏移Note指定的毫秒数。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|value|int|偏移的毫秒数|

##### 返回值

偏移后的Note对象。

## `TimingGroup`

### 原型

`arcfutil.aff.note.common_note.NoteGroup(list)`

--`arcfutil.aff.note.notegroup.TimingGroup(NoteGroup)`

### 构造函数

|参数名|类型|说明|默认值|
|--|--|--|--|
|notes||接收可迭代对象，或者多个Note对象|
|opt|str|控制时间组参数|`None`|

### 方法

#### `__str__()`

##### 参数

无。

##### 返回值

Note容器内所有Note的Note语句形式字符串。

#### `align()`

将Note容器内部所有Note对象时间对齐。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|bpm|float|基准bpm|
|error|int|允许的误差|3|
|lcd||需要对齐的细分的最小公倍数|96|

##### 返回值

时间对齐的Note容器。

#### `append()`

向容器中追加Note对象。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|__objects||接收Note或NoteGroup对象|

##### 返回值

`None`

#### `extend()`

将一个Note容器与一个可迭代对象拼接。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|__iterable||接收可迭代对象|

##### 返回值

`None`

#### `mirror()`

将Note容器内部所有Note镜像。

##### 参数

无。

##### 返回值

镜像后的Note容器。

#### `moveto()`

将Note容器整体偏移到一个时间点。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|dest|int|偏移到的时间点|

##### 返回值

偏移后的Note对象。

#### `offsetto()`

将Note容器整体偏移一个毫秒数。

##### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|value|int|偏移的毫秒数|

##### 返回值

偏移后的Note容器。

# 函数

## `time_align()`

输入时间，输出对齐后的时间。

### 原型

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|time|int|待偏移的时间点|
|bpm|float|基准bpm|
|error|int|允许的误差|3|
|lcd||需要对齐的细分的最小公倍数|96|

### 返回值

时间对齐后的时间点。

