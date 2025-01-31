from lark import Lark, Transformer

def gethead(funclist):
    res = ""
    for i in range(len(funclist)):
        if funclist[i] == "length":
            res = res + f"(defun orifunc{i} (lst)(cond((eq lst '()) 0)(t (+ 1 (orifunc{i} (cdr lst))))))"
        elif funclist[i] == "push":
            res = res + f"(defun orifunc{i} (item list)(cons item list))"
    return res

class LispTransformer(Transformer):
    func = []
    fnum = 0
    def start(self, tree):
        head = gethead(self.func)
        return head + tree[0][0]
    def code(self, tree):
        return tree
    def list(self, tree):
        return tree[0]
    def basefunc(self, tree):
        return f"({' '.join(map(str, tree))})"
    def adfunc(self, tree):
        return f"({' '.join(map(str, tree))})"
    def nlist(self, tree):
        return f"({' '.join(map(str, tree))})"
    def qlist(self, tree):
        return f"(quote ({' '.join(map(str, tree))}))"
    def expr(self, tree):
        return tree[0]
    def originword(self, tree):
        return tree[0]
    def adword(self, tree):
        return tree[0]
    def atom(self, tree):
        return tree[0]
    def cname(self, tree):
        return str(tree[0])
    def number(self, tree):
        return tree[0]#float(tree[0]) if '.' in tree else int(tree[0])
    def length(self, tree):
        self.fnum += 1
        self.func.append("length")
        return f"orifunc{self.fnum-1}"
    def car(self, tree):
        return "car"
    def cdr(self, tree):
        return "cdr"
    def eq(self, tree):
        return "eq"
    def cons(self, tree):
        return "cons"
    def defun(self, tree):
        return "defun"
    def cond(self, tree):
        return "cond"
    def quote(self, tree):
        return "quote"
    def _lambda(self, tree):
        return "lambda"
    def plus(self, tree):
        return "+"
    def minus(self, tree):
        return "-"


# 文法の読み込み
with open("grammar.lark", "r") as file:
    lisp_grammar = file.read()
parser = Lark(lisp_grammar, parser='lalr', transformer=LispTransformer())

# 構文解析と変換
print(parser.parse("(car (quote(1 2 4)))"))
print(parser.parse("(car '(1 2 4))"))
print(parser.parse("(length '(1 2 4))"))