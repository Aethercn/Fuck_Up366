import os
import re
import time
import sys

# ==========================================
# 配置区域
# ==========================================
DEFAULT_BASE_PATH = "/storage/emulated/0/Android/data/com.up366.mobile/files/flipbook"
EXCLUDE_DIRS = ['bookres', 'images', 'resources', 'checkFile', 'config.json', 'index.html', 'valid.bin']

def get_latest_dir(parent_path, exclude_list=[]):
    """返回目录下修改时间最新的子文件夹"""
    if not os.path.exists(parent_path): return None
    try:
        all_items = [os.path.join(parent_path, d) for d in os.listdir(parent_path)]
        valid_dirs = [p for p in all_items if os.path.isdir(p) and os.path.basename(p) not in exclude_list]
        if not valid_dirs: return None
        valid_dirs.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return valid_dirs[0]
    except Exception:
        return None

def extract_from_path(target_path):
    """核心提取逻辑：在指定路径下找题、解密、输出"""
    js_files = []
    print(f"[*] 正在深度扫描: {target_path}")
    
    for root, dirs, files in os.walk(target_path):
        if "questions" in root or "net" in root or root == target_path: 
             for file in files:
                if file.endswith(".js"):
                    full_path = os.path.join(root, file)
                    q_num = 999
                    
                    # 1. 找MP3定题号
                    potential_media = [
                        os.path.join(root, "media"),
                        os.path.join(os.path.dirname(root), "media"),
                        os.path.join(os.path.dirname(os.path.dirname(root)), "media")
                    ]
                    for m_dir in potential_media:
                        if os.path.exists(m_dir):
                            for f in os.listdir(m_dir):
                                if f.lower().endswith(".mp3"):
                                    res = re.search(r'T(\d+)', f, re.IGNORECASE)
                                    if res: q_num = int(res.group(1)); break
                            if q_num != 999: break
                    
                    # 2. 找文件夹名定题号
                    if q_num == 999:
                        parts = full_path.split(os.sep)
                        for part in reversed(parts):
                            if part.lower() in ["questions", "net", "media"]: continue
                            if part.isdigit(): q_num = int(part); break

                    js_files.append((q_num, full_path))

    if not js_files:
        print("❌ 未找到题目文件 (.js)。请确认路径正确且已下载题目。")
        return False

    js_files.sort(key=lambda x: x[0])
    print(f"[+] 找到 {len(js_files)} 个文件片段，正在解密...")
    
    combined = ""
    for _, p in js_files:
        try:
            with open(p, 'r', encoding='utf-8') as f: combined += f.read() + "\n"
        except: pass

    Outs = []
    # 正则提取
    blocks = re.findall(r'"answer_text"(.*?)"knowledge"', combined, re.DOTALL)
    if not blocks: blocks = re.findall(r'answer_text(.*?)"knowledge"', combined, re.DOTALL)

    for b in blocks:
        opt = re.search(r'[A-D]', b)
        if opt:
            res = re.search(r'"id"\s*:\s*"{}"(.*?)"content"\s*:\s*"(.*?)"'.format(opt.group()), b, re.DOTALL)
            if res: Outs.append(res.group(2).replace('\\"', '"'))

    print("\n" + "="*15 + f" 🎉 答案 (共{len(Outs)}题) 🎉 " + "="*15)
    if not Outs:
        print("⚠️  未提取到答案 (可能文件已加密或格式变更)")
    else:
        for i, ans in enumerate(Outs):
            print(f"[{i+1}] {ans}")
            print("-" * 30)
    print("="*40)
    return True

def manual_mode():
    """手动模式"""
    print("\n" + "-"*30)
    print("🛠️ 进入手动模式")
    print("请输入(或粘贴)包含 'questions' 的文件夹路径")
    print("适用：抓包解压后的路径 / 高版本安卓路径")
    print("-" * 30)
    while True:
        p = input("路径 > ").strip().replace('"', '').replace("'", "")
        if not p: continue
        if os.path.exists(p):
            extract_from_path(p)
            break
        else:
            print(f"❌ 路径不存在: {p}")

def main():
    print("="*40)
    print("🥚 Up366 听力砸蛋器 (Android)")
    print("="*40)

    # ---------------------------------------------------------
    # 阶段 1: “铺路” (环境检测与创建)
    # ---------------------------------------------------------
    if not os.path.exists(DEFAULT_BASE_PATH):
        print(f"[!] 检测到 flipbook 文件夹不存在")
        print(f"[*] 正在尝试自动创建...")
        try:
            os.makedirs(DEFAULT_BASE_PATH, exist_ok=True)
            print("\n✅ 自动创建成功！")
            print("🛑 脚本已暂停。请执行以下步骤：")
            print("1. 打开天学网 App")
            print("2. 下载/重新下载你要做的听力题")
            print("3. 再次运行本脚本查看答案")
            input("按回车键退出...")
            return
        except PermissionError:
            print("\n❌ 自动创建失败 (权限不足)")
            print("请手动操作：")
            print("1. 用 MT管理器 进入 /Android/data/com.up366.mobile/files/")
            print("2. 新建名为 flipbook 的文件夹")
            print("3. 去 App 下载题目，然后重试脚本")
            input("按回车键退出...")
            return

    # ---------------------------------------------------------
    # 阶段 2: “跑车” (尝试自动提取)
    # ---------------------------------------------------------
    print("[*] 正在尝试自动定位题目...")
    auto_success = False
    
    try:
        # 找最新用户 -> 找最新书本
        user_dir = get_latest_dir(DEFAULT_BASE_PATH)
        if user_dir:
            book_dir = get_latest_dir(user_dir, EXCLUDE_DIRS)
            if book_dir:
                print(f"[+] 锁定目标: {os.path.basename(book_dir)}")
                auto_success = extract_from_path(book_dir)
            else:
                print("[!] 找到用户目录，但没找到书本目录 (请确认已下载题目)")
        else:
            print("[!] flipbook 目录为空 (请先去 App 下载题目)")
            
    except PermissionError:
        print("[!] 无权访问 Android/data (高版本安卓限制)")
    except Exception as e:
        print(f"[!] 自动扫描出错: {e}")

    # ---------------------------------------------------------
    # 阶段 3: 兜底 (手动模式)
    # ---------------------------------------------------------
    if not auto_success:
        print("\n[?] 自动提取未成功，是否切换到手动模式？")
        choice = input("输入 'y' 进入手动模式，直接回车退出: ").strip().lower()
        if choice == 'y':
            manual_mode()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
        input()
