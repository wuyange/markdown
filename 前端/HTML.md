# HTML

[教程链接](https://developer.mozilla.org/zh-CN/docs/learn/HTML/Introduction_to_HTML/HTML_text_fundamentals)

## HTML的头部元素：<head&gt; 

### 标题

```html
<title>用来表示这个网页上页签的标题
<title>这是一个标题</title>
```

### 编码

```html
<meta charset="utf-8">
```

### 作者和描述

`<meta> `元素包含了name 和 content 特性

- `name` 指定了meta元素的类型；说明该元素包含什么类型的信息
- `content` 指定了直接的元数据内容

```html
<!-- 指定了作者 -->
<meta name="author" content="shunyu">
<!-- 指定了描述信息 -->
<meta name="description" content="这是一个描述信息">
<!-- 指定了网页的关键字 -->
<meta name="keywords" content="前端,html">
<!-- 网页的重定向 表示三秒后，跳转到百度页面-->
<meta http-equiv="refresh" content="3;url=https://www.baidu.com">
```

### 自定义标题

`<link>`元素可以用来引入HTML页面外部的资源文件

- `rel`: 表示将要引用的资源类型 `rel="shortcut icon"`是一种固定写法。如果缺省该属性会影响ico图标的正确显示
- `href`:表示指向资源的URL

```html
<link rel="shortcut icon" href="favicon.ico" type="image/x-icon">
```

### 为文档设置语言

```html
<html lang="zh-CN">
<html lang="en">
```

### 在HTML中设置CSS和JavaScript

-  `<link>`元素经常位于文档的头部。这个link元素有2个属性，`rel="stylesheet"`表明这是文档的样式表，而 href包含了样式表文件的路径：

  ```html
  <link rel="stylesheet" href="my-css-file.css">
  ```

- `<script>`部分没必要非要放在文档头部；实际上，把它放在文档的尾部（在 `</body>`标签之前）是一个更好的选择，这样可以确保在加载脚本之前浏览器已经解析了HTML内容（如果脚本加载某个不存在的元素，浏览器会报错）。

  ```html
  <script src="my-js-file.js"></script>
  ```

## 注释

```html
<!-- 注释 -->
```

## 标题和段落

~~~html
<h1>一级标题</h1>
<h2>二级标题</h2>
<h3>三级标题</h3>
<h6>六级标题</h6>

<p>这是段落标签</p>
~~~

## 列表

### 无序列表

项目的顺序并不重要，就像购物列表。用一个 <ul> 元素包围。
### 有序列表

项目的顺序很重要，就像烹调指南。用一个 <ol> 元素包围。

```html
<ul>
    <li>xxx</li>
    <li>aaa</li>
</ul>
<ol>
    <li>123</li>
    <li>456</li>
</ol>

<!-- 嵌套列表 -->
<ol>
    <li>123</li>
    <li>456</li>
    <ul>
        <li>aaa</li>
        <li>bbb</li>
    </ul>
</ol>
```

### 描述列表

描述列表使用与其他列表类型不同的闭合标签—— `<div>`; 此外，每一项都用`<dt>`元素闭合。每个描述都用`<dd>`元素闭合。

```html
<dl>
  <dt>标签一</dt>
    <dd>描述一</dd>
  <dt>标签二</dt>
    <dd>描述二</dd>
  <dt>标签三</dt>
    <dd>描述三</dd>
</dl>
```

## 斜体

```html
<em>我是一个斜体</em>
<i>我也是一个斜体</i>
```

## 加粗

```html
<strong>这个字被加粗了</strong>
<b>这个字也被加粗了</b>
```

## 下划线

```html
<u>我有下划线</u>
```

## 超链接

```html
<a href="http://www.baidu.com" title="百度一下" target="_blank">百度</a>
href:超链接 地址或者网址
title:鼠标悬浮时展示的内容
target:鼠标点击时，是新打开一个页面还是在原来的页面上跳转
	_blank 表示新打开一个页面
	_self  表示在原有的页面上跳转(默认值)
```

### 去顶部

```html
<a href="#">去顶部</a>
```

### 图片链接

例如你想要将一个图像转换为链接，你只需把图像元素放到`<a></a>`标签中间

```html
<a href="https://www.mozilla.org/zh-CN/">
  <img src="mozilla-image.png" alt="链接至 Mozilla 主页的 Mozilla 标志">
</a>
```

### 文档片段链接

超链接除了可以链接到文档外，也可以链接到HTML文档的特定部分（被称为文档片段）。要做到这一点，你必须首先给要链接到的元素分配一个`id`属性。

```html
<h2 id="Mailing_address">跳转目的地</h2>
```

然后链接到那个特定的`id`，您可以在URL的结尾使用一个`#`号指向它，例如：

```html
<a href="contacts.html#Mailing_address">跳转</a>
```

你甚至可以在同一份文档下，通过链接文档片段，来链接到同一份文档的另一部分：

```html
<a href="#Mailing_address">跳转</a>
```

### 下载链接

链接到要下载的资源而不是在浏览器中打开时，可以使用 download 属性来提供一个默认的保存文件名

```html
<a href="https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=zh-CN"
   download="firefox-latest-64bit-installer.exe">
  下载最新的 Firefox 中文版 - Windows（64位）
</a>
```

### 发送电子邮件链接

当点击一个链接或按钮时，打开一个新的电子邮件发送信息而不是连接到一个资源或页面，这种情况是可能做到的。这样做是使用`mailto：URL`的方案。其最基本和最常用的使用形式为一个`mailto`:link （链接），链接简单说明收件人的电子邮件地址。

```html
<a href="mailto:shunyu@qq.com">向 shunyu 发邮件</a>
```

实际上，邮件地址甚至是可选的。如果你忘记了（也就是说，你的`href`仅仅只是简单的"`mailto:`"），一个新的发送电子邮件的窗口也会被用户的邮件客户端打开，只是没有收件人的地址信息，这通常在“分享”链接是很有用的，用户可以发送给他们选择的地址邮件

## 引用

### 块引用

### 行内测试

### 引文

## 缩略语

另一个在web上看到的相当常见的元素`<addr>`——它常被用来包裹一个缩略语或缩写，并且提供缩写的解释（包含在`title`属性中，当光标移动到项目上时会出现title中的内容）

```html
<p>我们使用 <abbr title="超文本标记语言（Hyper text Markup Language）">HTML</abbr> 来组织网页文档。</p>
<p>第 33 届 <abbr title="夏季奥林匹克运动会">奥运会</abbr> 将于 2024 年 8 月在法国巴黎举行。</p>
```

## 上标和下标

当使用日期、化学方程式、和数学方程式时会偶尔使用上标和下标。 `<sub>`和`<sup>`元素可以解决这样的问题。

```html
<p>水的化学方程式是 H<sub>2</sub>O<sub>2</sub></p>
<p>如果 x<sup>2</sup> 的值为 9，那么 x 的值必为 3 或 -3</p>
```

## 计算机代码

- `<code>`用于标记计算机通用代码。
- `<pre>`: 用于保留空白字符（通常用于代码块）——如果您在文本中使用缩进或多余的空白，浏览器将忽略它，您将不会在呈现的页面上看到它。但是，如果您将文本包含在`<pre></pre>`标签中，那么空白将会以与你在文本编辑器中看到的相同的方式渲染出来。
- `<var>`: 用于标记具体变量名。
- `<kbd>`: 用于标记输入电脑的键盘（或其他类型）输入。
- `<samp>`: 用于标记计算机程序的输出。

```html
<pre><code>const para = document.querySelector('p');

para.onclick = function() {
  alert('噢，噢，噢，别点我了。');
}</code></pre>

<p>请不要使用 <code>&lt;font&gt;</code> 、 <code>&lt;center&gt;</code> 等表象元素。</p>

<p>在上述的 JavaScript 示例中，<var>para</var> 表示一个段落元素。</p>


<p>按 <kbd>Ctrl</kbd>/<kbd>Cmd</kbd> + <kbd>A</kbd> 选择全部内容。</p>

<pre>$ <kbd>ping mozilla.org</kbd>
<samp>PING mozilla.org (63.245.215.20): 56 data bytes
64 bytes from 63.245.215.20: icmp_seq=0 ttl=40 time=158.233 ms</samp></pre>
```

## HTML文档结构

### 语义化标记

为了实现语义化标记，HTML 提供了明确这些区段的专用标签，例如：

- `<header>`：页眉。
- `<nav>`：导航栏。
- `<main>`:  主内容,主内容中还可以有各种子内容区段等元素表示。可用`<article>`、`<section>`和`<div>`等元素表示。
- `<aside>`:  侧边栏，经常嵌套在`<main>`中
- `<footer>`：页脚  

### 无语义元素

- `<div>`:  啥用没有
- `<span>`:  无语义块级元素，会换行

### 换行和水平分割线

- `<br>`: 换行符
- `<hr>`: 分割线

## HTML中的图片

我们可以用`<img>`元素来把图片放到网页上。它是一个空元素（它不需要包含文本内容或闭合标签），最少只需要一个 `src` 来使其生效。

```html
<img src="./背景.jpg" alt="图片加载不出来时显示的内容">
```

### 备选文本

 `alt` 的值应该是对图片的文字描述，用于在图片无法显示或不能被看到的情况

```html
<img src="./背景.jpg" alt="图片加载不出来时显示的内容">
```

### 图片的高度和宽度

- `width`用于指定图片的宽度 

- `height`用于指定图片的高度

```html
<img src="./背景.jpg" alt="图片加载不出来时显示的内容" width ="1080" height="720">
```

> 如果需要改变图片的尺寸，应该使用CSS而不是HTML

### 图片标题

`title`：鼠标悬浮在图片上时展示`title`中的内容

```html
<img src="./背景.jpg" alt="图片加载不出来时显示的内容" width ="1080" height="720" title="鼠标悬浮在图片上时显示的内容">
```

### 图片语义容器`<figure>`和`<figcaption>`

`<figcaption>`元素: 告诉浏览器和其他辅助的技术工具这段说明文字描述了 `<figure>`元素的内容

## 视频和音频内容

### 视频`<video>`

- `src`：同 `<img>`标签使用方式相同，`src` 属性指向你想要嵌入网页当中的视频资源，他们的使用方式完全相同。
- `controls`:用户必须能够控制视频和音频的回放功能，你可以使用 `controls` 来包含浏览器提供的控件界面
- `<video>`标签中的内容：这个叫做后备内容 — 当浏览器不支持 `<video>` 标签的时候，就会显示这段内容，这使得我们能够对旧的浏览器提供回退内容。
- `width` 和 `height`:你可以用属性控制视频的尺寸
- `autoplay`:这个属性会使音频和视频内容立即播放，即使页面的其他部分还没有加载完全(__在测试的时候中只有和muted搭配使用才有效__)  布尔参数
- `loop`:这个属性可以让音频或者视频文件循环播放 布尔参数
- `muted`:这个属性会导致媒体播放时，默认关闭声音 布尔参数
- `poster`:这个属性指向了一个图像的URL，这个图像会在视频播放前显示。通常用于粗略的预览或者广告。
- `preload`:这个属性被用来缓冲较大的文件，有3个值可选：
  - `"none"` ：不缓冲
  - `"auto"` ：页面加载后缓存媒体文件
  - `"metadata"` ：仅缓冲文件的元数据

#### 使用多个播放源提高兼容性

将 `src` 属性从 `<video>` 标签中移除，转而将它放在几个单独的标签`<source>`当中。在这个例子当中，浏览器将会检查 `<source>` 标签，并且播放第一个与其自身 codec 相匹配的媒体。

```html
<video controls>
  <source src="rabbit320.mp4" type="video/mp4">
  <source src="rabbit320.webm" type="video/webm">
  <p>你的浏览器不支持 HTML5 视频。可点击<a href="rabbit320.mp4">此链接</a>观看</p>
</video>
```

每个 `<source>` 标签页含有一个 `type` 属性，这个属性是可选的，但是建议你添加上这个属性 — 它包含了视频文件的 [MIME types](https://developer.mozilla.org/zh-CN/docs/Glossary/MIME_type) ，同时浏览器也会通过检查这个属性来迅速的跳过那些不支持的格式。如果你没有添加 `type` 属性，浏览器会尝试加载每一个文件，直到找到一个能正确播放的格式，这样会消耗掉大量的时间和资源。

### 音频`<audio>`

同`<video>`的使用方法一致，但是没有`width` 和 `height`

## 表格标签

```html
<table>
    <caption>这是表格的标题</caption>
    <thead>
        <tr><th>姓名</th><th>年龄</th><th>收入</th></tr>
    </thead>
    <tbody>
        <tr><td>喻顺</td><td>23</td><td>1w</td><tr>
    </tbody>
</table>
```

- `<table>`：每一个表格的内容都包含在`<table></tables>`之中
- `<thead>`：表格的表头，语义标签
- `<tbody>`：表格的内容，语义标签
- `<caption>`：表格的标题，语义标签
- `tr`：表格中的行，`<tr></tr>`表示表格中的一行
- `th`：表格中每一列的标题，会让字体居中，加粗
- `td`：表格中的单元格

### 合并单元格

- `colspan`：合并行，占几个单元格的宽度
- `rowspan`：合并列，占几个单元格的高度

```html
<table border="1">
    <caption>这是表格的标题</caption>
    <thead>
        <tr><th>姓名</th><th>年龄</th><th>收入</th></tr>
    </thead>
    <tbody>
        <tr><td rowspan="2" >喻顺</td><td colspan="2">23</td></tr>
        <tr><td>18</td><td>2W</td></tr>
    </tbody>
</table>
```

![image-20220420222355987](https://gitee.com/shunyu-online/shunyu_typora_image/raw/master/image/image-20220420222355987.png)

`colspan`可以和`rowspan`一起使用

```html
<table border="1">
    <caption>这是表格的标题</caption>
    <thead>
        <tr><th>姓名</th><th>年龄</th><th>收入</th></tr>
    </thead>
    <tbody>
        <tr><td rowspan="2" colspan="2">喻顺</td><td colspan="1">23</td></tr>
        <tr><td>18</td></tr>
    </tbody>
</table>
```

![image-20220420222711608](https://gitee.com/shunyu-online/shunyu_typora_image/raw/master/image/image-20220420222711608.png)

### 为表格中的列提供共同的样式

- `<col>` ：定义列中的样式
- `<colgroup>`：`<col>`元素要被包含在<colgroup>

```html
<table>
  <colgroup>
    <col>
    <col style="background-color: yellow">
  </colgroup>
  <tr><th>Data 1</th><th>Data 2</th></tr>
  <tr><td>Calcutta</td><td>Orange</td></tr>
  <tr><td>Robots</td><td>Jazz</td></tr>
</table>
```

每一个`<col>`都会制定每列的样式，对于第一列，没有采取任何样式，但是仍然需要添加一个空的 `<col>` 元素，如果不这样做，那么样式就会应用到第一列上

如果想把这种样式信息应用到每一列，可以只使用一个 `<col>` 元素，不过需要包含 span 属性

```html
<colgroup>
  <col style="background-color: yellow" span="2">
</colgroup>
```

### 嵌套表格

```html
<table border="1">
    <tr>
        <th>title1</th>
        <th>title2</th>
        <th>title3</th>
    </tr>
    <tr>
        <td>
            <table>
                <tr>
                    <td>cell1</td>
                    <td>cell2</td>
                    <td>cell3</td>
                </tr>
            </table>
        </td>
        <td>cell2</td>
        <td>cell3</td>
    </tr>
    <tr>
        <td>cell4</td>
        <td>cell5</td>
        <td>cell6</td>
    </tr>
</table>
```

