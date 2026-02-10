#!/system/bin/sh

# =========================================================
# 🥚 Up366 听力砸蛋器
# Android Version By Aether
# =========================================================

echo "========================================"
echo "   🥚 Up366 听力砸蛋器   "
echo "========================================"

CURRENT_DIR=$(dirname "$0")
cd "$CURRENT_DIR" || exit

# 1. 查找 .js 文件
JS_FILES=$(find . -name "*.js" 2>/dev/null)

if [ -z "$JS_FILES" ]; then
    echo "❌ 未找到 .js 文件，请确认脚本在 '2' 文件夹内。"
    exit 1
fi

# 2. 创建临时文件
TMP_FILE="./up366_raw.txt"
PARSED_FILE="./up366_parsed.txt"
rm -f "$TMP_FILE" "$PARSED_FILE"

# 3. 合并文件
echo "$JS_FILES" | while read -r f; do
    if [ -f "$f" ] && grep -q "answer_text" "$f"; then
        cat "$f" >> "$TMP_FILE"
        echo "" >> "$TMP_FILE"
    fi
done

if [ ! -s "$TMP_FILE" ]; then
    echo "❌ 未找到包含答案的题目文件。"
    rm -f "$TMP_FILE"
    exit 1
fi

echo "✅ 正在解析..."
echo ""

# 4. 预处理并写入中间文件 (避开管道子shell问题)
cat "$TMP_FILE" | sed 's/\\"/"/g' | sed 's/"answer_text"/\nANSWER_BLOCK_START/g' | grep "ANSWER_BLOCK_START" > "$PARSED_FILE"

# 5. 读取解析
count=1
echo "🎉 答案列表 🎉"
echo "----------------------------------------"

while read -r line; do
    # 截取直到 "knowledge"
    block=$(echo "$line" | sed 's/"knowledge".*//')
    
    # 提取选项字母
    opt=$(echo "$block" | grep -o "[A-D]" | head -n 1)
    
    if [ -n "$opt" ]; then
        # 提取内容
        content=$(echo "$block" | sed -n "s/.*\"id\":\"$opt\".*\"content\":\"\([^\"]*\)\".*/\1/p")
        
        if [ -n "$content" ]; then
            echo "[$count] $content"
            echo "----------------------------------------"
            count=$((count + 1))
        fi
    fi
done < "$PARSED_FILE"

# 清理
rm -f "$TMP_FILE" "$PARSED_FILE"

if [ $count -eq 1 ]; then
    echo "⚠️  未提取到答案。"
else
    echo ""
    echo "✅ 提取结束 (共 $((count - 1)) 题)"
fi