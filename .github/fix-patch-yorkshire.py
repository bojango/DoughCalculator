from pathlib import Path

p=Path('.github/patch-yorkshire.py')
s=p.read_text()
start=s.index('# Calculation branch and optional yeast selector handling.')
end=s.index('# Modified-state logic.', start)
fixed=r'''# Calculation branch and optional yeast selector handling.
s = s.replace("    const type = $('#type').value;\n", "    const type = $('#type')?.value || r.def || null;\n", 1)
calc_old = """    let rawDough = 0;

    if (key === 'pizza') {"""
calc_new = """    let rawDough = 0;
    let totalLabel = 'TOTAL';

    if (key === 'yorkshire') {
      syncYorkshireBasisUI();
      const f=read('flour',r.flour,25,5000);
      const q=read('yorkQty',r.qty,.1,100);
      const milk=f*r.milkPct/100;
      const eggMass=f*r.eggPct/100;
      const oilMl=q*r.oilMlPer;
      addRow('Plain flour','100%',f);
      addRow('Whole milk',pct(r.milkPct),milk,'','ml');
      addRow('Large egg',pct(r.eggPct),eggMass,eggNote(eggMass));
      addRow('Sunflower / vegetable oil','—',oilMl,'for the tin','ml');
      rawDough=total=f+milk+eggMass;
      totalLabel='BATTER';
      $('#yieldLine').innerHTML=`<span>~${fmt(q)} standard muffin-size puddings</span><span>Batter ~${fmt(rawDough)} g</span>`;
      lastResult.yield=`~${fmt(q)} standard muffin-size Yorkshire puddings | Batter ~${fmt(rawDough)} g`;
      $('#foot').textContent=`~${fmt(q)} Yorkshire puddings // standard muffin tin`;

    } else if (key === 'pizza') {"""
assert calc_old in s, 'calculation branch anchor missing'
s = s.replace(calc_old, calc_new, 1)
s = s.replace("    $('#total').textContent=`TOTAL / ${fmt(total)} G`;\n", "    $('#total').textContent=`${totalLabel} / ${fmt(total)} G`;\n", 1)

'''
s=s[:start]+fixed+s[end:]
p.write_text(s)
