import math
import random
from collections import defaultdict


# 划分数据集
def data_split(full_list, seed, ratio, shuffle=False):
    n_total = len(full_list)
    offset = int(n_total * ratio)
    if n_total == 0 or offset < 1:
        return [], full_list
    if shuffle:
        random.seed(seed)
        random.shuffle(full_list)
    sublist_1 = full_list[:offset]
    sublist_2 = full_list[offset:]
    return sublist_1, sublist_2

# 获取词的标签
def get_label(word):
    if len(word) == 1:
        return 'S'
    else:
        return 'B' + 'M' * (len(word) - 2) + 'E'

# 获取词的特征
def get_features(i, sentence):
    features = [sentence[i]]
    if i > 0:
        features.append(sentence[i-1]) # w_{i-1}
        features.append(sentence[i-1:i+1]) # w_{i-1}, w_i
    else:
        features.append('0')
        features.append('0')

    if i < len(sentence) - 1:
        features.append(sentence[i+1]) # w_{i+1}
        features.append(sentence[i:i+2]) # w_i, w_{i+1}
    else:
        features.append('0')
        features.append('0')

    if i > 1:
        features.append(sentence[i-2]) # w_{i-2}
        features.append(sentence[i-2:i+1]) # w_{i-2}, w_{i-1}, w_i
    else:
        features.append('0')
        features.append('0')

    if i < len(sentence) - 2:
        features.append(sentence[i+2]) # w_{i+2}
        features.append(sentence[i:i+3]) # w_i, w_{i+1}, w_{i+2}
    else:
        features.append('0')
        features.append('0')

    if i > 1 and i < len(sentence) - 2:
        features.append(sentence[i-2:i+3]) # w_{i-2}, w_{i-1}, w_i, w_{i+1}, w_{i+2}
    else:
        features.append('0')

    return(features)

file = list(open('sentences.txt', 'r', encoding="utf-8")) # 19056行
train, test = data_split(list(file), seed=123, ratio=0.7, shuffle=True) # 分割数据集

y_labels = ['S','B','M','E']
px = defaultdict(int) # 每个特征的概率
pxy = defaultdict(int) # 每个(特征,标注)的概率
pyx = defaultdict(int) # P(标注|特征)
w = defaultdict(int) # 每个特征的权重
samples = []
ep_ = defaultdict(int) # 模型特征期望

for sentence in train: # 循环每句句子
    words_list = sentence.split('  ')[:-1]
    label = '' # 获取句子的标注
    for word in words_list:
        label += get_label(word)

    sentence = ''.join(words_list)
    for i in range(len(sentence)):
        features = get_features(i, sentence)
        tmp = list(zip(features, [label[i] for _ in range(len(features))])) # (特征,标注)
        samples += tmp
        for (x, y) in tmp:
            pxy[(x,y)] += 1
            px[x] += 1

features = pxy.keys()
n_features = len(features)
n_samples = len(samples) # 样本个数

def prob(p):
    for value, key in enumerate(p):
        p[key] = value / n_samples

prob(pxy)
prob(x)

def get_pyx(x, y):
    pyx[(x,y)] = math.exp(w[(x,y)])
    z = 0
    for y1 in y_labels:
        z += math.exp(w.get((x,y1)))
    pyx[(x,y)] /= z

def get_ep_(x, y):
    ep_[(x,y)] = px[x] * pyx[(x,y)]

epochs = 100 # 训练次数
for i in range(epochs):
    for (x, y) in samples:
        get_pyx(x, y)
        get_ep_(x, y)
        w[(x,y)] += 1 / n_features * math.log(pxy[(x,y)]) - math.log(ep_[(x,y)])
    
    
        
