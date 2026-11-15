import re, math, subprocess, html
from PIL import ImageFont
W,H=1080,1350
FD='/usr/share/fonts/opentype/inter/'
FW={400:'Inter-Regular.otf',500:'Inter-Medium.otf',600:'Inter-SemiBold.otf',700:'Inter-Bold.otf',800:'Inter-ExtraBold.otf'}
_f={}
def font(sz,w): 
    k=(sz,w); 
    if k not in _f: _f[k]=ImageFont.truetype(FD+FW[w],sz)
    return _f[k]
def wrap(t,sz,w,maxw):
    out=[]
    for para in t.split('\n'):
        line=''
        for word in para.split(' '):
            tst=(line+' '+word).strip()
            if font(sz,w).getlength(tst)<=maxw: line=tst
            else: out.append(line); line=word
        out.append(line)
    return out
def text(x,y,t,sz=34,w=400,fill='#c8d7de',maxw=1000,lh=1.38,anchor='start'):
    lines=wrap(t,sz,w,maxw); s=''
    for i,l in enumerate(lines):
        s+=f'<text x="{x}" y="{y+i*sz*lh:.1f}" font-size="{sz}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}">{html.escape(l)}</text>'
    return s, y+len(lines)*sz*lh
SYS={'syn':'#9fb4ff','rheintal':'#ef8a5b','rhein':'#5bc0ef','wald':'#7bd88f','pfaender':'#f2c94c','swiss':'#d38cf2','thermal':'#f27fa5'}
LOGO='''<defs><linearGradient id="lg" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#4fc3a1"/><stop offset="1" stop-color="#9fb4ff"/></linearGradient>
<radialGradient id="bg" cx="0.5" cy="0.25" r="0.9"><stop offset="0" stop-color="#14293a"/><stop offset="1" stop-color="#0b1620"/></radialGradient></defs>'''
def mark(x,y,s):
    return f'''<g transform="translate({x} {y}) scale({s})"><path d="M9 33 H35 A10.5 10.5 0 1 0 24.5 22.5" fill="none" stroke="url(#lg)" stroke-width="5.5" stroke-linecap="round"/><path d="M24.5 30 L19 20.5 H30 Z" fill="#9fb4ff" stroke="#9fb4ff" stroke-width="1.5" stroke-linejoin="round"/><path d="M9 45 H44" stroke="#7fb3c8" stroke-width="5" stroke-linecap="round" opacity=".85"/><path d="M15 54 H33" stroke="#7fb3c8" stroke-width="4" stroke-linecap="round" opacity=".5"/></g>'''
N=8
def slide(i, body, kicker, title):
    t,ty=text(60,250,title,64,800,'#e8f1f5',960,1.18)
    s=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Inter">{LOGO}
<rect width="{W}" height="{H}" fill="url(#bg)"/>
{mark(48,44,0.95)}<text x="112" y="88" font-size="30" font-weight="800" fill="#e8f1f5">Windshift</text>
<text x="{W-60}" y="88" font-size="26" font-weight="600" fill="#8aa6b3" text-anchor="end">{i} / {N}</text>
<text x="60" y="176" font-size="26" font-weight="700" fill="#4fc3a1" letter-spacing="3">{html.escape(kicker.upper())}</text>
{t}
{body(ty)}
<line x1="60" y1="{H-92}" x2="{W-60}" y2="{H-92}" stroke="#21414f" stroke-width="2"/>
<text x="60" y="{H-46}" font-size="24" font-weight="700" fill="#e8f1f5">joemoe.at/windshift</text>
<text x="{W-60}" y="{H-46}" font-size="24" font-weight="600" fill="#8aa6b3" text-anchor="end">{'Wischen →' if i<N else '@windshift.bodensee'}</text>
</svg>'''
    open(f's{i}.svg','w').write(s); subprocess.run(['rsvg-convert',f's{i}.svg','-o',f's{i}.png'],check=True)

def arrow(x,y,ang,L,col,w=8):  # ang = direction it points TO (deg, 0=up)
    a=math.radians(ang); dx,dy=math.sin(a),-math.cos(a)
    x2,y2=x+dx*L,y+dy*L; hx,hy=x2-dx*w*2.2,y2-dy*w*2.2; px,py=-dy*w*1.6,dx*w*1.6
    return f'<line x1="{x}" y1="{y}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/><path d="M{x2:.1f} {y2:.1f} L{hx+px:.1f} {hy+py:.1f} L{hx-px:.1f} {hy-py:.1f}Z" fill="{col}"/>'

# ---------- 1 cover ----------
def s1():
    s=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Inter">{LOGO}
<rect width="{W}" height="{H}" fill="url(#bg)"/>'''
    # decorative streamlines
    import random; random.seed(4)
    for k in range(70):
        y=random.uniform(780,1180); x=random.uniform(-50,W); L=random.uniform(60,180); c=random.choice(list(SYS.values()))
        s+=f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+L:.0f}" y2="{y-L*0.18:.0f}" stroke="{c}" stroke-opacity="{random.uniform(.25,.7):.2f}" stroke-width="3" stroke-linecap="round"/>'
    s+=mark(390,140,4.6)
    s+='<text x="540" y="520" font-size="92" font-weight="800" fill="#e8f1f5" text-anchor="middle">Windshift</text>'
    t,_=text(540,600,'So funktioniert die Wind-Karte für den östlichen Bodensee',40,600,'#c8d7de',820,1.3,'middle'); s+=t
    t,_=text(540,1250,'Messung · Windsysteme · Modell · Prognose-Check',28,600,'#4fc3a1',900,1.3,'middle'); s+=t
    s+=f'<text x="{W-60}" y="{H-46}" font-size="24" font-weight="600" fill="#8aa6b3" text-anchor="end">Wischen →</text></svg>'
    open('s1.svg','w').write(s); subprocess.run(['rsvg-convert','s1.svg','-o','s1.png'],check=True)
s1()

# ---------- 2 measurements map ----------
LAKE=eval(re.search(r'const LAKE = (\[\[.*?\]\]);', open('/home/claude/windshift/index.html').read()).group(1))
LAKES=[('Lindau',47.540,9.684),('Bregenz',47.499,9.746),('Rohrspitz',47.497,9.630),('Altenrhein',47.485,9.566),('Friedrichshafen',47.6454,9.4795)]
CATCH=[('Konstanz',47.6774,9.1901,'syn'),('Güttingen',47.6017,9.2794,'syn'),('Säntis',47.2494,9.3435,'syn'),('Dornbirn',47.4325,9.7256,'rheintal'),('Vaduz',47.1275,9.5176,'rheintal'),('Bad Ragaz',47.0166,9.5026,'rheintal'),('Alberschwende',47.4575,9.8486,'wald'),('Sulzberg',47.5219,9.9144,'pfaender'),('St. Gallen',47.4255,9.3985,'swiss')]
def s2(ty):
    lo0,lo1,la0,la1=9.13,9.97,47.39,47.71
    box=(60,ty+20,W-60,ty+20+600)
    kx=75.1; ky=111.2; sc=min((box[2]-box[0])/((lo1-lo0)*kx),(box[3]-box[1])/((la1-la0)*ky))
    ox=box[0]+((box[2]-box[0])-(lo1-lo0)*kx*sc)/2; oy=box[1]
    P=lambda la,lo:(ox+(lo-lo0)*kx*sc, oy+(la1-la)*ky*sc)
    bot=oy+(la1-la0)*ky*sc
    s='<path d="M'+' L'.join(f'{P(la,lo)[0]:.1f} {P(la,lo)[1]:.1f}' for lo,la in LAKE)+'Z" fill="#123a52" stroke="#2b6a8a" stroke-width="2"/>'
    s+='<text x="%.0f" y="%.0f" font-size="24" font-style="italic" fill="#5f93ad" text-anchor="middle">Bodensee</text>'%P(47.585,9.47)
    for n,la,lo,sy in CATCH:
        if la<la0:
            if n=='Bad Ragaz': continue
            lab='Vaduz · Bad Ragaz' if n=='Vaduz' else n
            x,_=P(la0,lo); s+=arrow(round(x,1),round(bot-50,1),180,40,SYS[sy],4)+f'<text x="{x+14:.1f}" y="{bot-18:.1f}" font-size="21" font-weight="600" fill="#c8d7de">{lab} ↓</text>'
            continue
        x,y=P(la,lo); right=n in ('Sulzberg','Alberschwende')
        s+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="#0b1620" stroke="{SYS[sy]}" stroke-width="4"/><text x="{x-18 if right else x+18:.1f}" y="{y+8:.1f}" font-size="22" font-weight="600" fill="#c8d7de" text-anchor="{'end' if right else 'start'}">{n}</text>'
    pos={'Lindau':(14,-16,'start'),'Bregenz':(16,34,'start'),'Rohrspitz':(0,40,'middle'),'Altenrhein':(-16,-14,'end'),'Friedrichshafen':(16,-14,'start')}
    for n,la,lo in LAKES:
        x,y=P(la,lo); dx,dy,an=pos[n]
        s+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="#4fc3a1" stroke="#0b1620" stroke-width="3"/><text x="{x+dx:.1f}" y="{y+dy:.1f}" font-size="24" font-weight="800" fill="#e8f1f5" text-anchor="{an}">{n}</text>'
    y=bot+60
    s+=f'<circle cx="74" cy="{y-8}" r="12" fill="#4fc3a1"/>'
    t,y2=text(100,y,'5 Stationen am See – ihre Messungen zeigt die Karte als Pfeile.',28,500,'#c8d7de',920,1.3); s+=t
    s+=f'<circle cx="74" cy="{y2+8}" r="10" fill="none" stroke="#ef8a5b" stroke-width="4"/>'
    t,y3=text(100,y2+16,'9 Stationen im Umland – farbig nach dem Windsystem, das sie verraten (z. B. Vaduz → Föhn im Rheintal).',28,500,'#c8d7de',920,1.3); s+=t
    t,_=text(60,y3+20,'Alle 10 Minuten neu · offene Daten von GeoSphere Austria, MeteoSwiss und DWD',24,600,'#8aa6b3',960,1.3); s+=t
    return s
slide(2,s2,'1 · Die Messungen','Echte Messwerte')

# ---------- 3 systems ----------
SYSL=[('syn','Großwetterlage','Die großräumige Strömung – vom Gelände entlang der Seeachse gelenkt, an Pfänder und Alpen gebremst.'),
('rheintal','Rheintal','Föhn oder nächtlicher Bergwind aus dem Rheintal – tagsüber umgekehrt als Talwind.'),
('rhein','Rhein-Ausfluss','Kalte Luft fließt nachts entlang des Rheins und tritt bei der Mündung als schmaler Strahl aus.'),
('wald','Bregenzerwald','Abflusswind aus dem Tal der Bregenzer Ach, abends bis morgens, zwischen Bregenz und Hard.'),
('pfaender','Pfänder-Fallwind','Ost-/Nordostwind fällt über den Pfänder auf Lochau und Bregenz – stark am Ufer, draußen schnell weg.'),
('swiss','Appenzeller Hänge','Hangabwind von Süden über Rorschach und Altenrhein.'),
('thermal','Land- ⇄ Seewind','Nachts fließt Luft von allen Ufern aufs Wasser, an sonnigen Nachmittagen umgekehrt.')]
def s3(ty):
    s=''; y=ty+30
    for k,n,d in SYSL:
        s+=f'<rect x="60" y="{y-26}" width="14" height="96" rx="7" fill="{SYS[k]}"/>'
        s+=f'<text x="96" y="{y+4}" font-size="31" font-weight="800" fill="{SYS[k]}">{n}</text>'
        t,y2=text(96,y+42,d,24,500,'#c8d7de',920,1.28); s+=t
        y=max(y2,y+66)+30
    return s
slide(3,s3,'2 · Die Windsysteme','Sieben Windsysteme')

# ---------- 4 model ----------
def s4(ty):
    s=''; y=ty+30
    steps=[('1','Messen','Die Stationen liefern Richtung, Mittelwind und Böen.','#4fc3a1'),
           ('2','Zerlegen','Das Modell sucht die Mischung der 7 Windsysteme, die die Messungen am See am besten erklärt. Die Stationen im Einzugsgebiet liefern Hinweise, z. B. ob gerade Föhn im Rheintal weht.','#9fb4ff'),
           ('3','Füllen','Aus dieser Mischung entsteht ein Windfeld für den ganzen See – dort, wo gemessen wird, wird es an die Messung angepasst.','#f2c94c')]
    for i,(nn,h,d,c) in enumerate(steps):
        bh=190 if i!=1 else 250
        s+=f'<rect x="60" y="{y}" width="960" height="{bh}" rx="22" fill="#112230" stroke="{c}" stroke-width="3"/>'
        s+=f'<circle cx="128" cy="{y+66}" r="38" fill="{c}"/><text x="128" y="{y+80}" font-size="40" font-weight="800" fill="#0b1620" text-anchor="middle">{nn}</text>'
        s+=f'<text x="196" y="{y+78}" font-size="36" font-weight="800" fill="#e8f1f5">{html.escape(h)}</text>'
        t,_=text(196,y+122,d,26,500,'#c8d7de',790,1.32); s+=t
        y+=bh
        if i<2: s+=arrow(540,y+8,180,34,'#3d6577',6); y+=52
    t,_=text(60,y+56,'Wichtig: Das ist ein vereinfachtes Erklär-Modell, kein Wettermodell. Es zeigt, was gerade passiert – eine Vorhersage ist es nicht.',26,600,'#f2a93b',960,1.32); s+=t
    return s
slide(4,s4,'3 · Das Modell','Vom Messpunkt zum Windfeld')

# ---------- 5 legend ----------
def s5(ty):
    s=''; y=ty+40; X=200
    def row(icon, h, d):
        nonlocal s,y
        s+=icon(110,y+20)
        s+=f'<text x="{X}" y="{y+12}" font-size="31" font-weight="800" fill="#e8f1f5">{html.escape(h)}</text>'
        t,y2=text(X,y+52,d,25,500,'#c8d7de',820,1.3); s+=t
        y=max(y2,y+90)+30
    row(lambda x,y: arrow(x-34,y+20,60,80,'#c9d85a',9), 'Pfeil = Messung','Zeigt, wohin der Wind weht. Zahlen: Mittelwind / Böe der letzten 10 Minuten.')
    def flow(x,y):
        o=''
        for k,(dy,c) in enumerate([(-22,'#ef8a5b'),(0,'#f27fa5'),(22,'#9fb4ff')]):
            o+=f'<path d="M{x-50} {y+dy+10} q30 -14 60 -6 t40 -8" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round"/>'
        return o
    row(flow,'Strömung = Modell','Die fließenden Linien kommen aus dem Modell. Ihre Farbe zeigt, welches Windsystem dort dominiert.')
    row(lambda x,y: f'<path d="M{x-10} {y-20} L{x+50} {y-38} L{x+50} {y+50} Z" fill="#ef8a5b" fill-opacity=".25" stroke="#ef8a5b" stroke-width="3"/><circle cx="{x-10}" cy="{y-20}" r="6" fill="#ef8a5b"/>','Fächer & Linien = aktive Systeme','Wie weit ein Windsystem reicht. Je kräftiger die Farbe, desto stärker ist es gerade.')
    row(lambda x,y: f'<rect x="{x-56}" y="{y-8}" width="128" height="40" rx="20" fill="#0b1620" stroke="#ef8a5b" stroke-width="3"/><text x="{x+8}" y="{y+20}" font-size="20" font-weight="700" fill="#e8f1f5" text-anchor="middle">Föhn 29%</text>','Prozent = Stärke','Wie stark das System im Vergleich zu seinem typischen Maximum weht.')
    row(lambda x,y: f'<rect x="{x-60}" y="{y-12}" width="70" height="38" rx="19" fill="#4fc3a1"/><text x="{x-25}" y="{y+14}" font-size="16" font-weight="800" fill="#071a14" text-anchor="middle">LIVE</text><rect x="{x+16}" y="{y-12}" width="70" height="38" rx="19" fill="#f2a93b"/><text x="{x+51}" y="{y+14}" font-size="13" font-weight="800" fill="#071a14" text-anchor="middle">SIMUL.</text>','Grün = Live · Orange = Simulation','In geteilten Bildern verrät der Rahmen sofort, ob echte Messdaten oder ein angenommenes Szenario zu sehen sind.')
    return s
slide(5,s5,'4 · Die Karte lesen','Was bedeutet was?')

# ---------- 6 simulator & circle ----------
def s6(ty):
    s=''; cx,cy=540,ty+250
    # land-breeze convergence: arrows inward
    for a in range(0,360,30):
        r1,r2=230,140; x1=cx+math.sin(math.radians(a))*r1; y1=cy-math.cos(math.radians(a))*r1
        s+=arrow(round(x1,1),round(y1,1),(a+180)%360,r1-r2,'#f27fa5',6)
    s+=f'<circle cx="{cx}" cy="{cy}" r="12" fill="#f27fa5"/>'
    s+=f'<circle cx="{cx}" cy="{cy}" r="95" fill="none" stroke="#ffd166" stroke-width="5" stroke-dasharray="2 14" stroke-linecap="round"/>'
    s+=f'<g transform="translate({cx+95} {cy}) rotate(0)"><path d="M0 -22 L12 16 L0 10 L-12 16Z" fill="#ffd166" stroke="#0b1620" stroke-width="3"/></g>'
    s+=f'<text x="{cx}" y="{cy+290}" font-size="22" font-weight="600" fill="#8aa6b3" text-anchor="middle">Nachts: Landwind läuft von allen Ufern zusammen – das Boot fährt mit festem Windwinkel im Kreis</text>' if False else ''
    y=cy+300
    t,y=text(60,y,'Im Simulator stellst du die Windsysteme selbst ein oder lädst Szenarien wie Föhnsturm, Bise mit Pfänderwind oder Sommernachmittag.',27,500,'#c8d7de',960,1.32); s+=t
    t,y=text(60,y+14,'Setz ein Boot aufs Wasser: Es hält stur denselben Winkel zum Wind – wie mit festgeschoteten Segeln.',27,500,'#c8d7de',960,1.32); s+=t
    t,y=text(60,y+14,'In einer ruhigen Nacht läuft der Landwind von allen Ufern zusammen. Wer quer zum Wind segelt, fährt einmal im Kreis – ohne die Segel anzufassen.',27,700,'#ffd166',960,1.32); s+=t
    return s
slide(6,s6,'5 · Simulator & Boots-Test','Warum man im Kreis segeln kann')

# ---------- 7 forecast check ----------
def s7(ty):
    s=''; y=ty+20
    t,y=text(60,y+10,'Windshift speichert jede Stunde die Prognosen von 6 Wettermodellen und vergleicht sie mit den Messungen.',27,500,'#c8d7de',960,1.32); s+=t
    s+=f'<text x="60" y="{y+50:.0f}" font-size="28" font-weight="800" fill="#e8f1f5">Treffer bei Wind ab 4 Bft</text><text x="60" y="{y+86:.0f}" font-size="22" font-weight="500" fill="#8aa6b3">Prognose vom Vortag · erste 30 Tage (Herbst)</text>'
    bars=[('ICON-CH2 · MeteoSwiss',39,'#ff9b85'),('ICON-D2 · DWD',32,'#f2c94c'),('ICON-EU · DWD',23,'#b08d57'),('ECMWF · global',16,'#9fb4ff')]
    by=y+130; bw=600
    for n,v,c in bars:
        s+=f'<text x="60" y="{by+30:.0f}" font-size="25" font-weight="700" fill="#e8f1f5">{n}</text>'
        s+=f'<rect x="60" y="{by+46:.0f}" width="{bw}" height="30" rx="15" fill="#16303f"/><rect x="60" y="{by+46:.0f}" width="{bw*v/50:.0f}" height="30" rx="15" fill="{c}"/>'
        s+=f'<text x="{60+bw*v/50+16:.0f}" y="{by+71:.0f}" font-size="28" font-weight="800" fill="{c}">{v}%</text>'
        by+=104
    t,_=text(60,by+40,'Im Schnitt liegt auch das beste Modell rund 2 kn und 35° daneben. Für die Entscheidung vor Ort zählen die Live-Messungen.',27,600,'#f2c94c',960,1.32); s+=t
    return s
slide(7,s7,'6 · Prognose-Check','Welches Wettermodell trifft den See?')

# ---------- 8 outro ----------
def s8(ty):
    s=''; y=ty+30
    items=[('Jeden Morgen um 8:00','die aktuelle Lage als Bild – automatisch aus den Messungen.'),
           ('Rückblicke vom Wasser','Fotos und Beobachtungen mit den Messdaten des Tages.'),
           ('Live-Karte & Simulator','auf joemoe.at/windshift – Link in der Bio.')]
    for h,d in items:
        s+=f'<rect x="60" y="{y-34}" width="960" height="132" rx="22" fill="#112230" stroke="#21414f" stroke-width="2"/>'
        s+=f'<text x="96" y="{y+14}" font-size="30" font-weight="800" fill="#4fc3a1">{html.escape(h)}</text>'
        t,_=text(96,y+56,d,25,500,'#c8d7de',890,1.3); s+=t
        y+=152
    y+=6
    s+=f'<rect x="60" y="{y-34}" width="960" height="330" rx="22" fill="#2a2110" stroke="#f2a93b" stroke-width="3"/>'
    s+=f'<text x="96" y="{y+16}" font-size="31" font-weight="800" fill="#f2a93b">Kein Meteorologe am Werk</text>'
    t,yy=text(96,y+60,'Windshift ist ein Hobbyprojekt aus echten Messdaten, künstlicher Intelligenz, jahrzehntelanger Segelerfahrung in diesem Revier – und einer wilden Theorie.',26,500,'#e8dcc4',890,1.32); s+=t
    t,_=text(96,yy+10,'Keine offizielle Wettervorhersage und kein Ersatz für Sturmwarnungen. Feedback, Daten und Widerspruch sind willkommen!',26,700,'#f2c94c',890,1.32); s+=t
    return s
slide(8,s8,'Folge @windshift.bodensee','Was dich hier erwartet')
