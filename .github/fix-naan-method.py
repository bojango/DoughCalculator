from pathlib import Path

p=Path('index.html')
s=p.read_text()
old="      steps.push('Combine flour, remaining sugar, salt and baking powder. Add yogurt, melted butter or ghee, nigella seeds and the water/yeast mixture; bring together into a very soft dough.');"
new="      steps.push(`Combine flour, remaining sugar, salt and baking powder. Add yogurt, melted butter or ghee, nigella seeds and ${type === 'idy' ? 'the warm water' : 'the yeast-water mixture'}; bring together into a very soft dough.`);"
if old in s:
    s=s.replace(old,new,1)
p.write_text(s)
