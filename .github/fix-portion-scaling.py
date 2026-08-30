from pathlib import Path

p=Path('index.html')
s=p.read_text()

s=s.replace("else qty.value=Math.round((read('flour',recipe().flour,25,5000)/recipe().flourPer)*10)/10;", "else qty.value=Math.round((read('flour',recipe().flour,1,5000)/recipe().flourPer)*10)/10;", 1)
s=s.replace("h += stepField('flour','Flour basis',r.flour,'g',12.5,25,5000);", "h += stepField('flour','Flour basis',r.flour,'g',r.flourPer,1,5000);", 1)
s=s.replace("const f=read('flour',r.flour,25,5000);", "const f=read('flour',r.flour,1,5000);", 3)

p.write_text(s)
