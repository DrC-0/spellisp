import re
from lark import Transformer, Lark
from functools import reduce

def devideCode(lispcode):
    with open(lispcode, "r") as file:
        data = file.readlines()
    data = [line.strip() for line in data]

    # ネストが閉じていない場合に行を結合
    combined_data = []
    temp_line = ""
    for line in data:
        temp_line += line
        if temp_line.count('(') == temp_line.count(')') and temp_line.count('(') != 0:
            combined_data.append(temp_line)
            temp_line = ""
    
    return combined_data

def divide(line,word):
    if word in line:
        #lineをwordで分割し,wordより前の部分,word,wordより後の部分をリストにして返す
        parts = line.split(word)
        before_push = parts[0]
        after_push = parts[1]
        return before_push, word, after_push
    return line

class lispTransformer(Transformer):
    def start(self, tree):
        return tree
    
    def list(self, tree):
        return tree
    
    def atom(self, tree):
        return tree[0]
    def symbol(self, tree):
        return tree[0]
    def number(self, tree):
        return int(tree[0])


def split_line(line, word):
    if word in line:
        print(line)
        parts = line.split(word)
        before_push = parts[0]
        after_push = parts[1]

        # 正規表現でネストを考慮して分割
        pattern = re.compile(r'^[^()]*\((?:[^()]*\([^()]*\))*[^()]*\)[^()]*')
        matches = pattern.split(after_push, 1)
        first_part = pattern.match(after_push).group().strip()
        
        if len(matches) > 1:
            second_part = matches[1]
            return before_push, first_part, second_part
        else:
            return before_push, after_push
    return line

def split_elem(line):
    elems = [line]
    flag = True
    while flag:
        flag = False
        for i in range(len(elems)):
            elem = elems[i]
            print(elem)
            if "(" not in elem or ")" not in elem:
                continue
            front = elem.index("(")
            back = elem.rfind(")")
            #lineからfrontとbackの間を取り出す
            if front == -1 or back == -1:
                continue
            print(front, back)
            if front != 0 or back != len(elem)-1:
                print("wooooo\n")
                flag = True
                new_elem = elems.pop(i)[front:back+1]
                elems = elems[:i]+ [elem.partition(new_elem).strip()] + elems[i:]
    return elems

def purelizeLisp(rawcode):
    #以下が何も含まれなくなるまで繰り返す
    flag = True
    while flag:
        flag = False
        for line in rawcode:
            #pushが含まれる場合変換
            if "push" in line:
                text = divide(line, "push")
                print(text)
                flag = True
                pass
            else:
                flag = False
                pass




def main():
    # lispcode = "test.lisp"
    # rawcode = devideCode(lispcode)
    # print(rawcode)
    # purelizeLisp(rawcode)
    code = "(+ 1 2)"
    with open("grammar.lark", "r") as grammar:
        parser = Lark(grammar.read(), parser="lalr")
    tree = parser.parse(code)
    print(tree)


if __name__ == "__main__":
    main()