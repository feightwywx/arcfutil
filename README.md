# arcfutil

(**Arc**aea **F**ile **Util**ity)

为处理[音乐游戏Arcaea](https://arcaea.lowiro.com/)相关文件（谱面，songlist，etc.）设计的Python模块。

## 安装

使用pip进行安装：

```bash
pip install -U arcfutil
```

## 功能

本模块大致分为处理.aff文件的`arcfutil.aff`包和命令行工具两部分。

### `aff`编辑框架

- 将`.aff`中的note解析为python对象（以及将这些对象编码回`.aff`中的note格式）

  - 支持切片等特性。Python式地创作谱面吧！

  - 支持Arcaea谱面的各种元素！
  
  - `timinggroup`支持
  
  - 为note对象提供了谱面编辑中的常用方法（复制、镜像、偏移等）

  - 提供Timing缓动、帧动画等常用谱面片段的构造工具


### 命令行工具

- `arcadeclean`：清理Arcade产生的多余文件！

- `sortassets`：对Arcaea下载的数据文件进行整理，方便制谱器读取。

- `songlist`：根据`songconfig.txt`自动生成`songlist`

  - 兼容`Brcbeb Soulmate`等生成工具使用的`songconfig.txt`

  - 根据`songlist`批量生成对应的`songconfig.txt`

  - 自动生成`packlist`

  - 自动复制曲目背景
  
## 用法

请参阅[文档](https://docs.arcaea.icu/)。

## 感谢

- 预置缓动曲线实现来自[easings.net](https://easings.net/)。

- 贝塞尔曲线实现来自[WebKit](https://webkit.org/)。
