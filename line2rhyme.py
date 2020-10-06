import numpy as np
import random
import pandas as pd
import re
from sklearn.neighbors import NearestNeighbors
from russtress import Accent
# from making_matrix import get_meter, chunks, clean_line

accent = Accent()

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
        for x in chunks(syllables, 3):
            if x == meter:
                meterline[n] += 1
    meterline[:3] /= len(list(chunks(syllables, 3)))+1
    for n, meter in enumerate(meters2.values()):
        for x in chunks(syllables, 2):
            if x == meter:
                meterline[n+3] += 1
    meterline[3:] /= len(list(chunks(syllables, 2))) + 1
    return meterline

poems_matrix = pd.read_csv('poems_matrix.csv',encoding='utf-8')

with open('twograms0.txt', encoding='utf-8') as f:
    twograms0 = f.read()
twograms0 = twograms0.splitlines()
with open('twograms1.txt', encoding='utf-8') as f:
    twograms1 = f.read()
twograms1 = twograms1.splitlines()
with open('poems.txt', encoding='utf-8') as f:
    corpus_poems = f.read()
corpus_poems = corpus_poems.splitlines()


def line2vector(new_line):
    vector = np.zeros(80)
    new_line = clean_line(new_line)
    if new_line == '':
        return vector
    vowels = re.findall(r"[ёуеыаоэяию]'?",accent.put_stress(new_line))
    last = new_line.split()[-1]
    if last == '':
        last = new_line.split()[-2]
    twogram = last[-2:].lower()
    metre = get_metre(vowels)

    vector[0] = len(vowels)
    vector[1:6] = metre
    if twogram[0] in twograms0:
        vector[twograms0.index(twogram[0])+6] = 1
    if twogram[1] in twograms1:
        vector[twograms1.index(twogram[1]) + len(twograms0) + 6] = 1
    return vector


def chose_rhyme(matrix, vector):
    nn = NearestNeighbors(metric='euclidean')
    nn.fit(matrix)
    r = nn.kneighbors(vector.reshape(1, -1), 1)
    neighbors = nn.radius_neighbors(vector.reshape(1, -1), r[0][0][0])[1][0]
    if neighbors.shape == (0,):
        return r[1][0][0]
    else:
        return random.choice(neighbors)


def clean_ending_line(line):
    line = re.sub(r'[-,.:;_]+$',r'', line)
    return line


def line2rhyme(line):
    vector = line2vector(line)
    return clean_ending_line(corpus_poems[chose_rhyme(poems_matrix, vector)])