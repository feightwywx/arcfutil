# arcfutil

(a.k.a. Arcaea File Utility)

为处理Arcaea相关文件（谱面，songlist，etc.）设计的Python模块。

## 安装

使用pip进行安装：
```commandline
pip install -U arcfutil
```

## 功能
~~同时也是Todo list~~

- [x] 将`.aff`中的note解析为python对象（以及将这些对象编码回`.aff`中的note格式）

  - [x] 支持切片等特性。Python式地创作谱面吧！

  - [x] 支持Arcaea谱面的各种元素！（截至2021年愚人节版本v3.5.3）
  
  - [x] `timinggroup`支持
  
  - [x] 为note对象提供了谱面编辑中的常用方法（复制、镜像、偏移等）

- [x] 对Arcaea下载的数据文件进行整理，方便制谱器读取。

- [x] 根据`songconfig.txt`自动生成`songlist`

  - [x] 兼容`Brcbeb Soulmate`等生成工具使用的`songconfig.txt`

  - [x] 根据`songlist`批量生成对应的`songconfig.txt`

  - [x] 自动生成`packlist`

  - [x] 自动复制曲目背景
  
## 用法
  
请参阅[文档](https://github.com/feightwywx/arcfutil/wiki)。

