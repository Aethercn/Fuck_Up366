# Up366 听力答案提取工具 (Up366-Answer-Extractor/Up366-Egg-Cracker)
天学网/Up366听力答案获取，支持电脑和手机！（手机无需ROOT）目前仅支持获取听力答案
这是一个用于提取天学网（Up366）听力练习答案的 Python 工具。思路来自B站BV1bVGVzNEtA，代码由我编写
支持PC和Android（还在做），PC用户请使用Fuck_Up366_PC  Android用户请使用Fuck_Up366_Android

## 前置准备 (非常重要！)

## PC端使用方法
1.确保安装了 Python 3并配置好了PATH。
2. 下载并安装抓包工具 **Reqable**。
3.配置Reqable证书
4. 在天学网电脑客户端配置代理，开启抓包。
5. 点进练习，等待下载完毕。
6. Reqable中Ctrl+F搜索 `fileinfo` 请求。
7. 找到`fileinfo`的响应体中的 `downloadUrl`  并下载(通常是 `Pc.zip`)。
8. 解压`Pc.zip`（也有可能是其他的）
9. 双击脚本
10. 选择解压后的包含 `questions` 目录的文件夹（通常叫 `2`）。
11. 查看答案

## Android端使用方法
等会写，总之要用到MT管理器

## Tips
建议您低调使用，不建议张扬
PC端如果觉得做听力速度太慢，可以使用CE修改器+旧版天学网客户端加速20倍做题（教师端时长显示正常），参考教程：B站BV1xz4y1Y7kc
PC端大部分操作可以参考B站BV1bVGVzNEtA，脚本推荐使用我的，更省心，一键获取，顺序正确

## 免责声明
本项目仅供学习交流使用，请勿用于商业用途或作弊。开发者不对使用本工具造成的任何后果负责。
