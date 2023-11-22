import copy

def list_to_str(expr) -> str:
    expr = delete_comma(expr)
    ret = ""
    for i in expr:
        if i == "!":
            ret += "¬" + " "
        elif i == "->":
            ret += "→" + " "
        elif i == "&":
            ret += "∧" + " "
        elif i == "|":
            ret += "∨" + " "
        elif i == "<->":
            ret += "↔" + " "
        elif i == "=>":
            ret += "⇒" + " "
        else:
            ret += i + " "
    return ret

def find_braces(expr) -> list:
    marks, positions, braces = [], [], []
    for i, c in enumerate(expr):
        if c == "(":
            marks.append(-1)
            positions.append(i)
        elif c == ")":
            marks.append(1)
            positions.append(i)
        else:
            continue
        braces_match = sum(marks)
        if braces_match == 0:
            braces.append([positions[0], positions[-1]])
            marks, positions = [], []
    return braces

def find_com_seq(expr) -> list:
    com_seq_list = [-1]
    for i, c in enumerate(expr):
        if c == "," or c == "=>":
            com_seq_list.append(i)
    return com_seq_list

def detect(subsection) -> int:
    braces = find_braces(subsection)
    if subsection[0] == "!":
        return 1
    elif subsection[1] == "->":
        return 2
    elif subsection[1] == "&":
        return 3
    elif subsection[1] == "|":
        return 4
    elif subsection[1] == "<->":
        return 5
    elif braces != []:
        if subsection[braces[0][-1] + 1] == "->":
            return 2
        elif subsection[braces[0][-1] + 1] == "&":
            return 3
        elif subsection[braces[0][-1] + 1] == "|":
            return 4
        elif subsection[braces[0][-1] + 1] == "<->":
            return 5

def find_(expr, com_seq_list):
    t = expr.index("=>")
    if com_seq_list[1] - 1 == com_seq_list[0]:
        com_seq_list.pop(0)
    k = 0
    for i in com_seq_list:
        if (
            i + 2 == len(expr) or expr[i + 2] == "," or expr[i + 2] == "=>"
        ):
            k = k + 1
            continue
        if k + 1 == len(com_seq_list):
            last = len(expr)
        else:
            last = com_seq_list[k + 1]
        subsection = expr[i + 1 : last]
        end = last
        typ = detect(subsection)
        if typ == 1:
            if i < t:
                return not_left(subsection, expr, end - 1, i)
            elif i >= t:
                return not_right(subsection, expr, end - 1, i)
            break
        elif typ == 2:
            if i < t:
                return inclu_left(subsection, expr, end, i)
            elif i >= t:
                return inclu_right(subsection, expr, end, i)
            break
        elif typ == 3:
            return conjuction(subsection, expr, end, i)
        elif typ == 4:
            return division(subsection, expr, end, i)
        elif typ == 5:
            return bi_inclu(subsection, expr, end, i)
        k += 1

def delete_comma(expr) -> list:
    while " " in expr:
        expr.remove(" ")
    for i, c in enumerate(expr):
        if i == len(expr) - 1:
            if c == ",":
                expr.pop()
            break
        elif c == "," and expr[i + 1] == ",":
            expr.pop(i)
        elif c == "," and expr[i + 1] == "=>":
            expr.pop(i)
        elif c == "=>" and expr[i + 1] == ",":
            expr.pop(i + 1)
    return expr

def not_left(subsection, expr, end, beg) -> list:
    subsection.pop(0)
    braces = find_braces(subsection)
    if braces != []:
        subsection.pop(0)
        subsection.pop(-1)
    for x in range(end, beg, -1):
        expr.pop(x)
    expr = delete_comma(expr)
    t = expr.index("=>")
    subsection.append(",")
    subsection.insert(0, "=>")
    expr[t : t + 1] = subsection
    return [[expr, "¬⇒规则", " ", [0]]]

def not_right(subsection, expr, end, beg) -> list:
    subsection.pop(0)
    braces = find_braces(subsection)
    if braces != []:
        subsection.pop(0)
        subsection.pop(-1)
    for x in range(end, beg, -1):
        expr.pop(x)
    expr = delete_comma(expr)
    t = expr.index("=>")
    if t == 0:
        subsection.append("=>")
        expr[t : t + 1] = subsection
    else:
        subsection.insert(0, ",")
        subsection.append("=>")
        expr[t : t + 1] = subsection
    return [[expr, "⇒¬规则", " ", [0]]]

def inclu(subsection) -> int:
    braces = find_braces(subsection)
    if subsection[1] == "->":
        return 1
    else:
        return braces[0][-1] + 1

def inclu_left(subsection, expr, end, i) -> list:
    inc_mark = inclu(subsection)
    subsection_front = subsection[:inc_mark]
    subsection_back = subsection[inc_mark + 1 :]
    kuossy = find_braces(subsection_back)
    if kuossy != []:
        subsection_back.pop(0)
        subsection_back.pop(-1)
    subsection_front.insert(0, "!")
    expr1 = copy.deepcopy(expr)
    expr2 = copy.deepcopy(expr)
    if i == 0:
        i -= 1
    expr1[i + 1 : end] = subsection_front
    expr2[i + 1 : end] = subsection_back
    return [[expr1, "→⇒规则", " ", [0]], [expr2, "→⇒规则", " ", [0]]]

def inclu_right(subsection, expr, end, i) -> list:
    inc_mark = inclu(subsection)
    subsection_front = subsection[:inc_mark]
    subsection_back = subsection[inc_mark + 1 :]
    kuossy = find_braces(subsection_back)
    if kuossy != []:
        subsection_back.pop(0)
        subsection_back.pop(-1)
    subsection_front.insert(0, "!")
    subsection_front_back = subsection_front + [","] + subsection_back
    expr[i + 1 : end] = subsection_front_back
    return [[expr, "⇒→规则", " ", [0]]]

def equiv_trans(expr) -> list:
    if "&" in expr:
        t = expr.index("&")
        para1 = expr[0:t]
        para2 = expr[t + 1 : len(expr)]
        return ["!", "("] + para1 + ["->", "!"] + para2 + [")"]
    elif "|" in expr:
        t = expr.index("|")
        para1 = expr[0:t]
        para2 = expr[t + 1 : len(expr)]
        return ["!"] + para1 + ["->"] + para2
    elif "<->" in expr:
        t = expr.index("<->")
        para1 = expr[0:t]
        para2 = expr[t + 1 : len(expr)]
        return (
            ["!", "(", "("]
            + para1
            + ["->"]
            + para2
            + [")", "->", "(", "!", "("]
            + para2
            + ["->"]
            + para1
            + [")", ")", ")"]
        )

def conjuction(subsection, expr, end, i):
    subsection = equiv_trans(subsection)
    expr[i + 1 : end] = subsection
    return [[expr, "∧等价变换", " ", [0]]]

def division(subsection, expr, end, i):
    subsection = equiv_trans(subsection)
    expr[i + 1 : end] = subsection
    return [[expr, "∨等价变换", " ", [0]]]

def bi_inclu(subsection, expr, end, i):
    subsection = equiv_trans(subsection)
    expr[i + 1 : end] = subsection
    return [[expr, "↔等价变换", " ", [0]]]

if __name__ == "__main__":
    s = input('输入要证明的公式，公式以=>开始，符号与字母之间以空格分割（包括括号）。直接按回车，将使用默认的演示示例：\n')
    if s=="":
        s = "=> ( a -> c ) -> ( ( b -> c ) -> ( ( a | b ) -> c ) )"
        print('默认的演示示例：',s)
    expr = s.split()
    step = 0
    stock = []
    stock.append([expr, "不是公理", " ", [0]])
    resolution = []
    while stock:
        step = step + 1
        y = 0
        current_expr = stock.pop()
        expr = current_expr[0]
        if (
            "->" not in expr
            and "!" not in expr
            and "|" not in expr
            and "&" not in expr
            and "<->" not in expr
        ):
            d = expr.index("=>")
            expr1 = expr[:d]
            expr2 = expr[d + 1 :]
            for i in expr1:
                if i != ",":
                    if i in expr2:
                        resolution.append(
                            [list_to_str(expr), current_expr[1], "公理", current_expr[3]]
                        )
                        break
                    else:
                        y = y + 1
            for i in expr1:
                if i == ",":
                    expr1.remove(i)
            if y == len(expr1):
                resolution.append(
                    [list_to_str(expr), current_expr[1], "不是公理", current_expr[3]]
                )
                break
            continue
        resolution.append(
            [list_to_str(expr), current_expr[1], current_expr[2], current_expr[3]]
        )
        com_seq_list = find_com_seq(expr)
        f = find_(expr, com_seq_list)
        for i in range(len(f)):
            f[i][3] = [current_expr[3][0] + i]
            stock.append(f[i])
    for i in resolution:
        if i[2] == "不是公理":
            print("推理失败\t" + i[0] + i[2])
    k = []
    for i in range(len(resolution)):
        k.append([len(resolution) - i, resolution[i][3][0]])

    rule3 = []
    for x in range(len(k) - 1):
        if k[x][1] == k[x + 1][1] - 1:
            for i in range(x + 1, len(k)):
                if k[i][1] == k[x][1]:
                    index = i
                    rule3.append([k[x][0], k[index][0], k[x + 1][0]])
                    break

    resolution.reverse()
    p = []
    for i, r in enumerate(resolution):
        flag = 1
        for x in rule3:
            if i + 1 == x[0]:
                p.append(
                    [r[0], str(x[1]) + "、" + str(x[2]) + " " + resolution[i - 1][1]]
                )
                flag = 0
        if flag == 1:
            if r[2] == "公理":
                p.append([r[0], "公理"])
            else:
                p.append([r[0], str(i) + " " + resolution[i - 1][1]])
    print("_" * 100)
    for i in range(len(p)):
        print(
            "{:>3}".format(str(i + 1)) + ")", "{:<60}".format(p[i][0]), "\t\t", p[i][1]
        )
    print("{:>80}\n".format("Q.E.D."))