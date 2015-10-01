# -*- coding: utf-8 -*-
from math import sqrt


class point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def prnt(self):
        str_x = "{:.2f}".format(self.x)
        str_y = "{:.2f}".format(self.y)
        return "("+str_x+","+str_y+")"
    def add(self, p):
        return point(self.x+p.x, self.y+p.y)
    def scale(self, s):
        return point(self.x*s, self.y*s)
def _prnt(x):
    return x.prnt()
    
class line():
    def __init__(self, start, end, tp="", text=None):
        self.start = start
        self.end = end
        self.tp = tp
        self.text = text
    def prnt(self):
        ins = ""
        if self.text:
            ins = "node [midway, above] {{\\tiny {}}}".format(self.text)
        return "\\draw [{}] ".format(self.tp)+self.start.prnt()\
        +"--"+self.end.prnt()+ins+";"
class textnode():
    def __init__(self,s):
        self.str = s
    def prnt(self):
        return self.str
class rectangle():
    def __init__(self, left_corner, width,height,
                 scale_factor=100.0, color="blue", text=False):
        self.t = text
        self.width = width
        self.scale_factor = scale_factor
        w = width*1.0/scale_factor
        h = height*1.0/scale_factor
        self.node1 = left_corner
        self.node2 = left_corner.add(point(1, 1).scale(sqrt(2)*h/2))
        str1 = " node[midway, sloped, above, xslant=-1]{{\\tiny {}}}"\
               .format(height)
        self.strnode2 = textnode(self.node2.prnt()+str1)
        self.node3 = self.node2.add(point(w, 0))
        self.node4 = self.node3.add(point(-1,-1).scale(sqrt(2)*h/2))
        self.strnode3 = textnode(self.node3.prnt()+
                        " node[midway, above, xslant=0.8] {{\\tiny {}}}"\
                        .format(width))
        self.color = color
    def prnt(self):
        node1 = textnode(self.node1.prnt()+";")
        if self.t:
            node2 = self.strnode2
            node3 = self.strnode3
        else:
            node2 = self.node2
            node3 = self.node3
        path = '\\draw'+'--'.join(map(_prnt, [self.node1, node2, 
                                  node3,self.node4, node1]))
        shade = '\\shade[left color={}!50] '.format(self.color) +\
                '--'.join(map(_prnt, [self.node1, self.node2, 
                                      node3, self.node4, 
                                      textnode("cycle;")]))
        return path + '\n' + shade
    def up(self, width, height, up, color="blue", text=False):
        left = (self.width-width)/2.0
        return rectangle(self.node1.add(point(left/self.scale_factor,up)),
                         width, height, color=color, text=text)
    def up_circle(self, up, width, text="", radius = .05, color="red"):
        left = (self.width-width)/2.0
        nodel = self.node1.add(self.node2).scale(0.5)
        noder = self.node3.add(self.node4).scale(0.5)
        p1 = nodel.add(point(left/self.scale_factor, up))
        p2 = noder.add(point(-left/self.scale_factor, up))
        l = []
        for i in range(4):
            l.append(circle(p1, color, radius))
            l.append(circle(p2, color, radius))
            p1 = p1.add(point(radius*2, 0))
            p2 = p2.add(point(-radius*2, 0))
        if p1.x <p2.x:            
            l.append(line(p1, p2, text=text))
        return circleset(l)
        
        
class circle():
    def __init__(self, center, color, radius=.05):
        self.center = center
        self.radius = radius
        self.color = color
    def prnt(self):
        return "\\draw[fill={}!50] {} circle ({});"\
        .format(self.color, self.center.prnt(), self.radius)
def projection(a, b):
    return [line(a.node1, b.node1,"dotted"),
            line(a.node2, b.node2,"dotted"),
            line(a.node3, b.node3, "dotted"),
            line(a.node4, b.node4, "dotted")]
def projr_c(a, b):
    return [line(a.node1, b.center,"dotted"),
            line(a.node2, b.center,"dotted"),
            line(a.node3, b.center, "dotted"),
            line(a.node4, b.center, "dotted")]
class circleset():
    def __init__(self,l):
        self.l = l;
        self.radius = l[0].radius
    def __len__(self):
        return len(self.l)
    def __getitem__(self, k):
        return self.l[k]
    def prnt(self):
        return '\n'.join(map(_prnt, self.l))
    def up_c(self, num, color, up):
        center = self.l[0].center.add(self.l[1].center).scale(.5)
        center = center.add(point(0,up))
        l = []
        if num%2 is 0:
            p1 = center.add(point(-self.radius, 0))
            p2 = center.add(point(self.radius, 0))
            for i in range(num/2):
                l.append(circle(p1, color, self.radius))
                l.append(circle(p2, color, self.radius))
                p1 = p1.add(point(-2*self.radius,0))
                p2 = p2.add(point(2*self.radius, 0))
        else:
            l.append(circle(center, color, self.radius ))
            p1 = center.add(point(-2*self.radius,0))
            p2 = center.add(point(2*self.radius,0))
            for i in range((num-1)/2):
                l.append(circle(p1, color, self.radius))
                l.append(circle(p2, color, self.radius))
                p1 = p1.add(point(-2*self.radius,0))
                p2 = p2.add(point(2*self.radius, 0))
        return circleset(l)
def proj_c(l1, l2, tp="dotted"):
    l = []
    ll1 = filter(lambda x:isinstance(x,circle), l1)
    ll2 = filter(lambda x:isinstance(x,circle), l2)    
    for circle1 in ll1:
        for circle2 in ll2:
            l.append(line(circle1.center, circle2.center, tp))
    return l
def print2tex(fname, caption, string,scale=3):
    s = "\\documentclass{{article}}\n\
        \\usepackage{{tikz}}\n\
        \\usepackage{{caption}}\n\
        \\usetikzlibrary{{backgrounds}}\n\
        \\begin{{document}}\n\
        \\begin{{figure}}[h!]\n\
        \\begin{{center}}\n\
        \\begin{{tikzpicture}}[scale={}]\n\
        {}\n\
        \\end{{tikzpicture}}\n\
        \\caption*{{{}}}\n\
        \\end{{center}}\n\
        \\end{{figure}}\n\
        \\end{{document}}".format(scale, string, caption)
    with open(fname,"w") as f:
        print>>f, s,
        
if __name__ == "__main__":
    r1 = rectangle(point(0,0),400,62, text=True)
    r11 = rectangle(point(0,0), 120, 10)
    r2 = r1.up(280, 62, 1,"yellow")
    r22 = rectangle(r2.node1, 10,10, color=r2.color)
    r3 = r2.up(280, 62, .1,"green")
    r4 = r3.up(280, 62, .1,"cyan",text=True)
    l = r4.up_circle(1, 200, "1302")
    l2 = l.up_c(2, "orange", .5)
    l3 = l2.up_c(1, "black", .5)
    r44 = rectangle(r4.node1, 40, 10, color="cyan")
    t1 = textnode("\\begin{pgfonlayer}{background}")
    t2 = textnode("\\end{pgfonlayer}")
    string = '\n'.join(map(_prnt, [r1,r11,r2,r22,r3,r4,r44,l,l2,l3]\
        +projr_c(r44, l[0])+projection(r11, r22)+[t1]+proj_c(l,l2,"ultra thin")\
        +proj_c(l2,l3,"ultra thin")+[t2]))
    print2tex("test.tex", "model architecture", string)