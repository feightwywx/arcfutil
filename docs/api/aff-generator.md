---
title: arcfutil.aff.generator
language: zh-CN
---

# `arcfutil.aff.generator`

aff片段生成函数。

## `arc_animation_assist()`

逐帧动画辅助工具。

### 原型

`arcfutil.aff.generator.arc_sample.arc_animation_assist(...) -> NoteGroup`

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|arc|Arc|要变换的Arc|
|start_t|int|动画开始时间点|
|stop_t|int|动画结束时间点|
|delta_x|float|x轴位移量|
|delta_y|float|y轴位移量|
|basebpm|float|基准BPM|
|easing_x|Callable|x轴缓动函数|`aff.easing.linear`|
|easing_y|Callable|y轴缓动函数|`aff.easing.linear`|
|infbpm|float|极大值BPM|999999|
|framerate|float|帧率|60|
|fake_note_t|float|100000|假Note时间偏移量|
|offset_t|int|动画整体时间偏移，影响物件z轴距离|0|
|delta_offset_t||动画整体时间偏移变化量，可产生z轴位移|0|
|easing_offset_t|str|z轴缓动函数|`aff.easing.linear`|


### 返回值

`(NoteGroup)` 生成的Note。

## `arc_crease_line()`

生成折线Arc。

### 原型

`arcfutil.aff.generator.arc_sample.arc_crease_line(...) -> NoteGroup`

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|base|Arc|基线|
|x_range|float|x轴变动范围|
|y_range|float|y轴变动范围|
|count|int|切分数量|
|mode|str|模式，`m`以基线为中线，`b`以基线为边线|m|
|easing|str|生成Arc的缓动类型|s|

### 返回值

`(NoteGroup)` 生成的Note。

## `arc_envelope()`

以两条Arc为包络线，生成一条新的折线Arc。

### 原型

`arcfutil.aff.generator.arc_sample.arc_envelope(...) -> NoteGroup`

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|arc1|Arc|主包络线，决定了新Arc的起点，缓动类型，颜色和虚实|
|arc2|Arc|副包络线|
|count|int|切分数量|
|mode|Literal['c', 'p']|生成模式，c为折线，p为平行线|c|

### 返回值

`(NoteGroup)` 生成的Note。

## `arc_interlace()`

将一组Arc转换为虚实相间的Arc。

### 原型

`arcfutil.aff.generator.arc_sample.arc_interlace(...) -> NoteGroup`

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|arcs|NoteGroup|输入的Arc列表|

### 返回值

`(NoteGroup)` 生成的Note。

## `arc_rain()`

生成下雨黑线。

### 原型

`arcfutil.aff.generator.arc_sample.arc_rain(...) -> NoteGroup`

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|original_t|int|下雨起始时间|
|dest_t|int|下雨结束时间|
|step|float|雨点起始点之间的间隔|
|length|float|雨点的长度，`None`则表示充满间隔|None|

### 返回值

`(NoteGroup)` 生成的Note。

## `arc_slice_by_count()`

将Arc切分为固定段数。

### 原型

`arcfutil.aff.generator.arc_sample.arc_slice_by_count(...) -> NoteGroup`

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|arc|Arc|要切分的Arc|
|count|切分数量||
|start|int|切分起始点，`None`表示不指定|None|
|stop|int|切分终点，`None`表示不指定|None|

### 返回值

`(NoteGroup)` 生成的Note。

## `arc_slice_by_timing()`

以Timing组为基准切分Arc。

### 原型

`arcfutil.aff.generator.arc_sample.arc_slice_by_timing(...) -> NoteGroup`

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|arc|Arc|要切分的Arc|
|timings|Iterable|作为切分基准的Timing组|

### 返回值

`(NoteGroup)` 生成的Note。

## `arc_straighten()`

拉直Arc。

### 原型

`arcfutil.aff.generator.arc_sample.arc_straighten(...) -> NoteGroup`

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|arcs|NoteGroup|输入的Arc列表|
|x|bool|是否x方向拉直|false|
|y|bool|是否y方向拉直|false|
|connector|bool|是否建立连接符（0时长s蛇）|false|

### 返回值

`(NoteGroup)` 生成的Note。

## `timing_easing()`

生成平缓变化的Timing。

### 原型

`arcfutil.aff.generator.timing_sample.timing_easing(...) -> NoteGroup`

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|origin_t|int|效果起始时间|
|dest_t|int|效果结束时间|
|origin_bpm|float|起始BPM|
|dest_bpm|float|目标BPM|
|count|int|Timing数量|
|bar|float|小节线数值|4.00|
|mode|Literal['s', 'b', 'si', 'so'], Callable|缓动模式，可选`b|s|si|so`或传入函数|s|
|b_point|list|贝塞尔缓动曲线，mode的值为`b`时生效|[1/3, 0, 2/3, 1]|

### 返回值

`(NoteGroup)` 生成的Note。

## `timing_easing_by_disp()`

生成平缓变化的Timing。基于持续时间和缓动函数，位移可控。

### 原型

`arcfutil.aff.generator.timing_sample.timing_easing_by_disp(...) -> NoteGroup`

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|start_t|int|效果起始时间|
|stop_t|int|效果结束时间|
|base|float|起始BPM|
|count|int|Timing数量|
|easing|Callable|缓动函数|s|
|bar|float|小节线数值|4.00|


### 返回值

`(NoteGroup)` 生成的Note。

## `timing_easing_linear()`

::: warning 注意
这个方法已被废弃。请使用[`aff.generator.timing_easing()`](#timing-easing)代替。
:::

生成线性变化的Timing。

### 原型

`arcfutil.aff.generator.timing_sample.timing_easing_linear(...) -> NoteGroup`

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|origin_t|int|效果起始时间|
|dest_t|int|效果结束时间|
|origin_bpm|float|起始BPM|
|dest_bpm|float|目标BPM|
|count|int|Timing数量|
|bar|float|小节线数值|4.00|

### 返回值

`(NoteGroup)` 生成的Note。

## `timing_glitch()`

生成原地抖动的Timing。

### 原型

`arcfutil.aff.generator.timing_sample.timing_glitch(...) -> NoteGroup`

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|origin_t|int|效果起始时间|
|dest_t|int|效果结束时间|
|count|int|Timing数量|
|bpm_range|float|BPM变化范围|
|exact_bar|float|BPM变化极值时的小节线数值|4.00|
|zero_bar|float|BPM为零值时的小节线数值|4.00|

### 返回值

`(NoteGroup)` 生成的Note。


