import re, subprocess, os, sys
from collections import OrderedDict
PORT='dc6e5ffd74f6275390a9c4a676aafdca058df7dd'; FORK='9208dcf5a358f40afd95c99480e4e09f781ed566'
OUT='/srv/dune/tasks/p7s/lead'; os.makedirs(OUT, exist_ok=True)
env=dict(os.environ, PATH='/srv/dune/tools/git-lfs-3.6.1/usr/bin:'+os.environ['PATH'])
def grep(args):
    r=subprocess.run(['git','-C','/srv/dune/worktrees/u35','grep','-n']+args, capture_output=True, text=True, env=env)
    return r.stdout.splitlines()
LIT=re.compile('"((?:[^"\\\\\\n]|\\\\.)*)"')
TXT=re.compile(r'[A-Za-zА-Яа-яЁё]')
def split(l, sha):
    rest=l[len(sha)+1:]; p, n, code = rest.split(':',2); return p, n, code
pc=grep(['-E', r'withLabel\(|drawText[A-Za-z]*\(|setText\(|withText\(|setMessage\(|addNotification\(', PORT, '--', 'src/gamestates','src/drawers','src/managers','src/sidebar','src/gui','src/game'])
open(f'{OUT}/port-calls.txt','w').write('\n'.join(pc)+'\n')
ps=[]
for l in pc:
    p,n,code=split(l,PORT); lits=[m.group(1) for m in LIT.finditer(code) if TXT.search(m.group(1))]
    if lits: ps.append((p,n,lits))
with open(f'{OUT}/port-strings.tsv','w') as f:
    f.write('путь\tстрока\tлитералы\n')
    for p,n,lits in ps: f.write(f'{p}\t{n}\t{" | ".join(lits)}\n')
fc=grep(['-E', r'localization::text\(', FORK, '--', 'src'])
open(f'{OUT}/fork-calls.txt','w').write('\n'.join(fc)+'\n')
def call_args(code, start):
    depth=1; i=start; out=[]; 
    while i < len(code):
        c=code[i]
        if c=='"':
            m=LIT.match(code,i)
            if m: out.append(m.group(1)); i=m.end(); continue
        if c=="'":
            m=re.compile("'(?:[^'\\\\]|\\\\.)'").match(code,i)
            if m: i=m.end(); continue
        if c=='(': depth+=1
        elif c==')':
            depth-=1
            if depth==0: break
        i+=1
    return out
fp=[]
for l in fc:
    p,n,code=split(l,FORK)
    for m in re.finditer(r'localization::text\(', code):
        a=call_args(code, m.end())
        fp.append((p,n,a[0],a[1]) if len(a)>=2 else (p,n,'не литерал','не литерал'))
with open(f'{OUT}/fork-pairs.tsv','w') as f:
    f.write('путь\tстрока\tанглийский\tрусский\n')
    for r in fp: f.write('\t'.join(r)+'\n')
eng=OrderedDict()
for p,n,e,ru in fp:
    if e!='не литерал' and e not in eng: eng[e]=ru
with open(f'{OUT}/match.tsv','w') as f:
    f.write('английский\tрусский\tстрок в PORT\tместа в PORT\n')
    for e,ru in eng.items():
        g=grep(['-F', '"'+e+'"', PORT, '--', 'src'])
        places=' | '.join(':'.join(split(x,PORT)[:2]) for x in g[:5]) or 'нет'
        f.write(f'{e}\t{ru}\t{len(g)}\t{places}\n')
po=OrderedDict()
for p,n,lits in ps:
    for x in lits:
        if x not in eng: po.setdefault(x,[]).append(f'{p}:{n}')
with open(f'{OUT}/port-only.tsv','w') as f:
    f.write('литерал\tместа\n')
    for x,pl in po.items(): f.write(f'{x}\t{" | ".join(pl)}\n')
print('port-calls',len(pc),'port-strings',len(ps),'distinct',len({x for _,_,l in ps for x in l}))
print('fork-calls',len(fc),'fork-pairs',len(fp),'nonlit',sum(1 for r in fp if r[2]=='не литерал'),'eng distinct',len(eng))
print('match',len(eng),'zero',sum(1 for e in eng if True) , 'port-only',len(po))
