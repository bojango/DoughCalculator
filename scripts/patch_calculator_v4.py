from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

def replace_once(old, new, label):
    global s
    if old not in s:
        raise SystemExit(f'Missing expected block: {label}')
    s = s.replace(old, new, 1)

replace_once(
    ".actions{display:grid;grid-template-columns:1fr 1fr;gap:6px}\n.secondary{min-height:39px;border:1px solid var(--line);background:transparent;color:var(--text);padding:8px 10px;font-size:9px;font-weight:800;letter-spacing:.1em;text-transform:uppercase}\n.status{min-height:15px;text-align:center;font-size:8px;color:var(--accent)}",
    ".actions{display:grid;grid-template-columns:1fr 1fr;gap:6px}\n.save-wide{grid-column:1/-1}\n.secondary{min-height:39px;border:1px solid var(--line);background:transparent;color:var(--text);padding:8px 10px;font-size:9px;font-weight:800;letter-spacing:.1em;text-transform:uppercase}\n.saved-details{border:1px solid var(--line);background:var(--panel)}\n.saved-list{border-top:1px solid var(--line)}\n.saved-empty{padding:9px 11px;font-size:9px;color:var(--muted)}\n.saved-row{display:grid;grid-template-columns:minmax(0,1fr) auto auto;align-items:center;gap:6px;min-height:40px;padding:6px 9px;border-bottom:1px solid var(--line2)}\n.saved-row:last-child{border-bottom:0}\n.saved-name{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:11px;font-weight:800}\n.saved-btn{min-height:29px;border:0;background:transparent;color:var(--accent);padding:4px 6px;font-size:8px;font-weight:800;letter-spacing:.08em;text-transform:uppercase}\n.saved-btn.delete{color:var(--muted)}\n.status{min-height:15px;text-align:center;font-size:8px;color:var(--accent)}",
    'saved recipe styles')

replace_once(
    '''        <div class="actions">\n          <button id="reset" class="secondary" type="button">Reset preset</button>\n          <button id="copyRecipe" class="secondary" type="button">Copy recipe</button>\n        </div>\n        <div id="status" class="status"></div>''',
    '''        <div class="actions">\n          <button id="saveRecipe" class="secondary save-wide" type="button">Save recipe</button>\n          <button id="reset" class="secondary" type="button">Reset preset</button>\n          <button id="copyRecipe" class="secondary" type="button">Copy recipe</button>\n        </div>\n        <details id="savedDetails" class="saved-details">\n          <summary>Saved recipes</summary>\n          <div id="savedList" class="saved-list"></div>\n        </details>\n        <div id="status" class="status"></div>''',
    'saved recipe UI')

replace_once(
    "const names = { idy:'Instant dry yeast', ady:'Active dry yeast', fresh:'Fresh yeast', starter:'Sourdough starter' };",
    "const names = { idy:'IDY', ady:'Active dry yeast', fresh:'Fresh yeast', starter:'Sourdough starter' };\n  const SAVE_KEY = 'dough-calculator-saved-recipes-v1';",
    'yeast names')

replace_once(
    '''    sandwich:{\n      mode:'flour',flour:360,hyd:63.1,salt:2.22,types:['idy','ady','fresh'],def:'idy',\n      yeastPct:{idy:1.67,ady:2.09,fresh:5.0},\n      desc:'Classic soft white sandwich loaf with milk, butter and sugar.',\n      method:['Heat milk to a simmer; pour over butter.','Cool to lukewarm.','Mix in sugar and yeast.','Add flour + salt; knead 6–8 min.','Rise about 1 hr.','Shape into loaf tin.','Proof about 1 hr until domed above tin.','Bake at 175°C for 30–35 min; cool.']\n    },''',
    '''    sandwich:{\n      mode:'flour',flour:500,hyd:64,salt:2,types:['idy','ady','fresh'],def:'idy',\n      yeastPct:{idy:1.4,ady:1.75,fresh:4.2},\n      desc:'Soft white loaf sized for one 900 g / 2 lb loaf tin: 500 g flour, 320 g whole milk, 7 g IDY, 10 g salt, 25 g sugar or honey and 35 g butter.',\n      method:['Warm the whole milk until lukewarm.','Mix flour, salt and sugar or honey.','Add milk + yeast; mix into a dough.','Knead 6–8 min.','Add softened butter; knead until smooth and elastic.','Cover and rise until roughly doubled, about 1 hr.','Shape and place in a greased 900 g / 2 lb loaf tin.','Proof until well risen above the tin.','Bake at 190°C / 170°C fan for 30–35 min; cool on a rack.']\n    },''',
    'white loaf preset')

replace_once(
    '''    } else if (key === 'sandwich') {\n      const f=read('flour',r.flour,100,5000);\n      const h=read('hyd',r.hyd,40,100)/100;\n      const yp=read('yeastPct',r.yeastPct[type],.001,15), y=yp/100;\n      const butter=f*28/360, sugar=f*25/360, salt=f*8/360;\n\n      addRow('Flour','100%',f);\n      addRow('Whole milk',pct(h*100),f*h);\n      addRow('Butter',pct(28/360*100),butter);\n      addRow('Sugar',pct(25/360*100),sugar);\n      addRow('Salt',pct(8/360*100),salt);\n      addRow(names[type],pct(yp),f*y);\n\n      total=rawDough=f+f*h+butter+sugar+salt+f*y;\n      setYield(rawDough,'1 sandwich loaf',.12);\n      $('#foot').textContent=`${fmt(f)} g flour basis // white sandwich loaf`;\n''',
    '''    } else if (key === 'sandwich') {\n      const f=read('flour',r.flour,100,5000);\n      const h=read('hyd',r.hyd,40,100)/100;\n      const yp=read('yeastPct',r.yeastPct[type],.001,15), y=yp/100;\n      const butter=f*.07, sugar=f*.05, salt=f*.02;\n\n      addRow('Strong white bread flour','100%',f);\n      addRow('Whole milk',pct(h*100),f*h);\n      addRow(names[type],pct(yp),f*y);\n      addRow('Fine salt','2%',salt);\n      addRow('Sugar / honey','5%',sugar);\n      addRow('Softened butter','7%',butter);\n\n      total=rawDough=f+f*h+f*y+salt+sugar+butter;\n      setYield(rawDough,'1 × 900 g / 2 lb tin',.12);\n      $('#foot').textContent=`${fmt(f)} g flour basis // white sandwich loaf`;\n''',
    'white loaf calculation')

saved_functions = r'''  function loadSavedStore() {
    try {
      const parsed = JSON.parse(localStorage.getItem(SAVE_KEY) || '{}');
      return parsed && typeof parsed === 'object' ? parsed : {};
    } catch(e) { return {}; }
  }

  function writeSavedStore(store) {
    try { localStorage.setItem(SAVE_KEY, JSON.stringify(store)); return true; }
    catch(e) { $('#status').textContent='Saving unavailable'; return false; }
  }

  function captureCurrentSettings() {
    const ids=['balls','weight','flour','hyd','rolls','type','salt','starter','starterHyd','yeastCalc','yeastPct','fermentHours','fermentTemp','oil'];
    const values={};
    ids.forEach(id=>{ const el=$('#'+id); if(el) values[id]=el.value; });
    if($('#oilOn')) values.oilOn=$('#oilOn').checked;
    return values;
  }

  function defaultSavedName() {
    const breadName=$('#bread').selectedOptions[0].textContent;
    if($('#bread').value==='pizza') return `${breadName} ${fmt(read('hyd',recipe().hyd,40,100))}%`;
    if($('#bread').value==='cinnamon') return `${breadName} × ${Math.round(read('rolls',recipe().rolls,1,50))}`;
    if($('#flour')) return `${breadName} ${fmt(read('flour',recipe().flour,100,5000))}g`;
    return breadName;
  }

  function saveCurrentRecipe() {
    calculate();
    const name=window.prompt('Recipe name',defaultSavedName());
    if(!name||!name.trim()) return;
    const key=$('#bread').value,store=loadSavedStore(),list=Array.isArray(store[key])?store[key]:[],cleanName=name.trim();
    const entry={id:`${Date.now()}-${Math.random().toString(36).slice(2,8)}`,name:cleanName,bread:key,values:captureCurrentSettings(),advancedOpen:$('#advancedDetails').open,savedAt:Date.now()};
    const existing=list.findIndex(item=>item.name.toLowerCase()===cleanName.toLowerCase());
    if(existing>=0){entry.id=list[existing].id;list[existing]=entry;}else{list.unshift(entry);}
    store[key]=list;
    if(writeSavedStore(store)){
      renderSavedRecipes();$('#savedDetails').open=true;
      $('#status').textContent=existing>=0?'Saved recipe updated':'Recipe saved';
      window.setTimeout(()=>$('#status').textContent='',1600);
    }
  }

  function applySavedRecipe(entry) {
    if(!entry||!recipes[entry.bread]) return;
    $('#bread').value=entry.bread;renderInputs();
    if(entry.values?.type&&$('#type')) $('#type').value=entry.values.type;
    renderAdvanced();
    Object.entries(entry.values||{}).forEach(([id,value])=>{if(id==='oilOn'||id==='type')return;const el=$('#'+id);if(el)el.value=value;});
    if($('#oilOn')){$('#oilOn').checked=!!entry.values?.oilOn;$('#oilField')?.classList.toggle('hidden',!$('#oilOn').checked);}
    if($('#yeastCalc')){$('#yeastCalc').value=entry.values?.yeastCalc||'recipe';$('#fermentFields')?.classList.toggle('hidden',$('#yeastCalc').value!=='ferment');}
    $('#advancedDetails').open=!!entry.advancedOpen;$('#method').open=false;calculate();renderSavedRecipes();
    $('#status').textContent='Recipe loaded';window.setTimeout(()=>$('#status').textContent='',1400);
  }

  function deleteSavedRecipe(id) {
    const key=$('#bread').value,store=loadSavedStore(),list=Array.isArray(store[key])?store[key]:[],item=list.find(x=>x.id===id);
    if(!item||!window.confirm(`Delete “${item.name}”?`)) return;
    store[key]=list.filter(x=>x.id!==id);writeSavedStore(store);renderSavedRecipes();
    $('#status').textContent='Saved recipe deleted';window.setTimeout(()=>$('#status').textContent='',1400);
  }

  function renderSavedRecipes() {
    const key=$('#bread').value,store=loadSavedStore(),list=Array.isArray(store[key])?store[key]:[],wrap=$('#savedList');
    if(!wrap)return;
    if(!list.length){wrap.innerHTML='<div class="saved-empty">No saved recipes for this bread type.</div>';return;}
    wrap.innerHTML='';
    list.sort((a,b)=>(b.savedAt||0)-(a.savedAt||0)).forEach(item=>{
      const row=document.createElement('div');row.className='saved-row';
      const name=document.createElement('div');name.className='saved-name';name.textContent=item.name;
      const load=document.createElement('button');load.className='saved-btn';load.type='button';load.textContent='Load';load.addEventListener('click',()=>applySavedRecipe(item));
      const del=document.createElement('button');del.className='saved-btn delete';del.type='button';del.textContent='Delete';del.addEventListener('click',()=>deleteSavedRecipe(item.id));
      row.append(name,load,del);wrap.appendChild(row);
    });
  }

'''
replace_once('  function buildCopyText() {\n', saved_functions + '  function buildCopyText() {\n', 'saved recipe functions')
replace_once("    renderAdvanced();\n    calculate();\n  }\n\n  function renderMethod() {", "    renderAdvanced();\n    calculate();\n    renderSavedRecipes();\n  }\n\n  function renderMethod() {", 'saved recipe refresh')
replace_once("  $('#copyRecipe').addEventListener('click', copyRecipe);\n\n  // Extra insurance", "  $('#copyRecipe').addEventListener('click', copyRecipe);\n  $('#saveRecipe').addEventListener('click', saveCurrentRecipe);\n\n  // Extra insurance", 'save listener')

p.write_text(s, encoding='utf-8')

sw = Path('sw.js')
sw.write_text(sw.read_text(encoding='utf-8').replace('dough-calculator-v3','dough-calculator-v4',1), encoding='utf-8')

script = re.search(r'<script>\s*(.*?)\s*</script>', s, re.S).group(1)
Path('/tmp/calculator.js').write_text(script, encoding='utf-8')
