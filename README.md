# arcfutil

(a.k.a. Arcaea File Utility)

为处理Arcaea相关文件（谱面，songlist，etc.）设计的Python模块。

## 功能
~~同时也是Todo list~~

- [x] 将`.aff`中的note解析为python对象（以及将这些对象生成回`.aff`的note格式）

  - [x] `AudioOffset`，`tap`，`hold`，`arc`（包含`arctap`）以及`timing`

  - [ ] `camera`和`scene`计划中
  
  - [x] 为note对象提供了谱面编辑中的常用方法（复制、镜像）
  
  - [ ] selector（计划中）

- [x] 对Arcaea下载的数据文件进行整理，方便制谱器读取。

- [x] 根据`songconfig.txt`自动生成`songlist`

  - [x] 兼容`Brcbeb Soulmate`等生成工具使用的`songconfig.txt`

  - [x] 根据`songlist`批量生成对应的`songconfig.txt`

  - [x] 自动生成`packlist`

  - [x] 自动复制曲目背景
