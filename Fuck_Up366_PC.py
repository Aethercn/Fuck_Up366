import os
import re
import sys
import tkinter as tk
from tkinter import font, filedialog, messagebox

def main_process():
    print("="*50)
    print("天学网听力的加密就是个蛋")
    print("="*50)
    
    root_temp = tk.Tk()
    root_temp.withdraw()
    
    print("你先下个Reqable，再在天学网电脑客户端里配置代理，开着抓包，Ctrl+F搜fileinfo抓到的包选那个响应体，里面有个downloadUrl，就下载那个，现在是叫Pc.zip，不知道以后会不会改名。下载完了解压，里面的2文件夹随便拖到哪里都行。然后弹出的窗口中选择那个叫2的文件夹，记得解压啊！之后可能天学网会改命名，你找包含 questions 目录的文件夹")
    
    source_path = filedialog.askdirectory(title="选择叫2文件夹或其他包含 questions 目录的文件夹")
    root_temp.destroy()
    
    if not source_path:
        print("未选择路径，退出。")
        input("按回车键退出")
        return

    questions_dir = os.path.join(source_path, "questions")
    if not os.path.exists(questions_dir):
        if os.path.basename(source_path).lower() == 'questions':
            questions_dir = source_path
        else:
            print(f"\n错误：未找到 'questions' 目录！再仔细看看上面那段话\n你选择的路径: {source_path}")
            input("按回车键退出")
            return

    print(f"\n成功定位目录: {questions_dir}")

    js_files_list = []
    print("正在匹配题号...")
    
    for folder_name in os.listdir(questions_dir):
        full_folder_path = os.path.join(questions_dir, folder_name)
        if os.path.isdir(full_folder_path):
            question_num = 999 
            found_by = "未识别"
            
            media_path = os.path.join(full_folder_path, "media")
            if os.path.exists(media_path):
                for f in os.listdir(media_path):
                    if f.lower().endswith(".mp3"):
                        mp3_match = re.search(r'T(\d+)', f, re.IGNORECASE)
                        if mp3_match:
                            question_num = int(mp3_match.group(1))
                            found_by = f"MP3({f})"
                            break
            
            if question_num == 999:
                folder_match = re.search(r'(\d+)', folder_name)
                if folder_match:
                    question_num = int(folder_match.group(1))
                    found_by = f"文件夹名({folder_name})"
            
            target_js_path = None
            net_path = os.path.join(full_folder_path, "net")
            if os.path.exists(net_path):
                for f in os.listdir(net_path):
                    if f.endswith(".js"):
                        target_js_path = os.path.join(net_path, f)
                        break
            
            if not target_js_path:
                for f in os.listdir(full_folder_path):
                    if f.endswith(".js"):
                        target_js_path = os.path.join(full_folder_path, f)
                        break
            
            if target_js_path:
                js_files_list.append((question_num, target_js_path))
                print(f"  [题号 {question_num:02d}] 来源:{found_by:15s} | 文件: {os.path.basename(target_js_path)}")

    if not js_files_list:
        print("\n错误：未找到任何 .js 文件！")
        input("按回车键退出...")
        return

    js_files_list.sort(key=lambda x: x[0])
    print(f"\n已按题号排序合并 {len(js_files_list)} 个文件。")

    combined_content = ""
    for _, js_path in js_files_list:
        try:
            with open(js_path, 'r', encoding='utf-8') as f:
                combined_content += f.read() + "\n"
        except Exception as e:
            try:
                with open(js_path, 'r', encoding='gbk') as f:
                    combined_content += f.read() + "\n"
            except:
                print(f"读取失败: {js_path}")

    print("正在提取答案内容...")
    Outs = []
    
    try:
        pattern = r'"answer_text"(.*?)"knowledge"'
        matches = re.findall(pattern, combined_content, re.DOTALL)
        
        if not matches:
             pattern = r'answer_text(.*?)"knowledge"'
             matches = re.findall(pattern, combined_content, re.DOTALL)
             
        for answer_block in matches:
            opt_match = re.search(r'[A-D]', answer_block)
            if opt_match:
                option = opt_match.group()
                content_pattern = r'"id"\s*:\s*"{}"(.*?)"content"\s*:\s*"(.*?)"'.format(option)
                res = re.search(content_pattern, answer_block, re.DOTALL)
                if res:
                    clean_text = res.group(2).replace('\\"', '"')
                    Outs.append(clean_text)
    except Exception as e:
        print(f"正则提取出错: {e}")

    if not Outs:
        print("\n警告：未提取到答案。请检查文件是否为加密格式(.u3enc)，这个脚本专破加密的哦哦哦哦齁齁齁齁")
        input("按回车键退出...")
        return

    window = tk.Tk()
    window.title(f"成功了就来Github给我点个 Star 吧！ - 共 {len(Outs)} 题")
    window.attributes("-topmost", True)
    window.geometry("600x600")

    custom_font = font.Font(family="微软雅黑", size=12)
    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    text_area = tk.Text(window, font=custom_font, yscrollcommand=scrollbar.set, padx=15, pady=15)
    text_area.pack(fill=tk.BOTH, expand=True)
    
    scrollbar.config(command=text_area.yview)

    for i, out in enumerate(Outs):
        text_area.insert(tk.END, f"{i+1}. {out}\n")
        text_area.insert(tk.END, "-"*40 + "\n")

    print("小菜一碟！")
    window.mainloop()

if __name__ == "__main__":
    try:
        main_process()
    except Exception as e:
        print(f"\n又发生啥事了啊: {e}")
        import traceback
        traceback.print_exc()

        input("按回车键退出...")
