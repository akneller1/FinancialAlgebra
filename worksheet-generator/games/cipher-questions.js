/* Unit-aligned numerical cipher problems.
   Construct the answer first, then substitute it into a unit-specific problem.
   Every generated answer is a positive whole number from 1 to 25 for a Caesar shift.
   No generic equation fallback for unrelated units. */
(function(G){
'use strict';
const familyByUnit={
 algebra:{
  'foundations-algebra':'integers','expressions-equations':'equations',
  'inequalities':'inequalities','relations-functions':'functions',
  'linear-equations-slope':'slope','systems-of-equations':'systems',
  'exponents-exponential-functions':'exponents','exponential-functions':'exponents',
  'polynomials-factoring':'polynomials','factoring-zero-product':'polynomials',
  'quadratics':'quadratics','statistics-data-modeling':'statistics'
 },
 geometry:{
  'foundations-geometry':'angles','angles-parallel-lines':'parallel',
  'triangle-congruence':'congruence','triangle-relationships':'triangle',
  'similarity':'similarity','right-triangles-trigonometry':'right-triangle',
  'quadrilaterals-polygons':'quadrilateral','transformations':'transformations',
  'circles':'circles','area-surface-area-volume':'area-volume'
 },
 algebra2:{
  'functions-transformations':'functions','linear-functions-systems':'systems',
  'quadratic-functions-complex-numbers':'quadratics',
  'polynomial-functions':'polynomials',
  'radicals-rational-exponents':'radicals',
  'exponential-logarithmic-functions':'logarithms',
  'rational-functions':'rational','sequences-series':'sequences',
  'conic-sections':'conics','trigonometric-functions':'trigonometry',
  'probability-statistics':'probability'
 },
 prealgebra:{
  'real-numbers-exponents':'exponents','equations-expressions':'equations',
  'linear-functional-relationships':'functions','systems-linear-equations':'systems',
  'patterns-bivariate-data':'statistics','congruence-similarity':'similarity',
  'geometry-applications':'area-volume'
 },
 prealgebra7:{
  'algebraic-expressions-integers':'integers','one-step-equations-inequalities':'equations',
  'decimals-equations':'decimals','factors-fractions-exponents':'fractions',
  'operations-fractions':'fractions','ratios-proportions-percentages':'ratios',
  'solving-equations-inequalities':'inequalities','linear-functions-graphing':'slope',
  'spatial-thinking':'area-volume','area-volume':'area-volume',
  'right-triangles-algebra':'right-triangle','data-analysis-probability':'statistics',
  'nonlinear-functions-polynomials':'polynomials'
 },
 math5:{
  'place-value-number-sense':'g5-place-value','multi-digit-multiplication-division':'g5-multiply-divide',
  'decimal-operations':'g5-decimals','numerical-expressions-patterns':'g5-expressions',
  'fraction-addition-subtraction':'g5-fraction-add','fraction-multiplication-division':'g5-fraction-multiply',
  'measurement-conversions':'g5-measurement','volume-three-dimensional-figures':'g5-volume',
  'coordinate-plane-graphing':'g5-coordinates','classifying-two-dimensional-figures':'g5-shapes',
  'data-line-plots-problem-solving':'g5-line-plot'
 },
 math6:{
  'ratios-rates-percent-proportions':'ratios','fractions-decimals-operations':'decimals',
  'rational-numbers':'integers','expressions-equations':'equations',
  'inequalities':'inequalities','geometry':'area-volume','data-displays':'statistics'
 },
 precalculus:{
  'equations-inequalities':'inequalities','functions':'functions','conics':'conics',
  'trigonometric-functions':'trigonometry',
  'general-triangle-trigonometry':'trigonometry','matrices':'matrices',
  'vectors':'vectors','probability':'probability'
 },
 calculus:{
  'precalculus-review':'functions','limits-continuity':'limits',
  'derivatives':'derivatives','applications-derivatives':'derivatives',
  'antiderivatives-definite-integrals':'integrals','fundamental-theorem-calculus':'integrals',
  'applications-integrals':'integrals','differential-equations':'differential',
  'ap-review':'derivatives'
 }
};
const int=(a,b)=>a+Math.floor(Math.random()*(b-a+1));
const result=(family,level,x,prompt,steps)=>({
 id:'cipher-'+family+'-'+level+'-'+Math.random().toString(36).slice(2),
 skillId:'cipher-'+family, prompt,answer:String(x),
 format:'short-answer',solutionSteps:steps||[],cipherFamily:family
});
function create({courseId,unitId,level='cp1'}){
 const family=familyByUnit[courseId]&&familyByUnit[courseId][unitId];
 if(!family)return null; // Never silently substitute an unrelated skill.
 const hard=level==='honors',easy=level==='cp2';
 const x=int(2,hard?18:easy?12:20),a=int(2,hard?6:4),b=int(2,9),c=int(2,7);
 let p,steps;
 switch(family){
 case 'systems': {
   const y=int(1,8);
   if(easy){
     p='Solve the system: x + y = '+(x+y)+' and x − y = '+(x-y)+'. What is x?';
     steps=['Add the two equations to eliminate y.','Divide by 2 to find x.'];
   }else if(hard){
     const k=int(2,5),m=int(2,5),n=int(2,4);
     p='Solve the system: '+k+'x + '+m+'y = '+(k*x+m*y)+
       ' and '+n+'x − '+m+'y = '+(n*x-m*y)+'. What is x?';
     steps=['Add the equations to eliminate y.','Divide by '+(k+n)+' to find x.'];
   }else{
     p='Solve the system: 2x + '+a+'y = '+(2*x+a*y)+
       ' and 3x − '+a+'y = '+(3*x-a*y)+'. What is x?';
     steps=['Add the equations to eliminate y.','Divide by 5 to find x.'];
   }
   break;
 }
 case 'slope':{
   const m=easy?1:hard?3:2,run=hard?3:2,y0=int(-4,3);
   const y1=y0+m*x;
   // Slope comes from two coordinates; not from a generic linear equation.
   p='A line passes through (0, '+y0+') and ('+run+', '+(y0+run*x)+
     '). What is its slope?';
   steps=['Slope = (change in y) ÷ (change in x).'];
   break;
 }
 case 'integers':{
   const neg=int(3,12),increase=x+neg;
   p='The temperature is −'+neg+'°C. It rises '+increase+
     '°C. What is the new temperature?';
   steps=['Add the temperature change to the starting temperature.'];break;
 }
 case 'equations':{
   if(hard){p='Solve for x: '+a+'(x + '+b+') − '+c+' = '+(a*(x+b)-c)+'.';
     steps=['Distribute, then isolate x.'];}
   else if(easy){p='Solve for x: '+a+'x = '+(a*x)+'.';steps=['Divide both sides by '+a+'.'];}
   else{p='Solve for x: '+a+'x − '+b+' = '+(a*x-b)+'.';steps=['Add '+b+', then divide by '+a+'.'];}
   break;
 }
 case 'inequalities':{
   const s=hard?a:1;
   // Compute the least integer solution to a strict inequality.
   p='Find the smallest integer n satisfying '+s+'n > '+(s*(x-1))+'.';
   steps=['Divide by the positive coefficient.','Because the inequality is strict, use the next integer.'];break;
 }
 case 'functions':{
   const input=int(1,4),k=int(2,5);
   const output=k*input+x;
   p='A function is f(t) = '+k+'t + b. If f('+input+') = '+output+', find b.';
   steps=['Substitute the input and output into the function.','Subtract '+(k*input)+' to isolate b.'];break;
 }
 case 'exponents':{
   const base=int(2,4),z=int(1,4);
   p='Simplify '+base+'^'+(x+z)+' ÷ '+base+'^'+z+
     '. What exponent remains on the base?';
   steps=['When dividing powers of the same base, subtract the exponents.'];break;
 }
 case 'polynomials':{
   const q=int(1,5),co=int(2,5);
   p='Factor '+co+'x² + '+(co*(x+q))+'x + '+(co*x*q)+
     ' completely. In the factorization '+co+'(x + '+q+')(x + k), find k.';
   steps=['Factor out '+co+', then find the pair of binomial factors.'];break;
 }
 case 'quadratics':{
   const h=int(1,5),v=int(1,9);
   p='A parabola is y = (t − '+x+')² + '+v+
     '. Find the t-coordinate of its vertex.';
   if(hard){
     const k=int(1,4);
     p='A parabola has equation y = '+k+'(t − '+x+')² + '+v+
       '. Find the axis of symmetry t = ?';
   }
   steps=['A quadratic in vertex form has its vertex at (h, k).'];break;
 }
 case 'statistics':{
   // Symmetrically spaced observations have mean equal to the middle value.
   p='The data set contains '+(x-b)+', '+x+', and '+(x+b)+
     '. Find the mean.';
   steps=['Add all three values and divide by 3.'];break;
 }
 case 'angles':{
   p='Two complementary angles measure '+(90-x)+'° and n°. Find n.';
   steps=['Complementary angles sum to 90°.'];break;
 }
 case 'parallel':{
   const angle=int(35,60);
   // Same-side interior angles are supplementary.
   p='Two parallel lines are cut by a transversal. An angle measures '+(180-x)+
     '°. Its same-side interior angle measures n°. Find n.';
   steps=['Same-side interior angles are supplementary.'];break;
 }
 case 'congruence':{
   p='Two congruent triangles have corresponding sides of lengths '+(x+b)+
     ' and n + '+b+'. Find n.';
   steps=['Corresponding sides of congruent triangles are equal.'];break;
 }
 case 'triangle':{
   const ang1=int(35,60),ang2=180-ang1-x;
   // x <= 20 ensures third angle valid.
   p='A triangle has interior angles '+ang1+'° and '+ang2+
     '°. What is the third angle in degrees?';
   steps=['The angles in a triangle sum to 180°.'];break;
 }
 case 'similarity':{
   const scale=easy?2:hard?4:3;
   p='Two similar triangles have corresponding side lengths '+b+' and '+(b*scale)+
     '. A second pair has side lengths n and '+(x*scale)+
     '. Find the missing side length n in the smaller triangle.';
   steps=['Set up a proportion using corresponding sides.'];break;
 }
 case 'right-triangle':{
   const leg=3*x,hyp=5*x,other=4*x;
   // The unknown leg must first be obtained from a right-triangle relationship.
   p='A right triangle has one leg '+(3*x)+' and hypotenuse '+(5*x)+
     '. The other leg is 4n. Use the Pythagorean theorem to find n.';
   steps=['Use a² + b² = c².','The missing leg is '+(4*x)+'. Divide by 4.'];break;
 }
 case 'quadrilateral':{
   const width=int(3,9);
   p='A rectangle has width '+width+' and perimeter '+(2*(x+width))+
     '. Find its length.';
   steps=['Perimeter = 2(length + width).'];break;
 }
 case 'transformations':{
   const start=int(-7,5),end=start+x;
   p='A point has x-coordinate '+start+'. After a horizontal translation, its x-coordinate is '+
     end+'. How many units to the right did it move?';
   steps=['Subtract the original x-coordinate from the new one.'];break;
 }
 case 'circles':{
   const r=x;
   p='A circle has circumference '+(2*r)+'π units. Use C = 2πr to find its radius.';
   steps=['Divide the circumference by 2π.'];break;
 }
 case 'area-volume':{
   const width=int(3,8);
   if(hard){p='A rectangular prism has width '+width+', height '+a+
     ', and volume '+(width*a*x)+'. Find its length.';
     steps=['Use V = length × width × height.'];}
   else{p='A rectangle has width '+width+' and area '+(width*x)+
     ' square units. Find its length.';
     steps=['Area = length × width.'];}break;
 }
 case 'radicals':{
   const n=x*x;
   p='Find the positive square root of '+n+'.';
   steps=['Find the positive number whose square equals '+n+'.'];break;
 }
 case 'logarithms':{
   const base=int(2,3),k=hard?2:1;
   // The exponent is unknown; students evaluate the actual logarithm.
   p='Evaluate log base '+base+' of '+(base**x)+'.';
    steps=['Logarithms undo exponentiation.'];break;
 }
 case 'rational':{
   p='Solve the rational equation '+(a*x)+'/n = '+a+
     ' for the positive integer n.';
   steps=['Multiply both sides by n, then divide by '+a+'.'];break;
 }
 case 'sequences':{
   const d=int(2,6),first=x-3*d;
   p='An arithmetic sequence has terms '+first+', '+(first+d)+', '+(first+2*d)+
     ', ____. Find the fourth term.';
   steps=['The common difference is '+d+'.'];break;
 }
 case 'conics':{
    p='A circle has equation (u − '+x+')² + (v + '+b+')² = '+(c*c)+
     '. Find the u-coordinate of its center.';
   steps=['The center of (u − h)² + (v − k)² = r² is (h, k).'];break;
 }
 case 'trigonometry':{
    p='In a right triangle, sin θ = 3/5 and the hypotenuse is '+(5*x)+
     '. The opposite side is 3n. Find n.';
   steps=['Use opposite / hypotenuse = 3/5.','Solve for the opposite side, then divide by 3.'];break;
 }
 case 'probability':{
   const total=hard?5*x:2*x;
    p='A bag has '+total+' tickets. The probability of drawing a marked ticket is '+
     (hard?'1/5':'1/2')+'. How many marked tickets are in the bag?';
   steps=['Multiply the total number of tickets by the probability.'];break;
 }
 case 'decimals':{
   const tenths=level==='cp2'?10:100,amt=x*tenths;
   p='A quantity is '+amt+' tenths'.replace('tenths',tenths===100?'hundredths':'tenths')+
     '. Express its value as a whole number.';
   steps=['Divide by '+tenths+'.'];break;
 }
 case 'fractions':{
   const k=int(2,5),den=int(2,7);
   p='Solve the equivalent-fraction equation n/'+den+' = '+(x*k)+'/'+(den*k)+'.';
   steps=['Simplify the right-hand fraction, or cross-multiply.'];break;
 }
 case 'ratios':{
   const ratio=int(2,5);
   p='The ratio of blue marbles to red marbles is 1:'+ratio+
     '. If there are '+(x*ratio)+' red marbles, how many blue marbles are there?';
   steps=['Use a proportion for equivalent ratios.'];break;
 }
 case 'matrices':{
   p='Matrix A = [[n, '+b+'], ['+a+', '+c+
     ']]. Its trace (sum of diagonal entries) is '+(x+c)+
     '. Find n.';
   steps=['The trace of a square matrix is the sum of its main diagonal entries.'];break;
 }
 case 'vectors':{
   const initial=int(-6,5);
   p='The vector ⟨'+x+', '+a+'⟩ has horizontal component n and vertical component '+
     a+'. Find n.';
   // Avoid literal answer in problem:
   p='Two vectors are ⟨'+initial+', '+a+'⟩ and ⟨'+(x-initial)+
     ', −'+a+'⟩. Find the horizontal component of their sum.';
   steps=['Add horizontal components and vertical components separately.'];break;
 }
 case 'limits':{
   p='Evaluate the limit as t approaches '+x+': (3t² − '+(3*x*x)+')/(t − '+x+
     '), then divide the result by 6.';
   // The removable discontinuity resolves to 6x, yielding the desired shift.
   steps=['Factor the difference of squares.','Cancel t − '+x+' before substituting.'];break;
 }
 case 'derivatives':{
   const factor=int(2,5);
   p='For f(t) = '+factor+'t² + '+b+'t, find t if f’(t) = '+(2*factor*x+b)+'.';
   steps=['Differentiate: f’(t) = '+(2*factor)+'t + '+b+'.','Isolate t.'];break;
 }
 case 'integrals':{
   const width=int(2,6);
   p='Find n if the definite integral from 0 to '+width+
     ' of the constant function n equals '+(width*x)+'.';
   steps=['The integral of a constant n over an interval of width '+width+' equals n times width.'];break;
 }
 case 'differential':{
   p='A function solves y’(t) = '+a+' with initial condition y(0) = '+b+
     '. If y(k) = '+(a*x+b)+', find k.';
   steps=['Integrate y’ to get y(t) = '+a+'t + '+b+'.'];break;
 }
 /* Grade 5: whole-number answers, no negatives, grade-level wording. */
 case 'g5-place-value':{
   const pw=easy?10:hard?1000:100,z=String(pw).length-1;
   p='What number times '+pw+' equals '+(x*pw)+'?';
   steps=['Multiplying by '+pw+' moves each digit '+z+' place'+(z>1?'s':'')+' to the left.','So divide '+(x*pw)+' by '+pw+'.'];break;
 }
 case 'g5-multiply-divide':{
   const d=easy?int(2,9):int(11,hard?48:25);
   p='Divide: '+(x*d)+' ÷ '+d+' = ?';
   steps=['Think: what number times '+d+' equals '+(x*d)+'?'];break;
 }
 case 'g5-decimals':{
   if(easy){const h=int(1,x-1);p='Add the decimals: '+(h/2).toFixed(1)+' + '+((2*x-h)/2).toFixed(1)+' = ?';steps=['Line up the decimal points and add.'];}
   else if(hard){p='Divide: '+String(x*0.25)+' ÷ 0.25 = ?';steps=['Dividing by 0.25 is the same as multiplying by 4.'];}
   else{p='Multiply: '+(x/10).toFixed(1)+' × 10 = ?';steps=['Multiplying by 10 moves each digit one place to the left.'];}
   break;
 }
 case 'g5-expressions':{
   const k=int(2,5),m2=int(1,Math.max(1,x-1));
   if(easy){p='Evaluate: ('+(x*k)+' ÷ '+k+') = ?';}
   else if(hard){p='Evaluate: ['+(x-m2)+' + '+m2+'] × '+k+' ÷ {'+(k+2)+' − 2} = ?';}
   else{p='Evaluate: '+k+' × ('+(x-m2)+' + '+m2+') ÷ '+k+' = ?';}
   steps=['Work inside parentheses, brackets or braces first.','Then multiply or divide from left to right.'];break;
 }
 case 'g5-fraction-add':{
   const den=easy?int(3,8):int(4,9),a1=int(1,den-1);
   const whole=x;
   p='Add: '+(whole-1)+' '+a1+'/'+den+' + '+(den-a1)+'/'+den+' = ? (Write the whole number.)';
   steps=['Add the fraction parts. They make a whole number of wholes.','Write the total as a whole number.'];break;
 }
 case 'g5-fraction-multiply':{
   const divs=[2,3,4,5].filter(d=>x%d===0&&x/d>=1);
   if(hard&&divs.length){const den=divs[int(0,divs.length-1)],m=x/den;
     p='How many 1/'+den+' pieces are in '+m+' whole'+(m>1?'s':'')+'? ('+m+' ÷ 1/'+den+')';
     steps=['Each whole has '+den+' pieces that are 1/'+den+' in size.','Multiply '+m+' × '+den+'.'];}
   else{const den=int(2,easy?5:8);p='What is 1/'+den+' of '+(x*den)+'?';steps=['Divide '+(x*den)+' into '+den+' equal groups.'];}
   break;
 }
 case 'g5-measurement':{
   if(hard){p='How many gallons equal '+(x*4)+' quarts?';steps=['There are 4 quarts in 1 gallon.','Divide by 4.'];}
   else if(easy){p='How many feet equal '+(x*12)+' inches?';steps=['There are 12 inches in 1 foot.','Divide by 12.'];}
   else{p='How many yards equal '+(x*3)+' feet?';steps=['There are 3 feet in 1 yard.','Divide by 3.'];}
   break;
 }
 case 'g5-volume':{
   const w=int(2,easy?3:5),h=int(2,easy?3:4);
   p='A rectangular prism is '+w+' units wide and '+h+' units tall. Its volume is '+(x*w*h)+' cubic units. How long is it?';
   steps=['Volume = length × width × height.','Divide '+(x*w*h)+' by '+(w*h)+'.'];break;
 }
 case 'g5-coordinates':{
   const sx=int(0,5),sy=int(0,6);
   p=easy?'Point A is at ('+x+', '+sy+'). What is its x‑coordinate?':'Start at ('+sx+', '+sy+'). Move right until you reach ('+(sx+x)+', '+sy+'). How many units did you move?';
   steps=[easy?'The first number in an ordered pair is the x‑coordinate.':'Subtract the x‑coordinates: '+(sx+x)+' − '+sx+'.'];break;
 }
 case 'g5-shapes':{
   const w=int(2,9);
   p=easy?'A square has a perimeter of '+(4*x)+' units. How long is each side?':'A rectangle is '+w+' units wide and has a perimeter of '+(2*(x+w))+' units. How long is it?';
   steps=[easy?'A square has 4 equal sides, so divide by 4.':'Perimeter = 2 × (length + width).'];break;
 }
 case 'g5-line-plot':{
   const d=easy?int(1,3):int(2,5);
   p='A line plot shows these values: '+(x-d)+', '+x+', '+(x+d)+'. If the total is shared equally, how much does each get?';
   steps=['Add the three values.','Divide the total by 3.'];break;
 }
 default: return null;
 }
 return result(family,level,x,p,steps);
}
G.MK_CIPHER_QUESTIONS={create,familyByUnit};
})(window);
