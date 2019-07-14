# h2md
本项目目的是将html中正文部分转化为markdown文件，部分参考自 [html2md](https://github.com/davidcavazos/html2md)，我把实现方式全改了，第一个 Python 项目，希望能给大家带来帮助。

## 安装

```sh
pip install -U h2md
```

## 用法

As a command line tool:

```sh
# 转换一个文件
h2md examples/hello.html

# 从标准输入读取文件进行转换
cat examples/hello.html | h2md
```

使用 Python 脚本:

```py
import h2md

html = '''
<h1>Header</h1>
<b><i>Hello</i></b> from <code>h2md</code>
<pre class="py"><code>
print('Hello')
</code></pre>
'''

md = h2md.convert(html)
print(md)
```