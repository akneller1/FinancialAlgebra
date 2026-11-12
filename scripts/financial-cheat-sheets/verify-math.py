"""Independent Decimal checks of the authored cheat-sheet examples.
Amortization and deposit projections use period-by-period balances, not the
closed-form expressions printed on the sheets. No course math helpers used.
"""
from decimal import Decimal as D, ROUND_HALF_UP, getcontext
from pathlib import Path
getcontext().prec=45
SOURCE=(Path(__file__).resolve().parents[2]/'financial/content/cheat-sheets.mjs').read_text()
SOURCE=SOURCE.replace('{,}',',')
count=0

def check(label, result, expected, places=2):
    global count
    expected=D(str(expected)); result=D(str(result))
    quantum=D(10)**-places
    actual=result.quantize(quantum,rounding=ROUND_HALF_UP)
    assert actual==expected, f'{label}: {actual} != {expected}'
    # Expected values must occur in authored content (without requiring currency syntax).
    fragment=f'{expected:,.{places}f}' if places else f'{expected:,.0f}'
    assert fragment in SOURCE, f'{label}: {fragment} absent from authored source'
    count+=1

def payment(principal,annual,months):
    # Independent bisection on the month-by-month final balance.
    principal=D(str(principal)); i=D(str(annual))/12
    lo=D(0); hi=principal*(1+i)
    for _ in range(190):
        pay=(lo+hi)/2; balance=principal
        for _ in range(months): balance=balance*(1+i)-pay
        if balance>0:lo=pay
        else:hi=pay
    return (lo+hi)/2

def deposits(amount,annual,months):
    bal=D(0); i=D(str(annual))/12
    for _ in range(months):bal=bal*(1+i)+D(str(amount))
    return bal

def growth(principal,annual,years):
    bal=D(str(principal))
    for _ in range(years):bal*=1+D(str(annual))
    return bal

# Income: every numerical example and offer valuation.
check('salary per check',D(52000)/26,2000,0)
check('regular wage',40*20,800,0);check('OT wage',6*D('1.5')*20,180,0)
check('weekly wage',800+180,980,0)
check('annual wage',21*40*50,42000,0)
check('commission gross',2000+D('.04')*30000,3200,0)
check('deductions',150+153+90+60+100,553,0)
check('net pay',2000-553,1447,0)
check('payroll model',2000*D('.0765'),153,0)
check('YTD periods',18000//2000,9,0)
check('taxable income',54000-15000,39000,0)
check('tax slice1',12000*D('.10'),1200,0)
check('tax slice2',27000*D('.12'),3240,0)
check('total tax',1200+3240,4440,0)
check('effective gross',D(4440)/54000*100,'8.22')
check('effective taxable',D(4440)/39000*100,'11.38')
check('A match',52000*D('.05'),2600,0)
check('A premium',80*12,960,0);check('B premium',350*12,4200,0)
check('job A',52000+2600-960,53640,0);check('job B',56000-4200,51800,0)
check('offer difference',53640-51800,1840,0)
# Budgeting.
check('annual net',1300*26,33800,0);check('monthly net',D(33800)/12,'2816.67')
check('50% needs',3000*D('.5'),1500,0);check('30% wants',3000*D('.3'),900,0);check('20% saving',3000*D('.2'),600,0)
check('initial cash flow',D('2816.67')-2640,'176.67');check('sinking fund',780//6,130,0)
check('true cash flow',D('176.67')-130,'46.67')
check('gym B',8*5,40,0);check('gym break-even',D(30)/8,'3.75');check('gym difference',40-30,10,0)
check('unit price small',D('3.60')/12,'.30');check('unit price large',D(5)/20,'.25')
check('habit weekly',6*4,24,0);check('habit annual',6*4*52,1248,0);check('habit monthly',D(1248)/12,104,0)
# Banking.
check('simple years',D(18)/12,'1.5',1);check('simple interest',2000*D('.04')*D('1.5'),120,0)
check('simple balance',2000+120,2120,0)
check('monthly compounding',1000*(1+D('.04')/12)**12,'1040.74')
check('APY percent',((1+D('.04')/12)**12-1)*100,'4.0742',4)
check('CD nine months',2000*D('.04')*D(9)/12,60,0);check('CD penalty',2000*D('.04')*D(3)/12,20,0)
check('CD returned',2000+60-20,2040,0)
check('account A',1000*D('.04')-5*12,-20,0);check('account B',1000*D('.03'),30,0)
check('account difference',30-(-20),50,0);check('fee threshold',D(60)/D('.01'),6000,0)
check('bank adjusted',1250-80+200,1370,0);check('record adjusted',1385-15,1370,0)
# Credit.
check('monthly card rate',D('.2499')/12,'.020825',6)
check('interest card',3000*D('.2499')/12,'62.48')
check('daily balance',(D(1000)*10+600*20)/30,'733.33')
check('minimum',D('62.48')+30,'92.48');check('next balance',D(3000)+D('62.48')-D('92.48'),2970,0)
check('26-month payment',payment(3000,'.2499',26),'150.60')
check('utilization',D(900)/3000*100,30,0);check('new utilization',D(300)/3000*100,10,0)
check('extra A interest',100*D('.24')/12,2,0);check('extra B interest',100*D('.12')/12,1,0)
check('keep card interest',sum(range(200,2001,200))*D('.02'),220,0)
check('transfer fee',2000*D('.03'),60,0);check('transfer advantage',220-60,160,0)
# Borrowing; monthly simulation validates payments independently.
a=payment(22000,'.069',48);b=payment(22000,'.069',84)
check('48 month payment',a,'525.80');check('84 month payment',b,'330.96')
check('48 total',a*48,'25238.27');check('84 total',b*84,'27801.02')
check('48 interest',a*48-22000,'3238.27');check('84 interest',b*84-22000,'5801.02')
check('term advantage',b*84-a*48,'2562.75')
check('first interest',22000*D('.069')/12,'126.50')
check('first principal',D('525.80')-D('126.50'),'399.30')
check('new loan balance',22000-D('399.30'),'21600.70')
# Present value by discounting each $300 payment.
check('max loan',sum(D(300)/(D('1.005')**m) for m in range(1,61)),'15517.67')
check('lease depreciation',D(12000)/36,'333.33');check('lease finance',48000*D('.002'),96,0)
check('lease total',D(12000)/36+96,'429.33')
# Investing.
check('lump sum',growth(1000,'.06',10),'1790.85')
v=deposits(200,'.07',420);check('deposit future value',v,'360210.92')
check('deposits paid',200*420,84000,0);check('investment growth',v-84000,'276210.92')
check('deposit for goal',D(10000)/deposits(1,'.06',60),'143.33')
a=growth(10000,'.068',20);b=growth(10000,'.06',20)
check('fee A',a,'37275.64');check('fee B',b,'32071.35');check('fee difference',a-b,'5204.28')
check('expense ratio',10000*D('.002'),20,0)
check('real investment return',(D('1.07')/D('1.03')-1)*100,'3.88')
check('loss balance',1000*D('.8'),800,0);check('20 percent rebound',800*D('1.2'),960,0)
check('required recovery',D(200)/800*100,25,0);check('rule72',72//6,12,0)
check('doubling factor',D('1.06')**12,'2.012',3)
# Housing.
p=payment(280000,'.0675',360);check('mortgage',p,'1816.07')
check('down payment',350000*D('.2'),70000,0);check('mortgage principal',350000-70000,280000,0)
check('property tax monthly',350000*D('.012')/12,350,0);check('insurance monthly',1500//12,125,0)
check('maintenance monthly',350000*D('.01')/12,'291.67')
check('owner cash flow',D('1816.07')+350+125+D('291.67'),'2582.74')
check('housing DTI',D(2400)/8000*100,30,0)
check('rent cost',1800*12,21600,0);check('buy cost',2500*12-4000+6000,32000,0)
check('rent advantage',32000-21600,10400,0)
check('equity',360000-270000,90000,0);check('sell cost',360000*D('.06'),21600,0)
check('net sale',90000-21600,68400,0)
check('alternative value',growth(70000,'.04',3),'78740.48')
check('opportunity cost',growth(70000,'.04',3)-70000,'8740.48')
# Insurance.
check('claim payout',min(max(8000-1000,0),10000),7000,0)
def health(bill,deduct,coins,cap):return min(D(cap),min(D(bill),D(deduct))+D(coins)*max(D(bill)-D(deduct),0))
check('covered health share',health(9000,2000,'.2',6000),3400,0)
check('annual health premium',210*12,2520,0);check('annual health cost',2520+3400,5920,0)
check('A no claims',150*12,1800,0);check('B no claims',250*12,3000,0)
check('A at 9000',1800+health(9000,3000,'.2',6000),6000,0)
check('B at 9000',3000+health(9000,1000,'.2',4000),5600,0)
check('B savings',6000-5600,400,0);check('A worst',1800+6000,7800,0);check('B worst',3000+4000,7000,0)
check('expected loss',D('.02')*10000,200,0);check('deductible extra',1500-500,1000,0)
check('deductible recovery years',1000//200,5,0)
# College.
check('net college price',30500-13000,17500,0);check('funding gap',17500-8000-4000,5500,0)
p=payment(22000,'.065',120);check('student loan payment',p,'249.81')
check('annual student loan',p*12,'2997.67');check('loan salary share',p*12/55000*100,'5.45')
check('certificate payback',12000//6000,2,0);check('degree payback',40000//10000,4,0)
check('certificate 10y gain',6000*10-12000,48000,0);check('degree 10y gain',10000*10-40000,60000,0)
check('college economic cost',2*20000+15000,55000,0)
check('year2 pay',40000*D('1.03'),41200,0);check('year3 pay',40000*D('1.03')**2,42436,0)
check('3y total',sum(D(40000)*D('1.03')**t for t in range(3)),123636,0)
# Retirement.
check('future price',growth(100,'.03',10),'134.39')
check('price multiplier',D('1.03')**10,'1.343916',6)
check('purchasing power',D(50000)/D('1.025')**20,'30513.55')
check('CPI change',D(210-200)/200*100,5,0)
check('real retirement return',(D('1.06')/D('1.025')-1)*100,'3.41')
check('employee saving',50000*D('.06'),3000,0);check('employer match',3000*D('.5'),1500,0)
check('monthly combined',4500//12,375,0)
v=deposits(375,'.06',504);check('retirement future balance',v,'851310.08')
check('retirement real balance',v/D('1.025')**42,'301776.51')
check('retirement contributions',375*504,189000,0)
check('traditional low tax',1000*2*D('.9'),1800,0);check('Roth',1000*D('.8')*2,1600,0)
check('traditional high tax',1000*2*D('.7'),1400,0);check('tax comparison difference',1800-1600,200,0)
check('spending gap',40000-16000,24000,0);check('target',D(24000)/D('.04'),600000,0)
print(f'{count} independent numerical checks passed; expected figures found in authored source.')
