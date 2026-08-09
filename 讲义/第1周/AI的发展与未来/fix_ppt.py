import re
with open('generate_ppt_v2.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix: insert False before PP_ALIGN when PP_ALIGN is in bold parameter position
code = re.sub(r'(Pt\(\d+\)),\s*(PP_ALIGN)', r'\1, False, \2', code)

with open('generate_ppt_v2.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('Fixed')
