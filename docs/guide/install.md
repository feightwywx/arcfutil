---
title: 安装
language: zh-CN
---

# 安装

::: tip 提示
建议使用Python >= 3.8。
:::

## 从pip安装

推荐通过pip安装（或者更新）arcfutil，这也是最快捷的方式。只需运行以下命令：

```bash
pip install -U arcfutil
```

## 从源码安装

::: warning 注意
我们不推荐从源代码安装arcfutil，因为它可能产生一些不稳定的构建。要获取最新的稳定版本，请通过pip安装。
:::

::: warning 注意
从0.7.0版本开始，arcfutil不再支持`setuptools`安装，这种方式不支持native namespace package，而这会导致在导入拓展包时出现问题。
:::

要从源码安装，需要先从仓库下载最新的代码并切换工作目录：

```bash
git clone https://github.com/feightwywx/arcfutil.git && cd arcfutil
```

之后，通过pip来将arcfutil安装到当前环境：

```bash
pip install -e .
```
