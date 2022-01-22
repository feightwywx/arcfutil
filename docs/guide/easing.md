---
title: 缓动控制
language: zh-CN
---

# 缓动控制

缓动在提升谱面视觉效果方面非常实用。arcfutil为Arc和Timing物件提供便捷且可高度自定义的缓动系统。

## 缓动函数

总的来说，缓动函数是一种位移-时间函数，定义域为[0,1]。大多数缓动函数的值域也为[0,1]，但是也有一些特殊的缓动函数。

### 内置缓动函数

arcfutil内置的缓动函数按照是否被Arcaea直接支持分为两块。

Arcaea支持的缓动函数位于`aff.easing`，为以下四个：

- `bezier()`，对应`b`

- `linear()`，对应`s`

- `sine()`，对应`si`

- `cosine()`，对应`so`

其中，`bezier()`还支持传入四个参数作为两个控制点的坐标来对贝塞尔曲线进行自定义。不过，一般在需要自定义贝塞尔曲线时，更建议使用`make_bezier()`函数，这将在下一节进行介绍。

除此之外，arcfutil还内置了30个不被Arcaea支持的缓动函数于`easing.cheatsheet`，具体可以查阅[这个页面](https://easings.net/)。
略有区别的是，这些缓动函数在arcfutil内部使用小写字母和下划线组合的命名方式而非小驼峰。
例如，当您需要使用`easeInSine`缓动时，应当引入`aff.easing.cheatsheet.ease_in_sine`。

### 自定义缓动函数

arcfutil提供了`make_bezier()`来方便地建立自定义贝塞尔缓动函数。该函数接受一个元组作为参数，返回一个自定义的贝塞尔缓动函数。
例如，利用贝塞尔曲线建立一个自定义的`linear()`函数：

```python
from arcfutil.aff.easing import make_bezier

my_linear = make_bezier((0, 0, 1, 1))
```

您可以在[这个页面](https://cubic-bezier.com/)测试您的贝塞尔缓动曲线。

当然，直接定义一个函数用作缓动函数也是可行的。

## Arc缓动

Arc在游戏内仅支持特定的几种缓动函数，但是在进行Arc分割时可能需要其它的缓动函数。`slideeasing`属性控制一个Arc对象使用的缓动类型，该属性支持传入特定字符串或自定义的缓动函数。

### 字符串形式

Arc支持的缓动字符串为两个单缓动字符串的组合，它们分别控制Arc在x轴和y轴上的缓动。例如，对一个x轴上使用b缓动，y轴上使用s缓动的Arc，其`slideeasing`可以这样表示：

```python
arc.slideeasing = 'bs'
```

显然，这样的缓动类型在Arcaea中并不存在。arcfutil也仅支持用这样的Arc来进行切片等操作，如果对这样的Arc调用str()函数，arcfutil会抛出异常。

您可能注意到，`bs`这种写法看起来有些奇怪。因此，当y轴上的缓动为`s`时也允许省略。下面的表达与上面的是等效的：

```python
arc.slideeasing = 'b'
```
### 函数形式

Arc的`slideeasing`属性也支持传入一个由两个缓动函数组成的元组，分别作为x轴和y轴的缓动。例如将Arc的缓动类型设置为`sisi`：

```python
from arcfutil.aff.easing import sine

# ...
arc.slideeasing = (sine, sine)
```

也可以只传入一个缓动函数，此时与传入两个相同的缓动函数等效：

```python
from arcfutil.aff.easing import sine

# ...
arc.slideeasing = sine
```

## Timing缓动

arcfutil提供了`timing_easing_by_disp()`和`timing_easing()`生成函数用于生成缓动Timing。
前者基于位移，可以更好地使用现有的缓动函数，并且更易于控制缓动行程；后者则基于直接的bpm控制。

`timing_easing_by_disp()`接受缓动开始时间，结束时间，基准bpm，细分数量和缓动函数作为参数。
下面是一个回弹的例子。

```python
from arcfutil.aff.generator import timing_easing_by_disp
from arcfutil.aff.easing.cheatsheet import ease_in_back

timing_easing_by_disp(0, 1000, 200, 10, ease_in_back)

# 结果：
# timing(0,0.00,4.00);
# timing(100,-46.68,4.00);
# timing(200,-68.15,4.00);
# timing(300,-59.72,4.00);
# timing(400,-17.62,4.00);
# timing(500,60.38,4.00);
# timing(600,174.39,4.00);
# timing(700,322.22,4.00);
# timing(800,491.52,4.00);
# timing(900,700.27,4.00);
# timing(1000,936.00,4.00);
```

如果需要精细地控制bpm而非位移，则可以使用`timing_easing()`函数。下面是一个bpm从0线性加速到200的例子。

```python
from arcfutil.aff.generator import timing_easing

timing_easing(0, 1000, 0, 200, 10, mode='s')

# 结果：
# timing(0,0.00,4.00);
# timing(100,20.00,4.00);
# timing(200,40.00,4.00);
# timing(300,60.00,4.00);
# timing(400,80.00,4.00);
# timing(500,100.00,4.00);
# timing(600,120.00,4.00);
# timing(700,140.00,4.00);
# timing(800,160.00,4.00);
# timing(900,180.00,4.00);
# timing(1000,200.00,4.00);
```


