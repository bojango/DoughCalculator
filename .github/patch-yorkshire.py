from pathlib import Path
import re

p = Path('index.html')
s = p.read_text()

# CSS for a simple Yorkshire pudding profile and disabled derived inputs.
anchor = ".roll:after{content:\"\";position:absolute;width:12px;height:10px;left:6px;top:4px;border:2px solid var(--bg);border-left-color:transparent;border-radius:50%;transform:rotate(-25deg)}\n"
insert = anchor + ".yorkie{position:relative;width:24px;height:18px;background:var(--offwhite);border-radius:5px 5px 10px 10px;transform:perspective(30px) rotateX(-4deg)}\n.yorkie:after{content:\"\";position:absolute;left:5px;right:5px;top:3px;height:7px;border-radius:50%;background:var(--bg);opacity:.78}\n.value-row input:disabled{color:var(--muted);opacity:.72}\n.step-btn:disabled{opacity:.18;pointer-events:none}\n"
if '.yorkie{' not in s:
    assert anchor in s, 'Yorkshire CSS anchor missing'
    s = s.replace(anchor, insert, 1)

# Bread selector.
anchor = '        <option value="focaccia">Focaccia</option>\n'
insert = anchor + '        <option value="yorkshire">Yorkshire puddings</option>\n'
if 'value="yorkshire"' not in s:
    assert anchor in s, 'bread selector anchor missing'
    s = s.replace(anchor, insert, 1)

# Recipe definition. Baseline scales Good Food's 4 medium muffin-tin puddings to a 12-hole standard tray.
anchor = "    sandwich:{\n"
recipe = """    yorkshire:{
      mode:'yorkshire',flour:150,qty:12,flourPer:12.5,milkPct:120,eggPct:100,oilMlPer:3.75,
      desc:'Standard muffin-tin Yorkshire puddings. Scaling basis: 4 medium puddings = 50 g plain flour, 1 large egg, 60 ml milk and 1 tbsp sunflower oil.',
      method:['Heat oven to 230°C / 210°C fan.','Divide the sunflower or vegetable oil between the selected muffin-tin holes.','Heat the tin in the oven until the oil is very hot.','Whisk the plain flour and eggs until smooth.','Gradually whisk in the milk until completely lump-free; season with salt and pepper.','Rest the batter for at least 15 min if time allows, then give it a quick whisk.','Working quickly, divide the batter evenly between the hot muffin-tin holes.','Bake undisturbed for 20–25 min until well risen, crisp and browned. Do not open the oven door during baking.']
    },
""" + anchor
if "mode:'yorkshire'" not in s:
    assert anchor in s, 'recipe anchor missing'
    s = s.replace(anchor, recipe, 1)

# Generalise ingredient rows so Yorkshire milk/oil can display ml without disturbing existing gram rows.
old = "  function addRow(name,p,m,sub='') {\n    $('#rows').insertAdjacentHTML('beforeend', `<div class=\"result-row\">\n      <div class=\"result-name\">${name}</div><div class=\"result-pct\">${p}</div><div class=\"result-mass\">${fmt(m)} g${sub?`<div class=\"result-sub\">${sub}</div>`:''}</div>\n    </div>`);\n    lastResult.lines.push(`${name}: ${fmt(m)} g${p && p!=='—' ? ` (${p})` : ''}${sub?` [${sub}]`:''}`);\n  }\n"
new = "  function addRow(name,p,m,sub='',unit='g') {\n    $('#rows').insertAdjacentHTML('beforeend', `<div class=\"result-row\">\n      <div class=\"result-name\">${name}</div><div class=\"result-pct\">${p}</div><div class=\"result-mass\">${fmt(m)} ${unit}${sub?`<div class=\"result-sub\">${sub}</div>`:''}</div>\n    </div>`);\n    lastResult.lines.push(`${name}: ${fmt(m)} ${unit}${p && p!=='—' ? ` (${p})` : ''}${sub?` [${sub}]`:''}`);\n  }\n"
if "function addRow(name,p,m,sub='',unit='g')" not in s:
    assert old in s, 'addRow anchor missing'
    s = s.replace(old, new, 1)

# Replace renderInputs with a Yorkshire-aware version.
start = s.index('  function renderInputs() {')
end = s.index('\n  function renderAdvanced() {', start)
render_inputs = r'''  function syncYorkshireBasisUI() {
    if (recipe().mode !== 'yorkshire') return;
    const basis=$('#yorkBasis')?.value||'qty';
    const qty=$('#yorkQty'), flour=$('#flour');
    if(!qty||!flour) return;
    if(basis==='qty') flour.value=Math.round((read('yorkQty',recipe().qty,1,60)*recipe().flourPer)*100)/100;
    else qty.value=Math.round((read('flour',recipe().flour,25,5000)/recipe().flourPer)*10)/10;
    qty.disabled=basis!=='qty';
    flour.disabled=basis!=='flour';
    root.querySelectorAll('[data-step-target="yorkQty"]').forEach(b=>b.disabled=basis!=='qty');
    root.querySelectorAll('[data-step-target="flour"]').forEach(b=>b.disabled=basis!=='flour');
    renderIcon();
  }

  function renderInputs() {
    const r = recipe();
    const key = $('#bread').value;
    let h = '';
    $('#advancedDetails').classList.toggle('hidden', r.mode==='yorkshire');
    if (r.mode === 'yorkshire') {
      h += selectField('yorkBasis','Scale by','<option value="qty">Quantity</option><option value="flour">Flour weight</option>');
      h += stepField('yorkQty','Yorkshire puddings',r.qty,'qty',1,1,60);
      h += stepField('flour','Flour basis',r.flour,'g',12.5,25,5000);
    } else if (r.mode === 'balls') {
      h += stepField('balls','Dough balls',3,'qty',1,1,50);
      h += stepField('weight','Ball size',310,'g',5,50,1000);
      h += stepField('hyd','Hydration',r.hyd,'%',1,40,100);
    } else if (r.mode === 'rolls') {
      h += stepField('rolls','Cinnamon rolls',r.rolls,'qty',1,1,50);
    } else {
      h += stepField('flour','Flour basis',r.flour,'g',25,100,5000);
      h += stepField('hyd',r.mode==='milk'?'Milk + water':'Hydration',r.hyd,'%',1,20,100);
    }
    if (r.types?.length) h += selectField('type','Yeast type',typeOptions(r));
    $('#inputs').innerHTML = h;
    if ($('#type')) {
      $('#type').disabled = r.types.length === 1;
      $('#type').addEventListener('change', () => {
        renderAdvanced();
        renderMethod();
        calculate();
      });
    }
    bindStepButtons($('#inputs'));

    if(r.mode==='yorkshire'){
      syncYorkshireBasisUI();
      $('#yorkBasis').addEventListener('change',()=>{syncYorkshireBasisUI();updateModifiedBadge();saveLastState();});
      $('#yorkQty').addEventListener('input',()=>{syncYorkshireBasisUI();updateModifiedBadge();scheduleStateSave();});
      $('#flour').addEventListener('input',()=>{syncYorkshireBasisUI();updateModifiedBadge();scheduleStateSave();});
    }
  }
'''
s = s[:start] + render_inputs + s[end:]

# Yorkshire has no Advanced settings.
anchor = "  function renderAdvanced() {\n    const r = recipe();\n    const type = $('#type')?.value || r.def;\n"
replace = "  function renderAdvanced() {\n    const r = recipe();\n    if (r.mode === 'yorkshire') { $('#advancedGrid').innerHTML=''; return; }\n    const type = $('#type')?.value || r.def;\n"
if "if (r.mode === 'yorkshire') { $('#advancedGrid').innerHTML=''; return; }" not in s:
    assert anchor in s, 'renderAdvanced anchor missing'
    s = s.replace(anchor, replace, 1)

# Step buttons keep the derived Yorkshire field in sync.
old = "        if (['balls','weight','rolls'].includes(target.id)) renderIcon();\n        updateModifiedBadge();\n"
new = "        if (recipe().mode==='yorkshire' && ['yorkQty','flour'].includes(target.id)) syncYorkshireBasisUI();\n        else if (['balls','weight','rolls'].includes(target.id)) renderIcon();\n        updateModifiedBadge();\n"
if "recipe().mode==='yorkshire'" not in s[s.index('function bindStepButtons'):s.index('function commercialYeastPct')]:
    assert old in s, 'step button anchor missing'
    s = s.replace(old, new, 1)

# Yorkshire visual.
anchor = "    } else if (k==='focaccia') {\n"
insert = "    } else if (k==='yorkshire') {\n      const c=Math.max(1,Math.round(read('yorkQty',recipe().qty,.1,100)));\n      $('#visualTitle').textContent='YORKSHIRE PUDDINGS';\n      $('#visualLabel').textContent=`~${fmt(read('yorkQty',recipe().qty,.1,100))} PUDS`;\n      stage.innerHTML=pairs(c,'yorkie');\n" + anchor
if "YORKSHIRE PUDDINGS';" not in s:
    assert anchor in s, 'visual anchor missing'
    s = s.replace(anchor, insert, 1)

# Calculation branch and optional yeast selector handling.
s = s.replace("    const type = $('#type').value;\n", "    const type = $('#type')?.value || r.def || null;\n", 1)
s = s.replace("    let rawDough = 0;\n\n    if (key === 'pizza') {", "    let rawDough = 0;\n    let totalLabel = 'TOTAL';\n\n    if (key === 'yorkshire') {\n      syncYorkshireBasisUI();\n      const f=read('flour',r.flour,25,5000);\n      const q=read('yorkQty',r.qty,.1,100);\n      const milk=f*r.milkPct/100;\n      const eggMass=f*r.eggPct/100;\n      const oilMl=q*r.oilMlPer;\n      addRow('Plain flour','100%',f);\n      addRow('Whole milk',pct(r.milkPct),milk,'','ml');\n      addRow('Large egg',pct(r.eggPct),eggMass,eggNote(eggMass));\n      addRow('Sunflower / vegetable oil','—',oilMl,'for the tin','ml');\n      rawDough=total=f+milk+eggMass;\n      totalLabel='BATTER';\n      $('#yieldLine').innerHTML=`<span>~${fmt(q)} standard muffin-size puddings</span><span>Batter ~${fmt(rawDough)} g</span>`;\n      lastResult.yield=`~${fmt(q)} standard muffin-size Yorkshire puddings | Batter ~${fmt(rawDough)} g`;
      $('#foot').textContent=`~${fmt(q)} Yorkshire puddings // standard muffin tin`;\n\n    } else if (key === 'pizza') {", 1)
s = s.replace("    $('#total').textContent=`TOTAL / ${fmt(total)} G`;\n", "    $('#total').textContent=`${totalLabel} / ${fmt(total)} G`;\n", 1)

# Modified-state logic.
anchor = "    if(key==='cinnamon'&&neq(read('rolls',r.rolls),r.rolls)) return true;\n"
insert = anchor + "    if(key==='yorkshire'&&(neq(read('flour',r.flour),r.flour)||neq(read('yorkQty',r.qty),r.qty))) return true;\n"
if "key==='yorkshire'&&(neq(read('flour'" not in s:
    assert anchor in s, 'modified state anchor missing'
    s = s.replace(anchor, insert, 1)
s = s.replace("    if(!['pizza','cinnamon'].includes(key)&&(neq(read('flour',r.flour),r.flour)||neq(read('hyd',r.hyd),r.hyd))) return true;\n", "    if(!['pizza','cinnamon','yorkshire'].includes(key)&&(neq(read('flour',r.flour),r.flour)||neq(read('hyd',r.hyd),r.hyd))) return true;\n", 1)

# Saved/last state captures the Yorkshire scaling basis and quantity.
s = s.replace("    const ids=['balls','weight','flour','hyd','rolls','type','salt','starter','starterHyd','yeastCalc','yeastPct','fermentHours','fermentTemp','oil'];\n", "    const ids=['balls','weight','flour','hyd','rolls','yorkBasis','yorkQty','type','salt','starter','starterHyd','yeastCalc','yeastPct','fermentHours','fermentTemp','oil'];\n", 1)
anchor = "    if($('#bread').value==='cinnamon') return `${breadName} × ${Math.round(read('rolls',recipe().rolls,1,50))}`;\n"
insert = anchor + "    if($('#bread').value==='yorkshire') return `${breadName} × ${fmt(read('yorkQty',recipe().qty,.1,100))}`;\n"
if "breadName} × ${fmt(read('yorkQty'" not in s:
    assert anchor in s, 'default saved name anchor missing'
    s = s.replace(anchor, insert, 1)

p.write_text(s)

# Bump service worker cache.
sw=Path('sw.js')
t=sw.read_text()
t=re.sub(r"const CACHE='dough-calculator-v\d+';", "const CACHE='dough-calculator-v9';", t, count=1)
sw.write_text(t)
