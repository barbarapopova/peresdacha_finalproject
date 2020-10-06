from russtress import Accent
import pandas as pd
import numpy as np

accent = Accent()

with open('poems.txt', encoding='utf-8') as f:
    corpus_poems = f.read()
corpus_poems = corpus_poems.splitlines()

meters3 = {'amphibrachys':[0,1,0],
'anapaistos':[0,0,1],
'daktylos':[1,0,0]}
meters2 = {'choreios':[1,0],
'iambos':[0,1]}

def clean_line(line):
    line = re.sub(r'[^-\w\s]', r'', line.lower())
    return re.sub(r'(\W)-|-(\W)', r'\1\2', line)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_metre(vowels):
    syllables = [0 if "'" not in vowel else 1 for vowel in vowels]
    meterline = np.zeros(5)
    for n, meter in enumerate(meters3.values()):
        for i, x in enumerate(chunks(syllables, 3)):
            if x == meter:
                meterline[n] += 1
    meterline[:3] /= i+1
    for n, meter in enumerate(meters2.values()):
        for i, x in enumerate(chunks(syllables, 2)):
            if x == meter:
                meterline[n+3] += 1
    meterline[3:] /= i + 1
    return meterline

lines_json = []
for line in corpus_poems:
    line = clean_line(line)
    vowels = re.findall(r"[ёуеыаоэяию]'?",accent.put_stress(line))
    last = line.split()[-1]
    if last == '':
        last = line.split()[-2]
    twogram = last[-2:].lower()
    metre = get_metre(vowels)
    lines_json.append([metre,len(vowels),twogram[0],twogram[-1]])

df = pd.DataFrame(lines_json, columns=['metre','n_syll','two_gram_0','two_gram_1'])
df[['amphibrachys','anapaistos','daktylos','choreios','iambos']] = pd.DataFrame(df.metre.to_list())
df.drop(columns='metre',inplace=True)

twograms0 = sorted(df.two_gram_0.unique().tolist())
twograms1 = sorted(df.two_gram_1.unique().tolist())

with open('twograms0.txt', 'w', encoding='utf-8') as f:
    for twogram0 in twograms0:
        f.write(twogram0+'\n')
with open('twograms1.txt', 'w', encoding='utf-8') as f:
    for twogram1 in twograms1:
        f.write(twogram1+'\n')

df_w_dummies = pd.concat([df, pd.get_dummies(df.two_gram_0, prefix='2gram0')], axis=1).drop(['two_gram_0'],axis=1)
df_w_dummies = pd.concat([df_w_dummies, pd.get_dummies(df.two_gram_1, prefix='2gram1')], axis=1).drop(['two_gram_1'],axis=1)

df_w_dummies.to_csv('poems_matrix.csv', index=False)