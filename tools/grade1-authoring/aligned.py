"""Target-specific Grade 1 sources. No domain fallback is permitted.

Each target owns its source, including every derived format. Ladders vary scaffolding,
number range, missing position, and explanation demand, rather than labels alone.
"""
from g1lib import Item, Diagram, FN, need, name, _norm
from families import wrong_numbers, ntext


def item(prompt, answer, check, steps=None, diagram=None, wrong=None, tags=()):
    answer = str(answer)
    if wrong is None:
        if answer.isdigit():
            n = int(answer)
            wrong = wrong_numbers(n, [n+1, n-1, n+10, max(0,n-10), n+2])
        else:
            wrong = [(s, 'does not match the model or rule') for s in ['0','1','2','10'] if s != answer]
    return Item(prompt, answer, steps or [f'Use the given information.', f'The answer is {answer}.'],
                wrong, check=check, diagram=diagram, tags=set(tags), qtype='conceptual')


def dg(kind, data, alt):
    return Diagram(kind, data, alt)


def calc(a,b,op='+',prompt=None,diagram=None,steps=None):
    ans=a+b if op=='+' else a-b
    return item(prompt or f'{a} {op} {b} = ?', ans, FN('add' if op=='+' else 'sub',a=a,b=b),
                steps or [f'{a} {op} {b} = {ans}.'],diagram,
                wrong_numbers(ans,[a+b if op!='+' else abs(a-b),ans+1,ans-1,ans+10,a,b]))


def numbers(r,L,top=20):
    cap = (min(top,8), min(top,16), top)[L]
    total=r.randint(3,cap); part=r.randint(1,total-1)
    return total,part,total-part


def story(r,L,kind,top=20,model=False,equation=False):
    t,a,b=numbers(r,L,top); nm=name(r); thing=r.choice(['shells','stickers','blocks','books'])
    if kind in ['result','subtract']:
        take=kind=='subtract' or r.choice([False,True]); op='−' if take else '+'
        x,y=(t,b) if take else (a,b); ans=a if take else t
        p=f'{nm} has {x} {thing} and '+(f'gives away {b}. How many are left?' if take else f'gets {b} more. How many now?')
        ck=FN('sub' if take else 'add',a=x,b=y)
    elif kind=='change':
        take=(L==0 or r.choice([True,False]));x,y=(t,a) if take else (a,t);ans=b
        p=(f'{nm} had {t} {thing}. Some were given away. Now there are {a}. How many were given away?' if take else
           f'{nm} had {a} {thing}. Some more arrived. Now there are {t}. How many arrived?')
        ck=FN('missing_part',total=t,part=a);op='−' if take else '+'
    elif kind=='start':
        x,y=t,b;ans=a;op='+'
        p=f'{nm} had some {thing}. {b} more arrived. Now there are {t}. How many were there at the start?'
        ck=FN('missing_part',total=t,part=b)
    elif kind=='sub-start':
        x,y=a,b;ans=t;op='−'
        p=f'{nm} had some {thing}. {b} were given away. Now there are {a}. How many were there at the start?'
        ck=FN('add',a=a,b=b)
    elif kind=='part':
        x,y=t,a;ans=b;op='−'
        p=f'{nm} has {t} {thing} in all. {a} are red and the rest are blue. How many are blue?'
        ck=FN('missing_part',total=t,part=a)
    else:
        x,y=t,a;ans=b;op='−'
        p=f'{nm} has {t} {thing}. Sam has {a}. How many '+('fewer does Sam have?' if L==2 else f'more does {nm} have?')
        ck=FN('sub',a=t,b=a)
    diagram=None
    if model:
        # Unknown quantities are boxes, never revealed by a completed counter model.
        if kind=='compare':
            diagram=dg('comparegroups',{'left':{'count':t,'label':nm,'color':'blue'},'right':{'count':a,'label':'Sam','color':'orange'}},f'{nm}: {t} counters. Sam: {a} counters.')
        elif kind in ['result','subtract']:
            diagram=dg('numbercards',{'cards':[str(x),str(y),'?'],'caption':'Start, change, unknown result'},f'Start {x}; change {y}; result unknown.')
        else:
            diagram=dg('numbercards',{'cards':[str(t),str(a),'?'],'caption':'Whole, known part, missing part'},f'Whole {t}; known part {a}; other part unknown.')
    if equation:
        # Result stories only here: require writing an equation, not merely a total.
        ans=f'{x} {op} {y} = {ans}'
        ck=FN('eq_text',kind='add' if op=='+' else 'sub',a=x,b=y)
        p+=' Write an equation with its answer.'
        wrong=[(f'{x} {op} {y} = {x+y+1}', 'incorrect result'),(f'{x} + {y} = {x+y+2}','incorrect operation or result'),(f'{x} − {y} = {x-y-1}','incorrect result')]
    else:wrong=None
    return item(p,ans,ck,[f'The whole is {t}; its parts are {a} and {b}.',f'{a} + {b} = {t}; {t} − {a} = {b}.'],diagram,wrong,tags={'story'})


def arithmetic(r,L,task):
    t,a,b=numbers(r,L,10 if task in ['add10','sub10','facts10','parts10','unknown10','equal'] else 20)
    if task in ['add10','sub10','facts10','facts20']:
        op='−' if task=='sub10' or task.startswith('facts') and r.choice([True,False]) else '+'
        if L==2:
            if op=='−':return item(f'{t} − □ = {a}. Find the missing number.',b,FN('missing_part',total=t,part=a),[f'{t} − {b} = {a}.'])
            return item(f'□ + {a} = {t}. Find the missing addend.',b,FN('missing_part',total=t,part=a),[f'{b} + {a} = {t}.'])
        if op=='−':return calc(t,a,'−')
        return calc(a,b)
    if task=='count12':
        a=r.randint(2,(7,12,18)[L]);b=r.randint(1,2);back=r.choice([True,False]);ans=a-b if back else a+b
        return calc(a,b,'−' if back else '+',f'Count {"back" if back else "on"} {b} from {a}. Where do you land?',
                    dg('numberline',{'min':0,'max':20,'marks':[a]},f'Number line with start {a} marked.') if L==0 else None)
    if task=='frame10':
        t,a,b=numbers(r,L,10)
        if L==2:
            return item(f'The two frames have {t} counters in all. One frame shows {a}. How many must the other frame show?',b,FN('missing_part',total=t,part=a),[f'{a} + {b} = {t}.'],dg('tenframe',{'filled':[a],'caption':'Other frame hidden'},f'One frame shows {a}; the other is hidden.'))
        return calc(a,b,prompt=f'Use the ten-frames. {a} + {b} = ?',diagram=dg('tenframe',{'filled':[a,b]},f'Two ten-frames with {a} and {b} counters.'))
    if task in ['parts10','unknown10','unknown20','missing10']:
        if task=='missing10':t=10;a=r.randint(1,9);b=t-a
        style=L
        p=([f'{a} + □ = {t}',f'□ + {a} = {t}',f'{t} − □ = {a}'][style])+' What number belongs in □?'
        return item(p,b,FN('missing_part',total=t,part=a),[f'{a} and {b} make {t}.',f'{t} − {a} = {b}.'])
    if task=='equal':
        # Equality across both sides; Advanced uses two nontrivial expressions.
        c=0 if L==0 else r.randint(1,t-1); d=t-c
        p=f'{a} + {b} = '+(f'□' if L==0 else f'{c} + □')+'. What number makes both sides equal?'
        return item(p,d,FN('missing_part',total=t,part=c),[f'The left side is {t}.',f'The right side must also be {t}: {c} + {d} = {t}.'])
    if task in ['related','related-sub','count-diff']:
        p=f'{a} + □ = {t}. Use addition to find {t} − {a}.'
        if task=='related' and L==0:p=f'{a} + {b} = {t}. Use this fact to find {t} − {a}.'
        if L==2:p=f'{t} − □ = {a}. What missing number makes the related addition fact true?'
        if task=='count-diff':p=f'Count on from {a} to {t}. How many steps of 1? Use this to find {t} − {a}.'
        return item(p,b,FN('sub',a=t,b=a),[f'{a} + {b} = {t}.',f'So {t} − {a} = {b}.'])
    if task=='compose10':
        # Ask about the trade; no unrelated counting by tens.
        n=r.randint(10,(19,29,39)[L]);full=n//10;loose=n%10
        return item(f'Bundle every 10 of these {n} loose ones. How many full tens can you make?',full,
                    FN('bundle',n=n),[f'Each bundle uses 10 ones.',f'{n} ones make {full} full tens and {loose} loose ones.'],
                    dg('counters',{'groups':[{'count':n,'color':'blue'}],'caption':'Bundle groups of 10'},f'{n} loose counters to bundle.') if L==0 else None)
    if task=='teen':
        n=r.randint(11,19)
        if L==0:return item(f'1 ten and {n-10} ones make what number?',n,FN('tens_ones',tens=1,ones=n-10),diagram=dg('baseten',{'tens':1,'ones':n-10},f'1 ten and {n-10} ones.'))
        p=f'{n} = 10 + □. How many extra ones?'
        if L==2:p=f'{n} is 1 ten and some extra ones. How many extra ones must be removed to leave 10?'
        return item(p,n-10,FN('sub',a=n,b=10),[f'{n} = 10 + {n-10}.'])
    if task in ['teen-ops','teen-sub']:
        a=r.randint(12,19);b=r.randint(1,a-10);sub=task=='teen-sub' or r.choice([True,False]);
        if not sub:b=r.randint(1,19-a) if a<19 else 0
        p=calc(a,b,'−' if sub else '+')
        if L==0 or task=='teen-sub':p.diagram=dg('tenframe',{'filled':[10,a-10]},f'A full ten-frame and {a-10} extra counters.')
        if L==2:p.prompt=f'Keep the ten whole. {p.prompt} Explain using the extra ones.'
        p.steps=[f'Keep 10. Work with the extra ones: {a-10} {"−" if sub else "+"} {b}.']+p.steps
        return p
    if task in ['make-ten','cross10']:
        a=r.randint(6,9);b=r.randint(11-a,9);s=a+b;k=10-a
        if task=='cross10' or L==0:
            return calc(a,b,prompt=f'Make a ten to solve {a} + {b}. What is the sum?',diagram=dg('tenframe',{'filled':[a,b]},f'Ten-frames with {a} and {b} counters.') if L==0 else None,
                        steps=[f'Split {b} into {k} and {b-k}.',f'{a} + {k} = 10; 10 + {b-k} = {s}.'])
        if L==1:return item(f'To make a ten in {a} + {b}, split {b}. How much must move to {a}?',k,FN('missing_part',total=10,part=a),[f'{a} + {k} = 10.'])
        return item(f'{a} + {b} = 10 + □. What is left after making a ten?',s-10,FN('sub',a=s,b=10),[f'Move {k} from {b} to {a}.',f'The rest is {b-k}.'])
    if task=='three':
        c=r.randint(1,(3,5,8)[L]);need(t+c<=20)
        return item(f'{a} + {b} + {c} = ?',t+c,FN('add3',a=a,b=b,c=c),[f'{a} + {b} = {t}.',f'{t} + {c} = {t+c}.'])
    raise ValueError(task)


def place(r,L,task):
    n=r.randint((10,30,60)[L],(39,79,99)[L]);t,o=divmod(n,10)
    if task in ['group','regroup','equiv']:
        if task=='group':
            return item(f'{n} loose ones are bundled in groups of 10. How many full tens?',t,FN('bundle',n=n),[f'{t} groups of 10 and {o} loose ones make {n}.',f'Make {t} full tens; {o} ones remain.'])
        trade=1 if L<2 else r.randint(1,t);new=t-trade;ans=o+10*trade
        p=f'{n} is {t} tens and {o} ones. Trade {trade} '+('ten' if trade==1 else 'tens')+f' for ones. It is now {new} tens and how many ones?'
        return item(p,ans,FN('equiv_ones',n=n,tens=new),[f'Trade each ten for 10 ones.',f'{o} + {trade*10} = {ans} loose ones.'],dg('baseten',{'tens':t,'ones':o},f'{t} tens and {o} ones.') if L==0 else None)
    if task=='tens-count':
        a=r.randint(0,8)*10
        return calc(a,10,prompt=f'Count by tens: {a}, □. What comes next?')
    if task in ['complete-tens','ten-ops']:
        k=r.randint(1,(2,4,7)[L])*10
        a=r.randint(1,8)*10+(0 if task=='complete-tens' else r.randint(1,9));minus=r.choice([True,False]);need(0<=a-k if minus else a+k<=99)
        return calc(a,k,'−' if minus else '+',steps=[f'Change the tens by {k//10}; keep the ones.',f'{a} {"−" if minus else "+"} {k} = {a-k if minus else a+k}.'])
    if task=='represent':
        alt=t-1;ones=o+10
        return item(f'One model has {t} tens and {o} ones. Another has {alt} tens and {ones} ones. Which numeral matches BOTH?',n,FN('tens_ones',tens=alt,ones=ones),[f'Trade 1 ten for 10 ones.',f'Both show {n}.'])
    if task in ['model','draw','numeral']:
        if task=='draw':
            ans=f'{t} tens and {o} ones'
            return item(f'Draw base-ten blocks for {n}. How many tens rods and loose ones should your drawing have?',ans,FN('model_parts',n=n),[f'The tens digit is {t}; the ones digit is {o}.',f'Draw {t} rods and {o} loose cubes.'],wrong=[(f'{o} tens and {t} ones','swapped digits'),(f'{t+1} tens and {o} ones','extra ten'),(f'{t} tens and {o+1} ones','extra one')])
        return item('Write the numeral shown by these base-ten blocks.',n,FN('tens_ones',tens=t,ones=o),[f'{t} tens = {t*10}; add {o} ones.',f'The numeral is {n}.'],dg('baseten',{'tens':t,'ones':o},f'{t} tens rods and {o} one cubes.'))
    if task=='value':
        which='ones' if r.choice([True,False]) else 'tens';val=o if which=='ones' else t*10
        return item(f'What is the value of the {which} digit in {n}?',val,FN('digit_value',n=n,which=which),[f'The {which} digit stands for {val}.'])
    if task in ['compare','symbol']:
        m=r.randint(10,99) if L==0 else t*10+r.randint(0,9)
        if L==2:m=n+r.choice([-1,0,1]);need(10<=m<=99)
        if task=='symbol':return item(f'Fill in <, >, or =: {n} □ {m}', '>' if n>m else '<' if n<m else '=',FN('symbol',a=n,b=m),[f'Compare tens, then ones: {n} and {m}.'],wrong=[(x,'wrong comparison') for x in ['<','>','='] if x!=('>' if n>m else '<' if n<m else '=')])
        need(n!=m)
        return item(f'Compare the tens, then the ones. Which is greater: {n} or {m}?',max(n,m),FN('which_number',a=n,b=m,which='greater'),[f'{max(n,m)} is greater than {min(n,m)}.'])
    if task=='order':
        vals=r.sample(range(10,40) if L==0 else range(t*10,min(t*10+10,100)),3 if L<2 else 4)
        return item('Order from least to greatest: '+', '.join(map(str,vals)),', '.join(map(str,sorted(vals))),FN('sorted',values=vals,direction='asc'),['Compare tens first, then ones.','Order: '+', '.join(map(str,sorted(vals)))],wrong=[(', '.join(map(str,sorted(vals,reverse=True))),'reversed order'),(', '.join(map(str,vals[::-1])),'did not compare digits'),(', '.join(map(str,vals)),'kept original order')])
    if task=='riddle':
        p=f'I have {t} tens and {o} ones. What number am I?'
        if L==1:p=f'I am between {t*10} and {t*10+10}. My ones digit is {o}. What number am I?';need(o>0)
        if L==2:p=f'I have {t-1} tens and {o+10} loose ones. What number am I?'
        return item(p,n,FN('tens_ones',tens=t,ones=o),[f'{t} tens and {o} ones make {n}.'])
    raise ValueError(task)


def addition100(r,L,i):
    carry=i in [4,5,7,8,9];one=i in [1,4]
    at=r.randint(1,(3,5,7)[L]);ao=r.randint(1,8);bt=0 if one else r.randint(1,9-at)
    bo=r.randint(10-ao,9) if carry else r.randint(1,9-ao)
    a,b=at*10+ao,bt*10+bo;s=a+b;need(s<=100)
    steps=[f'Add tens: {at*10} + {bt*10} = {(at+bt)*10}.',f'Add ones: {ao} + {bo} = {ao+bo}.']
    if carry:steps.append(f'{ao+bo} ones = 1 ten and {ao+bo-10} ones.')
    steps.append(f'The sum is {s}.')
    model=dg('addmodel',{'a':a,'b':b},f'Two separate addends: {at} tens and {ao} ones; {bt} tens and {bo} ones.') if L==0 or i in [5,8] else None
    if i in [1,2,4,7]:return calc(a,b,diagram=model,steps=steps)
    if i==3:
        ans=f'{(at+bt)*10} + {ao+bo} = {s}'
        return item(f'Add {a} + {b} by place value. Write the equation combining the total tens and total ones.',ans,FN('place_equation',a=a,b=b),steps,model,wrong=[(f'{at+bt} + {ao+bo} = {s}','tens treated as ones'),(f'{(at+bt)*10} + {ao+bo} = {s+1}','incorrect sum'),(f'{a} + {b} = {s-1}','incorrect sum')])
    if i==5:
        return item(f'The drawings show {a} + {b}. Circle 10 loose ones to make a new ten. How many loose ones remain?',(ao+bo)%10,FN('regroup_remainder',a=a,b=b),steps,model)
    if i==6:
        ans=f'{at*10+bt*10} + {ao+bo} = {s}'
        return item(f'{a} + {b} = {s}. Write an equal equation by adding tens together and ones together.',ans,FN('place_equation',a=a,b=b),steps,model,wrong=[(f'{at+bt} + {ao+bo} = {s}','lost tens value'),(f'{at*10+bt*10} + {ao+bo} = {s-1}','wrong sum'),(f'{a} − {b} = {s}','wrong operation')])
    if i==8:
        return item(f'Use the drawings for {a} + {b}. After trading 10 ones, how many tens are there in all?',s//10,FN('regroup_tens',a=a,b=b),steps,model)
    ans=f'10 ones make 1 ten; both methods give {s}'
    return item(f'{a} + {b}: One method gives {(at+bt)*10} + {ao+bo}. Another gives {(s//10)*10} + {s%10}. Why are they equal?',ans,FN('regroup_reason',a=a,b=b),steps,model,wrong=[(f'10 ones make 10 tens; both methods give {s}','incorrect trade'),(f'Trading adds 10 to the total, giving {s+10}','changes value'),(f'Trading removes 10, giving {s-10}','changes value')])


def data(r,L,i):
    labels=r.sample(['red','blue','green','yellow'],2 if L==0 else 3)
    counts=r.sample(range(1,(6,9,11)[L]),len(labels)); rows=list(zip(labels,counts));j=r.randrange(len(labels))
    if i==4:
        a,b=counts[:2];kind=r.choice(['color','shape']);chosen=labels[0] if kind=='color' else 'circle'
        entries=([{'type':'circle','color':labels[0]}]*a+[{'type':'square','color':labels[1]}]*b)
        r.shuffle(entries)
        prompt=f'Sort by {kind}. How many belong in the {chosen} group?'
        diagram=dg('sortobjects',{'objects':entries,'caption':f'Sort by {kind}'},f'Unsorted collection: {a} {labels[0]} circles and {b} {labels[1]} squares.')
        return item(prompt,a,FN('sort_count',objects=entries,attribute='color' if kind=='color' else 'type',value=chosen),[f'Group objects with the same {kind}.',f'The {chosen} group has {a}.'],diagram)
    if i in [5,6]:
        votes=[label for label,n in rows for _ in range(n)];r.shuffle(votes)
        p='Votes: '+', '.join(votes)+f'. '+('How many tally marks should be recorded for ' if i==5 else 'How many objects or marks should represent ')+labels[j]+'?'
        return item(p,counts[j],FN('survey_count',votes=votes,label=labels[j]),[f'Count one mark for each {labels[j]} vote.',f'Record {counts[j]} marks.'])
    kind='tally' if i==7 else 'pictograph' if i==8 else r.choice(['tally','pictograph','bargraph'])
    diagram=dg(kind,{'rows':rows,'caption':'Class votes','key':1,'symbol':'dot'},'Class votes: '+', '.join(f'{x}: {n}' for x,n in rows)+'. Each picture stands for 1 vote.')
    if i==9:
        x,y=r.sample(range(len(rows)),2);a,b=counts[x],counts[y]
        return item(f'How many more votes does {labels[x] if a>b else labels[y]} have than {labels[y] if a>b else labels[x]}?',abs(a-b),FN('graph_diff',rows=rows,labels=[labels[x],labels[y]]),[f'Compare {a} and {b}.',f'{max(a,b)} − {min(a,b)} = {abs(a-b)}.'],diagram)
    return item(f'How many votes are in the {labels[j]} category?',counts[j],FN('tally_one' if i==7 else 'graph_one',rows=rows,label=labels[j]),[f'Count only the {labels[j]} row.',f'There are {counts[j]} votes.'],diagram)


def measure(r,L,i):
    a=r.randint(3,(7,12,20)[L]);b=r.randint(1,a-1);nm=r.choice(['ribbon','string','rope','yarn'])
    if i==1:
        vals=r.sample(range(3,18),2);a,b=vals;want=r.choice(['longer','shorter']);ans='A' if (a>b)==(want=='longer') else 'B'
        return item(f'The objects start at the same line. Which is {want}: A or B?',ans,FN('direct_length',a=a,b=b,want=want),[f'Compare the far ends from the shared start.',f'{ans} is {want}.'],dg('lengthbars',{'values':[a,b],'labels':['A','B'],'offset':L*17},f'Objects A and B share a start; their lengths are {a} and {b} units.'),[(x,'incorrect end comparison') for x in ['A','B','same length','cannot tell'] if x!=ans])
    if i==2:
        # Third object is an actual common comparator, not a list of measured numbers.
        longer=r.choice([True,False]);other='longer' if longer else 'shorter';ans='A' if longer else 'B'
        p=f'A is {other} than a {nm}. B is {"shorter" if longer else "longer"} than that same {nm}. Which is longer, A or B?'
        return item(p,ans,FN('indirect_length',a_vs_ref=1 if longer else -1,b_vs_ref=-1 if longer else 1),[f'Use the same {nm} as a bridge.',f'{ans} is longer than the {nm}; the other is shorter.'],wrong=[(x,'ignores the shared comparison') for x in ['A','B','same length','cannot tell'] if x!=ans])
    if i==3:
        vals=r.sample(range(2,(9,16,25)[L]),3 if L<2 else 4);labels=['A','B','C','D'][:len(vals)];pairs=list(zip(labels,vals));order=', '.join(x for x,_ in sorted(pairs,key=lambda x:x[1]))
        return item('Order the objects from shortest to longest.',order,FN('order_len',pairs=pairs),[f'Compare all {len(vals)} lengths.',f'Order: {order}.'],dg('lengthbars',{'values':vals,'labels':labels},', '.join(f'{x}: {n} units' for x,n in pairs)),[(', '.join(reversed(order.split(', '))),'reversed order'),(', '.join(labels),'did not compare'),(', '.join(labels[1:]+labels[:1]),'incorrect order')])
    if i==4:
        n=r.randint(3,12);gap=r.choice([True,False]);bad='gaps' if gap else 'overlaps';which=r.choice(['A','B']);ans=which
        return item(f'Which row measures the {nm} correctly with equal-size units, A or B?',ans,FN('unit_layout',correct=which,units=n,bad=bad),['Measuring units must touch end to end, without gaps or overlaps.',f'Row {which} follows this rule.'],dg('unitlayout',{'units':n,'correct':which,'bad':bad},f'Row {which} has equal units touching end to end. The other row has {bad}.'),[(x,'gaps or overlaps do not measure length') for x in ['A','B','both','neither'] if x!=ans])
    if i==5:
        n=r.randint((3,8,15)[L],(10,18,24)[L])
        return item('Count the equal-size units from end to end. How many units long is the object?',n,FN('ruler',n=n),[f'Count intervals, not boundary marks.',f'The length is {n} units.'],dg('unitlength',{'n':n},f'An object spans {n} equal units with no gaps.'))
    if i==6:return collection(r,L)
    if i==7:
        return calc(a,b,'−',f'A {nm} is {a} cubes long. A second {nm} is {b} cubes long. Using the same-size cubes, how much longer is the first?')
    if i==8:
        return calc(a,b,'−',f'A {nm} is {a} tiles long. Another is {b} tiles long. How many tiles shorter is the second?')
    if i==9:return story(r,L,'sub-start' if L==2 or r.choice([True,False]) else 'change')
    return story(r,L,'result',model=True,equation=True)


def collection(r,L):
    n=r.randint((12,40,90)[L],(39,89,120)[L]);t,o=divmod(n,10)
    return item('Count the collection. Each outlined group has 10 counters. Write the numeral.',n,FN('tens_ones',tens=t,ones=o),[f'Count {t} full groups of 10 and {o} loose counters.',f'{t*10} + {o} = {n}.'],dg('collection',{'tens':t,'ones':o},f'{t} groups of 10 counters and {o} loose counters.'))


def geometry(r,L,i):
    color=r.choice(['blue','orange','green','purple','teal']);nm=name(r)
    if i==1:
        shape=r.choice(['triangle','square','rectangle','hexagon']);s={'triangle':3,'square':4,'rectangle':4,'hexagon':6}[shape]
        ask='sides' if L==0 else r.choice(['sides','corners'])
        prompt=f'{nm} draws a {color} {shape}. How many {ask} must it have?'
        if L==2:prompt=f'{nm} turns a {color} {shape} on its side. How many {ask} does it still have?'
        return item(prompt,s,FN('shape_'+ask,kind=shape),[f'Turning or coloring a shape does not change its {ask}.',f'A {shape} has {s} {ask}.'],dg('shapes',{'shapes':[{'type':shape,'color':color}]},f'A {color} {shape}.') if L==0 else None)
    if i==2:
        kind=r.choice(['cube','sphere','cone','cylinder']);looks={'cube':'a block with 6 square faces','sphere':'a ball with no flat faces','cone':'a party hat with one circular base and a point','cylinder':'a can with two circular bases'}
        p=f'{nm} sees a solid like {looks[kind]}. What solid is it?'
        if L==0:p='Name the solid shape shown.'
        if L==2:p=f'{nm} compares a sphere, cube, cone, and cylinder. Which one matches this rule: {looks[kind]}?'
        return item(p,kind,FN('solid_name',kind=kind),[f'The defining features match a {kind}.'],dg('shapes',{'shapes':[{'type':kind,'color':color}]},f'One {color} {kind}.') if L==0 else None,[(s,'different solid attributes') for s in looks if s!=kind])
    if i==3:
        shape=r.choice(['square','hexagon']);n=2 if shape=='square' else 6
        if L==0:p=f'{nm} joins the triangle pieces with no gaps. Name the outside shape.';ans=shape;ck=FN('composition_shape',pieces=n)
        else:p=f'{nm} builds a {shape} using the triangle pieces shown. How many triangle pieces are needed?';ans=n;ck=FN('composition_count',shape=shape)
        return item(p,ans,ck,[f'{n} matching triangles tile a {shape}.'],dg('composition',{'shape':shape,'color':color},f'A {shape} tiled by {n} triangles.'),wrong=None if isinstance(ans,int) else [('triangle','names a piece'),('circle','curved outline'),('rectangle','not the named outside shape')])
    if i==4:
        rows=r.randint(1,(2,3,4)[L]);cols=r.randint(2,(3,4,5)[L]);layers=1 if L==0 else r.randint(1,2)
        n=rows*cols*layers
        p=f'{nm} builds a solid box. Each layer has {rows} rows of {cols} small cubes. There are {layers} '+('layer' if layers==1 else 'layers')+'. How many cubes are needed?'
        return item(p,n,FN('solid_composition',rows=rows,cols=cols,layers=layers),[f'Count {rows*cols} cubes in each layer.',f'{layers} '+('layer' if layers==1 else 'layers')+f' use {n} cubes.'],dg('cubeplan',{'rows':rows,'cols':cols,'layers':layers},f'A plan: {rows} rows of {cols} cube spaces per layer, {layers} layers.'))
    if i in [5,6,7,8]:
        shape='circle' if i==6 else 'rectangle' if i==5 else r.choice(['circle','rectangle']);parts=2 if L==0 else r.choice([2,4]);word='halves' if parts==2 else 'fourths';shaded=1
        diagram=dg('partition',{'shape':shape,'parts':parts,'shaded':shaded,'caption':f'{nm}: equal pieces'},f'A {shape} divided into {parts} equal pieces; one is shaded.')
        if i in [5,6]:
            # Students plan the partition, rather than merely name a finished picture.
            ask='halves' if parts==2 else 'fourths'
            p=f'{nm} wants {ask} of a {color} {shape}. How many equal pieces should the {shape} be divided into?'
            if L==2:p=f'{nm} cuts a {color} {shape} into halves, then cuts each half into 2 equal pieces. How many equal pieces are there now?';parts=4;diagram=None
            return item(p,parts,FN('partition_count',parts=parts),[f'{"Halves" if parts==2 else "Fourths"} require {parts} equal pieces.'],diagram if L==0 else None)
        if i==7:
            ans='no' if L<2 else 'equal size'
            if L<2:p=f'{nm} cuts a {color} {shape} into {parts} pieces of different sizes. Are these pieces {word}?';ck=FN('fair_parts',equal=False)
            else:p=f'{nm} says any {parts} pieces of a {color} {shape} are {word}. What must be true about their size?';ck=FN('fair_parts',equal=True)
            return item(p,ans,ck,[f'{word.capitalize()} must be equal in size, not just {parts} pieces.'],wrong=[(x,'parts must have the same size') for x in ['yes','no','equal size','any size'] if x!=ans])
        return item(f'{nm} divides a {color} {shape} into {parts} equal pieces. What are the pieces called?',word,FN('partition_word',parts=parts),[f'{parts} equal parts are called {word}.'],diagram if L==0 else None,[(x,'incorrect equal part name') for x in ['halves','fourths','thirds','wholes'] if x!=word])
    h=r.randint(1,12);m=0 if i==9 else 30 if i==10 else r.choice([0,30]);time=f'{h}:{m:02d}'
    if i==12:
        # Drawing target is represented as a hand-placement response, usable by shared games.
        minute=12 if m==0 else 6
        pos=str(h) if m==0 else f'between {h} and {h%12+1}'
        ans=f'short: {pos}; long: {minute}'
        p=f'{nm} draws clock hands for {time}. Where should the short hour hand and long minute hand go?'
        return item(p,ans,FN('clock_hands',h=h,m=m),[f'The minute hand points to {minute}.',f'The hour hand is {"at " if m==0 else ""}{pos}.'],dg('blankclock',{'caption':f'Draw {time}','color':color},f'A clock face without hands. Target time {time}.') if L==0 else None,[(f'short: {minute}; long: {h}','hands reversed'),(f'short: {h%12+1}; long: {minute}','hour advanced too soon'),(f'short: {pos}; long: {6 if m==0 else 12}','wrong minute hand')])
    p=(f'Write the digital time that matches {nm}\'s analog clock.' if i==11 else f'Read {nm}\'s clock. What time is shown?')
    if L==2:p+=' Tell how you used both hands.'
    return item(p,time,FN('clock',h=h,m=m),[f'The minute hand points to {12 if m==0 else 6}.',f'The hour hand is {"at "+str(h) if m==0 else "between "+str(h)+" and "+str(h%12+1)}.',f'The time is {time}.'],dg('clock',{'hour':h,'minute':m,'caption':nm+' — '+color},f'Analog clock: hour {h}, minute {m}.'),[(f'{h%12+1}:{m:02d}','hour too far ahead'),(f'{h}:{30 if m==0 else 0:02d}','wrong minute'),(f'{h%12+1}:{30 if m==0 else 0:02d}','both hands misread')])

# Explicit dispatch covers all 93 targets. A missing target is a build failure.
A1=['count12','frame10','facts10']
A3=['add10','sub10','related','compose10','teen','teen-ops','missing10','make-ten','cross10','three','start','teen-sub','related-sub','count-diff','sub-missing']
P4=['group','tens-count','complete-tens','model','draw','value','ten-ops','compare','symbol','order','equiv','regroup','represent']

def source(unit,i):
    def f(r,L):
        if unit==0:
            p=arithmetic(r,L,A1[i-1]) if i<=3 else data(r,L,i)
        elif unit==1:
            if i==1:p=story(r,L,'result',10)
            elif i==2:p=story(r,L,'change',10)
            elif i==3:p=story(r,L,'result',10,equation=True)
            elif i==4:p=arithmetic(r,L,'equal')
            elif i==5:p=arithmetic(r,L,'parts10')
            elif i==6:p=story(r,L,'result' if L==0 else 'part',10)
            elif i in [7,12]:p=arithmetic(r,L,'unknown10')
            elif i==8:p=story(r,L,'compare',10,model=True)
            elif i==9:p=story(r,L,'compare',10)
            elif i==10:p=arithmetic(r,L,'related-sub')
            elif i==11:p=story(r,L,r.choice(['result','change','part','compare']),10)
            elif i==13:
                t,a,b=numbers(r,L,10)
                ans=f'{a} + {b} = {t}; {t} − {b} = {a}'
                p=item(f'{name(r)} has {a} red blocks and {b} blue blocks. Write an addition equation for the total and a related subtraction equation.',ans,FN('story_equations',a=a,b=b),[f'Join the groups: {a} + {b} = {t}.',f'Check by taking away blue: {t} − {b} = {a}.'],wrong=[(f'{a} − {b} = {t}; {t} + {b} = {a}','operations reversed'),(f'{a} + {b} = {t+1}; {t} − {b} = {a}','wrong total'),(f'{a} + {b} = {t}; {t} − {b} = {b}','wrong check')])
            else:
                t,a,b=numbers(r,L,10);nm=name(r)
                ans=f'{nm} has {a} shells, gets {b} more, and now has {t} shells.'
                p=item(f'Write a joining story for {a} + {b} = {t}. Use {nm}, shells, a start, a change, and an ending.',ans,FN('constructed_story',a=a,b=b,person=nm),[f'Start with {a}; get {b} more; end with {t}.',ans],wrong=[(f'{nm} has {a} shells, gives away {b}, and now has {t} shells.','wrong change'),(f'{nm} has {a} shells, gets {b} more, and now has {t+1} shells.','wrong total'),(f'{nm} has {t} shells, gets {b} more, and now has {a} shells.','start and total reversed')])

        elif unit==2:
            task=A3[i-1]
            p=story(r,L,'start') if task=='start' else (story(r,L,'subtract') if r.choice([True,False]) else arithmetic(r,L,'unknown20')) if task=='sub-missing' else arithmetic(r,L,task)
        elif unit==3:p=place(r,L,P4[i-1])
        elif unit==4:p=addition100(r,L,i)
        elif unit==5:p=measure(r,L,i)
        elif unit==6:p=geometry(r,L,i)
        elif unit==7:
            if i<=3:p=arithmetic(r,L,['facts20','facts10','related'][i-1])
            elif i in [4,5,6]:p=story(r,L,{4:'change',5:'compare',6:'part'}[i])
            elif i==7:p=story(r,L,'result',model=True,equation=True)
            elif i in [8,9]:p=collection(r,L)
            else:p=place(r,L,'equiv' if i==10 else 'riddle')
        else:raise ValueError((unit,i))
        # Prompt variants refer to a real task, not generic filler facts.
        if L==0 and not p.diagram:p.prompt+=' You may use counters or a drawing.'
        p.prompt = r.choice(['', 'Find the answer. ', 'Work it out. ']) + p.prompt
        p.tags.add('reasoning')
        return p
    f.__name__=f'target_u{unit+1:02d}_s{i:02d}'
    f.levels=[0,1,2];f.mode='any';f.qtype='conceptual'
    return f
