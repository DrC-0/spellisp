from lark import  Lark, Tree
import math
import random
from cairosvg import svg2png

def getcircleinf(px, py, pr, child_count):
    res = []
    rd = random.randint(0, 180)
    if child_count > 2:
        for i in range(child_count):
            angle = 360 / child_count * i + rd
            c = math.sin(math.radians(360 / child_count))
            rn = pr / (1 + c)
            r = rn * c
            x = px + rn * math.cos(math.radians(angle))
            y = py + rn * math.sin(math.radians(angle))
            res.append([x, y, r])
    elif child_count == 1:
        res.append([px, py, pr *0.95])
    elif child_count == 2:
        res.append([px + pr / 2 * math.cos(math.radians(90+rd)), py + pr / 2 * math.sin(math.radians(90+rd)), pr / 2])
        res.append([px + pr / 2 * math.cos(math.radians(270+rd)), py + pr / 2 * math.sin(math.radians(270+rd)), pr / 2])
    return res

def getpolyinf(px, py, pr, child_count):
    res = []
    rd = random.randint(0, 360)
    if child_count > 0:
        for i in range(child_count):
            angle = 360 / child_count * i + rd
            x = px + pr * math.cos(math.radians(angle))
            y = py + pr * math.sin(math.radians(angle))
            res.append([x, y])
    else :
        print("less than 1  children")
    return res

def circlepath(x, y, r, n):
    rd = random.randint(0, 360)
    dx = r * math.cos(math.radians(rd)) 
    dy = r * math.sin(math.radians(rd))
    return f'<path id="Path{n}" d="M {x-dx},{y-dy} A {r},{r} 0 1,1 {x+dx},{y+dy} A {r},{r} 0 1,1 {x-dx},{y-dy}" />'

def linepath(x1, y1, x2, y2, n):
    return f'<path id="Path{n}" d="M {x1},{y1} L {x2},{y2}" />'

def getpolypath(xylist):
    res = []
    if len(xylist) > 1:
        for i in range(len(xylist)):
            if i == len(xylist) - 1:
                res.append([xylist[i][0], xylist[i][1], xylist[0][0], xylist[0][1]])
            else:
                res.append([xylist[i][0], xylist[i][1], xylist[i+1][0], xylist[i+1][1]])
        return res
    else:
        return xylist

def tree_depth(tree):
    if not isinstance(tree, Tree) or not tree.children:
        return 0
    return 1 + max((tree_depth(child) for child in tree.children if isinstance(child, Tree)), default=0)

def isCircle(tree):
    return tree.data in {"start", "code", "list"}

def count_child_atom(tree):
    return sum(1 for child in tree.children if isinstance(child, Tree) and child.data == "atom")

def count_child_list(tree):
    return sum(1 for child in tree.children if isinstance(child, Tree) and child.data == "list")

def get_max_childatom_length(tree):
    max = 0
    if not tree.data == "list":
        return max
    for child in tree.children:
        if child.data != "atom":
            return 0
        text = child.children[0].children[0]
        if text > max:
            max = text
    return max

def traverse_tree(tree, px, py, pr, svg_elements, defs_elements, path_counter):
    if isinstance(tree,Tree):
        if isCircle(tree):
            atom_count = count_child_atom(tree)
            list_count = count_child_list(tree)
            child_count = len(tree.children)
            if child_count == atom_count:
                poly_info = getpolyinf(px, py, pr, child_count)
                svg_elements.append(f'<circle cx="{px}" cy="{py}" r="{pr}" stroke="black" stroke-width="1" fill="none"/>')
                svg_elements.append(f'<polygon points="{" ".join([f"{x},{y}" for x, y in poly_info])}" fill="black" />')
                in_circ = pr * math.cos(math.radians(180 / child_count))
                svg_elements.append(f'<circle cx="{px}" cy="{py}" r="{in_circ}" fill="white"/>')
                points = getpolypath(poly_info)
                # get_max_childatom_length(tree)

                for i, child in enumerate(tree.children):
                    if child_count > 2:
                        text_size = pr * 5 / 7 * (1 - math.cos(math.radians(180 / child_count)))
                        path = len(defs_elements)
                        defs_elements.append(linepath(points[i][0],points[i][1],points[i][2],points[i][3], path))
                        traverse_tree(child, 1, text_size, 50, svg_elements, defs_elements, path)
                    else:
                        text_size = 10
                        traverse_tree(child, 1, text_size, 50, svg_elements, defs_elements, path_counter)
            elif atom_count != 0 and child_count == list_count + atom_count:
                in_circ = pr * 0.9
                svg_elements.append(f'<circle cx="{px}" cy="{py}" r="{pr}" fill="black" />')
                svg_elements.append(f'<circle cx="{px}" cy="{py}" r="{in_circ}" fill="white" />')
                circle_info = getcircleinf(px, py, in_circ, list_count)
                poly_info = getpolyinf(px, py, pr, atom_count)
                # text_info = gettextinf(poly_info)
                t = 0
                c = 0
                path = len(defs_elements)
                text_size = (pr - in_circ) * 5 / 7
                defs_elements.append(circlepath(px, py, (pr+3*in_circ)/4, path))
                for child in tree.children:
                    if child.data == "list":
                        traverse_tree(child, circle_info[c][0], circle_info[c][1], circle_info[c][2], svg_elements, defs_elements, path_counter)
                        c += 1
                    elif child.data == "atom":
                        traverse_tree(child, 0, text_size, (50/atom_count)+100/atom_count*t, svg_elements, defs_elements, path)
                        t += 1
            else :
                svg_elements.append(f'<circle cx="{px}" cy="{py}" r="{pr}" stroke="black" stroke-width="1" fill="none" />')
                circle_info = getcircleinf(px, py, pr, child_count)
                for i, child in enumerate(tree.children):
                    traverse_tree(child, circle_info[i][0], circle_info[i][1], circle_info[i][2], svg_elements, defs_elements, path_counter)
                    
        else:
            traverse_tree(tree.children[0], px, py, pr, svg_elements, defs_elements, path_counter)

    elif isinstance(tree, str):
        if(px == 0):
            svg_elements.append(f'<text font-size="{py}" text-anchor="middle" fill="white"><textPath href="#Path{path_counter}" startOffset="{pr}%">{tree}</textPath></text>')
        elif(px == 1):
            svg_elements.append(f'<text font-size="{py}" text-anchor="middle" fill="black"><textPath href="#Path{path_counter}" startOffset="{pr}%">{tree}</textPath></text>')

def generate_svg(tree,font):
    square_size = 800
    svg_elements = []
    defs_elements = []
    depth = tree_depth(tree)
    traverse_tree(tree, square_size/2, square_size/2, square_size*0.4, svg_elements, defs_elements, 0)
    defs_elements.append(f"<style type='text/css'> @font-face {{font-family: 'CustomFont';src: url('data:font/woff;base64,{font}') format('woff');}}text {{font-family: 'CustomFont';}}</style>")
    svg_content = "\n".join(svg_elements)
    defs_content = "\n".join(defs_elements)
    svg = f'<svg width="{square_size}" height="{square_size}" xmlns="http://www.w3.org/2000/svg">\n<defs>\n{defs_content}\n</defs>\n<rect x="0" y="0" width="{square_size}" height="{square_size}" fill="white"/>\n{svg_content}\n</svg>'
    return svg


with open("lispell.lark", "r") as file:
    spell_grammar = file.read()
with open("test.lisp", "r") as file:
    test = file.read()
with open("floranteatlaura_base64.txt", "r") as file:
    font = file.read()[:-1]
tree = Lark(spell_grammar).parse(test)
svg = generate_svg(tree,font)
with open("output.svg", "w") as f:
    f.write(svg)
svg2png(url="output.svg", write_to="output.png")