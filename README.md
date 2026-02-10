# 🥚 Up366 Egg Cracker (天学网听力砸蛋器)

**天学网/Up366 听力答案一键提取工具** 支持 **Windows/Mac** (抓包法) 和 **Android** (无需ROOT，直读法/抓包法)！

> **关于本项目** > 这是一个用于提取天学网（Up366）听力练习答案的 Python 工具。  
> 核心思路来自 B站 视频 [BV1bVGVzNEtA](https://www.bilibili.com/video/BV1bVGVzNEtA/)中的脚本，代码由本仓库作者编写及优化。  
> Android 端直接读取Android/data，无需 Root 权限即可提取。

---

## 📂 文件说明
* `Up366_Egg_Cracker_PC.py`: **电脑端主程序** (需配合抓包工具)
* `Up366_Egg_Cracker_Android.py`: **安卓端主程序** (需配合 MT管理器)

---

## 📺 视频教程

[![还没录](https://github.com/user-attachments/assets/placeholder-image)](https://www.bilibili.com/video/BV1w64y127gu/)
> **[还没录] 还没录** > *点击上方图片或 [此处链接](https://www.bilibili.com/video/BV1w64y127gu/) 跳转至 Bilibili 观看演示*

---

## 🖥️ PC 端使用方法

适用于 Windows / MacOS，原理是通过抓包获取题目下载链接。

1.  **环境准备**：确保安装了 [Python 3](https://www.python.org/downloads/) 并配置好了环境变量。
2.  **工具准备**：下载并安装抓包工具**Reqable**。
3.  **配置抓包**：
    * 在 Reqable 中配置好 CA 证书。
    * 在天学网电脑客户端的设置里配置代理（指向 Reqable 的端口）。
4.  **获取题目**：
    * 开启抓包，点进听力练习，等待下载完毕。
    * 在 Reqable 中 `Ctrl+F` 搜索 `fileinfo` 请求。
    * 在响应体（Response）中找到 `downloadUrl` 字段并复制链接。
    * 下载该链接文件（通常名为 `Pc.zip`）。
5.  **运行脚本**：
    * **解压** `Pc.zip`。
    * 双击运行 `Up366_Egg_Cracker_PC.py`。
    * 在弹窗中选择解压后包含 `questions` 目录的文件夹（通常是一个名为 `2` 的文件夹）。
6.  **查看结果**：脚本将自动解析并显示答案。

---

## 📱 Android 端使用方法 (无需 Root)

用MT管理器直接读取`/Android/data/com.up366.mobile/files/flipbook/随机/随机/2/`下的答案

### 📌 准备工作
下载并安装 **MT管理器** (或其他能访问 `/Android/data` 的文件管理器)。

### 🛠️ 步骤一：环境铺设 (仅首次需要)
1.  在 MT管理器 中找到并点击运行 `Up366_Egg_Cracker_Android.py`。
2.  **脚本会自动检测环境**：
    * 如果提示检测不到 `flipbook` 文件夹，脚本会尝试**自动创建**。
    * *注：如果因系统限制（Android 11+）导致自动创建失败，请按脚本提示手动在 `/Android/data/com.up366.mobile/files/` 下新建名为 `flipbook` 的文件夹。*
3.  环境创建成功后，脚本会暂停，请退出脚本。

### 📥 步骤二：下载题目
1.  打开天学网 App。
2.  **下载**（或清楚应用数据后重新下载）你要做的听力题。
    * *原理：只有在 flipbook 文件夹存在**之后**下载的题目，App 才会将其保存在我们能访问的目录中。*

### 🔓 步骤三：一键提取
1.  回到 MT管理器，**再次运行** `Up366_Egg_Cracker_Android.py`。
2.  脚本会自动定位你刚刚下载的那套题（自动识别最新的题目），并直接显示答案。

> **💡 备用方案 (手动模式)** > 如果你无法访问 data 目录(如部分Android 13/14 用户)，或者你是通过手机抓包下载的 zip：  
> 运行脚本后，如果自动扫描失败，会进入**手动模式**。你可以将包含 `questions` 的文件夹（2）路径复制粘贴进去进行解析。

---

## ⚡ Tips
1.  **低调使用**：建议自己用，不要在班级里大肆张扬，这样往往会出事。
2.  **PC端加速做题**：
    * 如果觉得听力播放太慢，可以使用 **CE修改器 (Cheat Engine)** + **旧版天学网客户端** 开启 20倍速 刷题。
    * 开启加速后，教师端显示的时长依然是正常的（安全）。
    * 参考教程：[B站 BV1xz4y1Y7kc](https://www.bilibili.com/video/BV1xz4y1Y7kc)
3.  **PC端操作参考**：PC端操作可参考 [B站 BV1bVGVzNEtA](https://www.bilibili.com/video/BV1bVGVzNEtA)，但推荐使用本仓库的脚本，**一键自动合并、自动解密、顺序修正**，比视频里的手动操作更省心。  
4.  **需要重新下载听力文件怎么办？**：
    * PC端：去把缓存目录删了（默认为`"C:\Up366StudentFiles"`）
    * Android端：清除应用数据
---

## ⚠️ 免责声明
1.  本项目仅供学习交流使用。
2.  **严禁用于商业用途**（如倒卖答案、倒卖脚本、收费代做等）。
3.  开发者不对使用本工具造成的任何后果（包括但不限于账号被封禁、学业受影响）负责。
4.  祝倒卖脚本的全家只剩半瓶可乐在冒气。

## 📜 License
[MIT License](./LICENSE)
