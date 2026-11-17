exec(open('/tmp/car/helpers.py').read())
import shutil
def out(prefix,i): shutil.copy(f's{i}.png', f'{prefix}-{i}.png')
def cover(prefix,kicker,title,sub,cols,angles):
    import random; random.seed(len(title))
    s=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Inter">{LOGO}<rect width="{W}" height="{H}" fill="url(#bg)"/>'''
    for k in range(110):
        x=random.uniform(40,1040); y=random.uniform(860,1190); c=random.choice(cols); a=math.radians(angles[cols.index(c)]+random.uniform(-14,14)); L=random.uniform(40,120)
        s+=f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+math.sin(a)*L:.0f}" y2="{y-math.cos(a)*L:.0f}" stroke="{c}" stroke-opacity="{random.uniform(.3,.85):.2f}" stroke-width="3" stroke-linecap="round"/>'
    s+=mark(60,140,2.2)+f'<text x="60" y="330" font-size="30" font-weight="700" fill="{cols[0]}" letter-spacing="3">{html.escape(kicker.upper())}</text>'
    t,y=text(60,420,title,80,800,'#e8f1f5',960,1.12); s+=t
    t,_=text(60,y+20,sub,34,500,'#c8d7de',920,1.3); s+=t
    s+=f'<text x="60" y="{H-46}" font-size="24" font-weight="700" fill="#e8f1f5">joemoe.at/windshift</text><text x="{W-60}" y="{H-46}" font-size="24" font-weight="600" fill="#8aa6b3" text-anchor="end">Wischen →</text></svg>'
    open('s1.svg','w').write(s); subprocess.run(['rsvg-convert','s1.svg','-o','s1.png'],check=True); out(prefix,1)
def chart(x0,y0,w,h,labels,series,vmax,unit='kn',hlines=()):
    s=''; n=len(labels); X=lambda i:x0+i*w/(n-1); Y=lambda v:y0+h-min(v,vmax)/vmax*h
    for v,c,l in hlines:
        s+=f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x0+w}" y2="{Y(v):.1f}" stroke="{c}" stroke-width="3" stroke-dasharray="10 8"/><text x="{x0+10}" y="{Y(v)-10:.1f}" font-size="20" font-weight="700" fill="{c}">{html.escape(l)}</text>'
    for k in range(5):
        v=vmax*k/4; s+=f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x0+w}" y2="{Y(v):.1f}" stroke="#ffffff" stroke-opacity=".1"/><text x="{x0-12}" y="{Y(v)+7:.1f}" font-size="20" fill="#8aa6b3" text-anchor="end">{v:.0f}</text>'
    for i,l in enumerate(labels):
        if l: s+=f'<text x="{X(i):.1f}" y="{y0+h+32}" font-size="20" fill="#8aa6b3" text-anchor="middle">{l}</text>'
    lx=x0
    for name,vals,c,dash in series:
        pts=' '.join(f'{X(i):.1f},{Y(v):.1f}' for i,v in enumerate(vals) if v is not None)
        s+=f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round" {"stroke-dasharray=\"10 8\"" if dash else ""}/>'
        s+=f'<rect x="{lx}" y="{y0+h+56}" width="26" height="6" rx="3" fill="{c}"/><text x="{lx+34}" y="{y0+h+65}" font-size="21" font-weight="600" fill="#c8d7de">{html.escape(name)}</text>'
        lx+=font(21,600).getlength(name)+80
    s+=f'<text x="{x0+w}" y="{y0-14}" font-size="20" fill="#8aa6b3" text-anchor="end">{unit}</text>'
    return s
def bullets(y,items,sz=27,col='#c8d7de',dot='#4fc3a1'):
    s=''
    for it in items:
        s+=f'<circle cx="74" cy="{y-9}" r="7" fill="{dot}"/>'; t,y=text(96,y,it,sz,500,col,920,1.32); s+=t; y+=16
    return s,y

# ================= A: FÖHN =================
N=6
cover('foehn','Windsysteme · Teil 1','Föhn – der Wind aus dem Süden','Warum er am Bodensee mal ankommt – und oft nicht.',['#ef8a5b','#f2c94c'],[340,350])
def a2(ty):
    s=''; y=ty+40
    # mountain profile
    base=y+300; s+=f'<path d="M60 {base} L300 {base-40} L480 {base-230} L560 {base-260} L640 {base-220} L820 {base-40} L1020 {base} Z" fill="#1d3442" stroke="#3d6577" stroke-width="3"/>'
    s+=f'<path d="M120 {base-150} Q300 {base-330} 520 {base-300}" fill="#5d7684" fill-opacity=".9"/><text x="150" y="{base-210}" font-size="22" font-weight="700" fill="#e8f1f5">Stau, Regen</text>'
    s+=f'<text x="70" y="{base+40}" font-size="24" font-weight="700" fill="#8aa6b3">Süden (Italien)</text><text x="1010" y="{base+40}" font-size="24" font-weight="700" fill="#8aa6b3" text-anchor="end">Norden (Bodensee)</text>'
    s+=f'<path d="M160 {base-60} Q350 {base-160} 560 {base-290} Q720 {base-200} 940 {base-30}" fill="none" stroke="#ef8a5b" stroke-width="7" stroke-linecap="round"/>'
    s+=arrow(900,base-55,125,60,'#ef8a5b',7)
    s+=f'<text x="760" y="{base-170}" font-size="24" font-weight="800" fill="#ef8a5b">warm &amp; trocken</text>'
    y=base+100
    t,y=text(60,y,'Liegt im Süden der Alpen höherer Luftdruck als im Norden – etwa wenn sich ein Tief von Westen nähert –, strömt Luft über den Alpenkamm.',27,500,'#c8d7de',960,1.32); s+=t
    t,y=text(60,y+16,'Auf der Südseite staut sie sich und regnet ab. Auf der Nordseite fällt sie ins Tal, erwärmt sich und kommt warm, trocken und böig an.',27,500,'#c8d7de',960,1.32); s+=t
    t,_=text(60,y+16,'Die Wolkenwand über dem Kamm heißt Föhnmauer. Typisch sind Frühling und Herbst.',27,700,'#f2c94c',960,1.32); s+=t
    return s
slide(2,a2,'1 · Entstehung','Druckunterschied über den Alpen'); out('foehn',2)
def a3(ty):
    s=''; y=ty+30
    pts=[(300,y+560,'Bad Ragaz'),(380,y+400,'Vaduz'),(470,y+220,'Altstätten'),(560,y+60,'Altenrhein / Bodensee')]
    s+=f'<path d="M260 {y+600} C330 {y+450} 360 {y+300} 470 {y+200} S560 {y+80} 600 {y+30}" fill="none" stroke="#ef8a5b" stroke-opacity=".3" stroke-width="70" stroke-linecap="round"/>'
    for i in range(len(pts)-1):
        a,b=pts[i],pts[i+1]; ang=math.degrees(math.atan2(b[0]-a[0],-(b[1]-a[1]))); L=math.hypot(b[0]-a[0],b[1]-a[1])*0.75
        s+=arrow(a[0],a[1],ang,L,'#ef8a5b',6+i*1.5)
    for x,yy,n in pts: s+=f'<circle cx="{x}" cy="{yy}" r="9" fill="#e8f1f5"/><text x="{x+26}" y="{yy+8}" font-size="25" font-weight="700" fill="#e8f1f5">{n}</text>'
    t,yy=text(640,y+300,'Das Rheintal wirkt wie eine Düse: Der Föhn wird kanalisiert und beschleunigt.',26,500,'#c8d7de',380,1.3); s+=t
    t,_=text(640,yy+16,'So stößt er bis Rorschach und Altenrhein vor – laut SRF Meteo dort auch im Winter häufig.',26,700,'#ef8a5b',380,1.3); s+=t
    return s
slide(3,a3,'2 · Das Rheintal','Ein Kanal bis zum See'); out('foehn',3)
def a4(ty):
    labels=['10','','12','','14','','16','','18','','20','','22']
    vad=[3,None,6,None,7,None,20,None,14,None,4,None,2]; alt=[3,None,6,None,3,None,7,None,8,None,7,None,8]
    import itertools
    def fill(v):
        out=[]; 
        for i,x in enumerate(v):
            if x is None: out.append((v[i-1]+v[i+1])/2)
            else: out.append(x)
        return out
    s=chart(110,ty+70,900,360,labels,[('Vaduz (Rheintal)',fill(vad),'#ef8a5b',False),('Altenrhein (See)',fill(alt),'#9fb4ff',False)],24)
    y=ty+560
    t,y=text(60,y,'Um 16 Uhr bläst in Vaduz Föhn aus Süd mit 20 kn – Böen bis 41 kn. Am See in Altenrhein zur selben Zeit: 7 kn aus West.',27,500,'#c8d7de',960,1.32); s+=t
    t,_=text(60,y+16,'Der Föhn war da – aber nur im Tal. Bis zum See kam er nicht durch.',28,800,'#f2c94c',960,1.32); s+=t
    return s
slide(4,a4,'3 · Beispiel 20. Oktober','Föhn in Vaduz, Westwind am See'); out('foehn',4)
def a5(ty):
    s=''; y=ty+40
    s+=f'<rect x="60" y="{y}" width="960" height="300" rx="22" fill="#112230"/>'
    s+=f'<rect x="60" y="{y+190}" width="960" height="110" rx="0" fill="#2b5876" fill-opacity=".55"/><text x="90" y="{y+260}" font-size="24" font-weight="700" fill="#9fd0f0">kalte, schwere Luft – Kaltluftsee</text>'
    s+=f'<path d="M90 {y+80} Q500 {y+60} 990 {y+150}" fill="none" stroke="#ef8a5b" stroke-width="8" stroke-linecap="round"/>'+arrow(970,y+146,105,30,'#ef8a5b',8)
    s+=f'<text x="90" y="{y+60}" font-size="24" font-weight="800" fill="#ef8a5b">warmer Föhn gleitet darüber</text>'
    y+=360
    t,y=text(60,y,'Im Winter liegt im unteren Rheintal und über dem See oft kalte, schwere Luft. Der warme Föhn gleitet darüber hinweg – am Wasser merkt man wenig.',27,500,'#c8d7de',960,1.32); s+=t
    t,y=text(60,y+16,'Erst wenn er die Kaltluft ausräumt, bricht er bis zum Boden durch. Dann kann es am See innerhalb von Minuten böig werden.',27,500,'#c8d7de',960,1.32); s+=t
    t,_=text(60,y+16,'Tipp: Weht es in Vaduz kräftig aus Süd, Böen in Altenrhein und Rohrspitz im Auge behalten.',27,700,'#4fc3a1',960,1.32); s+=t
    return s
slide(5,a5,'4 · Warum oft nicht?','Der Kaltluftsee bremst'); out('foehn',5)
def a6(ty):
    s=''; y=ty+40
    t,y=text(60,y,'In Windshift ist der Föhn das System „Rheintal“. Die Späher Vaduz, Bad Ragaz und Dornbirn verraten, ob er im Tal läuft – die Seestationen zeigen, ob er durchkommt.',28,500,'#c8d7de',960,1.32); s+=t
    s+=f'<rect x="60" y="{y+30}" width="960" height="250" rx="22" fill="#112230" stroke="#ef8a5b" stroke-width="3"/>'
    t,_=text(96,y+90,'Deine Föhn-Erfahrung am See?',32,800,'#ef8a5b',890,1.25); s+=t
    t,_=text(96,y+140,'Wann ist er bei dir durchgebrochen – und wie schnell? Schreib es in die Kommentare. Genau solche Beobachtungen machen das Modell besser.',26,500,'#e8dcc4',890,1.32); s+=t
    t,_=text(60,y+340,'Quellen: SRF Meteo, inatura Dornbirn (Föhnforschung im Rheintal), austria-forum. Kein Meteorologe am Werk.',22,500,'#8aa6b3',960,1.3); s+=t
    return s
slide(6,a6,'Windshift','Föhn im Blick'); out('foehn',6)

# ================= B: STURMWARNUNG =================
N=5
cover('sturm','Sicherheit','Wenn es orange blinkt','Die Sturmwarnung am Bodensee – in 5 Slides erklärt.',['#f2a93b','#ef5b4c'],[290,280])
def b2(ty):
    s=''; y=ty+40
    for i,(n,f,c,txt) in enumerate([('Starkwindwarnung','40×','#f2a93b','Böen von 25 bis 33 kn erwartet (Bft 6–7)'),('Sturmwarnung','90×','#ef5b4c','Böen ab 33 kn erwartet (ab Bft 8)')]):
        yy=y+i*330; s+=f'<rect x="60" y="{yy}" width="960" height="300" rx="22" fill="#112230" stroke="{c}" stroke-width="3"/>'
        s+=f'<circle cx="190" cy="{yy+150}" r="70" fill="{c}"/>'
        for k in range(8):
            a=math.radians(k*45); s+=f'<line x1="{190+math.cos(a)*88:.0f}" y1="{yy+150+math.sin(a)*88:.0f}" x2="{190+math.cos(a)*112:.0f}" y2="{yy+150+math.sin(a)*112:.0f}" stroke="{c}" stroke-width="6" stroke-linecap="round"/>'
        s+=f'<text x="330" y="{yy+110}" font-size="36" font-weight="800" fill="{c}">{n}</text><text x="330" y="{yy+170}" font-size="44" font-weight="800" fill="#e8f1f5">{f} pro Minute</text>'
        t,_=text(330,yy+225,txt,26,600,'#c8d7de',660,1.3); s+=t
    return s
slide(2,b2,'1 · Zwei Stufen','Zählen hilft: 40 oder 90?'); out('sturm',2)
def b3(ty):
    s=''; y=ty+40
    s+=f'<rect x="60" y="{y}" width="960" height="210" rx="22" fill="#2a1414" stroke="#ef5b4c" stroke-width="3"/>'
    t,_=text(96,y+60,'Keine Vorwarnung!',34,800,'#ef5b4c',890,1.2); s+=t
    t,_=text(96,y+112,'Die Starkwindwarnung kündigt nicht zwingend den Sturm an. Bei schnellen Gewittern kann direkt die Sturmwarnung kommen.',26,500,'#e8dcc4',890,1.32); s+=t
    y+=270
    b,y=bullets(y,['Warnzeiten: April–Oktober 6–22 Uhr, November–März 7–20 Uhr.','Der See ist in drei Warnregionen geteilt: West, Mitte, Ost – es kann im Osten warnen und im Westen nicht.','Bei Sturmwarnung gilt: sofort Maßnahmen für Crew und Boot treffen, den nächsten Hafen ansteuern.']); s+=b
    return s
slide(3,b3,'2 · Gut zu wissen','Was viele nicht wissen'); out('sturm',3)
def b4(ty):
    labels=['10','11','12','13','14','15','16','17']
    s=chart(110,ty+70,900,360,labels,[('Lindau – Böen',[10,19,22,28,36,38,34,14],'#9fb4ff',False),('Rohrspitz – Böen',[14,18,22,25,31,30,31,9],'#c9d85a',False)],44,hlines=((25,'#f2a93b','Starkwind 25 kn'),(33,'#ef5b4c','Sturm 33 kn')))
    y=ty+560
    t,y=text(60,y,'Am 21. Oktober drehte der Wind auf West und frischte stark auf: In Lindau stiegen die Böen am Nachmittag auf 38 kn – über die Sturm-Schwelle.',27,500,'#c8d7de',960,1.32); s+=t
    t,_=text(60,y+16,'Innerhalb von drei Stunden von 19 auf 38 kn. Genau dafür gibt es die Leuchten.',28,800,'#f2c94c',960,1.32); s+=t
    return s
slide(4,b4,'3 · Beispiel 21. Oktober','Von gemütlich zu stürmisch'); out('sturm',4)
def b5(ty):
    s=''; y=ty+40
    t,y=text(60,y,'Windshift zeigt gemessene Böen – live und im Rückblick. Eine Sturmwarnung ersetzt es nicht.',30,700,'#e8f1f5',960,1.3); s+=t
    s+=f'<rect x="60" y="{y+30}" width="960" height="260" rx="22" fill="#2a2110" stroke="#f2a93b" stroke-width="3"/>'
    t,_=text(96,y+92,'Blinkt es orange, gilt die Leuchte – nicht die App.',30,800,'#f2a93b',890,1.25); s+=t
    t,_=text(96,y+150,'Schau vor dem Ablegen auf die Warnleuchten und die Warnungen der Wetterdienste. Und speicher dir die Notrufnummer der Seepolizei.',26,500,'#e8dcc4',890,1.32); s+=t
    t,_=text(60,y+360,'Quellen: Seepolizei Thurgau, YACHT, wetterdienst.de. Kein Meteorologe am Werk.',22,500,'#8aa6b3',960,1.3); s+=t
    return s
slide(5,b5,'Windshift','Was die App kann – und was nicht'); out('sturm',5)

# ================= C: PFÄNDERWIND =================
N=5
cover('pfaender','Windsysteme · Teil 2','Pfänderwind','Wenn es in Bregenz bläst und draußen kaum.',['#f2c94c','#7bd88f'],[200,315])
def c2(ty):
    s=''; y=ty+30
    for i,(h,d,c,meta) in enumerate([('Typ 1: Ost / Nordost','Kalte Luft schwappt über den Pfänderrücken und fällt auf Lochau und Bregenz. Kräftig am Ufer, draußen schnell weg.','#f2c94c','ca. 12 Tage im Jahr · vor allem im Frühling'),('Typ 2: Südost','Nachts und am Morgen fließt Luft aus dem Tal der Bregenzer Ach über den Gebhardsberg Richtung See.','#7bd88f','ca. 40 Tage im Jahr · abends bis morgens')]):
        yy=y+i*340; s+=f'<rect x="60" y="{yy}" width="960" height="310" rx="22" fill="#112230" stroke="{c}" stroke-width="3"/>'
        s+=f'<text x="96" y="{yy+64}" font-size="34" font-weight="800" fill="{c}">{html.escape(h)}</text>'
        t,_=text(96,yy+116,d,26,500,'#c8d7de',890,1.32); s+=t
        s+=f'<text x="96" y="{yy+276}" font-size="24" font-weight="700" fill="#e8f1f5">{html.escape(meta)}</text>'
    t,_=text(60,y+720,'Quelle: Gohm et al. (2015), Untersuchung zum Pfänderwind.',22,500,'#8aa6b3',960,1.3); s+=t
    return s
slide(2,c2,'1 · Zwei Typen','Pfänderwind ist nicht gleich Pfänderwind'); out('pfaender',2)
def c3(ty):
    labels=['02','','04','','06','','08','','10','','12','']
    s=chart(110,ty+70,900,340,labels,[('Bregenz',[3,6,5,7,8,9,9,9,7,3,3,2],'#4fc3a1',False),('Rohrspitz',[4,5,3,2,3,4,5,3,6,3,4,4],'#c9d85a',False)],16)
    y=ty+530
    t,y=text(60,y,'26. Oktober: Von 3 bis 10 Uhr weht in Bregenz Südost mit 7–9 kn, Böen bis 17 kn. Nur 9 km weiter in Rohrspitz: meist 3–5 kn.',27,500,'#c8d7de',960,1.32); s+=t
    t,_=text(60,y+16,'Um 11 Uhr ist der Spuk vorbei – typisch für Typ 2, der in den Vormittag hinein ausläuft.',28,800,'#7bd88f',960,1.32); s+=t
    return s
slide(3,c3,'2 · Beispiel 26. Oktober','Südost am Morgen – nur in Bregenz'); out('pfaender',3)
def c4(ty):
    s=''; y=ty+40
    b,y=bullets(y,['Wer früh morgens aus Bregenz oder Lochau ausläuft, hat oft Südost-Wind – der draußen schnell einschläft.','Bei Typ 1 (Ost/Nordost) wird es direkt unter dem Pfänder böig, während vor Lindau oder Hard viel weniger los ist.','In Windshift zeigen die gelbe Pfänder-Linie und der grüne Bregenzerwald-Fächer, wann die beiden aktiv sind. Späher: Sulzberg und Alberschwende.'],dot='#f2c94c'); s+=b
    s+=f'<rect x="60" y="{y+20}" width="960" height="220" rx="22" fill="#112230" stroke="#f2c94c" stroke-width="3"/>'
    t,_=text(96,y+82,'Kennst du den Pfänderwind?',32,800,'#f2c94c',890,1.25); s+=t
    t,_=text(96,y+132,'Wo hat er dich erwischt – und wie weit draußen war er noch zu spüren? Erzähl es in den Kommentaren.',26,500,'#e8dcc4',890,1.32); s+=t
    return s
slide(4,c4,'3 · Für Segler','Was das auf dem Wasser heißt'); out('pfaender',4)
def c5(ty):
    s=''; y=ty+60
    t,y=text(60,y,'Nächste Woche in der Serie:',30,700,'#8aa6b3',960,1.3); s+=t
    t,y=text(60,y+10,'Bise – der kalte Ostwind',56,800,'#9fb4ff',960,1.15); s+=t
    t,_=text(60,y+30,'Folge @windshift.bodensee, um keinen Teil zu verpassen. Live-Karte & Simulator: joemoe.at/windshift (Link in Bio).',28,500,'#c8d7de',960,1.32); s+=t
    return s
slide(5,c5,'Windshift','Die Serie geht weiter'); out('pfaender',5)
