from minisom import MiniSom

import sklearn.cluster as cl
import numpy as np
import matplotlib.pyplot as plt

import json
from pprint import pprint


test = json.load(open('analysis.json'))
segments = []
times = []
for segment in test['segments']:
    row = []
    #row += segment['pitches']
    row += segment['timbre']

    times.append(segment['start'])
    segments.append(row)

data = np.array(segments)

data = np.apply_along_axis(lambda x: x/np.linalg.norm(x), 1, data)
'''
x = 20
y = 20
som = MiniSom(x, y, 12, sigma=.3, learning_rate=0.1)
som.random_weights_init(data)
print("Training...")
som.train_batch(data, 1000)  # random training
print("\n...ready!")
'''

time_dict = {6:'Intro',21:'Verse',40:'Chorus',53:'Verse',85:'Chorus',101:'Solo',120:'Chorus',135:'Outro'}
time_dict = {6:0,21:1,40:2,53:1,85:2,101:3,120:2,135:0}
struct = []
for time in times:
    for edge in time_dict.keys():
        if time < edge:
            struct.append(time_dict[edge])
            break

#struct_dict = {'Intro':0,'Verse':1,'Chorus':2,'Solo':3,'Outro':0}
#t = list(map(lambda x: struct_dict[x],struct))
print(data)

'''
# use different colors and markers for each label
markers = ['o', 's', 'D','+']
colors = ['r', 'g', 'b','c']
for cnt, xx in enumerate(data):
    w = som.winner(xx)  # getting the winner
    # palce a marker on the winning position for the sample xx
    plt.plot(w[0]+.5, w[1]+.5, markers[t[cnt]], markerfacecolor='None',
             markeredgecolor=colors[t[cnt]], markersize=12, markeredgewidth=2)
plt.axis([0, x, 0, y])
plt.show()
'''
print(cl.SpectralClustering(4,n_init=20,n_neighbors=4).fit(data).fit_predict(data))
print(np.array(struct))
