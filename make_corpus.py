import re
import requests

corpus_poems = []
for i, book in enumerate(['text_0050.shtml','text_0052.shtml','text_0054.shtml']):
    result = requests.get(f'http://az.lib.ru/b/blok_a_a/{book}')
    html = result.text
    if i == 0:
        poems = re.findall(r'<A NAME=.*?>(.*?)<A', html, flags=re.DOTALL | re.IGNORECASE)
    else:
        poems = re.findall(r'<A NAME=.*?></A>(.*?)<A', html, flags=re.DOTALL | re.IGNORECASE)
    lines = []
    for poem in poems:
        for line in poem.split('\r\n'):
            line = line.strip()
            line = line.replace('<I>','').replace('</I>','')
            if (line != '') and (line != '* * *') and ('<' not in line) and (re.match(r'[a-zа-я]',line,flags=re.IGNORECASE) != None) and (line.isupper() != True):
                lines.append(line)
    corpus_poems.extend(lines)

with open('poems.txt', 'w', encoding='utf-8') as f:
    for line in corpus_poems:
        f.write(line+'\n')