# Output parser

## 概述
现在当下大模型主要输出的文本形式，输出格式根据我们 prompt 中要求，可以按要求输出结构化的数据，例如类似 json、xml 或者 csv 这样常见的结构化格式来组数输出结构，好处更容易和其他进行对接

对于 parser 主要输入一段文本，输出一个结构化的数据，parpser 主要有两个用途