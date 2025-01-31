from lark import Lark, Transformer

variables = {}

class ToMyLang(Transformer):
    def number(self, tree):
        # print(tree)
        token = tree[0].value
        return float(token)

    def var_name(self, tree):
        token = tree[0].value
        return str(token)

    def var(self, tree):
        name = tree[0]
        value = tree[1]
        variables[name] = value

    def show(self, tree):
        target = tree[0]
        if(type(target) == str):
            target = variables[target]
        elif(type(target) == int):
            target = float(target)
        print("表示:", target)


parser = Lark(
    open("./cmd.lark"), parser='lalr',
    transformer=ToMyLang()
)

parser.parse(r"変数 x に 10 を代入")
parser.parse(r"変数 y に 10 を代入")
parser.parse(r"変数 z に 10 を代入")
parser.parse(r"x を表示")
parser.parse(r"40 を表示")
