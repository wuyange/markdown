# CSS

## CSS的添加方式

### 外部样式表

指将CSS编写在扩展名为`.css` 的单独文件中，并从HTML`<link>` 元素引用它

- 可以多个网页进行复用
- 可以使用到；浏览器的缓存机制，从而加快网页的加载速度

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>My CSS experiment</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <h1>Hello World!</h1>
    <p>This is my first CSS example</p>
  </body>
</html>
```

### 内部样式表

内部样式表是指不使用外部CSS文件，而是将CSS放在HTML文件`<head>`标签里的`<style>`标签之中

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>My CSS experiment</title>
    <style>
      h1 {
        color: blue;
        background-color: yellow;
        border: 1px solid black;
      }

      p {
        color: red;
      }
    </style>
  </head>
  <body>
    <h1>Hello World!</h1>
    <p>This is my first CSS example</p>
  </body>
</html>
```

### 内联样式

内联样式表存在于HTML元素的style属性之中，其特点是每个CSS表只影响一个元素

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>My CSS experiment</title>
  </head>
  <body>
    <h1 style="color: blue;background-color: yellow;border: 1px solid black;">Hello World!</h1>
    <p style="color:red;">This is my first CSS example</p>
  </body>
</html>
```

# CSS的基本语法

## 注释

在css中的注释是/**/，html文件中的`<style></style>`标签中包裹的内容属于css，所以格式和注释都应该个css中一样

```css
<style>
    .sss {
    color: black;
    }
    /* p {
    color: blue;
    } */
</style>
```

## 选择器和声明块

选择器：通过选择器可以选中页面中的元素

声明块：通过声明块来指定元素的样式

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
        /* 其中.sss就是选择器 大括号以及里面的内容就是声明块 */
        .sss {
            color: black;
        }
    </style>
</head>
<body>
    <h1>这是标题</h1>
    <p class="sss">这是段落</p>
</body>
</html>
```

# 选择器详解

## 标签选择器

根据元素的标签名来选中元素如`p{} div{} h1{}`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
        h1{
            color: black;
        }
    </style>
</head>
<body>
    <h1>这是标题</h1>
</body>
</html>
```

## id选择器

根据元素的id值来选中元素如`#3{}`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
        #red{
            color: red;
        }
    </style>
</head>
<body>
    <div id="red">id选择器</div>
</body>
</html>
```

## 类选择器

根据元素的class值来选中元素如`.class{}`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
        .red{
            color: red;
        }
    </style>
</head>
<body>
    <div class="red">class选择器</div>
</body>
</html>
```

class属性可以等于多个值，需要使用空格隔开

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
        .red{
            color: red;
        }
    </style>
</head>
<body>
    <div class="red green">class选择器</div>
</body>
</html>
```

## 通配符

*可以匹配所有的便签

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
        *{
            color: blue;
        }
    </style>
</head>
<body>
    <h1>这是标题h1</h1>
    <h2>这是标题h2</h2>
    <h3>这是标题h3</h3>
</body>
</html>
```

## 关系选择器

通过元素之间的关系来选中元素

- 选中子元素 `div > p > span`  
- 选中后代元素 `div span`
- 选中下一个兄弟 `p + span` p元素和span元素必须紧紧的挨着
- 选中下面所有的兄弟 `p ~ span` 选中p元素下面所有的标签名为span的兄弟

## 属性选择器

通过元素的属性来选中元素的属性

- 选中有title属性的div元素 `div[title]`
- 选中title属性为aaa的元素`*[title="aaa"]`
- 选中title属性以b结尾的元素`*[title$="b"]`
- 选中title属性以b开头的div元素`div[title^="b"]`
- 选中title属性有b的div元素`div[title*="b"]`
- 选中title的所有属性中，至少有一个属性是asd的div元素`div[title~="asd"]`
  - `div[title~="asd"]`和`div[title="asd"]`的区别
  - `<div title="asd ccc">`想要匹配到这个元素，就需要`div[title~="asd"]`或者`div[title="asd ccc"]`
- 选中id以d结尾且class为xxx的h1元素`h1[id$="d"][class="xxx"]`

## 复合选择器

可以多种选择器组合使用

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
        div.green.red{
            color: green;
        }
        /*选中同时满足标签名为h1 id值为red class值为xxx的标签*/
        h1#red.xxx{
            color: red;
        }
        /*同时选中h2 和 span两个标签*/
        h2, span{
            color: pink;
        }
    </style>
</head>
<body>
    <div class="red green">class选择器</div>
    <h1 id="red" class="xxx">这是标题h1</h1>
    <h2>标题2</h2>
    <span>span文本</span>
</body>
</html>
```

## 伪类选择器

伪类用于描述一个元素的特殊状态，伪类使用 : 开头

[伪类 - CSS（层叠样式表） | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Pseudo-classes)

- 选中ul元素的第一个**并且**名称为li的子元素`ul > li:first-child`  
- 选中ul元素的最后一个**并且**名称为li的子元素`ul > li:last-child`  
- 选中ul元素的第n个**并且**名称为li的子元素`ul > li:nth-child(n)`  
  - n  他的范围是0-正无穷，便是选中所有的
  - 2n 或者 even 选中所有的偶数位的元素
  - 2n + 1 或者 odd 选中所有的奇数数位的元素
- 选中ul元素的第一个名称为li的子元素`ul > li:first-of-type`  
- 选中ul元素的最后一个名称为li的子元素`ul > li:last-of-type` 
- 选中ul元素的第n个名称为li的子元素`ul > li:nth-of-type(n)`  
  - n  他的范围是0-正无穷，便是选中所有的
  - 2n 或者 even 选中所有的偶数位的元素
  - 2n + 1 或者 odd 选中所有的奇数数位的元素
- 在选中的元素中排除使用not() 
  - `ul > li:not(:nth-child(3))`
- **鼠标移动到元素上时的元素样式`a:hover`**
- **鼠标点击元素时的元素样式`a:active`**

## 伪元素选择器

[伪元素 - CSS（层叠样式表） | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Pseudo-elements)

伪元素：表示页面中一些特殊的并不真实存在的元素，为元素使用 :: 开头

- `::first-letter` 会选中某块级元素第一行的第一个字母
- `::first-line`会选中某个块级元素的第一行
- `::selection`会选中被鼠标选中的内容
- `::before`会选中元素的开始
- `::after`会选中元素的末尾
  - `::before和::after`一般和 `content`一起使用

## 继承

- 样式的继承，我们为一个元素设置的样式同时也会应用到他的后代上

- 并不是所有的样式都会被继承，比如背景相关的，布局相关等，这些样式都不会被继承

## 选择器的优先级

[CSS选择器的优先级（精讲版） (biancheng.net)](http://c.biancheng.net/view/7216.html)

**样式冲突**：当我们通过不同的选择器，选中相同的元素，并且为相同的样式设置不同的值时，就会发生样式的冲突

**选择器的权重从从上到下，从大到小**

- !important
- 内联样式
- id选择器
- 类、属性、伪类选择器
- 元素选择器
- 通配符选择器
- 继承的样式

**比较选择器的优先级时，需要将所有的选择器的优先级进行相加计算（分组选择器是分开计算）**

**如果优先级相同时，则下面的样式会覆盖上面的样式**

# 单位

## 样式中的长度单位

- px 像素
- 百分比 相对于其父元素属性的百分比（随父元素的改变而改变）
- em 相对元素字体的大小来计算的 1em = 1 font-size
- rem 相对于根元素的（<html>）的字体大小来计算

## 颜色单位

- 直接使用颜色名称 red、orange、yellow等
- RGB值　语法rgb(红色，绿色，蓝色)每个b值的的范围是 0-255 或者使用百分比
  - rgb(255,0,0)
  - rgb(100%,0,0)
  - rgba(255,0,0,.5)最后一位表示透明度，.5表示半透明
- 十六进制的RGB　语法＃红色绿色蓝色  00-ff
  - #ff0000
  - #ff0000 可以简写为#f00
- HSL值 H 色相（0-360） S 饱和度（0%-100%） L 亮度 （0%-100%）
  - hsl(360,100%,50%)



