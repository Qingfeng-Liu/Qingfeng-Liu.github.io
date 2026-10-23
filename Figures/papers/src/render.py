"""Rebuild all paper figures: python3 Figures/papers/src/render.py (Pillow).
Set PAPER_FONT_DIR to a directory containing Arial.ttf and Arial Bold.ttf
on systems other than macOS. Diagrams are conceptual, not empirical plots.
"""
import os, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
OUT = Path(__file__).resolve().parents[1]
FONT = Path(os.environ.get('PAPER_FONT_DIR', '/System/Library/Fonts/Supplemental'))
NAVY='#173653'; BLUE='#176cbe'; TEAL='#008f98'; MUTED='#547086'; LIGHT='#eaf3fb'; LINE='#c7dce9'

def render(kind, scale):
    im=Image.new('RGB',(1600*scale,900*scale),'#f7fbff'); d=ImageDraw.Draw(im)
    def xy(box): return tuple(round(v*scale) for v in box)
    def text(x,y,t,size=28,color=NAVY,bold=False):
        font=ImageFont.truetype(str(FONT/('Arial Bold.ttf' if bold else 'Arial.ttf')),size*scale)
        d.text(xy((x,y)),t,font=font,fill=color)
    def box(x,y,w,h,fill='white',outline=LINE):
        d.rounded_rectangle(xy((x,y,x+w,y+h)),radius=20*scale,fill=fill,outline=outline,width=2*scale)
    def line(points,color=BLUE,width=4): d.line([xy(p) for p in points],fill=color,width=width*scale)
    def arrow(x1,y1,x2,y2,color=BLUE):
        line([(x1,y1),(x2,y2)],color)
        a=math.atan2(y2-y1,x2-x1)
        pts=[(x2,y2),(x2-16*math.cos(a-.5),y2-16*math.sin(a-.5)),(x2-16*math.cos(a+.5),y2-16*math.sin(a+.5))]
        d.polygon([xy(p) for p in pts],fill=color)
    text(70,42,'DSELab  /  RESEARCH IN FOCUS',22,TEAL,True)
    titles={'subgoal':('Frozen models. One lightweight head.','Xiang & Liu (2026)  /  Frozen hierarchical world models'), 'tvs-adf':('Changing structure. Dynamic forecasts.','Zhao & Liu (2026)  /  Time-varying structural approximate dynamic factor model'), 'tmle':('Long histories help short series.','Iwasawa, Liu & Zhao (2026)  /  Tying maximum likelihood estimation'), 'model-averaging':('Choose weights for the loss that matters.','Gu, Liu & Zhang (2025)  /  Model averaging under flexible loss functions')}
    title,sub=titles[kind]; text(70,100,title,52,bold=True); text(70,176,sub,26,MUTED)
    if kind=='subgoal':
        # arXiv:2610.26179v2, Fig. 1 and Secs. 3.1-3.4.
        # E encodes observations; g emits conditions; F2 emits waypoints.
        # Simplified one-step view, not the full autoregressive algorithm.
        def dot(x,y,r,color):
            d.ellipse(xy((x-r,y-r,x+r,y+r)),fill=color)
        def lock(cx,cy):
            d.arc(xy((cx-14,cy-28,cx+14,cy+7)),180,360,fill=BLUE,width=6*scale)
            d.rounded_rectangle(xy((cx-22,cy-7,cx+22,cy+28)),radius=7*scale,fill=BLUE)
            dot(cx,cy+7,3,'white')
        def neural(cx,cy):
            layers=[[(cx-70,cy-42),(cx-70,cy+42)],[(cx,cy-58),(cx,cy),(cx,cy+58)],[(cx+70,cy-35),(cx+70,cy+35)]]
            for left,right in zip(layers,layers[1:]):
                for p1 in left:
                    for p2 in right: line([p1,p2],'#79b9be',3)
            for layer in layers:
                for x,y in layer: dot(x,y,13,TEAL)
        for x,w,c in [(70,310,LIGHT),(440,310,'#d9f1f1'),(810,350,LIGHT),(1220,310,'white')]:
            box(x,310,w,320,c)
        text(96,333,'01  ENCODE',22,BLUE,True)
        # Camera/image encoder pictogram with a lock badge.
        box(145,385,150,95,'white',BLUE)
        d.rectangle(xy((160,399,183,412)),fill=BLUE)
        d.ellipse(xy((190,401,253,464)),outline=BLUE,width=7*scale)
        dot(222,433,15,'#afd8ed');lock(302,457)
        text(100,508,'Frozen encoder',32,BLUE,True)
        text(100,559,'Observation + goal',25)
        text(100,598,'Latent state + goal',23,MUTED)
        arrow(380,470,440,470)
        text(466,333,'02  CONDITION',22,TEAL,True)
        neural(595,433)
        text(467,508,'Lightweight head',30,TEAL,True)
        text(467,559,'+ Remaining steps',25)
        text(467,598,'Outputs a condition',23,MUTED)
        arrow(750,470,810,470,TEAL)
        text(836,333,'03  PREDICT',22,BLUE,True)
        # Stacked model blocks, with a lock: distinct from the trainable head.
        for x,y in [(925,385),(907,408),(889,431)]:
            box(x,y,130,45,'white',BLUE)
            for k in range(3): dot(x+26+k*37,y+23,5,BLUE)
        lock(1055,456)
        text(837,508,'Frozen predictor',32,BLUE,True)
        text(837,559,'State + condition',25)
        text(837,598,'Generates a waypoint',23,MUTED)
        arrow(1160,470,1220,470)
        text(1246,333,'04  SUBGOAL',22,TEAL,True)
        # Waypoint + flag pictogram; illustrative, not an experimental rollout.
        line([(1260,465),(1350,405),(1470,465)],'#a5c9d9',5)
        dot(1260,465,9,MUTED);dot(1350,405,13,TEAL);dot(1470,465,9,BLUE)
        line([(1470,465),(1470,390)],BLUE,4)
        d.polygon([xy(v) for v in [(1470,390),(1510,404),(1470,420)]],fill=BLUE)
        text(1247,508,'Next subgoal',32,TEAL,True)
        text(1247,559,'First waypoint',25)
        text(1247,598,'Guides action planning',23,MUTED)
        # Keep the retained low-level controller visible, without algorithm detail.
        box(70,690,1460,120,NAVY,NAVY)
        text(110,715,'Subgoal',34,'#88e0e2',True)
        arrow(295,742,395,742,'#88e0e2')
        # Friendly robot icon for low-level control.
        d.rounded_rectangle(xy((440,715,502,764)),radius=12*scale,outline='#88e0e2',width=3*scale)
        dot(459,738,5,'#88e0e2');dot(483,738,5,'#88e0e2')
        line([(471,715),(471,702)],'#88e0e2',3);dot(471,699,4,'#88e0e2')
        text(530,715,'Low-level MPC',34,'white',True)
        arrow(880,742,980,742,'#88e0e2')
        text(1030,715,'Action',34,'white',True)
        text(110,772,'High-level search replaced; low-level action planning retained.',21,'#d1e4f3')
    elif kind=='tvs-adf':
        for x,label in [(70,'Observed series'),(580,'Time-varying loadings'),(1090,'Structural forecast')]:
            box(x,285,440,350); text(x+26,310,label,29,bold=True)
        for j in range(4):
            points=[(100+i*10,420+j*44+math.sin(i*.38+j)*22) for i in range(37)]
            line(points,[BLUE,TEAL,MUTED,'#6d8ac7'][j],3)
        for j in range(3):
            for i in range(5):
                color=['#d6e9f7','#8ebcdd','#438fbd','#1d668f','#2fa6ad'][(i+j)%5]
                box(614+i*72,384+j*57,60,43,color,color)
        text(614,574,'t1     t2     t3     t4     t5',23,MUTED)
        line([(1122,560),(1490,560)],MUTED,2); line([(1122,560),(1122,390)],MUTED,2)
        line([(1132,530),(1180,490),(1230,509),(1280,465),(1330,470)],BLUE,5)
        line([(1330,470),(1380,436),(1430,440),(1480,400)],TEAL,5)
        text(1345,575,'Future',23,TEAL)
        arrow(510,462,580,462); arrow(1020,462,1090,462)
        box(70,685,1460,125,NAVY,NAVY); text(105,713,'Latent factors  +  changing loadings  +  structural identification',34,'white',True)
        text(105,765,'Track evolving relationships and use them to forecast  |  Conceptual overview',23,'#d1e4f3')
    elif kind=='tmle':
        box(70,285,470,350); text(100,310,'Unequal time-series lengths',29,bold=True)
        text(100,370,'Long history',24,BLUE,True)
        line([(100+i*10,437+math.sin(i*.45)*22) for i in range(40)],BLUE,4)
        text(100,495,'Short history',24,TEAL,True)
        line([(350+i*10,567+math.sin(i*.45)*22) for i in range(15)],TEAL,4)
        arrow(540,460,620,460)
        box(620,285,420,350,LIGHT); text(648,310,'Tie selected parameters',29,bold=True)
        box(650,380,150,65); text(670,397,'Long-series',23,BLUE,True)
        box(650,510,150,65); text(670,527,'Short-series',23,TEAL,True)
        arrow(725,445,725,510,TEAL)
        text(830,440,'Share',26,TEAL,True); text(830,475,'information',26,TEAL,True)
        text(648,592,'Bootstrap selects tying strength',23,MUTED)
        arrow(1040,460,1120,460)
        box(1120,285,410,350); text(1150,310,'More accurate estimation',27,bold=True)
        text(1150,397,'Short-series parameters',26,BLUE,True)
        text(1150,457,'Finite-sample risk bounds',24,MUTED)
        text(1150,512,'Volatility forecasting',26,TEAL,True)
        text(1150,559,'Multivariate GARCH application',22,MUTED)
        box(70,685,1460,125,NAVY,NAVY)
        text(105,713,'Transfer information across related dependent series',36,'white',True)
        text(105,765,'Parameter tying + data-driven tuning  |  Conceptual method overview',23,'#d1e4f3')
    else:
        box(70,285,410,340); text(100,310,'Candidate models',30,bold=True)
        for j in range(3):
            box(100,375+j*73,350,55,LIGHT); text(122,385+j*73,'Model '+str(j+1)+'  /  prediction',26)
        box(580,285,440,340); text(610,310,'Flexible loss',30,bold=True)
        line([(630,549),(956,549)],MUTED,2); line([(790,570),(790,375)],MUTED,2)
        line([(645,395),(790,548),(941,475)],TEAL,6)
        text(623,577,'Different costs on each side',24,MUTED)
        arrow(480,455,580,455); arrow(1020,455,1110,455)
        box(1110,285,420,340); text(1138,310,'Select weights',30,bold=True)
        for j,(w,c) in enumerate([(95,BLUE),(180,TEAL),(60,'#90b8d5')]):
            text(1138,378+j*59,'w'+str(j+1),23,MUTED); box(1190,380+j*59,w,30,c,c)
        text(1138,577,'Combine predictions',26,BLUE,True)
        box(70,685,1460,125,NAVY,NAVY); text(105,713,'Model averaging aligned with the decision objective',36,'white',True)
        text(105,765,'Flexible / asymmetric loss guides weight selection  |  Illustrative weights and loss',23,'#d1e4f3')
    text(70,845,'METHOD OVERVIEW   /   '+kind.upper(),20,MUTED)
    im.save(OUT/(kind+('@2x' if scale==2 else '')+'.png'),optimize=True)

if __name__=='__main__':
    for name in ['subgoal','tvs-adf','model-averaging','tmle']:
        for scale in [1,2]: render(name,scale)
