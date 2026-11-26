#!/usr/bin/env python3
"""Render the four exact imsets on their shared affine plane."""
from math import atan2, cos, hypot, sin, sqrt, tau
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BG, CARD, GRID = "#0b1523", "#132338", "#38516a"
INK, TEXT, GOLD, AQUA = "#eff8fe", "#bfd3e5", "#ffce79", "#76dfc7"
SIZE = (670, 438)
EDGES = [(0,1), (0,2), (0,3), (0,4), (1,2), (1,3)]
ORDERS = {"D": (4,2,0,3,1), "T": (4,0,3,1,2),
          "U": (4,0,3,2,1), "V": (4,2,0,1,3)}
SHAPE = {"D":(sqrt(2),1), "T":(-sqrt(2),-1), "U":(sqrt(2),-1), "V":(-sqrt(2),1)}
NODE = {0:(114,221), 1:(222,221), 2:(162,145), 3:(162,290), 4:(45,221)}


def font(size,bold=False):
    for folder,regular,strong in [
        ("/System/Library/Fonts/Supplemental","Arial.ttf","Arial Bold.ttf"),
        ("/usr/share/fonts/truetype/dejavu","DejaVuSans.ttf","DejaVuSans-Bold.ttf")]:
        path = Path(folder) / (strong if bold else regular)
        if path.is_file():
            return ImageFont.truetype(str(path),size)
    raise RuntimeError("Arial or DejaVu Sans is required")


TITLE, SUB, LABEL, BODY, EQ = font(32,True), font(19), font(20,True), font(19), font(30,True)


def arrow(draw, a, b, color):
    x,y = a
    u,v = b
    length = hypot(u-x,v-y)
    heading = atan2(v-y,u-x)
    dx,dy = (u-x)/length, (v-y)/length
    start,tip = (x+15*dx,y+15*dy), (u-17*dx,v-17*dy)
    draw.line((*start,*tip),fill=color,width=3)
    draw.polygon([tip, (tip[0]-12*cos(heading-.47),tip[1]-12*sin(heading-.47)),
                        (tip[0]-12*cos(heading+.47),tip[1]-12*sin(heading+.47))],fill=color)


def frame(i,n):
    name = ("D","T","U","V")[i * 4 // n]
    angle = tau * i / n + .18
    image = Image.new("RGB",SIZE,BG)
    draw = ImageDraw.Draw(image)
    draw.text((26,16),"Two pairs, one midpoint",font=TITLE,fill=INK)
    draw.text((27,55),"Making vertex 2 a sink changes the imset.",font=SUB,fill=TEXT)
    for card in ((23,89,259,338),(272,89,646,338)):
        draw.rounded_rectangle(card,14,fill=CARD,outline=GRID)
    draw.text((141,106),f"{name} · orientation",font=LABEL,fill=INK,anchor="mt")
    draw.text((459,106),"Affine plane of four imsets",font=LABEL,fill=INK,anchor="mt")
    order=ORDERS[name]
    for a,b in EDGES:
        if order.index(a) > order.index(b):
            a,b=b,a
        arrow(draw,NODE[a],NODE[b],GOLD if 2 in (a,b) and name in ("D","T") else TEXT)
    for v,(x,y) in NODE.items():
        color=GOLD if v==2 else AQUA
        draw.ellipse((x-14,y-14,x+14,y+14),fill=CARD,outline=color,width=2)
        draw.text((x,y+1),str(v),font=LABEL,fill=color,anchor="mm")
    # The two basis vectors correspond to two equal imset coordinates and one
    # independent coordinate, respectively. Their Euclidean lengths are sqrt(2) and 1.
    def project(x,y):
        turn=.9*sin(angle)
        z=-x*sin(turn)
        horizontal=x*cos(turn)
        vertical=y*cos(.46)-z*sin(.46)
        depth=y*sin(.46)+z*cos(.46)
        scale=53/(1+.075*depth)
        return (459+scale*horizontal,221-scale*vertical)
    points={k:project(*coords) for k,coords in SHAPE.items()}
    ring=("D","V","T","U","D")
    draw.line([points[k] for k in ring],fill=GRID,width=3)
    draw.line([points[k] for k in ("D","T")],fill=GOLD,width=4)
    draw.line([points[k] for k in ("U","V")],fill=AQUA,width=4)
    draw.ellipse((453,215,465,227),fill=INK)
    for k,(x,y) in points.items():
        color=GOLD if k in ("D","T") else AQUA
        r=14 if k==name else 12
        draw.ellipse((x-r,y-r,x+r,y+r),fill=CARD,outline=color,width=3 if k==name else 2)
        draw.text((x,y+1),k,font=LABEL,fill=color,anchor="mm")
    draw.text((335,359),"cD + cT = cU + cV",font=EQ,fill=INK,anchor="mt")
    draw.text((335,401),"Shared midpoint rules out D–T as a polytope edge.",font=BODY,fill=TEXT,anchor="mt")
    return image


def main():
    frames=[frame(i,40) for i in range(40)]
    colors=frames[0].quantize(colors=48)
    frames=[im.quantize(palette=colors,dither=Image.Dither.NONE) for im in frames]
    target=Path(__file__).with_name("imset-midpoint.gif")
    frames[0].save(target,save_all=True,append_images=frames[1:],duration=125,loop=0,optimize=True)
    print(f"{target.name}: {len(frames)} frames, {target.stat().st_size} bytes")


if __name__ == "__main__":
    main()
