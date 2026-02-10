#!/system/bin/sh

# =========================================================
# 🥚 Up366 听力砸蛋器 (修复错题版)
# 修复了之前版本因正则贪婪匹配导致抓取到错误选项内容的 Bug
# =========================================================

echo "========================================"
echo "   🥚 Up366 听力砸蛋器 (Shell版)   "
echo "========================================"

CURRENT_DIR=$(dirname "$0")
cd "$CURRENT_DIR" || exit

JS_FILES=$(find . -name "*.js" 2>/dev/null)

if [ -z "$JS_FILES" ]; then
    echo "❌ 未找到 .js 文件，请确认脚本在 '2' 文件夹内。"
    exit 1
fi

TMP_FILE="./up366_raw.txt"
PARSED_FILE="./up366_parsed.txt"
rm -f "$TMP_FILE" "$PARSED_FILE"

# 合并文件
echo "$JS_FILES" | while read -r f; do
    if [ -f "$f" ] && grep -q "answer_text" "$f"; then
        cat "$f" >> "$TMP_FILE"
        echo "" >> "$TMP_FILE"
    fi
done

if [ ! -s "$TMP_FILE" ]; then
    echo "❌ 未找到题目文件。"
    rm -f "$TMP_FILE"
    exit 1
fi

echo "✅ 正在解析 (已修正匹配逻辑)..."
echo ""

# 预处理
cat "$TMP_FILE" | sed 's/\\"/"/g' | sed 's/"answer_text"/\nANSWER_BLOCK_START/g' | grep "ANSWER_BLOCK_START" > "$PARSED_FILE"

count=1
echo "🎉 答案列表 🎉"
echo "----------------------------------------"

while read -r line; do
    # 1. 截取 block
    block=$(echo "$line" | sed 's/"knowledge".*//')
    
    # 2. 提取正确选项 (A/B/C/D)
    opt=$(echo "$block" | grep -o "[A-D]" | head -n 1)
    
    if [ -n "$opt" ]; then
        # 3. 核心修复：使用变量截取代替 sed 正则，避免贪婪匹配错位
        
        # 标记目标ID位置，例如把 "id":"A" 替换为 MARKER
        # 这一步能精确定位到正确选项的起始位置
        temp_str=$(echo "$block" | sed "s/\"id\":\"$opt\"/MARKER/")
        
        # 截取 MARKER 之后的内容 (去掉了 MARKER 之前的所有干扰项)
        after_id=${temp_str#*MARKER}
        
        # 在剩下的字符串里，找紧接着的 "content":"
        # 截取 "content":" 之后的内容
        after_content=${after_id#*\"content\":\"}
        
        # 截取第一个引号的内容 (即答案文本)
        # %%\"* 表示从右边删除，直到保留第一个引号左边的内容
        final_answer=${after_content%%\"*}
        
        if [ -n "$final_answer" ]; then
            echo "[$count] $final_answer"
            echo "----------------------------------------"
            count=$((count + 1))
        fi
    fi
done < "$PARSED_FILE"

rm -f "$TMP_FILE" "$PARSED_FILE"

if [ $count -eq 1 ]; then
    echo "⚠️  未提取到答案。"
else
    echo ""
    echo "✅ 提取结束 (共 $((count - 1)) 题)"
fi
