math4:{
  'place-value-number-sense':'g4-place-value','multi-digit-addition-subtraction':'g4-add-subtract',
  'multiplication-strategies':'g4-multiply','division-remainders':'g4-divide',
  'factors-multiples-patterns':'g4-factors','fractions-equivalent-fractions':'g4-equivalent',
  'fraction-operations-decimals':'g4-fraction-ops','measurement-unit-conversions':'g4-measurement',
  'geometry-angles-symmetry':'g4-angles','data-line-plots-word-problems':'g4-word-problems'
 },
/*---SPLIT---*/
 /* Grade 4: whole-number answers from 1 to 25, no negatives, grade-level wording. */
 case 'g4-place-value':{
   const pw=easy?10:hard?1000:100;
   p='How many '+(pw===10?'tens':pw===100?'hundreds':'thousands')+' are in '+(x*pw).toLocaleString('en-US')+'?';
   steps=['1 '+(pw===10?'ten':pw===100?'hundred':'thousand')+' = '+pw.toLocaleString('en-US')+'.','Divide '+(x*pw).toLocaleString('en-US')+' by '+pw.toLocaleString('en-US')+'.'];break;
 }
 case 'g4-add-subtract':{
   const a=easy?int(120,480):int(1200,hard?8600:4800);
   p='Find the missing number: '+a.toLocaleString('en-US')+' + ? = '+(a+x).toLocaleString('en-US');
   steps=['Subtract the known addend from the sum.',(a+x).toLocaleString('en-US')+' − '+a.toLocaleString('en-US')+' gives the missing number.'];break;
 }
 case 'g4-multiply':{
   const d=easy?int(2,9):hard?int(12,48):int(6,12);
   p='Find the missing factor: '+d+' × ? = '+(x*d).toLocaleString('en-US');
   steps=['Divide the product by the known factor.','Think: '+d+' times what number equals '+(x*d).toLocaleString('en-US')+'?'];break;
 }
 case 'g4-divide':{
   const d=easy?int(2,5):int(6,9),r=hard?int(1,d-1):0;
   p=r?(x*d+r)+' stickers are shared equally among '+d+' friends. Each friend gets as many as possible. How many stickers does each friend get?':'Divide: '+(x*d)+' ÷ '+d+' = ?';
   steps=r?['Divide '+(x*d+r)+' by '+d+'.','The remainder is left over, so the quotient is the answer.']:['Think: what number times '+d+' equals '+(x*d)+'?'];break;
 }
 case 'g4-factors':{
   const k=easy?int(2,5):int(3,9);
   p=easy?'What is the missing number in this factor pair of '+(x*k)+'? '+k+' and ?':'A pattern starts at '+k+' and follows the rule “add '+k+'.” Which term of the pattern is '+(x*k)+'? (The first term is '+k+'.)';
   steps=easy?['The two numbers in a factor pair multiply to '+(x*k)+'.','Divide '+(x*k)+' by '+k+'.']:['The terms are the multiples of '+k+'.',(x*k)+' ÷ '+k+' tells which multiple it is.'];break;
 }
 case 'g4-equivalent':{
   const k=easy?2:hard?int(4,6):3,d=x+int(1,5);
   p='Write '+(x*k)+'/'+(d*k)+' as an equivalent fraction with a denominator of '+d+'. What is the numerator?';
   steps=['The denominator was multiplied by '+k+' (or divided by '+k+' going back).','Divide '+(x*k)+' by '+k+'.'];break;
 }
 case 'g4-fraction-ops':{
   const d=easy?int(2,4):int(3,6);
   p=easy?'How many copies of 1/'+d+' make '+x+'/'+d+'?':'A whole number times 1/'+d+' equals '+x+'/'+d+'. What is the whole number?';
   steps=[x+'/'+d+' is '+x+' copies of 1/'+d+'.'];break;
 }
 case 'g4-measurement':{
   const w=int(2,9);
   p=easy?'A rectangle has an area of '+(x*w)+' square units and a width of '+w+' units. How many units long is it?':hard?'A rectangle has a perimeter of '+(2*(x+w))+' units and a width of '+w+' units. How many units long is it?':(x*12)+' inches = ? feet';
   steps=[easy?'Area = length × width, so divide the area by the width.':hard?'Subtract the two widths from the perimeter, then divide by 2.':'There are 12 inches in 1 foot, so divide by 12.'];break;
 }
 case 'g4-angles':{
   const a=easy?90:180,k=a-x;
   p=(easy?'A right angle (90°)':'A straight angle (180°)')+' is split into two angles. One angle measures '+k+'°. How many degrees is the other angle?';
   steps=['The two angles add up to '+a+'°.','Subtract: '+a+' − '+k+'.'];break;
 }
 case 'g4-word-problems':{
   const g=easy?int(2,5):int(3,8),c=int(2,9);
   p='A coach has '+(x*g+c)+' cones. The coach keeps '+c+' cones and shares the rest equally among '+g+' teams. How many cones does each team get?';
   steps=['Subtract the cones the coach keeps: '+(x*g+c)+' − '+c+' = '+(x*g)+'.','Divide '+(x*g)+' by '+g+'.'];break;
 }
