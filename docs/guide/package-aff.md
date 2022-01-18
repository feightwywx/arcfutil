---
title: aff编辑
language: zh-CN
---

# aff编辑

在下文的叙述中，我们假设您已经了解了Arcaea谱面各种物件的基本结构。arcfutil使用Note对象来描述Arcaea谱面及其内部的各种元素，在此基础上还提供了一些实用的函数。要使用Note对象及这些函数，首先引入aff包：

```python
from arcfutil import aff
```

为了更直观地感受arcfutil的工作方式，我们从一个简短的例子开始。

## 第一个项目

新建一个.py文件，然后填入以下代码：

```python
from arcfutil import aff

afflist = aff.AffList(
    aff.Timing(0, 222.22),
    aff.Tap(0, 1),
    aff.Hold(0, 100, 2),
    aff.Arc(0, 200, 0, 1, 's', 1, 0, 0, True, [0, 100, 200]),
    aff.TimingGroup(
        aff.Timing(0, 222.22),
    )
)

aff.dumps(afflist, '0.aff')
```

运行这段Python代码，会在当前工作目录下生成一个`0.aff`文件，内容为：
```
AudioOffset:248
-
timing(0,222.22,4.00);
(0,1);
hold(0,100,2);
arc(0,200,0.00,1.00,s,1.00,0.00,0,none,true)[arctap(0),arctap(100),arctap(200)];
timinggroup(noinput){
timing(0,222.22,4.00);
};
```

恭喜！您得到了一个offset为248，初始bpm为222.22，并且有一个地键，一个长条，一根带有3个天键的黑线的Arcaea谱面文件。

## Note对象

### 用对象描述语句

让我们回顾上面的代码。形如`aff.Timing(0, 222.22)`的语句调用对应Note类的构造方法，产生Note对象。例如，`aff.Timing()`语句可以实例化一个Timing对象，其与aff谱面中的一条Timing语句等价。构造函数的参数顺序与真正的aff文件中的参数顺序相仿，如果你编写过aff谱面文件，应当很熟悉各个参数的位置。通过Note对象可以便利地操作Arcaea谱面中的对应要素。

### Note容器

arcfutil中还提供了`NoteGroup`类及其派生类作为存放Note对象的容器。通过使用这些容器，可以便利地实现诸如谱面输出，整体偏移，整体时间对齐等操作。

具体点来说，arcfutil提供了`NoteGroup`、`AffList`、`TimingGroup`三个Note容器，它们具有相似的功能。要建立一个`NoteGroup`或者其衍生形式，只需要如上所示以参数的形式传入Note对象（以及属性，如果有）。也可以将现有的可迭代对象（`list`，`tuple`等）作为参数输入，例如：

```python
a_normal_list = [
    aff.Timing(0, 222.22),
    aff.Tap(0, 1),
    aff.Hold(0, 100, 2),
    aff.Arc(0, 200, 0, 1, 's', 1, 0, 0, True, [0, 100, 200]),
    aff.TimingGroup(
        aff.Timing(0, 222.22),
    )
]

afflist = aff.AffList(a_normal_list)
```

得到的结果与上面直接传入`Note`对象的例子相同。很显然，各种`NoteGroup`对象也是可迭代对象。如果将一个`NoteGroup`对象作为参数传入一个Note容器类的构造函数，可以起到类型转换的作用。

在上述的介绍中，您可能已经注意到，不同的Note容器的构造函数接受的参数有所不同。它们的大致用法如下表：

|容器|参数|用途|
|---|---|---|
|NoteGroup|无|任何一般用途|
|AffList|offset, desnity|用于描述一个完整的aff谱面文件|
|TimingGroup|opt|用于描述一个时间组|

例如，要建立一个AudioOffset和TimingPointDesnityFactor各为100和2.01的aff谱面：

```python
my_aff = aff.AffList(
    aff.Timing(0, 100),
    my_note_foo,
    my_note_bar,
    offset=100,
    desnity=2.01
)
```

再比如，建立一个noinput时间组：

```python
my_timinggroup = aff.TimingGroup(
    aff.Timing(0, 100),
    my_note_foo,
    my_note_bar,
    opt="noinput"
)
```

要将`NoteGroup`对象以字符串形式输出非常便利，只需调用它们的`str()`方法即可。对于`Note`而言同样，调用`str()`方法就能转换成字符串的形式。如果编写过aff谱面文件，应当能很快上手这些类。

## Note操作

`Note`相关的操作非常简单快捷，让我们通过具体的示例来介绍。

### Tap

从最简单的开始。例如，有一个Tap对象`foo`，我们可以修改它所处的时间点和轨道，也可以对它进行镜像、时间偏移或是时间对齐，又或许是复制：

```python
foo = aff.Tap(0, 2)

foo.time = 100               # 将时间点设置为100
foo.lane = 3                 # 将轨道设置为3号轨

foo.mirror()                 # 镜像
foo.offsetto(100)            # 正向偏移100ms
foo.align(222.22)            # 参数中填写的是曲目的BPM
another_foo = foo.copy()     # 复制
moved_foo = foo.copyto(500)  # 复制到500这个时间点
```

### Hold

`aff.Hold`类是`aff.Tap`类的子类，你对其可以使用上面提到的所有功能。不过Hold要稍微复杂一些，因为它多了一个结束时间点的参数。
因此，我们提供了一个“剪切”函数`moveto()`（其实对`Tap`也可以使用，但是完全没必要，不是吗）。

```python
bar = aff.Hold(0, 100, 3)

bar.totime = 200  # 将结束时间点设置为200
bar.moveto(500)   # 移动到500这个时间点
```

### Arc

之后就来到了`aff.Arc`类，这无疑是Arcaea的精髓所在，同时也更加复杂。类似地，由于`aff.Arc`继承自`aff.Hold`类，你可以使用上述的所有功能。
同时，对于Arc对象，我们还额外提供了一些实用的方法。请看示例：

```python
snake = aff.Arc(0, 200, 0, 1, 's', 1, 0, 0, True, [0, 100, 200])

# 空间参数
snake.fromx = 0.5
snake.tox = 0.5
snake.fromy = 0
snake.toy = 1

snake.slideeasing = 'sisi'  # 将缓动类型设置为sisi
snake.color = 1             # 将颜色设置为红色
snake.isskyline = False     # 设置实心Arc
snake.skynote = []          # 实心Arc不能有天键，让我们把它们删除

snake.vmirror()             # 垂直翻转
snake.transfer(0.5, 0)      # 将Arc向右平移0.5单位
```


此外，您还可以对Arc对象进行切片操作。就像对Python的列表所做的行为一样，您可以把Arc想象成一个包含了无数时间点及其对应坐标的容器，对其进行索引就可以“取出”对应点的坐标，对其进行切片则可以得到一段新的Arc。请看示例：

```python
another_snake = aff.Arc(0, 100, 0, 1, 's', 0, 1, 0, True)

another_snake[50]        # 得到一个元组(0,5, 0,5)

another_snake[25:75:25]  # 在25~75这一段，每25ms切割一次
                         # 得到一个NoteGroup
```

切片语句可以只提供任意的一个或两个参数。特别地，切片操作对Hold也可用，不过意义没有那么大，所以放在Arc这部分介绍。

### Timing

最后要介绍的是`aff.Timing`类。它支持移动，复制，时间偏移和对齐的方法。它的三个参数`time`，`bpm`和`bar`分别控制时间点，BPM和小节线。在此不过多介绍。

至于`Camera`，`SceneControl`和`Flick`这几个类，平时较少用到，支持的方法和`Tap`相同，也不再过多介绍。

### Note容器

arcfutil对Note容器也提供了各种方法。例如对前文所述的`AffList`对象`afflist`可以进行如下操作：

将AffList的TimingPointDensityFactor设置为`2`：
```python
afflist.density = 2
```

将AffList时间整体偏移300ms，并且整体镜像：
```python
afflist.offsetto(300)
afflist.mirror()
```

## 生成函数

arcfutil还提供了一些便于机械化生成谱面段落的函数，它们位于`aff.generator`下：

- `arc_crease_line()`: 生成折线Arc。

- `arc_rain()`:　生成下雨黑线。

- `arc_slice_by_count()`: 根据段落数切分Arc。

- `arc_slice_by_timing()`: 根据一组Timing切分Arc。

- `arc_animation_assist()`: 逐帧动画辅助。

- `arc_envelope()`: 以两条Arc为包络线，生成一条新的折线Arc。

- `timing_glitch()`: 原地抖动的Timing

- `timing_easing()`: 缓动Timing

各个参数的意义应当是非常显然的。并且，如果详细介绍每个参数，这篇快速上手教程会显得过于冗长。因此，要详细了解每个参数的意义，请参阅[API文档](/api/aff-generator)。

## 读取与写入

还记得吗？在我们的第一个程序中，有如下语句：

```python
aff.dumps(afflist, '0.aff')
```

这条语句将`afflist`写入工作目录下的`0.aff`文件中。

::: danger 警告
如果`0.aff`文件已经存在，`aff.dumps()`函数将会覆盖其中的内容！如果想要向文件中追加内容，请使用用法类似的`aff.extends()`函数。
```python
aff.extends(afflist, '0.aff')
```
:::


如要读取`*.aff`文件，则使用`aff.loads()`函数：

```python
afflist = aff.loads('0.aff')
```

显然，并非所有工作都需要和文件打交道。在这种情况下，您可以使用`aff.load()`和`aff.dump()`函数。这些函数实现了字符串形式的谱面和Note对象间的转换。
