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

