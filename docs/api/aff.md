---
title: arcfutil.aff
language: zh-CN
prev: false
---

# `arcfutil.aff`

aff处理相关类和函数。

## `dump()`

将Note列表转换为Note语句。

### 原型

`arcfutil.aff.parse.dump(notelist: note.NoteGroup)`

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|notelist|NoteGroup|要转字符串的Note容器||

### 返回值

`(str)`Note语句。

## `dumps()`

将Note列表覆盖写入进文件。

### 原型

`arcfutil.aff.parse.dumps(notelist: note.NoteGroup, destpath: str)`

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|notelist|NoteGroup|要写入的Note容器||
|destpath|str|要写入的文件路径||

### 返回值

`(int)`写入的字节数。

## `extends()`

将Note列表追加写入进文件。

### 原型

`arcfutil.aff.parse.extends(notelist: note.NoteGroup, destpath: str)`

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|notelist|NoteGroup|要写入的Note容器||
|destpath|str|要写入的文件路径||

### 返回值

`(int)`写入的字节数。

## `load()`

将Note语句转换为Note对象，并用Note容器包装。

### 原型

`arcfutil.aff.parse.load(affstr: str)`

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|affstr|str|Note字符串||

### 返回值

`(NoteGroup)`转换后的Note容器。

## `loads()`

将包含Note语句的文件转换为Note容器，一般用于转换aff。

### 原型

`arcfutil.aff.parse.loads(path: str)`

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|path|str|要读取的文件路径|

### 返回值

`(NoteGroup)`转换后的Note容器。

## `loadline()`

将单个（组）Note语句转换为Note对象。

### 原型

`arcfutil.aff.parse.loadline(notestr: str)`

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|affstr|str|Note语句字符串|

### 返回值

`(Note or NoteGroup)`转换后的Note或时间组对象。

## `sort()`

将Note容器内的Note按照时间顺序进行排序。

### 原型

`arcfutil.aff.sorter.sort(unsorted: NoteGroup)`

### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|unsorted|NoteGroup|待排序的Note容器|

### 返回值

`(NoteGroup)`排序后的Note容器。
