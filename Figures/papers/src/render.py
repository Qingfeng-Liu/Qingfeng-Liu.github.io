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
    titles={'subgoal':('Learn the condition. Predict the subgoal.','Xiang & Liu (2026)  /  Frozen hierarchical world models'), 'tvs-adf':('Changing structure. Dynamic forecasts.','Zhao & Liu (2026)  /  Time-varying structural approximate dynamic factor model'), 'tmle':('Long histories help short series.','Iwasawa, Liu & Zhao (2026)  /  Tying maximum likelihood estimation'), 'model-averaging':('Choose weights for the loss that matters.','Gu, Liu & Zhang (2025)  /  Model averaging under flexible loss functions')}
    title,sub=titles[kind]; text(70,100,title,52,bold=True); text(70,176,sub,26,MUTED)
    if kind=='subgoal':
        # arXiv:2610.26179v2, Figures 1-2 and Sections 3.2-3.4.
        # The trainable head emits a condition, never a direct latent subgoal.
        box(70,280,280,265)
        text(94,303,'ENCODED INPUTS',21,TEAL,True)
        for y,t in [(356,'State context'),(416,'Goal'),(476,'Remaining steps')]:
            text(94,y,t,27)
        arrow(350,410,410,410)
        box(410,315,260,180,'#d9f1f1')
        text(436,340,'Condition head',29,TEAL,True)
        text(436,390,'Trainable MLP',25)
        text(436,438,'Only trained module',20,MUTED)
        arrow(670,410,850,410,TEAL)
        text(690,345,'Condition',23,TEAL,True)
        text(705,374,'vector',23,TEAL,True)
        box(850,315,300,180,LIGHT)
        text(877,340,'Coarse predictor',28,BLUE,True)
        text(877,392,'Frozen world model',24)
        text(877,440,'Also takes state context',20,MUTED)
        # State context also enters the frozen coarse predictor directly.
        line([(210,280),(210,246),(1000,246),(1000,295)],MUTED,3)
        arrow(1000,295,1000,315,MUTED)
        text(560,220,'State context',20,MUTED)
        arrow(1150,410,1210,410)
        box(1210,315,320,180)
        text(1235,340,'Latent waypoint',29,bold=True)
        text(1235,396,'First = subgoal',27,TEAL,True)
        text(1235,443,'Continue rollout',21,MUTED)
        line([(1370,495),(1370,565),(540,565)],TEAL,3)
        arrow(540,565,540,495,TEAL)
        text(630,578,'Autoregressive high-level rollout; no candidate optimization',25,TEAL)
        arrow(1370,495,1370,665)
        box(70,665,1000,145,NAVY,NAVY)
        text(100,688,'TRAINING: recorded trajectories + hindsight goals',27,'white',True)
        text(100,735,'Prediction losses backpropagate through the frozen predictor.',24,'#d1e4f3')
        text(100,775,'Only the condition head is updated.',23,'#d1e4f3')
        box(1120,665,410,145,LIGHT)
        text(1147,688,'Low-level MPC',30,BLUE,True)
        text(1147,735,'Frozen fine predictor',25)
        text(1147,776,'Optimize primitive actions',23,MUTED)
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
