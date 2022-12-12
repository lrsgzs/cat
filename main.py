import json
import sys
from outputs import output
from configs import PyCodeClass, Functions, ERROR_STRING
import configs

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
except IndexError:
    # 索引错误，问名字
    sys.argv.append(input("File Name > "))

    # 打开文件
    file = open(sys.argv[1], "r", encoding="utf-8")
    codes = json.load(file)
    file.close()

print("\n-----STARTING-----\n")

# 设置一些变量
tab_count = 0

# 垃圾代码区
repr(ERROR_STRING)

# 代码解析，生成py代码
configs.cons.pcc = PyCodeClass()
configs.cons.f = Functions()
output(codes)

# 运行生成结果
exec(configs.cons.pcc.py_code)

# 退出
sys.exit()
