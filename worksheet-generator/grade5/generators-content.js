/* Grade 5 teacher-generator content: big ideas, student-friendly objectives, vocabulary,
   common misconceptions, differentiation and activity themes for all eleven math5 units.
   Curriculum facts (unit ids, skill ids, standards and questions) stay in the approved
   course catalog and question banks; this file only supplies teaching language. */
(function (G) {
  'use strict';
  var UNITS = {
    'place-value-number-sense': {
      bigIdea: 'Every digit has a value based on its place, and multiplying or dividing by powers of ten shifts that value.',
      objectives: [
        'I can explain how a digit’s value changes when it moves one place to the left or right.',
        'I can write powers of ten using exponents and expanded form.',
        'I can read, write and compare decimals through the thousandths.',
        'I can round decimals to any place and explain my reasoning.',
        'I can use place-value reasoning to solve real-world number problems.'
      ],
      vocabulary: [
        { term: 'place value', def: 'The value of a digit based on its position in a number.' },
        { term: 'period', def: 'A group of three digits separated by commas, such as thousands or millions.' },
        { term: 'expanded form', def: 'A number written as the sum of the values of its digits.' },
        { term: 'exponent', def: 'A small number that tells how many times the base is used as a factor.' },
        { term: 'base', def: 'The number that is multiplied repeatedly in a power.' },
        { term: 'decimal', def: 'A number with one or more digits to the right of the decimal point.' },
        { term: 'thousandth', def: 'One of one thousand equal parts of a whole.' },
        { term: 'round', def: 'To replace a number with a nearby number that has fewer non-zero digits.' }
      ],
      misconceptions: [
        ['The digit 7 in 4.7 is worth 7 ones.', 'In 4.7 the 7 is in the tenths place, so it is worth 7 tenths, or 0.7.'],
        ['0.5 is greater than 0.45 because 5 is greater than 45.', 'Line up place values: 0.50 is greater than 0.45.'],
        ['Multiplying by 10 always adds a zero to the written number.', 'Multiplying by 10 moves every digit one place left; 3.2 × 10 = 32, not 3.20.']
      ],
      support: ['Use a place-value chart and base-ten blocks before moving to symbols.', 'Read decimals aloud in word form to connect digits to values.'],
      extend: ['Compare decimals with different numbers of digits and justify with a number line.', 'Write a number that rounds to a target value from several starting numbers.'],
      materials: ['Place-value chart', 'Base-ten blocks or decimal grids', 'Number lines', 'Dry-erase markers']
    },
    'multi-digit-multiplication-division': {
      bigIdea: 'Multiplication and division can be broken into smaller, place-value-friendly steps, and remainders must be interpreted for the situation.',
      objectives: [
        'I can multiply multi-digit whole numbers using an efficient strategy.',
        'I can estimate products and quotients to check whether an answer is reasonable.',
        'I can divide by one-digit and two-digit divisors.',
        'I can explain what a remainder means in a word problem.',
        'I can choose a strategy and justify my answer with an estimate.'
      ],
      vocabulary: [
        { term: 'product', def: 'The answer to a multiplication problem.' },
        { term: 'quotient', def: 'The answer to a division problem.' },
        { term: 'factor', def: 'A number that is multiplied by another number.' },
        { term: 'divisor', def: 'The number you divide by.' },
        { term: 'dividend', def: 'The number being divided.' },
        { term: 'remainder', def: 'The amount left over when a number does not divide evenly.' },
        { term: 'estimate', def: 'A close answer found by rounding or using friendly numbers.' },
        { term: 'partial product', def: 'A product found by multiplying one place-value part at a time.' }
      ],
      misconceptions: [
        ['A remainder can always be ignored.', 'The situation decides: you may need to round up, drop the remainder, or split it.'],
        ['2,400 ÷ 30 = 80 because you can cross out one zero from each number.', 'Crossing out zeros works only when both numbers are multiples of ten; 2,400 ÷ 30 = 80 because 80 × 30 = 2,400.'],
        ['The estimate is the exact answer.', 'An estimate tells whether an exact answer is reasonable; it is not a substitute unless the problem asks for one.']
      ],
      support: ['Model with area models and partial products before the standard algorithm.', 'Use multiplication facts and friendly numbers to build estimates first.'],
      extend: ['Solve multi-step problems that require interpreting a remainder.', 'Compare two division strategies and explain which is more efficient.'],
      materials: ['Grid paper', 'Multiplication chart', 'Calculators for checking (teacher choice)', 'Word-problem cards']
    },
    'decimal-operations': {
      bigIdea: 'Decimal operations follow whole-number place-value rules, and the decimal point must be placed by reasoning, not by counting digits blindly.',
      objectives: [
        'I can add and subtract decimals by lining up place values.',
        'I can multiply decimals by whole numbers.',
        'I can multiply decimals by decimals.',
        'I can divide decimals by whole numbers and by decimals.',
        'I can estimate to check the reasonableness of a decimal answer.',
        'I can solve money and measurement problems involving decimals.'
      ],
      vocabulary: [
        { term: 'sum', def: 'The answer to an addition problem.' },
        { term: 'difference', def: 'The answer to a subtraction problem.' },
        { term: 'product', def: 'The answer to a multiplication problem.' },
        { term: 'quotient', def: 'The answer to a division problem.' },
        { term: 'decimal point', def: 'The dot that separates whole-number places from decimal places.' },
        { term: 'estimate', def: 'A close answer used to judge reasonableness.' },
        { term: 'reasonable', def: 'Close to an estimate and sensible for the situation.' }
      ],
      misconceptions: [
        ['When adding decimals, line up the last digits.', 'Line up the decimal points so like place values are added.'],
        ['0.3 × 0.4 = 1.2 because 3 × 4 = 12.', 'The product is smaller than either factor: 0.3 × 0.4 = 0.12.'],
        ['A quotient is always smaller than the dividend.', 'Dividing by a number less than 1 can make the quotient larger, as in 6 ÷ 0.5 = 12.']
      ],
      support: ['Use decimal grids and money models to make each operation visible.', 'Estimate first and compare the exact answer with the estimate.'],
      extend: ['Explain why multiplying by a decimal less than 1 makes the product smaller.', 'Solve multi-step money problems and justify rounding choices.'],
      materials: ['Decimal grids', 'Play money', 'Place-value charts', 'Number lines']
    },
    'numerical-expressions-patterns': {
      bigIdea: 'Numerical expressions communicate a calculation, and patterns can be described by rules that predict what comes next.',
      objectives: [
        'I can evaluate expressions using the order of operations and grouping symbols.',
        'I can write a numerical expression for a spoken or written calculation.',
        'I can interpret an expression without evaluating it.',
        'I can generate and extend numerical patterns using a rule.',
        'I can compare two patterns and describe the relationship between them.'
      ],
      vocabulary: [
        { term: 'expression', def: 'A combination of numbers and operations without an equals sign.' },
        { term: 'evaluate', def: 'To find the value of an expression.' },
        { term: 'order of operations', def: 'The agreed order for calculating: grouping symbols, then multiply/divide, then add/subtract.' },
        { term: 'grouping symbols', def: 'Parentheses, brackets or braces that show which part to calculate first.' },
        { term: 'pattern', def: 'A sequence that follows a rule.' },
        { term: 'rule', def: 'A description of how a pattern changes.' },
        { term: 'term', def: 'One number or item in a pattern.' }
      ],
      misconceptions: [
        ['Always calculate left to right.', 'Multiply and divide before adding and subtracting unless grouping symbols say otherwise.'],
        ['(4 + 6) × 2 and 4 + 6 × 2 are the same.', 'Grouping symbols change the value: 20 versus 16.'],
        ['A pattern must repeat the same numbers.', 'A pattern can grow or shrink by a rule, such as add 3 each time.']
      ],
      support: ['Underline the operation to do first and say the steps aloud.', 'Use two-color counters or a table to show a growing pattern.'],
      extend: ['Write two different expressions that have the same value.', 'Describe a two-step rule connecting two patterns.'],
      materials: ['Expression cards', 'Two-color counters', 'Pattern tables', 'Whiteboards']
    },
    'fraction-addition-subtraction': {
      bigIdea: 'Fractions can be added or subtracted only when they describe the same-size parts, so equivalent fractions are the key.',
      objectives: [
        'I can find common denominators to create equivalent fractions.',
        'I can add and subtract fractions with unlike denominators.',
        'I can add and subtract mixed numbers, regrouping when needed.',
        'I can estimate sums and differences using benchmark fractions.',
        'I can check whether a fraction answer is reasonable.',
        'I can solve fraction word problems and check that my answer is reasonable.'
      ],
      vocabulary: [
        { term: 'numerator', def: 'The top number of a fraction; it tells how many parts are counted.' },
        { term: 'denominator', def: 'The bottom number of a fraction; it tells the size of the parts.' },
        { term: 'equivalent fractions', def: 'Fractions that name the same amount, such as 1/2 and 2/4.' },
        { term: 'common denominator', def: 'A shared denominator that lets two fractions be added or subtracted.' },
        { term: 'mixed number', def: 'A whole number and a fraction together, such as 2 3/4.' },
        { term: 'benchmark fraction', def: 'A familiar fraction such as 0, 1/4, 1/2, 3/4 or 1 used to estimate.' },
        { term: 'simplest form', def: 'A fraction whose numerator and denominator have no common factor greater than 1.' }
      ],
      misconceptions: [
        ['Add the denominators: 1/2 + 1/3 = 2/5.', 'Find a common denominator first: 3/6 + 2/6 = 5/6.'],
        ['A bigger denominator means a bigger fraction.', 'With the same numerator, a bigger denominator makes smaller parts.'],
        ['Mixed numbers can be added by adding whole numbers and fractions separately without regrouping.', 'Sometimes the fraction parts make more than one whole and must be regrouped.']
      ],
      support: ['Use fraction strips and number lines to see equal-sized parts.', 'Estimate with benchmarks before calculating.'],
      extend: ['Solve problems that require regrouping a mixed number.', 'Explain why a common denominator is necessary using a visual model.'],
      materials: ['Fraction strips', 'Number lines', 'Fraction circles', 'Grid paper']
    },
    'fraction-multiplication-division': {
      bigIdea: 'Multiplying by a fraction scales a quantity, and dividing by a unit fraction asks how many of those parts fit.',
      objectives: [
        'I can interpret a fraction as division of the numerator by the denominator.',
        'I can multiply a fraction by a whole number.',
        'I can multiply a fraction by a fraction.',
        'I can find area with fractional side lengths.',
        'I can explain multiplication as scaling.',
        'I can divide unit fractions and whole numbers.',
        'I can solve fraction multiplication and division word problems.'
      ],
      vocabulary: [
        { term: 'scaling', def: 'Resizing a quantity by multiplying.' },
        { term: 'unit fraction', def: 'A fraction with numerator 1, such as 1/4.' },
        { term: 'area', def: 'The amount of surface inside a flat shape.' },
        { term: 'factor', def: 'A number being multiplied.' },
        { term: 'product', def: 'The answer to a multiplication problem.' },
        { term: 'quotient', def: 'The answer to a division problem.' },
        { term: 'reciprocal', def: 'Two numbers whose product is 1, such as 1/4 and 4.' }
      ],
      misconceptions: [
        ['Multiplying always makes a number larger.', 'Multiplying by a fraction less than 1 makes the product smaller, such as 8 × 1/2 = 4.'],
        ['3 ÷ 1/4 means 3 divided into 4 equal parts.', 'It asks how many fourths fit in 3 wholes: there are 12.'],
        ['To multiply fractions, multiply numerators and denominators and also find a common denominator.', 'No common denominator is needed for multiplication.']
      ],
      support: ['Fold paper or shade area models to show each product.', 'Use repeated addition for whole-number times a fraction.'],
      extend: ['Explain why dividing by a unit fraction is the same as multiplying by its reciprocal.', 'Create and solve a real-world scaling problem.'],
      materials: ['Fraction strips', 'Grid paper', 'Scissors', 'Area-model templates']
    },
    'measurement-conversions': {
      bigIdea: 'Measurements can be converted within a system by multiplying or dividing by a known unit relationship.',
      objectives: [
        'I can convert customary units of length.',
        'I can convert customary units of weight and capacity.',
        'I can convert metric units using powers of ten.',
        'I can solve multi-step measurement problems and label units.',
        'I can choose the most useful unit for a real-world measurement.'
      ],
      vocabulary: [
        { term: 'unit', def: 'A standard amount used to measure, such as an inch or a liter.' },
        { term: 'convert', def: 'To change a measurement to a different unit without changing the amount.' },
        { term: 'customary system', def: 'The measurement system used in the United States, including inches, feet, pounds and gallons.' },
        { term: 'metric system', def: 'A decimal measurement system based on meters, grams and liters.' },
        { term: 'capacity', def: 'The amount a container can hold.' },
        { term: 'weight', def: 'How heavy an object is in the customary system.' },
        { term: 'mass', def: 'The amount of matter in an object, measured in the metric system.' }
      ],
      misconceptions: [
        ['A larger unit always means a larger number.', 'A larger unit means fewer of them: 3 feet is 1 yard, not 3 yards.'],
        ['Metric conversions use different factors for every unit.', 'Metric units are related by powers of ten.'],
        ['You can add measurements with different units without converting.', 'Convert to the same unit before adding or comparing.']
      ],
      support: ['Keep a reference chart of unit relationships visible.', 'Use a two-column table to track multiplication or division by the conversion factor.'],
      extend: ['Solve problems that convert twice, such as hours to minutes to seconds.', 'Explain why the number changes but the measurement does not.'],
      materials: ['Rulers and meter sticks', 'Measuring cups', 'Balance scale', 'Conversion reference chart']
    },
    'volume-three-dimensional-figures': {
      bigIdea: 'Volume measures the space inside a solid and can be found by counting unit cubes or multiplying the area of the base by the height.',
      objectives: [
        'I can explain volume as the number of unit cubes that fill a solid.',
        'I can count unit cubes to find volume.',
        'I can use the formulas V = l × w × h and V = B × h.',
        'I can find the volume of a composite figure by decomposing it.',
        'I can solve real-world volume problems and label cubic units.'
      ],
      vocabulary: [
        { term: 'volume', def: 'The amount of space a solid figure occupies.' },
        { term: 'unit cube', def: 'A cube with edges one unit long; it measures one cubic unit.' },
        { term: 'cubic unit', def: 'The unit used to measure volume, such as cubic centimeters.' },
        { term: 'base', def: 'The face of a solid used as the bottom for volume formulas.' },
        { term: 'height', def: 'The perpendicular distance from the base to the top.' },
        { term: 'composite figure', def: 'A shape made from two or more simpler shapes.' },
        { term: 'decompose', def: 'To break a figure into smaller parts.' }
      ],
      misconceptions: [
        ['Volume is the same as area.', 'Area measures a flat surface in square units; volume measures space in cubic units.'],
        ['You can add the edge lengths to find volume.', 'Multiply length, width and height (or base area by height).'],
        ['A composite figure must be solved with one formula.', 'Decompose it, find each volume, then add or subtract.']
      ],
      support: ['Build solids with unit cubes and count layer by layer.', 'Label length, width and height on a sketch before calculating.'],
      extend: ['Find a missing dimension when the volume is known.', 'Design two different composite solids with the same volume.'],
      materials: ['Unit cubes', 'Isometric dot paper', 'Rulers', 'Solid models']
    },
    'coordinate-plane-graphing': {
      bigIdea: 'An ordered pair names one exact location on the coordinate plane, and patterns can be graphed as relationships between two quantities.',
      objectives: [
        'I can identify the axes, origin and quadrants of the coordinate plane.',
        'I can plot and read ordered pairs in quadrant I.',
        'I can solve real-world problems using coordinates.',
        'I can graph two numerical patterns and describe their relationship.'
      ],
      vocabulary: [
        { term: 'coordinate plane', def: 'A grid formed by a horizontal number line and a vertical number line.' },
        { term: 'x-axis', def: 'The horizontal number line.' },
        { term: 'y-axis', def: 'The vertical number line.' },
        { term: 'origin', def: 'The point (0, 0) where the axes meet.' },
        { term: 'ordered pair', def: 'Two numbers (x, y) that locate a point.' },
        { term: 'x-coordinate', def: 'The first number in an ordered pair; it tells how far to move right.' },
        { term: 'y-coordinate', def: 'The second number in an ordered pair; it tells how far to move up.' },
        { term: 'quadrant', def: 'One of the four regions of the coordinate plane.' }
      ],
      misconceptions: [
        ['(3, 5) and (5, 3) name the same point.', 'Order matters: the first number is horizontal, the second is vertical.'],
        ['Start counting at 1 on each axis.', 'The origin is 0; count spaces from the origin.'],
        ['A graph is only for math class.', 'Graphs show relationships between real quantities, such as time and distance.']
      ],
      support: ['Use a floor grid or large paper grid and walk to points.', 'Say “right then up” aloud for every ordered pair.'],
      extend: ['Graph two patterns and compare their steepness.', 'Write a real-world story for a set of points.'],
      materials: ['Grid paper', 'Rulers', 'Colored pencils', 'Coordinate-plane mats']
    },
    'classifying-two-dimensional-figures': {
      bigIdea: 'Shapes are classified by their properties, and a shape can belong to more than one category in a hierarchy.',
      objectives: [
        'I can identify polygons and describe their attributes.',
        'I can classify triangles by sides and angles.',
        'I can classify quadrilaterals by their properties.',
        'I can use a hierarchy to explain how shapes are related.',
        'I can justify a classification with evidence.'
      ],
      vocabulary: [
        { term: 'polygon', def: 'A closed flat shape made of straight sides.' },
        { term: 'regular polygon', def: 'A polygon with all sides and all angles equal.' },
        { term: 'triangle', def: 'A polygon with three sides.' },
        { term: 'quadrilateral', def: 'A polygon with four sides.' },
        { term: 'parallel', def: 'Lines that never cross and stay the same distance apart.' },
        { term: 'perpendicular', def: 'Lines that meet at a right angle.' },
        { term: 'hierarchy', def: 'A system that groups shapes from general to more specific.' }
      ],
      misconceptions: [
        ['A square is not a rectangle.', 'A square has four right angles, so it is a special rectangle.'],
        ['All quadrilaterals are rectangles.', 'A quadrilateral only needs four sides; rectangles are one kind of quadrilateral.'],
        ['A shape’s name depends on how it is turned.', 'A rotation does not change a shape’s properties or name.']
      ],
      support: ['Sort shape cards by one property at a time.', 'Trace and label parallel and perpendicular sides.'],
      extend: ['Build a shape hierarchy and defend each branch.', 'Find examples and non-examples of a definition.'],
      materials: ['Shape cards', 'Geoboards', 'Rulers and protractors', 'Sorting mats']
    },
    'data-line-plots-problem-solving': {
      bigIdea: 'A line plot organizes measurements so we can see the distribution and solve problems about the data.',
      objectives: [
        'I can read a line plot with fractional measurements.',
        'I can make a line plot from a set of measurements.',
        'I can find totals, differences and fair shares using line-plot data.',
        'I can solve multi-step problems with data and explain my reasoning.'
      ],
      vocabulary: [
        { term: 'data', def: 'Information collected by counting or measuring.' },
        { term: 'line plot', def: 'A number line that shows each measurement with an X or dot.' },
        { term: 'frequency', def: 'How often a value appears in a data set.' },
        { term: 'outlier', def: 'A value that is far away from most of the other data.' },
        { term: 'range', def: 'The difference between the greatest and least values.' },
        { term: 'fair share', def: 'The amount each group gets when a total is divided equally.' },
        { term: 'multi-step problem', def: 'A problem that needs more than one calculation to solve.' }
      ],
      misconceptions: [
        ['The tallest stack is the total number of measurements.', 'The tallest stack is the most frequent value; add all the Xs for the total.'],
        ['Line plots can only show whole numbers.', 'Line plots can show fractions by dividing the number line into equal parts.'],
        ['The range is the greatest value.', 'Range is greatest minus least.']
      ],
      support: ['Build the line plot with sticky notes or cubes first.', 'Read each question aloud and underline the quantities involved.'],
      extend: ['Compare two data sets shown on separate line plots.', 'Write a multi-step question that uses the data.'],
      materials: ['Number lines', 'Sticky notes', 'Rulers', 'Data cards']
    }
  };

  var THEMES = {
    space: { name: 'Space Adventure', icon: '🚀', colors: ['#2f7fd8', '#8a4fd6', '#f08c1a', '#1aa37a', '#d63c7a', '#0f97b5', '#ffd34d'] },
    ocean: { name: 'Ocean Dive', icon: '🐠', colors: ['#0f97b5', '#2f7fd8', '#1aa37a', '#8a4fd6', '#f08c1a', '#d63c7a', '#ffd34d'] },
    jungle: { name: 'Jungle Trek', icon: '🦜', colors: ['#1aa37a', '#8fbf2f', '#f08c1a', '#2f7fd8', '#d63c7a', '#8a4fd6', '#ffd34d'] },
    arcade: { name: 'Arcade Quest', icon: '🕹️', colors: ['#d63c7a', '#8a4fd6', '#2f7fd8', '#1aa37a', '#f08c1a', '#0f97b5', '#ffd34d'] },
    bakery: { name: 'Bakery Lab', icon: '🧁', colors: ['#d63c7a', '#f08c1a', '#ffd34d', '#1aa37a', '#8a4fd6', '#0f97b5', '#2f7fd8'] },
    carnival: { name: 'School Carnival', icon: '🎪', colors: ['#f08c1a', '#d63c7a', '#8a4fd6', '#2f7fd8', '#1aa37a', '#0f97b5', '#ffd34d'] }
  };

  var COLOR_NAMES = [
    ['Red', '#e94b3c'], ['Orange', '#f08c1a'], ['Yellow', '#f2c94c'], ['Green', '#1aa37a'],
    ['Blue', '#2f7fd8'], ['Purple', '#8a4fd6'], ['Pink', '#d63c7a'], ['Teal', '#0f97b5'],
    ['Brown', '#8b5a2b'], ['Black', '#333333']
  ];

  G.G5_GENERATOR_CONTENT = { units: UNITS, themes: THEMES, colorNames: COLOR_NAMES };
})(typeof window !== 'undefined' ? window : globalThis);
