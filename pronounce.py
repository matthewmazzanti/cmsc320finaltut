import pronouncing
import string
from collections import defaultdict
import re



sentence = '''His palms are sweaty, knees weak, arms are heavy
There's vomit on his sweater already, mom's spaghetti
He's nervous, but on the surface he looks calm and ready
To drop bombs, but he keeps on forgettin'
What he wrote down, the whole crowd goes so loud
He opens his mouth, but the words won't come out
He's chokin', how, everybody's jokin' now
The clocks run out, times up, over, blaow!
Snap back to reality, oh there goes gravity
Oh, there goes Rabbit, he choked
He's so mad, but he won't give up that easy? No
He won't have it, he knows his whole back city's ropes
It don't matter, he's dope, he knows that, but he's broke
He's so stacked that he knows, when he goes back to his mobile home, that's when its
Back to the lab again yo, this whole rhapsody
He better go capture this moment and hope it don't pass him'''

sentence = sentence.lower()


reg = re.compile('in\'')
sentence = reg.sub('ing',sentence)
reg2 = re.compile('[^a-z\' \n]')
sentence = reg2.sub('',sentence)
print(sentence)
lyrics = sentence.split('\n')
asdf = []
for line in lyrics:
    asdf.append(line.split())
lyrics = asdf

for line in lyrics:
    print(line)

vowels = set(['AA','AA0','AA1','AA2','AE','AE0','AE1','AE2','AH','AH0','AH1','AH2','AO','AO0','AO1','AO2','AW','AW0','AW1','AW2','AY','AY0','AY1','AY2','EH','EH0','EH1','EH2','ER','ER0','ER1','ER2','EY','EY0','EY1','EY2','IH','IH0','IH1','IH2','IY','IY0','IY1','IY2','OW','OW0','OW1','OW2','OY','OY0','OY1','OY2','UH','UH0','UH1','UH2','UW','UW0','UW1','UW2'])
arr = []
for line in asdf:
    arr2 = []
    for word in line:
        phones = pronouncing.phones_for_word(word)
        arr3 = []
        for phone in phones:
            phone = phone.split()
            arr3.append([x for x in phone if x in vowels])

        arr2.append(arr3)
    arr.append(arr2)

for line in arr:
    print(line)


pron_dict = defaultdict(lambda: 0)
for line in arr:
    for word in line:
        for phone in word:
            for vowel in phone:
                pron_dict[vowel] += 1

print(pron_dict)

def score(word):
    if len(word) > 1:
        scores = []
        for phone in word:
            score = 0
            for vowel in phone:
                score += pron_dict[vowel]

            scores.append(score)
       
        return word[scores.index(max(scores))]
    elif len(word) == 1:
        return word[0]
    else:
        return word

asdf2 = []
for line in arr:
    asdf21 = []
    for word in line:
        asdf21.append(score(word))

    asdf2.append(asdf21)

for idx in range(0,len(asdf2)):
    print(lyrics[idx])
    print(asdf2[idx])

pron_dict2 = defaultdict(lambda: [])
for i,line in enumerate(asdf2):
    for j,word in enumerate(line):
        for vowel in word:
            pron_dict2[vowel].append((i,j))

for key in pron_dict2.keys():
    print("\n")
    print(key)

    words = set([])
    for i,j in pron_dict2[key]:
        words.add(lyrics[i][j])

    print(words)

'''
for idx, prons in enumerate(arr):
    for pron in prons:
        for phrase in pron.split():
            pron_dict[phrase].append(idx)

keys = [x for x in pron_dict.keys() if x in vowels]
print(keys)
for key in keys:
    print('\n',key)
    for idx in pron_dict[key]:
        print(sent_arr[idx])
'''
