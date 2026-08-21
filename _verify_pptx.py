# -*- coding: utf-8 -*-
"""临时验证脚本：检查 PPTX 页数与内容，用后即删。"""
import zipfile, re, glob, os

def main():
    pattern = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           '讲义', '**', 'Excel-Agent开发文档-技术展示.pptx')
    hits = glob.glob(pattern, recursive=True)
    if not hits:
        print('PPTX NOT FOUND')
        return 1
    path = hits[0]
    print('PPTX:', path)
    z = zipfile.ZipFile(path)
    slides = [n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)]
    slides.sort()
    print('Slides:', len(slides))
    alltext = ''.join(z.read(n).decode('utf-8', 'ignore') for n in slides)
    for kw in ['Excel Agent', 'SKILL', 'pywin32', 'COM', 'MVP', 'chart.png']:
        print(f'contains {kw!r}:', kw in alltext)
    # 每页标题行抽样
    titles = []
    for n in slides:
        xml = z.read(n).decode('utf-8', 'ignore')
        m = re.findall(r'<a:t>([^<]{2,30})</a:t>', xml)
        titles.append(m[0] if m else '?')
    print('First title per slide:')
    for i, t in enumerate(titles, 1):
        print(f'  S{i}: {t}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
