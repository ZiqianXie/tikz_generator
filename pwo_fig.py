# -*- coding: utf-8 -*-
"""
Created on Sat Oct 03 10:55:04 2015

@author: Ziqian
"""
from generate_tikz_command import *
from generate_tikz_command import _prnt
from math import cos, sin, pi
import os


def make_snode(c, angle, y, text):
     start = c.point(angle)
     end = start.add(point(abs(y),y))
     l = line(start, end, "<-")
     l2 = line(end, point(c.center.x+1.7, end.y))
     t = textnode(l2.prnt()+" node[right]{{{}}}".format(text))
     return [l,t]
class textcircle(circle):
    def __init__(self, center, fill_color, text, position, 
                 radius=.05, tp="", color="blue"):
                     super(textcircle, self).__init__(center, fill_color,
                            radius=radius, tp="", color=color)
                     self.text = text
                     self.position = position
    def prnt(self):
        return super(textcircle, self).prnt()+" node[{}] {{{}}}".\
                format(self.position, self.text)
class pointpolar(point):
    def __init__(self, center, r, c):
        super(pointpolar, self).__init__(center.x + r*cos(c/180.*pi), center.y + \
        r*sin(c/180.*pi))
        self.r = r
        self.c = c
class curve():
    def __init__(self, start, end, aout, ain,tp="", text=""):
        self.start = start
        self.end = end
        self.tp = tp
        self.text = text
        self.ain = ain
        self.aout = aout
    def prnt(self):
        return "\draw[{}] {} to [out={}, in={}] {} node[midway, above]\
        {{{}}}".format(
        self.tp, self.start.prnt(), self.aout, self.ain, self.end.prnt(), 
        self.text)
os.chdir(os.path.dirname(__file__))
os.chdir("../Tikz test")
c0 = circle(point(1.8,0),color="blue",fill_color="white",radius=1.5,tp="dashed")
c1 = circle(c0.center,color="blue",fill_color="white",radius=1.2,tp="dashed")
c2 = circle(c0.center,color="blue",fill_color="white",radius=1,tp="dashed")
c3 = circle(c0.center,color="blue",fill_color="white",radius=0.8,tp="dashed")
c4 = circle(c0.center,color="blue",fill_color="white",radius=.5,tp="dashed")
n1 = make_snode(c0,30,.1,"attractive basin of $\lambda_1$")
n2 = make_snode(c1,20,.17,"attractive basin of $\lambda_{K-1}$")
n3 = make_snode(c2,0,-.3,"attractive basin of $\lambda_K$")
n4 = make_snode(c3,-20,-.35,"attractive basin of $\lambda_{K+1}$")
n5 = make_snode(c4,-45, -.6,"attractive basin of $\lambda_{N}$")
tc1 = textcircle(pointpolar(c0.center, 1.4, -120),color="black",
                 fill_color="red",radius=0.02, text = "$\hat{\\theta}^{\{0\}}$",
                    position="above")
tc2 = textcircle(pointpolar(c0.center, 1.1, 170),color="black",
                 fill_color="red",radius=0.02, text = "$\hat{\\theta}^{\{K-2\}}$",
                    position="above")
tc3 = textcircle(pointpolar(c0.center, 0.9, 90),color="black",
                 fill_color="red",radius=0.02, text = "$\hat{\\theta}^{\{K-1\}}$",
                    position="above")
tc4 = textcircle(pointpolar(c0.center, 0.7, 10),color="black",
                 fill_color="red",radius=0.02, text = "$\hat{\\theta}^{\{K\}}$",
                    position="above")
tc5 = textcircle(pointpolar(c0.center, 0.4, -90),color="black",
                 fill_color="red",radius=0.02, text = "$\hat{\\theta}^{\{N-1\}}$",
                    position="above")
tc6 = textcircle(c0.center,color="black",
                 fill_color="red",radius=0.02, text = "$\hat{\\theta}^*$",
                    position="above")
cc1 = curve(tc1.center,tc2.center,120,260,"dotted, ->, line width=1pt")
cc2 = curve(tc2.center,tc3.center,70,180,"->, line width=1pt")
cc3 = curve(tc3.center,tc4.center,-10,90,"->, line width=1pt")
cc4 = curve(tc4.center,tc5.center,-100,5,"dotted,->, line width=1pt")
string = ';\n'.join(map(_prnt,[c0,c1,c2,c3,c4,tc1,tc2,tc3,tc4,tc5,tc6,cc1,cc2,cc3,
                               cc4]+n1+n2+n3+n4+n5))
print2tex("pwo_fig.tex", "warm start initialization", string+";")