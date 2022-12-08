import json
import sys
import outputs
from configs import PyCodeClass, Functions, ERROR_STRING

# 检查文件是否能够打开
try:
    # 打开文件
    file = open(sys.argv[1], "r", encoding="utf-8")
    codes = json.load(file)
    file.close()
except FileNotFoundError:
    # 报错
    sys.stderr.write("Error! Can't open '" + sys.argv[1] + "'")
    sys.stderr.flush()
    sys.exit()

# 设置一些变量
tab_count = 0

# 代码解析，生成py代码
py_code_class = PyCodeClass()
f = Functions()
outputs.output(codes, py_code_class, f)

# 运行生成结果
exec(py_code_class.py_code)
# 退出
sys.exit()
