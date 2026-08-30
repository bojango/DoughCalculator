from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

# Selector
anchor='        <option value="yorkshire">Yorkshire puddings</option>\n'
insert=anchor+'        <option value="pancakes">Pancakes</option>\n        <option value="crepes">Crêpes</option>\n'
if 'value="pancakes"' not in s:
    assert anchor in s
    s=s.replace(anchor,insert,1)

# Simple visuals
anchor='.yorkie:after{content:"";position:absolute;left:5px;right:5px;top:3px;height:7px;border-radius:50%;background:var(--bg);opacity:.78}\n'
insert=anchor+'.pancake{width:27px;height:8px;border-radius:50%;background:var(--offwhite)}\n.crepe{width:30px;height:4px;border-radius:50%;background:var(--offwhite)}\n'
if '.pancake{' not in s:
    assert anchor in s
    s=s.replace(anchor,insert,1)

# Recipes
anchor='    sandwich:{\n'
recipes="""    pancakes:{
      mode:'pancake',flour:180,qty:12,flourPer:15,
      desc:'Fluffy American-style pancakes, scaled from a standard 12-pancake recipe. Default size is about 4½ in / 11.5 cm each.',
      method:['Whisk the eggs and milk until light and foamy, then stir in the melted butter or vegetable oil.','Whisk flour, sugar, baking powder and salt together separately.','Gently mix the dry ingredients into the wet just until combined; a few small lumps are fine.','Rest the batter for about 15 min while the pan heats.','Heat a lightly greased heavy frying pan over medium heat.','Use about 60 ml / ¼ cup batter per pancake to make roughly 11.5 cm pancakes.','Cook until bubbles form and break on top, about 2 min; flip once and cook the second side for 1½–2 min.','Serve immediately or keep warm while cooking the remaining pancakes.']
    },
    crepes:{
      mode:'crepe',flour:100,qty:12,flourPer:8.3333333333,
      desc:'Thin 18 cm crêpes, scaled from a standard 12-crêpe recipe using a roughly 18 cm frying pan.',
      method:['Put the plain flour, eggs, milk, oil and a pinch of salt into a bowl or jug.','Whisk until completely smooth and the batter is similar to single cream.','Rest for around 30 min if time allows, then whisk briefly again.','Heat an 18 cm frying pan over medium heat and wipe it with a very thin film of oil.','Pour in just enough batter to coat the base, swirling immediately to form a thin crêpe.','Cook until the underside is lightly golden and the edges release, then flip.','Cook the second side briefly until lightly coloured.','Stack and keep warm while cooking the remaining crêpes.']
    },
"""+anchor
if "mode:'pancake'" not in s:
    assert anchor in s
    s=s.replace(anchor,recipes,1)

# Generalise Yorkshire quantity/flour scaling to the three quantity-led batter types.
s=s.replace("if (recipe().mode !== 'yorkshire') return;", "if (!['yorkshire','pancake','crepe'].includes(recipe().mode)) return;",1)
s=s.replace("if (recipe().mode==='yorkshire' && ['yorkQty','flour'].includes(target.id)) syncYorkshireBasisUI();", "if (['yorkshire','pancake','crepe'].includes(recipe().mode) && ['yorkQty','flour'].includes(target.id)) syncYorkshireBasisUI();",1)
s=s.replace("$('#advancedDetails').classList.toggle('hidden', r.mode==='yorkshire');", "const portionMode=['yorkshire','pancake','crepe'].includes(r.mode);\n    $('#advancedDetails').classList.toggle('hidden', portionMode);\n    $('#calc').textContent=portionMode?'Calculate batter':'Calculate dough';",1)
s=s.replace("if (r.mode === 'yorkshire') {\n      h += selectField('yorkBasis','Scale by','<option value=\"qty\">Quantity</option><option value=\"flour\">Flour weight</option>');\n      h += stepField('yorkQty','Yorkshire puddings',r.qty,'qty',1,1,60);", "if (portionMode) {\n      const portionLabel=r.mode==='yorkshire'?'Yorkshire puddings':r.mode==='pancake'?'Pancakes':'Crêpes';\n      h += selectField('yorkBasis','Scale by','<option value=\"qty\">Quantity</option><option value=\"flour\">Flour weight</option>');\n      h += stepField('yorkQty',portionLabel,r.qty,'qty',1,1,60);",1)
s=s.replace("if(r.mode==='yorkshire'){", "if(portionMode){",1)
s=s.replace("if (r.mode === 'yorkshire') { $('#advancedGrid').innerHTML=''; return; }", "if (['yorkshire','pancake','crepe'].includes(r.mode)) { $('#advancedGrid').innerHTML=''; return; }",1)

# Visuals
anchor="    } else if (k==='focaccia') {\n"
insert="""    } else if (k==='pancakes') {
      const c=Math.max(1,Math.round(read('yorkQty',recipe().qty,.1,100)));
      $('#visualTitle').textContent='PANCAKES';
      $('#visualLabel').textContent=`~${fmt(read('yorkQty',recipe().qty,.1,100))} × 11.5 CM`;
      stage.innerHTML=pairs(c,'pancake');
    } else if (k==='crepes') {
      const c=Math.max(1,Math.round(read('yorkQty',recipe().qty,.1,100)));
      $('#visualTitle').textContent='CRÊPES';
      $('#visualLabel').textContent=`~${fmt(read('yorkQty',recipe().qty,.1,100))} × 18 CM`;
      stage.innerHTML=pairs(c,'crepe');
"""+anchor
if "$('#visualTitle').textContent='PANCAKES';" not in s:
    assert anchor in s
    s=s.replace(anchor,insert,1)

# Calculation branches. Salt and baking powder gram equivalents follow King Arthur's ingredient weight chart.
anchor="    } else if (key === 'pizza') {\n"
insert="""    } else if (key === 'pancakes') {
      syncYorkshireBasisUI();
      const f=read('flour',r.flour,25,5000);
      const q=read('yorkQty',r.qty,.1,100);
      const milk=f*(283/180);
      const eggMass=f*(100/180);
      const butter=f*(43/180);
      const sugar=f*(25/180);
      const salt=f*(4.5/180);
      const bakingPowder=f*(8/180);
      addRow('Plain flour','100%',f);
      addRow('Milk',pct(283/180*100),milk);
      addRow('Large egg',pct(100/180*100),eggMass,eggNote(eggMass));
      addRow('Melted butter / vegetable oil',pct(43/180*100),butter);
      addRow('Granulated sugar',pct(25/180*100),sugar);
      addRow('Baking powder',pct(8/180*100),bakingPowder,'~'+fmt((q/12)*2)+' tsp');
      addRow('Fine salt',pct(4.5/180*100),salt,'~'+fmt((q/12)*0.75)+' tsp');
      rawDough=total=f+milk+eggMass+butter+sugar+salt+bakingPowder;
      totalLabel='BATTER';
      $('#yieldLine').innerHTML=`<span>~${fmt(q)} × 11.5 cm pancakes</span><span>Batter ~${fmt(rawDough)} g</span>`;
      lastResult.yield=`~${fmt(q)} American-style pancakes, about 11.5 cm each | Batter ~${fmt(rawDough)} g`;
      $('#foot').textContent=`~${fmt(q)} pancakes // 11.5 cm standard size`;

    } else if (key === 'crepes') {
      syncYorkshireBasisUI();
      const f=read('flour',r.flour,25,5000);
      const q=read('yorkQty',r.qty,.1,100);
      const milk=f*3;
      const eggMass=f;
      const oilMl=f*.15;
      addRow('Plain flour','100%',f);
      addRow('Milk','300%',milk,'','ml');
      addRow('Large egg','100%',eggMass,eggNote(eggMass));
      addRow('Sunflower / vegetable oil','—',oilMl,'in the batter','ml');
      rawDough=total=f+milk+eggMass+(oilMl*.92);
      totalLabel='BATTER';
      $('#yieldLine').innerHTML=`<span>~${fmt(q)} × 18 cm crêpes</span><span>Batter ~${fmt(rawDough)} g</span>`;
      lastResult.yield=`~${fmt(q)} thin crêpes, about 18 cm each | Batter ~${fmt(rawDough)} g`;
      $('#foot').textContent=`~${fmt(q)} crêpes // 18 cm standard size`;

"""+anchor
if "key === 'pancakes'" not in s[s.index('  function calculate() {'):]:
    assert anchor in s
    s=s.replace(anchor,insert,1)

# Modified/default state logic and saved naming.
s=s.replace("if(key==='yorkshire'&&(neq(read('flour',r.flour),r.flour)||neq(read('yorkQty',r.qty),r.qty))) return true;", "if(['yorkshire','pancakes','crepes'].includes(key)&&(neq(read('flour',r.flour),r.flour)||neq(read('yorkQty',r.qty),r.qty))) return true;",1)
s=s.replace("if(!['pizza','cinnamon','yorkshire'].includes(key)&&(neq(read('flour',r.flour),r.flour)||neq(read('hyd',r.hyd),r.hyd))) return true;", "if(!['pizza','cinnamon','yorkshire','pancakes','crepes'].includes(key)&&(neq(read('flour',r.flour),r.flour)||neq(read('hyd',r.hyd),r.hyd))) return true;",1)
s=s.replace("if($('#bread').value==='yorkshire') return `${breadName} × ${fmt(read('yorkQty',recipe().qty,.1,100))}`;", "if(['yorkshire','pancakes','crepes'].includes($('#bread').value)) return `${breadName} × ${fmt(read('yorkQty',recipe().qty,.1,100))}`;",1)

p.write_text(s)

sw=Path('sw.js')
t=sw.read_text()
t=re.sub(r"const CACHE='dough-calculator-v\d+';", "const CACHE='dough-calculator-v10';", t, count=1)
sw.write_text(t)
