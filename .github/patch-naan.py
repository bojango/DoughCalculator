from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

# Selector
anchor='        <option value="khubz">Lebanese Khubz / Pita</option>\n'
insert=anchor+'        <option value="naan">Naan</option>\n'
if 'value="naan"' not in s:
    assert anchor in s, 'selector anchor missing'
    s=s.replace(anchor,insert,1)

# Naan graphic
anchor='.pita:after{content:"";position:absolute;left:8px;right:8px;top:50%;height:1px;background:var(--bg);opacity:.35}\n'
insert=anchor+'.naan{position:relative;width:48px;height:30px;background:var(--offwhite);border-radius:58% 42% 52% 48% / 62% 48% 52% 38%;transform:rotate(-7deg)}\n.naan:after{content:"";position:absolute;width:5px;height:3px;border-radius:50%;background:var(--bg);left:12px;top:8px;box-shadow:16px 7px 0 var(--bg),7px 14px 0 var(--bg);opacity:.45}\n'
if '.naan{' not in s:
    assert anchor in s, 'graphic anchor missing'
    s=s.replace(anchor,insert,1)

# Recipe. Good Food method makes six balls even though page header says serves 6-8.
anchor='    yorkshire:{\n'
recipe="""    naan:{
      mode:'naan',qty:6,flour:300,waterMl:125,yogurtMl:150,butter:25,sugarTsp:2,bakingPowderTsp:.5,saltTsp:.5,nigellaTbsp:1,types:['ady','idy','fresh'],def:'ady',
      yeastPct:{ady:2.3333333333,idy:1.8666666667,fresh:5.6},
      desc:'Good Food-style naan, scaled from the six-ball method: 300 g strong white flour, 125 ml warm water, 150 ml natural yogurt, 25 g butter or ghee, 7 g dried yeast, sugar, baking powder, salt and nigella seeds.',
      method:['Prepare the yeast with the warm water and some of the sugar if needed for the yeast type.','Combine flour, remaining sugar, salt and baking powder. Add yogurt, melted butter or ghee, nigella seeds and the water/yeast mixture; bring together into a very soft dough.','Knead for about 10 min until smooth and elastic, keeping the dough soft.','Place in a buttered bowl, cover and leave warm for about 1 hr, until doubled.','Divide into the selected number of balls and keep covered.','Heat a large non-stick frying pan over high heat.','Roll each ball into a teardrop roughly 21 cm long and 13 cm at its widest point.','Dry-fry in the very hot pan for about 3 min until puffed, then turn and cook for another 3–4 min until cooked and charred in patches.','Brush cooked naans with melted butter or ghee, cover and keep warm while cooking the rest.']
    },
"""+anchor
if "mode:'naan'" not in s:
    assert anchor in s, 'recipe anchor missing'
    s=s.replace(anchor,recipe,1)

# Quantity input
anchor="    } else if (r.mode === 'flatbread') {\n      h += stepField('khubzQty','Khubz breads',r.qty,'qty',1,1,50);\n"
insert=anchor+"    } else if (r.mode === 'naan') {\n      h += stepField('naanQty','Naans',r.qty,'qty',1,1,50);\n"
if "stepField('naanQty'" not in s:
    assert anchor in s, 'input anchor missing'
    s=s.replace(anchor,insert,1)

# Naan has recipe-defined salt in tsp, so do not expose baker-percentage salt control.
s=s.replace("if (r.mode !== 'rolls' && r.mode !== 'milk') {", "if (r.mode !== 'rolls' && r.mode !== 'milk' && r.mode !== 'naan') {", 1)

# Quantity stepper updates graphic immediately.
s=s.replace("['balls','weight','rolls','khubzQty'].includes(target.id)", "['balls','weight','rolls','khubzQty','naanQty'].includes(target.id)", 1)

# Dynamic naan method so yeast preparation matches selected yeast type.
anchor="    } else {\n      steps = [...r.method];\n"
insert="""    } else if (key === 'naan') {
      if (type === 'ady') steps.push('Stir the active dry yeast and half the sugar into the warm water; leave 10–15 min until frothy.');
      else if (type === 'fresh') steps.push('Crumble the fresh yeast into the warm water with half the sugar; stir until dissolved.');
      else steps.push('Mix the IDY with the flour; keep the warm water for the wet ingredients.');
      steps.push('Combine flour, remaining sugar, salt and baking powder. Add yogurt, melted butter or ghee, nigella seeds and the water/yeast mixture; bring together into a very soft dough.');
      steps.push('Knead for about 10 min until smooth and elastic, keeping the dough soft.');
      steps.push('Place in a buttered bowl, cover and leave warm for about 1 hr, until doubled.');
      steps.push('Divide into the selected number of balls and keep covered.');
      steps.push('Heat a large non-stick frying pan over high heat.');
      steps.push('Roll each ball into a teardrop roughly 21 cm long and 13 cm at its widest point.');
      steps.push('Dry-fry for about 3 min until puffed, then turn and cook for another 3–4 min until cooked through and charred in patches.');
      steps.push('Brush each naan with melted butter or ghee, cover and keep warm while cooking the rest.');
"""+anchor
if "key === 'naan'" not in s[s.index('  function renderMethod() {'):s.index('  function pairs(')]:
    assert anchor in s, 'method anchor missing'
    s=s.replace(anchor,insert,1)

# Visual
anchor="    } else if (k==='yorkshire') {\n"
insert="""    } else if (k==='naan') {
      const c=Math.round(read('naanQty',recipe().qty,1,50));
      $('#visualTitle').textContent='NAAN';
      $('#visualLabel').textContent=`${c} × ~21 × 13 CM`;
      stage.innerHTML=pairs(c,'naan');
"""+anchor
if "$('#visualTitle').textContent='NAAN';" not in s:
    assert anchor in s, 'visual anchor missing'
    s=s.replace(anchor,insert,1)

# Text result helper for source ingredients expressed as ranges/volume measures.
anchor="  function group(text) {\n"
helper="""  function addTextRow(name,p,text,sub='') {
    $('#rows').insertAdjacentHTML('beforeend', `<div class=\"result-row\">
      <div class=\"result-name\">${name}</div><div class=\"result-pct\">${p}</div><div class=\"result-mass\">${text}${sub?`<div class=\"result-sub\">${sub}</div>`:''}</div>
    </div>`);
    lastResult.lines.push(`${name}: ${text}${sub?` [${sub}]`:''}`);
  }

"""+anchor
if 'function addTextRow(' not in s:
    assert anchor in s, 'helper anchor missing'
    s=s.replace(anchor,helper,1)

# Calculation branch
anchor="    } else if (key === 'focaccia') {\n"
insert="""    } else if (key === 'naan') {
      const qty=Math.round(read('naanQty',r.qty,1,50));
      const sc=qty/6;
      const f=r.flour*sc;
      const water=r.waterMl*sc;
      const yogurt=r.yogurtMl*sc;
      const butter=r.butter*sc;
      const yp=read('yeastPct',r.yeastPct[type],.001,15), yeast=f*yp/100;
      const sugarTsp=r.sugarTsp*sc, bakingTsp=r.bakingPowderTsp*sc, saltTsp=r.saltTsp*sc, nigellaTbsp=r.nigellaTbsp*sc;

      addRow('Strong white bread flour','100%',f);
      addRow('Warm water',pct(r.waterMl/r.flour*100),water,'','ml');
      addRow('Natural yogurt',pct(r.yogurtMl/r.flour*100),yogurt,'','ml');
      addRow(names[type],pct(yp),yeast);
      addRow('Butter / ghee — dough',pct(r.butter/r.flour*100),butter);
      addTextRow('Golden caster sugar','—',`${fmt(sugarTsp)} tsp`);
      addTextRow('Fine salt','—',`${fmt(saltTsp)} tsp`);
      addTextRow('Baking powder','—',`${fmt(bakingTsp)} tsp`);
      addTextRow('Nigella seeds','—',`${fmt(nigellaTbsp)} tbsp`);
      addTextRow('Butter / ghee — brushing','—',`${fmt(2*sc)}–${fmt(3*sc)} tbsp`,'for tray + brushing');

      // Approximate total includes reasonable gram equivalents for the source's spoon measures.
      const smallDry=(8+3+2+9)*sc;
      total=rawDough=f+water+yogurt+butter+yeast+smallDry;
      totalLabel='DOUGH ~';
      const per=rawDough/qty;
      $('#yieldLine').innerHTML=`<span>${qty} naans × ~${fmt(per)} g dough</span><span>Roll to ~21 × 13 cm</span>`;
      lastResult.yield=`${qty} naans × ~${fmt(per)} g dough | Roll to roughly 21 × 13 cm`;
      $('#foot').textContent=`${qty} naans // hot dry frying pan`;

"""+anchor
if "key === 'naan'" not in s[s.index('  function calculate() {'):]:
    assert anchor in s, 'calculation anchor missing'
    s=s.replace(anchor,insert,1)

# Modified state, saved state, naming
anchor="    if(key==='khubz'&&neq(read('khubzQty',r.qty),r.qty)) return true;\n"
insert=anchor+"    if(key==='naan'&&neq(read('naanQty',r.qty),r.qty)) return true;\n"
if "key==='naan'&&neq(read('naanQty'" not in s:
    assert anchor in s, 'modified anchor missing'
    s=s.replace(anchor,insert,1)

old="    const ids=['balls','weight','flour','hyd','rolls','khubzQty','yorkBasis','yorkQty','type','salt','starter','starterHyd','yeastCalc','yeastPct','fermentHours','fermentTemp','oil'];\n"
new="    const ids=['balls','weight','flour','hyd','rolls','khubzQty','naanQty','yorkBasis','yorkQty','type','salt','starter','starterHyd','yeastCalc','yeastPct','fermentHours','fermentTemp','oil'];\n"
if old in s:
    s=s.replace(old,new,1)

anchor="    if($('#bread').value==='khubz') return `${breadName} × ${Math.round(read('khubzQty',recipe().qty,1,50))}`;\n"
insert=anchor+"    if($('#bread').value==='naan') return `${breadName} × ${Math.round(read('naanQty',recipe().qty,1,50))}`;\n"
if "$('#bread').value==='naan'" not in s:
    assert anchor in s, 'saved-name anchor missing'
    s=s.replace(anchor,insert,1)

p.write_text(s)

sw=Path('sw.js')
t=sw.read_text()
t=re.sub(r"const CACHE='dough-calculator-v\d+';", "const CACHE='dough-calculator-v12';", t, count=1)
sw.write_text(t)
