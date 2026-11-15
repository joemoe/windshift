exec(open('/tmp/car/helpers.py').read())
import random
def save(i): 
    import shutil; shutil.copy(f's{i}.png', f'dd{i}.png')

# 1 cover
def c1():
    s=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Inter">{LOGO}<rect width="{W}" height="{H}" fill="url(#bg)"/>'''
    random.seed(7)
    # three blended "systems" as streak fields
    for k in range(120):
        x=random.uniform(60,1020); y=random.uniform(860,1190); c=random.choice(['#9fb4ff','#ef8a5b','#f2c94c','#f27fa5'])
        a=math.radians({'#9fb4ff':115,'#ef8a5b':20,'#f2c94c':240,'#f27fa5':300}[c]+random.uniform(-15,15)); L=random.uniform(40,110)
        s+=f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+math.sin(a)*L:.0f}" y2="{y-math.cos(a)*L:.0f}" stroke="{c}" stroke-opacity="{random.uniform(.3,.8):.2f}" stroke-width="3" stroke-linecap="round"/>'
    s+=mark(60,140,2.2)
    s+='<text x="60" y="330" font-size="30" font-weight="700" fill="#4fc3a1" letter-spacing="3">DEEP-DIVE</text>'
    t,y=text(60,420,'Wie das Windshift-Modell rechnet',78,800,'#e8f1f5',960,1.12); s+=t
    t,_=text(60,y+20,'Aus 5 Pfeilen ein Windfeld für den ganzen See – Schritt für Schritt.',34,500,'#c8d7de',920,1.3); s+=t
    s+=f'<text x="60" y="{H-46}" font-size="24" font-weight="700" fill="#e8f1f5">joemoe.at/windshift</text><text x="{W-60}" y="{H-46}" font-size="24" font-weight="600" fill="#8aa6b3" text-anchor="end">Wischen →</text></svg>'
    open('s1.svg','w').write(s); subprocess.run(['rsvg-convert','s1.svg','-o','s1.png'],check=True)
c1(); save(1)


LAKE=eval(re.search(r'const LAKE = (\[\[.*?\]\]);', open('/home/claude/windshift/index.html').read()).group(1))
def mapslide(ty):
    x0,x1,y0,y1=-30,22,-16,17
    bx,by,bw=60,ty+10,960; sc=bw/(x1-x0); bh=(y1-y0)*sc
    P=lambda x,y:(bx+(x-x0)*sc, by+(y1-y)*sc)
    LL=lambda la,lo:P((lo-9.65)*75.1,(la-47.53)*111.2)
    s=f'<defs><clipPath id="mc"><rect x="{bx}" y="{by}" width="{bw}" height="{bh:.0f}" rx="18"/></clipPath></defs><rect x="{bx}" y="{by}" width="{bw}" height="{bh:.0f}" rx="18" fill="#0e1c27"/><g clip-path="url(#mc)">'
    s+='<path d="M'+' L'.join(f'{LL(la,lo)[0]:.1f} {LL(la,lo)[1]:.1f}' for lo,la in LAKE)+'Z" fill="#123a52" stroke="#2b6a8a" stroke-width="2"/>'
    # lake axis (Großwetterlage)
    ax=[P(-26,9.5),P(14,-2.5)]
    s+=f'<line x1="{ax[0][0]:.0f}" y1="{ax[0][1]:.0f}" x2="{ax[1][0]:.0f}" y2="{ax[1][1]:.0f}" stroke="#9fb4ff" stroke-width="3" stroke-dasharray="10 10" opacity=".8"/>'
    s+=f'<text x="{P(-17,9.6)[0]:.0f}" y="{P(-17,9.6)[1]:.0f}" font-size="22" font-weight="800" fill="#9fb4ff">Großwetterlage ⇄ Seeachse</text>'
    def fan(o,frm,width,reach,spread):
        to=frm+180; L=reach*1.4; pts=[]
        side=lambda a,d:(o[0]+math.sin(math.radians(a))*d, o[1]+math.cos(math.radians(a))*d)
        pts.append(side(to-90,width*0.6)); a=-spread-12
        while a<=spread+12: pts.append(side(to+a,L)); a+=6
        pts.append(side(to+90,width*0.6)); return pts
    for (o,frm,w,r,sp,c,lab,lp,an) in [((-2.5,-7.5),160,3.2,6.5,18,'#ef8a5b','Rheintal ↑',(-2.5,-10.4),'middle'),((-0.6,-3.2),160,0.9,3.0,20,'#5bc0ef','Rhein-Ausfluss',(1.6,-8.4),'start'),((5.2,-3.8),140,1.6,3.5,20,'#7bd88f','Bregenzerwald',(8.6,-5.4),'start')]:
        pts=[P(*p) for p in fan(o,frm,w,r,sp)]
        s+='<path d="M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)+f'Z" fill="{c}" fill-opacity=".28" stroke="{c}" stroke-width="3"/>'
        q=P(*lp); s+=f'<text x="{q[0]:.0f}" y="{q[1]:.0f}" font-size="22" font-weight="800" fill="{c}" text-anchor="{an}">{lab}</text>'
    for (p,c,lab,lp,an) in [([(8.2,-3.0),(7.0,2.5)],'#f2c94c','Pfänder',(9.0,3.6),'start'),([(-15,-6.6),(-5.5,-5.4)],'#d38cf2','Appenzeller Hänge',(-24.5,-8.8),'start')]:
        a,b=P(*p[0]),P(*p[1]); s+=f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="{c}" stroke-width="12" stroke-linecap="round"/>'
        q=P(*lp); s+=f'<text x="{q[0]:.0f}" y="{q[1]:.0f}" font-size="22" font-weight="800" fill="{c}" text-anchor="{an}">{lab}</text>'
    cx,cy=P(-3,0.5); r=6*sc
    s+=f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="none" stroke="#f27fa5" stroke-width="3" stroke-dasharray="4 12" stroke-linecap="round"/>'
    s+=f'<text x="{cx:.0f}" y="{cy-r-12:.0f}" font-size="22" font-weight="800" fill="#f27fa5" text-anchor="middle">Land- ⇄ Seewind</text>'
    s+='</g>'
    # stations
    lakes=[('Lindau',47.540,9.684),('Bregenz',47.499,9.746),('Rohrspitz',47.497,9.630),('Altenrhein',47.485,9.566),('Friedrichshafen',47.6454,9.4795)]
    for n,la,lo in lakes:
        x,y=LL(la,lo); s+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="#4fc3a1" stroke="#0b1620" stroke-width="3"/>'
    sp=[('Dornbirn',47.4325,9.7256,'#ef8a5b'),('Alberschwende',47.4575,9.8486,'#7bd88f'),('Sulzberg',47.5219,9.9144,'#f2c94c'),('St. Gallen',47.4255,9.3985,'#d38cf2'),('Güttingen',47.6017,9.2794,'#9fb4ff')]
    for n,la,lo,c in sp:
        x,y=LL(la,lo); s+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="#0b1620" stroke="{c}" stroke-width="4"/><text x="{x+14 if n!='Sulzberg' else x-14:.1f}" y="{y+22:.1f}" font-size="18" font-weight="600" fill="#c8d7de" text-anchor="{'start' if n!='Sulzberg' else 'end'}">{n}</text>'
    for n,lo,c in [('Säntis',9.3435,'#9fb4ff'),('Vaduz · Bad Ragaz',9.51,'#ef8a5b')]:
        x,_=LL(47.4,lo); yb=by+bh-14; s+=arrow(round(x,1),round(yb-34,1),180,26,c,3)+f'<text x="{x+12:.1f}" y="{yb:.1f}" font-size="18" font-weight="600" fill="#c8d7de">{n} ↓</text>'
    x,_=LL(47.68,9.19); s+=f'<text x="{bx+14}" y="{by+30}" font-size="18" font-weight="600" fill="#c8d7de">← Konstanz</text>'
    y=by+bh+52
    s+=f'<circle cx="74" cy="{y-8}" r="11" fill="#4fc3a1"/>'
    t,y2=text(100,y,'Seestationen – ihre Messungen muss das Modell erklären.',26,500,'#c8d7de',920,1.3); s+=t
    s+=f'<circle cx="74" cy="{y2+6}" r="9" fill="none" stroke="#f2c94c" stroke-width="4"/>'
    t,y3=text(100,y2+14,'Späher im Umland – sie verraten, welches System gerade anläuft: Vaduz und Dornbirn den Föhn, Sulzberg den Pfänderwind, Alberschwende den Bregenzerwald.',26,500,'#c8d7de',920,1.3); s+=t
    return s
slide(2,mapslide,'1 · Die Karte','Wo die Windsysteme wirken'); save(2)

# 2 building blocks
def b2(ty):
    s=''; y0=ty+30
    boxes=[('Strömung','Großwetterlage – aus jeder Richtung, vom Gelände gelenkt','#9fb4ff'),('Strahl','Föhn, Rhein-Ausfluss, Bregenzerwald','#ef8a5b'),('Fallwind','Pfänder, Appenzeller Hänge','#f2c94c'),('Radial','Land- und Seewind','#f27fa5')]
    for i,(h,d,c) in enumerate(boxes):
        x=60+(i%2)*490; y=y0+(i//2)*330; s+=f'<rect x="{x}" y="{y}" width="470" height="310" rx="22" fill="#112230" stroke="#21414f" stroke-width="2"/>'
        cx,cy=x+235,y+110
        if i==0:
            for dy in (-50,-10,30):
                s+=f'<path d="M{cx-170} {cy+dy-25} Q{cx-40} {cy+dy-20} {cx+40} {cy+dy+5} T{cx+150} {cy+dy+30}" fill="none" stroke="{c}" stroke-width="5" stroke-linecap="round"/>'
                s+=arrow(cx+140,cy+dy+27,108,1,c,5)
        if i==1:
            for a in (-22,-11,0,11,22): s+=arrow(cx,cy+70,a,105+(0 if a==0 else -12),c,5)
            s+=f'<circle cx="{cx}" cy="{cy+70}" r="9" fill="{c}"/>'
        if i==2:
            s+=f'<path d="M{cx-130} {cy-50} Q{cx} {cy-85} {cx+130} {cy-50}" fill="none" stroke="{c}" stroke-width="10" stroke-linecap="round"/>'
            for dx in (-90,-25,40,105): s+=arrow(cx+dx-10,cy-45,200,95,c,5)
        if i==3:
            for a in range(0,360,45): r1,r2=85,30; s+=arrow(round(cx+math.sin(math.radians(a))*r1,1),round(cy-math.cos(math.radians(a))*r1,1),(a+180)%360,r1-r2,c,5)
        s+=f'<text x="{x+24}" y="{y+240}" font-size="30" font-weight="800" fill="{c}">{h}</text>'
        t,_=text(x+24,y+276,d,21,500,'#c8d7de',430,1.25); s+=t
    y=y0+680
    t,y=text(60,y,'Jedes Windsystem ist ein festes Strömungsmuster: wo es herkommt, wie weit es reicht, wie schnell es abnimmt – mit einer typischen Maximalstärke, z. B. Föhn bis ca. 30 kn.',27,500,'#c8d7de',960,1.32); s+=t
    return s
slide(3,b2,'2 · Bausteine','Vier Grundformen'); save(3)

# 3 mixing
def m3(ty):
    s=''; y=ty+40
    rows=[('Großwetterlage aus West',0.5,'#9fb4ff'),('Rheintal-Föhn',0.3,'#ef8a5b'),('Pfänder-Fallwind',0.1,'#f2c94c'),('Landwind',0.0,'#f27fa5')]
    for n,v,c in rows:
        s+=f'<text x="60" y="{y+30}" font-size="30" font-weight="700" fill="#e8f1f5">{html.escape(n)}</text>'
        s+=f'<rect x="560" y="{y+6}" width="360" height="30" rx="15" fill="#16303f"/><rect x="560" y="{y+6}" width="{max(30,360*v):.0f}" height="30" rx="15" fill="{c}" fill-opacity="{1 if v else .3}"/>'
        s+=f'<text x="1020" y="{y+32}" font-size="30" font-weight="800" fill="{c}" text-anchor="end">{int(v*100)}%</text>'; y+=70
    s+=f'<line x1="60" y1="{y+10}" x2="1020" y2="{y+10}" stroke="#3d6577" stroke-width="3"/>'
    s+=f'<text x="60" y="{y+70}" font-size="34" font-weight="800" fill="#4fc3a1">= Windfeld über dem ganzen See</text>'
    y+=130
    t,y=text(60,y,'An jedem Punkt des Sees wird der Wind aller Systeme zusammengezählt – jedes mit seiner aktuellen Stärke in Prozent.',28,500,'#c8d7de',960,1.32); s+=t
    t,y=text(60,y+16,'Darum kann der Wind auf wenigen Kilometern völlig anders wehen: Vor Altenrhein dominiert der Föhn, vor Lindau die Großwetterlage.',28,500,'#c8d7de',960,1.32); s+=t
    t,_=text(60,y+16,'Die Großwetterlage hat zusätzlich eine Richtung – und wird vom Gelände verformt: entlang der Seeachse gelenkt, am Pfänder gebremst.',28,500,'#c8d7de',960,1.32); s+=t
    return s
slide(4,m3,'3 · Mischen','Wind = Summe aller Systeme'); save(4)

# 4 fitting
def f4(ty):
    s=''; y=ty+30
    # mini diagram: measured arrows vs model arrows
    pts=[(220,ty+150,60,10),(480,ty+120,40,350),(740,ty+170,75,20),(900,ty+110,20,5)]
    for x,yy,a,b in pts:
        s+=arrow(x,yy+60,a,110,'#e8f1f5',7)+arrow(x+8,yy+66,a-14 if b<180 else a+18,100,'#4fc3a1',5)
    s+=f'<text x="60" y="{ty+330}" font-size="22" font-weight="700" fill="#e8f1f5">⬤ Messung</text><text x="240" y="{ty+330}" font-size="22" font-weight="700" fill="#4fc3a1">⬤ Modell</text>'
    y=ty+390
    steps=['Alle 10 Minuten probiert das Modell die Großwetterlage aus 36 Richtungen durch.',
           'Für jede Richtung rechnet es aus, welche Stärken der 7 Systeme die Pfeile an den Seestationen am besten treffen.',
           'Die Späher im Umland geben Startwerte vor: Weht in Vaduz Südwind, ist Föhn im Rheintal wahrscheinlicher; frischt es in Sulzberg aus Nordost auf, droht Pfänderwind.',
           'Eine eingebaute Bremse verhindert, dass das Modell Systeme wild übertreibt, nur um jeden Pfeil exakt zu treffen.']
    for i,t0 in enumerate(steps):
        s+=f'<circle cx="80" cy="{y-9}" r="18" fill="#4fc3a1"/><text x="80" y="{y}" font-size="22" font-weight="800" fill="#0b1620" text-anchor="middle">{i+1}</text>'
        t,y=text(116,y,t0,26,500,'#c8d7de',900,1.3); s+=t; y+=20
    return s
slide(5,f4,'4 · Anpassen','Das Modell sucht die beste Mischung'); save(5)

# 5 residual blending
def r5(ty):
    s=''; cx,cy=540,ty+230
    for r,o in ((210,.08),(150,.14),(95,.22),(45,.35)): s+=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#4fc3a1" fill-opacity="{o}"/>'
    s+=f'<circle cx="{cx}" cy="{cy}" r="13" fill="#4fc3a1" stroke="#0b1620" stroke-width="3"/><text x="{cx+24}" y="{cy-20}" font-size="24" font-weight="800" fill="#e8f1f5">Station</text>'
    s+=f'<line x1="{cx}" y1="{cy+40}" x2="{cx+150}" y2="{cy+40}" stroke="#e8f1f5" stroke-width="2" stroke-dasharray="6 6"/><text x="{cx+75}" y="{cy+72}" font-size="22" font-weight="600" fill="#e8f1f5" text-anchor="middle">ca. 3 km</text>'
    y=cy+280
    t,y=text(60,y,'Auch die beste Mischung trifft nie jeden Pfeil exakt. Die Abweichung an jeder Station wird darum in ihrer Umgebung nachkorrigiert – direkt an der Station voll, nach rund 3 km nur noch halb, weiter draußen kaum.',28,500,'#c8d7de',960,1.32); s+=t
    t,_=text(60,y+16,'So stimmt die Strömung an den Messpunkten genau, und dazwischen übernimmt das Modell.',28,700,'#4fc3a1',960,1.32); s+=t
    return s
slide(6,r5,'5 · Feinschliff','Dort, wo gemessen wird, gilt die Messung'); save(6)

# 6 limits
def l6(ty):
    s=''; y=ty+30
    items=[('Wenige Messpunkte','Nur 5 Stationen am See. Wind, der dazwischen entsteht und wieder verschwindet, sieht das Modell nicht.'),
           ('Lückenfüller','Manchmal erklärt das Modell eine Abweichung mit dem falschen System – z. B. Rhein-Ausfluss mitten am Tag, obwohl der eigentlich nachts weht.'),
           ('Keine Vorhersage','Es erklärt, was gerade gemessen wird. Für morgen schau in die Wettermodelle – und bei Starkwind auf die Sturmwarnung.'),
           ('Version 1.0','Jeder Fit wird mitgeschrieben. Wenn wir das Modell verbessern, erklären wir hier, was sich geändert hat.')]
    for h,d in items:
        s+=f'<rect x="60" y="{y-34}" width="960" height="176" rx="22" fill="#112230" stroke="#21414f" stroke-width="2"/>'
        s+=f'<text x="96" y="{y+14}" font-size="30" font-weight="800" fill="#f2a93b">{html.escape(h)}</text>'
        t,_=text(96,y+56,d,25,500,'#c8d7de',890,1.3); s+=t; y+=196
    return s
slide(7,l6,'6 · Grenzen','Was das Modell nicht kann'); save(7)

# 7 participate
def p7(ty):
    s=''; y=ty+30
    t,y=text(60,y+10,'Das Modell wird besser, je mehr wir vom Wasser hören.',34,700,'#e8f1f5',960,1.25); s+=t
    items=[('💬','Kommentiere','direkt unter dem Beitrag, wenn die Karte nicht zu dem passt, was du draußen erlebt hast – mit Ort und Uhrzeit.'),
           ('📸','Schick Fotos per DM','an @windshift.bodensee – mit Ort, Uhrzeit und einem Satz, wie es war. Wir machen einen Rückblick mit den Messdaten daraus.'),
           ('📡','Teile Messdaten','Windmesser an Bord, im Hafen oder am Steg? Schreib uns per DM – jede zusätzliche Station hilft.')]
    y+=30
    for e,h,d in items:
        s+=f'<rect x="60" y="{y-34}" width="960" height="176" rx="22" fill="#112230" stroke="#21414f" stroke-width="2"/>'
        s+=f'<text x="96" y="{y+14}" font-size="30" font-weight="800" fill="#4fc3a1">{html.escape(h)}</text>'
        t,_=text(96,y+56,d,26,500,'#c8d7de',890,1.3); s+=t; y+=196
    t,_=text(60,y+20,'Kein Meteorologe am Werk – ein Hobbyprojekt aus echten Daten, KI und viel Zeit auf dem Wasser.',24,600,'#8aa6b3',960,1.3); s+=t
    return s
slide(8,p7,'Mitmachen','Hilf dem Modell') ; save(8)
