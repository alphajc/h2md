# h2md
[![Build Status](https://travis-ci.org/canovie/h2md.svg?branch=master)](https://travis-ci.org/canovie/h2md)
[![PyPI](https://img.shields.io/pypi/v/h2md.svg?style=popout)](https://pypi.org/project/h2md/)
[![GitHub repo size](https://img.shields.io/github/repo-size/canovie/h2md.svg)](https://github.com/canovie/h2md)
[![GitHub](https://img.shields.io/github/license/canovie/h2md.svg)](./LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/h2md.svg)](https://www.python.org/)
[![Twitter Follow](https://img.shields.io/twitter/follow/_canovie.svg?style=social)](https://twitter.com/_canovie)

本项目目的是将html中正文部分转化为markdown文件，部分参考自 [html2md](https://github.com/davidcavazos/html2md)，我把实现方式全改了，第一个 Python 项目，希望能给大家带来帮助。

## 安装

```sh
pip install -U h2md
```

## 用法

使用命令行工具:

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

最时髦的用法：

> 注：使用此方法邮箱可能被保护

```bash
curl -o- https://mydream.ink/archive/iaas-faas-serverless/ | h2md # 标准输出
curl -o- https://mydream.ink/archive/iaas-faas-serverless/ | h2md > xx.md # 输出到 md 文件
curl -o- https://mydream.ink/archive/iaas-faas-serverless/ | h2md >> xx.md # 追加到 md 文件
```