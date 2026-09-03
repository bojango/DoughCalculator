from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

# Bread selector.
anchor='        <option value="focaccia">Focaccia</option>\n'
insert=anchor+'        <option value="khubz">Lebanese Khubz / Pita</option>\n'
if 'value="khubz"' not in s:
    assert anchor in s, 'selector anchor missing'
    s=s.replace(anchor,insert,1)

# Flatbread profile.
anchor='.crepe{width:30px;height:4px;border-radius:50%;background:var(--offwhite)}\n'
insert=anchor+'.pita{position:relative;width:48px;height:28px;border-radius:50%;background:var(--offwhite)}\n.pita:after{content:"";position:absolute;left:8px;right:8px;top:50%;height:1px;background:var(--bg);opacity:.35}\n'
if '.pita{' not in s:
    assert anchor in s, 'profile anchor missing'
    s=s.replace(anchor,insert,1)

# Recipe data. Exact base ratio from the supplied 8-bread recipe.
anchor='    yorkshire:{\n'
recipe="""    khubz:{
      mode:'flatbread',qty:8,flour:500,flourPer:62.5,hyd:64,salt:2,sugar:2,oilPct:3,types:['idy','ady','fresh'],def:'idy',
      yeastPct:{idy:1.4,ady:1.75,fresh:4.2},
      desc:'Lebanese khubz / pita: soft, thin, pocket-forming flatbreads. Base recipe makes 8 from 500 g strong white flour, 320 ml water, 7 g IDY, 10 g salt, 10 g sugar and 15 g olive oil. High heat and even rolling are critical for the pocket.',
      method:['Mix flour, yeast, sugar and salt. Add the warm water + olive oil and mix to a rough dough.','Knead 8–10 min until smooth, elastic and slightly tacky. Add extra flour only if absolutely necessary.','Cover and rise somewhere warm for 60–90 min, until roughly doubled.','Knock the air out gently; divide into the selected number of equal pieces and shape into balls.','Cover and rest 20 min so the dough relaxes.','Put a pizza stone, baking steel or heavy upside-down tray in the oven. Heat to 250°C / 230°C fan, or as hot as the oven will reliably go, for at least 30 min.','Roll each ball to about 18–20 cm wide and around 3 mm thick. Keep the thickness even and keep waiting dough covered.','Bake one or two breads directly on the very hot surface for roughly 2–3 min, until they balloon. Flip for another 30–60 sec only if necessary; do not overbake.','Stack the cooked breads immediately inside a clean tea towel so trapped steam keeps them soft and flexible.']
    },
"""+anchor
if "mode:'flatbread'" not in s:
    assert anchor in s, 'recipe anchor missing'
    s=s.replace(anchor,recipe,1)

# Primary input is quantity; yeast type remains available in the normal second field.
anchor="    } else if (r.mode === 'rolls') {\n"
insert="""    } else if (r.mode === 'flatbread') {
      h += stepField('khubzQty','Khubz breads',r.qty,'qty',1,1,50);
"""+anchor
if "stepField('khubzQty'" not in s:
    assert anchor in s, 'input anchor missing'
    s=s.replace(anchor,insert,1)

# Quantity steppers update the graphic immediately.
s=s.replace("else if (['balls','weight','rolls'].includes(target.id)) renderIcon();", "else if (['balls','weight','rolls','khubzQty'].includes(target.id)) renderIcon();", 1)

# Flatbread visual.
anchor="    } else if (k==='yorkshire') {\n"
insert="""    } else if (k==='khubz') {
      const c=Math.round(read('khubzQty',recipe().qty,1,50));
      $('#visualTitle').textContent='LEBANESE KHUBZ / PITA';
      $('#visualLabel').textContent=`${c} × 18–20 CM`;
      stage.innerHTML=pairs(c,'pita');
"""+anchor
if "$('#visualTitle').textContent='LEBANESE KHUBZ / PITA';" not in s:
    assert anchor in s, 'visual anchor missing'
    s=s.replace(anchor,insert,1)

# Calculator branch. The ingredient ratios scale only from the selected bread quantity.
anchor="    } else if (key === 'focaccia') {\n"
insert="""    } else if (key === 'khubz') {
      const qty=Math.round(read('khubzQty',r.qty,1,50));
      const f=qty*r.flourPer;
      const h=r.hyd/100;
      const s=read('salt',r.salt,0,10)/100;
      const yp=read('yeastPct',r.yeastPct[type],.001,15), y=yp/100;
      const water=f*h, salt=f*s, sugar=f*r.sugar/100, oil=f*r.oilPct/100, yeast=f*y;

      addRow('Strong white bread flour','100%',f);
      addRow('Warm water',pct(r.hyd),water,`~${fmt(water)} ml`);
      addRow(names[type],pct(yp),yeast);
      addRow('Fine salt',pct(s*100),salt);
      addRow('Sugar',pct(r.sugar),sugar);
      addRow('Olive oil',pct(r.oilPct),oil);

      total=rawDough=f+water+yeast+salt+sugar+oil;
      const per=rawDough/qty;
      $('#yieldLine').innerHTML=`<span>${qty} breads × ~${fmt(per)} g dough</span><span>Roll to 18–20 cm / ~3 mm</span>`;
      lastResult.yield=`${qty} Lebanese khubz / pita × ~${fmt(per)} g dough | Roll to 18–20 cm and ~3 mm thick`;
      $('#foot').textContent=`${qty} khubz // 18–20 cm // very high heat`;

"""+anchor
if "key === 'khubz'" not in s[s.index('  function calculate() {'):]:
    assert anchor in s, 'calculation anchor missing'
    s=s.replace(anchor,insert,1)

# Modified-state tracking.
anchor="    if(key==='cinnamon'&&neq(read('rolls',r.rolls),r.rolls)) return true;\n"
insert=anchor+"    if(key==='khubz'&&neq(read('khubzQty',r.qty),r.qty)) return true;\n"
if "key==='khubz'&&neq(read('khubzQty'" not in s:
    assert anchor in s, 'modified anchor missing'
    s=s.replace(anchor,insert,1)

# Save/restore quantity for last-state and named saved recipes.
old="    const ids=['balls','weight','flour','hyd','rolls','yorkBasis','yorkQty','type','salt','starter','starterHyd','yeastCalc','yeastPct','fermentHours','fermentTemp','oil'];\n"
new="    const ids=['balls','weight','flour','hyd','rolls','khubzQty','yorkBasis','yorkQty','type','salt','starter','starterHyd','yeastCalc','yeastPct','fermentHours','fermentTemp','oil'];\n"
if old in s:
    s=s.replace(old,new,1)

anchor="    if($('#bread').value==='cinnamon') return `${breadName} × ${Math.round(read('rolls',recipe().rolls,1,50))}`;\n"
insert=anchor+"    if($('#bread').value==='khubz') return `${breadName} × ${Math.round(read('khubzQty',recipe().qty,1,50))}`;\n"
if "$('#bread').value==='khubz'" not in s:
    assert anchor in s, 'saved-name anchor missing'
    s=s.replace(anchor,insert,1)

p.write_text(s)

# Force the installed PWA to pick up the new recipe.
sw=Path('sw.js')
t=sw.read_text()
t=re.sub(r"const CACHE='dough-calculator-v\d+';", "const CACHE='dough-calculator-v11';", t, count=1)
sw.write_text(t)
