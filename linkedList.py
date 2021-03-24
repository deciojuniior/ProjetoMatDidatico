from manim import *
import math

# source py_env_manince/bin/activate
# manimce  -pl --media_dir ./media/ linkedList.py LinkedList_01

def new_cell(position, txt, p="0x00", h=1, w=1, ts=0.7):
    p = TextMobject(p, color=BLUE).scale(0.7).shift(position+(h-0.2)*UP)
    rec = Rectangle(height=h, width=w).shift(position)
    txt = TextMobject(txt).scale(ts).shift(position)
    return {
        'p': p,
        'rec': rec,
        'txt': txt,
    }

def new_line(position, txt_l, txt_r, new_r="", h=0.5, wl=1.25, wr=1.25, ts=0.7):
    rec_l = Rectangle(height=h, width=wl).shift(position)
    rec_r = Rectangle(height=h, width=wr).shift(position + RIGHT*wl)
    tl = TextMobject(txt_l).scale(ts).shift(position)
    tr = TextMobject(txt_r).scale(ts).shift(position + RIGHT*wl)
    nr = TextMobject(new_r).scale(ts).shift(position + RIGHT*wl)
    return {
        'rl': rec_l,
        'rr': rec_r,
        'tl': tl,
        'tr': tr,
    }, nr

def descriptor(position, p="0x00", phead="0x00"):
    p = TextMobject(p, color=BLUE).scale(0.7).shift(position+0.5*UP + 1.25*RIGHT/2)
    qtd, _ = new_line(position, "qtd", "0")
    size, _ = new_line(position + 0.5*DOWN, "size", "40")
    head, headaddr = new_line(position + 1.0*DOWN, "head", "NULL", new_r=phead)
    return {
        'p': p,
        'qtd': qtd,
        'size': size,
        'head': head,
        'headaddr': headaddr
    }

def node(position, txt, p="0x00", objAddr="0x1", nextAddr="0x2"):
    p = TextMobject(p, color=BLUE).scale(0.7).shift(position+0.5*UP + 1.25*RIGHT/2)
    _next, nextadd = new_line(position, "next", "NULL", new_r=nextAddr)
    data, dataadd = new_line(position + 0.5*DOWN, "data", objAddr)
    obj = new_cell(position + 3*DOWN + 1.25*RIGHT, txt, p=objAddr)
    return {
        'p': p,
        'next': _next,
        'data': data,
        'obj': obj,
        'nextaddr': nextadd,
        #~ 'dataadd': dataadd,
    }

def txt_rm_add(scene, t1, t2):
    scene.remove(t1)
    scene.add(t2)


def block_add(scene, d, keys, p=True, extra=None):
    # items = [FadeIn(cell) for line in d.values() for cell in line.values()]
    items = list()
    if extra is not None:
        items.extend(extra)
    for k in keys:
        items.extend([o for o in d[k].values()])
    if p is True:
        items.append(d['p'])
    scene.add(*items)

def block_FadeIn(scene, d, keys, p=True, extra=None, anim=FadeIn):
    items = list()
    if extra is not None:
        for item in extra:
            items.append(anim(item))
    for k in keys:
        items.extend([anim(o) for o in d[k].values()])
    if p is True:
        items.append(anim(d['p']))
    scene.play(*items)

class Nodes:
    def build(self):
        self.d = descriptor(3*UP + 6*LEFT, p="0x2a", phead="0x5c")
        self.n1 = node(6*LEFT, "5", p="0x5c", objAddr="0xb4", nextAddr="0xa0")
        self.n2 = node(1.5*LEFT, "1", p="0xa0", objAddr="0xd0", nextAddr="0xc2")
        self.n3 = node(3*RIGHT, "7", p="0xc2", objAddr="0xe0", nextAddr="")

        self.Adn1   = Arrow(self.d['head']['tr'].get_boundary_point(DOWN), self.n1['p'].get_boundary_point(UP))

        self.An1d = Arrow(self.n1['data']['tr'].get_boundary_point(DOWN), self.n1['obj']['p'].get_boundary_point(UP) + 0.15*LEFT)
        self.An1n2 = Arrow(self.n1['next']['tr'].get_boundary_point(RIGHT), self.n2['next']['tl'].get_boundary_point(LEFT) + 0.1*LEFT)

        self.An2d = Arrow(self.n2['data']['tr'].get_boundary_point(DOWN), self.n2['obj']['p'].get_boundary_point(UP) + 0.15*LEFT)
        self.An2n3 = Arrow(self.n2['next']['tr'].get_boundary_point(RIGHT), self.n3['next']['tl'].get_boundary_point(LEFT) + 0.1*LEFT)

        self.An3d = Arrow(self.n3['data']['tr'].get_boundary_point(DOWN), self.n3['obj']['p'].get_boundary_point(UP) + 0.15*LEFT)

        self.An1n3 = Arrow(self.n1['next']['tr'].get_boundary_point(RIGHT), self.n3['next']['tl'].get_boundary_point(LEFT) + 0.1*LEFT)
        self.Adn3 = Arrow(self.d['head']['tr'].get_boundary_point(DOWN), self.n3['next']['tl'].get_boundary_point(LEFT) + 0.1*LEFT)


class LinkedList_01(Scene, Nodes):
    def construct(self):
        self.build()
        block_FadeIn(self, self.d, ['qtd', 'size', 'head'])
        self.wait(2)

class LinkedList_02(Scene, Nodes):
    def construct(self):
        self.build()

        block_add(self, self.d, ['qtd', 'size', 'head'])
        block_FadeIn(self, self.n1, ['next', 'data', 'obj'], extra=[self.An1d])

        self.wait(2)

class LinkedList_03(Scene, Nodes):
    def construct(self):
        self.build()
        block_add(self, self.d, ['qtd', 'size', 'head'])
        block_add(self, self.n1, ['next', 'data', 'obj'], extra=[self.An1d])

        self.play(FadeIn(self.Adn1), FadeOut(self.d['head']['tr']), FadeIn(self.d['headaddr']))

        self.wait(2)

class LinkedList_04(Scene, Nodes):
    def construct(self):
        self.build()
        block_add(self, self.d, ['qtd', 'size', 'head'], extra=[self.Adn1])
        block_add(self, self.n1, ['next', 'data', 'obj'], extra=[self.An1d])
        txt_rm_add(self, self.d['head']['tr'], self.d['headaddr'])

        block_FadeIn(self, self.n2, ['next', 'data', 'obj'], extra=[self.An2d])

        self.wait(2)

class LinkedList_05(Scene, Nodes):
    def construct(self):
        self.build()
        block_add(self, self.d, ['qtd', 'size', 'head'], extra=[self.Adn1])
        block_add(self, self.n1, ['next', 'data', 'obj'], extra=[self.An1d])
        txt_rm_add(self, self.d['head']['tr'], self.d['headaddr'])
        block_add(self, self.n2, ['next', 'data', 'obj'], extra=[self.An2d])

        self.play(FadeIn(self.An1n2), FadeOut(self.n1['next']['tr']), FadeIn(self.n1['nextaddr']))



        self.wait(2)

class LinkedList_06(Scene, Nodes):
    def construct(self):
        self.build()
        block_add(self, self.d, ['qtd', 'size', 'head'], extra=[self.Adn1])
        block_add(self, self.n1, ['next', 'data', 'obj'], extra=[self.An1d])
        txt_rm_add(self, self.d['head']['tr'], self.d['headaddr'])
        block_add(self, self.n2, ['next', 'data', 'obj'], extra=[self.An2d, self.An1n2])
        txt_rm_add(self, self.n1['next']['tr'], self.n1['nextaddr'])

        bl7ock_FadeIn(self, self.n3, ['next', 'data', 'obj'], extra=[self.An3d])

        self.wait(2)

class LinkedList_07(Scene, Nodes):
    def construct(self):
        self.build()
        block_add(self, self.d, ['qtd', 'size', 'head'], extra=[self.Adn1])
        block_add(self, self.n1, ['next', 'data', 'obj'], extra=[self.An1d])
        txt_rm_add(self, self.d['head']['tr'], self.d['headaddr'])
        block_add(self, self.n2, ['next', 'data', 'obj'], extra=[self.An2d, self.An1n2])
        txt_rm_add(self, self.n1['next']['tr'], self.n1['nextaddr'])
        block_add(self, self.n3, ['next', 'data', 'obj'], extra=[self.An3d])

        self.play(FadeIn(self.An2n3), FadeOut(self.n2['next']['tr']), FadeIn(self.n2['nextaddr']))

        self.wait(2)

class LinkedList_08(Scene, Nodes):
    def construct(self):
        self.build()
        block_add(self, self.d, ['qtd', 'size', 'head'], extra=[self.Adn1])
        block_add(self, self.n1, ['next', 'data', 'obj'], extra=[self.An1d])
        txt_rm_add(self, self.d['head']['tr'], self.d['headaddr'])
        block_add(self, self.n2, ['next', 'data', 'obj'], extra=[self.An2d, self.An1n2])
        txt_rm_add(self, self.n1['next']['tr'], self.n1['nextaddr'])
        block_add(self, self.n3, ['next', 'data', 'obj'], extra=[self.An3d, self.An2n3])
        txt_rm_add(self, self.n2['next']['tr'], self.n2['nextaddr'])


        del self.n2['next']['tr']
        block_FadeIn(self, self.n2, ['next', 'data', 'obj'], extra=[self.An1n2, self.An2n3, self.An2d, self.n2['nextaddr']], anim=FadeOut)
        pos = self.n1['nextaddr'].get_center()
        new_tr = TextMobject("0xc2").scale(0.7).shift(pos)
        self.play(FadeOut(self.n1['nextaddr']), FadeIn(new_tr), FadeIn(self.An1n3))

        self.wait(4)

        del self.n1['next']['tr']
        del self.n1['nextaddr']
        block_FadeIn(self, self.n1, ['next', 'data', 'obj'], extra=[self.Adn1, self.An1n3, self.An1d, new_tr], anim=FadeOut)
        pos = self.d['headaddr'].get_center()
        new_tr = TextMobject("0xc2").scale(0.7).shift(pos)
        self.play(FadeOut(self.d['headaddr']), FadeIn(new_tr), FadeIn(self.Adn3))

        self.wait(2)

"""
        self.build()
        block_add(self, self.d, ['qtd', 'size', 'head'])
        block_add(self, self.n1, ['next', 'data', 'obj'])
        block_add(self, self.n2, ['next', 'data', 'obj'])
        txt_rm_add(self, self.d['head']['tr'], self.d['headaddr'])

        block_FadeIn(self, self.n3, ['next', 'data', 'obj'])

        self.play(FadeIn(self.Ad1))

        self.play(FadeIn(self.An1n2))
        self.play(FadeIn(self.An1d))

        self.wait(2)
"""

class Test(Scene):
    def construct(self):
        r1 = Rectangle(height=1, width=2, color=GREEN)
        r2 = Rectangle(height=3, width=1).shift(3*RIGHT + 2*UP)
        r3 = Rectangle(height=1, width=1).shift(3*LEFT + 1*DOWN)
        r2.set_color(RED)
        # t = Tex("f(x) = a_2 \\; \\times \\; x^{2} - a_1 \\; \\times \\;  x")
        t = Tex("$f(x)$", " = ", "$a_{0} \\times x^{2}$")
        t[1].set_color(RED)
        self.add(t)
        self.play(FadeIn(r1,  run_time=2))
        self.play(FadeToColor(r1, BLUE,  run_time=2))
        self.play(Transform(r1, r2, run_time=3))
        self.play(TransformFromCopy(r2, r3), run_time=2)
        self.wait(1)
        self.play(*[FadeOut(r) for r in [r2, r3]], run_time=3)








