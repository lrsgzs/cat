from configs import *
import sys


def output(codes, pcc, f, tab_count=0):
    i = 0
    print_end = "\\n"

    for code in codes:
        if code[0] == "print":  # 打印函数
            cout = []  # 打印内容
            for values in code[1]:  # 遍历参数
                if isinstance(values, dict):  # 检查类型
                    for key in values.keys():  # 遍历字典
                        if key == "end":  # 同print的end参数
                            print_end = values[key].replace("\n", "\\n")
                        else:
                            # 没有这种参数就报错
                            error = ERROR_STRING.replace("{{file}}", sys.argv[1])
                            error = error.replace("{{code}}", code.__str__())
                            error = error.replace("{{error}}", "KeyError")
                            error = error.replace("{{text}}", "Not has '" + key + "' key.")

                            sys.stderr.write(error)
                            sys.stderr.flush()
                            sys.exit()
                elif isinstance(values, list):
                    # 遍历参数
                    for text in values:
                        cout.append(text)  # 添加到打印内容
                else:
                    # 不是支持的类型就报错
                    error = ERROR_STRING.replace("{{file}}", sys.argv[1])
                    error = error.replace("{{code}}", code.__str__())
                    error = error.replace("{{error}}", "TypeError")
                    error = error.replace("{{text}}", "Not has this type in function.")

                    sys.stderr.write(error)
                    sys.stderr.flush()
                    sys.exit()
            if not cout:
                # 如果没有要打印的内容，就打印end参数（end参数默认是换行符
                pcc.py_code = pcc.py_code + tab_count * TAB_STRING + "print(end='" + print_end + "')\n"
            else:
                # 打印内容
                texts = ""
                for text in cout:
                    # 字符串
                    if isinstance(text, str):
                        if text[:2] == "^%" or text[-1:] == "%^":  # 变量
                            text = text[2:-2]  # 提取变量
                        else:  # 普通字符串
                            text = "'" + text + "'"  # 组成字符串
                    else:  # 其他字符
                        text = str(text)  # 转成字符串
                    texts = texts + text + ", "  # 加个逗号
                # 组成代码
                pcc.py_code = pcc.py_code + tab_count * TAB_STRING + "print(" + texts + "end='" + print_end + "')\n"
        elif code[0] == "def":  # 定义函数
            def_name = code[1]  # 名字
            def_ages = code[2]["args"]  # 参数
            def_code = code[2]["code"]  # 代码
            def_age = ""  # 参数字符串

            f.functions.append(def_name)  # 添加到函数表里
            for word in def_ages:  # 组成Python能理解的参数表
                def_age = def_age + word + ", "  # 组成

            pcc.py_code = pcc.py_code + tab_count * TAB_STRING + "def " + def_name + "(" + def_age + "):\n"  # 添加到代码
            output(def_code, pcc, f, tab_count=tab_count + 1)  # 递归这个函数的代码
        elif code[0] == "raise":
            # 报错函数
            # 没有详细内容，只有raise
            try:
                _ = code[1]
            except:
                code.append(["BaseError", "Default Error Text."])

            # 没有文本
            try:
                _ = code[1][1]
            except:
                code[1].append("Default Error Text.")

            tmp = """
exec('''error = ERROR_STRING.replace("{{file}}", """ + repr(repr(sys.argv[1])) + """)
error = error.replace("{{code}}", """ + repr(code.__str__()) + """)
error = error.replace("{{error}}", """ + repr(str(code[1][0])) + """)
error = error.replace("{{text}}", """ + repr(str(code[1][1])) + """)

sys.stderr.write(error)
sys.stderr.flush()
sys.exit()''')
"""
            pcc.py_code = pcc.py_code + TAB_STRING * tab_count + tmp
        else:
            if code[0] in f.functions:  # 在函数表里
                tmp_code = ""  # 临时代码
                tmp_code = tmp_code + code[0] + "("  # 函数左边
                argc = ""  # 普通参数
                argv = ""  # 字典型参数
                for arg in code[1]:  # 参数组成
                    if isinstance(arg, list):  # 普通
                        for arg_c in arg:  # 组成
                            if isinstance(arg_c, str):  # 字符串
                                if arg_c[:2] == "^%" or arg_c[-1:] == "%^":  # 变量
                                    argc = argc + arg_c[2:-2] + ", "  # 提取变量
                                else:  # 普通字符串
                                    argc = argc + repr(arg_c) + ", "  # 组成
                            else:  # 别的东西
                                argc = argc + repr(arg_c) + ", "  # 组成
                    elif isinstance(arg, dict):  # 高级
                        for arg_v in arg.keys():  # 组成
                            argv = argv + arg_v + "=" + repr(arg[arg_v]) + ", "  # 组成
                    else:
                        # 不是支持的类型就报错
                        error = ERROR_STRING.replace("{{file}}", sys.argv[1])
                        error = error.replace("{{code}}", code.__str__())
                        error = error.replace("{{error}}", "TypeError")
                        error = error.replace("{{text}}", "Not has this type in function.")

                        sys.stderr.write(error)
                        sys.stderr.flush()
                        sys.exit()
                tmp_code = tmp_code + argc + argv + ")"  # 组成一行完整的代码
                pcc.py_code = pcc.py_code + tmp_code + "\n"  # 添加到代码
            else:
                # 没有这个函数就报错
                error = ERROR_STRING.replace("{{file}}", sys.argv[1])
                error = error.replace("{{code}}", code.__str__())
                error = error.replace("{{error}}", "FunctionError")
                error = error.replace("{{text}}", "Not has '" + code[0] + "' function.")

                sys.stderr.write(error)
                sys.stderr.flush()
                sys.exit()

        # 设置变量
        print_end = "\\n"
        i = i + 1
