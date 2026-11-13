"""Derived formats draw exclusively from the selected target's source.
Visual questions retain their image; multipart questions use labelled image panels.
"""
from g1lib import Item, Diagram, FN, Reject, name, _norm


def extras_for(core):
    def draw(r,L):
        p=core(r,L)
        if p.answer is None or p.parts or p.options:raise Reject()
        return p
    def wrong(p,r):
        xs=[w for w,_ in p.wrong if _norm(w)!=_norm(p.answer)]
        if not xs:raise Reject()
        return r.choice(xs)
    def err(r,L):
        p=draw(r,L);shown=wrong(p,r);nm=name(r)
        return Item(f'{nm} tried this problem: {p.prompt}\n{nm} answered {shown}. Give the correct answer.',p.answer,
                    [f'{shown} is not correct.']+p.steps,p.wrong,check=p.check,qtype='error-analysis',
                    diagram=p.diagram,mode='sa',misconception=f'answered {shown}')
    def tf(r,L):
        p=draw(r,L);truth=r.choice([True,False]);shown=p.answer if truth else wrong(p,r)
        opts=[('True',truth),('False',not truth)]
        return Item(f'{p.prompt}\nAnswer shown: {shown}. Is that answer true or false?', 'True' if truth else 'False',
                    p.steps,check=FN('tf',inner=p.check,shown=shown),options=opts,diagram=p.diagram,qtype='true-false',mode='mc')
    def group(r,L,kind):
        ps=[];seen=set()
        for _ in range(100):
            p=draw(r,L);key=(p.prompt,p.diagram.alt if p.diagram else '')
            if key in seen:continue
            seen.add(key);ps.append(p)
            if len(ps)==4:break
        if len(ps)<4:raise Reject()
        panels=[];alt=[];parts=[];opts=[];table={};steps=[]
        for i,p in enumerate(ps):
            label='ABCD'[i];prefix=f'({label}) '
            prompt=prefix+p.prompt
            if p.diagram:
                panels.append({'label':label,'kind':p.diagram.kind,'data':p.diagram.data});alt.append(label+': '+p.diagram.alt)
            steps.append(prefix+' '.join(p.steps))
            if kind=='open':parts.append((prompt,p.answer,p.check))
            else:
                shown=p.answer if i<2 else wrong(p,r)
                text=prompt+' → '+shown
                opts.append((text,i<2));table[text]={'inner':p.check,'shown':shown}
        diagram=Diagram('panels',{'panels':panels},' '.join(alt)) if panels else None
        if kind=='open':return Item('Answer each part. Use the matching labelled picture when shown.',None,steps,parts=parts,diagram=diagram,qtype='multi-step')
        r.shuffle(opts)
        return Item('Select ALL the problems matched to a correct answer. Use the labelled pictures.',None,steps,
                    options=opts,check=FN('claims',table=table),diagram=diagram,qtype='explain')
    def sel(r,L):return group(r,L,'sel')
    def opn(r,L):return group(r,L,'open')
    result={'err':err,'tf':tf,'sel':sel,'open':opn}
    for k,f in result.items():f.__name__=k+'_'+core.__name__;f.levels=[0,1,2];f.mode='any';f.qtype='conceptual'
    return result
