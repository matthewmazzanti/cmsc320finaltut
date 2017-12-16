import pronouncing
import string
from collections import defaultdict, Counter
import re
import itertools as it
from functools import reduce

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def load_phones():
    phones = defaultdict(lambda: set([]))
    with open('cmudict-0.7b.phones','r') as f:
        for line in f:
            split = line.split()
            phones[split[1]].add(split[0])

    vowels = set([])
    for phone in phones['vowel']:
        vowels.add(phone)
        for i in range(0,2):
            vowels.add(phone + str(i))
    phones['vowel'] = vowels
    
    return phones

def flt(lst):
    return list(it.chain.from_iterable(lst))

def flt2(lst):
    for _ in range(0,2):
        lst = flt(lst) 

    return lst

def to_int_keys_best(l):
    """
    l: iterable of keys
    returns: a list with integer keys
    """
    seen = set()
    ls = []
    for e in l:
        if not e in seen:
            ls.append(e)
            seen.add(e)
    ls.sort()
    index = {v: i for i, v in enumerate(ls)}
    return [index[v] for v in l],ls

sentence = '''Look
If you had
One shot
Or one opportunity
To seize everything you ever wanted
In one moment
Would you capture
Or just let it slip?
Yo
His palms are sweaty, knees weak, arms are heavy
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
He better go capture this moment and hope it don't pass him
You better lose yourself in the music, the moment
You own it, you better never let it go
You only get one shot, do not miss your chance to blow
This opportunity comes once in a lifetime you better
[x2]
The souls escaping, through this hole that its gaping
This world is mine for the taking
Make me king, as we move toward a, new world order
A normal life is borin', but super stardom's close to post mortem
It only grows harder, only grows hotter
He blows us all over these hoes is all on him
Coast to coast shows, he's known as the globetrotter
Lonely roads, God only knows, he's grown farther from home, he's no father
He goes home and barely knows his own daughter
But hold your nose 'cause here goes the cold water
His hoes don't want him no mo, he's cold product
They moved on to the next schmo who flows, he nose dove and sold nada
So the soap opera is told and unfolds, I suppose it's old partna, but the beat goes on
Da da dumb da dumb da da
You better lose yourself in the music, the moment
You own it, you better never let it go
You only get one shot, do not miss your chance to blow
This opportunity comes once in a lifetime you better
[x2]
No more games, I'm a change what you call rage
Tear this motherfuckin' roof off like two dogs caged
I was playin' in the beginnin', the mood all changed
I been chewed up and spit out and booed off stage
But I kept rhymin' and stepwritin' the next cipher
Best believe somebody's payin' the pied piper
All the pain inside amplified by the
Fact that I can't get by with my nine to
Five and I can't provide the right type of
Life for my family 'cause man, these God damn food stamps don't buy diapers
And its no movie, there's no Mekhi Phifer
This is my life and these times are so hard
And it's getting even harder tryin' to feed and water my seed, plus
See dishonor caught up between bein' a father and a prima-donna
Baby mama drama screamin' on and too much
For me to want to say in one spot, another jam or not
Has gotten me to the point, I'm like a snail I've got
To formulate a plot fore I end up in jail or shot
Success is my only motherfuckin' option, failures not
Mom, I love you, but this trail has got to go, I cannot grow old in Salem's lot
So here I go is my shot
Feet fail me not 'cause maybe the only opportunity that I got
You better lose yourself in the music, the moment
You own it, you better never let it go
You only get one shot, do not miss your chance to blow
This opportunity comes once in a lifetime you better
[x2]
You can do anything you set your mind to, man
'''

class lyrics():
    reg = [(re.compile('in\''), 'ing'),
           (re.compile('\[.*\]'),''),
           (re.compile('[\n]+'),'\n'),
           (re.compile('[^a-z\' \n]'), '')]

    phones = load_phones()

    def __init__(this, lyrics):
        this.dirty = lyrics

        # Clean up the lyrics, remove capitals and punctuation
        this.clean = this.dirty.lower()
        for ex,replace in this.reg:
            this.clean = ex.sub(replace,this.clean)
        
        print(this.clean)
        this.clean = '\n'.join(f7(this.clean.split('\n')))

        # Set of unique words
        this.set = set(this.clean.split())
      
        # get unique pronunciations per word
        prons = {}
        for word in this.set:
            word_phones = list(map(lambda x: x.split(), pronouncing.phones_for_word(word)))
            word_vowels = []
            for phone in word_phones:
                word_vowels.append([x for x in phone if x in this.phones['vowel']])
            
            prons[word] = word_vowels
       
        cts = Counter(flt2(list(prons.values())))
       
        for word in this.set:
            prons[word] = this.best(cts,prons[word])
        
        # save pronunciation dictionary
        this.prons = prons

        # generate pronuncations for each word in each line
        lines = this.clean.split('\n')
        lines = list(map(lambda x: x.split(), lines))
        this.lines = lines
        lines_pron = []
        for line in lines:
            word_pron = []
            for word in line:
                word_pron.append(this.prons[word])
            lines_pron.append(word_pron)

        this.lines_pron = lines_pron
        
        print(this.lines_pron)

        lookup = []
        phones = []
        word_count = 0
        for ln_idx, line in enumerate(this.lines_pron):
            for wd_idx, word in enumerate(line):
                for phone in word:
                    lookup.append((ln_idx,wd_idx))
                    phones.append(phone)
                    
                word_count += 1

        keys,ls = to_int_keys_best(phones)
        char_keys = ''.join(list(map(lambda x: chr(97+x),keys)))
        print(char_keys)

        window = 5
        patterns = set([])
        for i in range(0, len(this.lines_pron) - window):
            lines = flt2(this.lines_pron[i:i+window])
            wind_patterns = defaultdict(lambda: 0)

            for j in range(2, 10):
                for k in range(0, len(lines) - j + 1):
                    wind_patterns[tuple(lines[k:k + j])] += 1

            patts = list(filter(lambda x: x[1] > 1, wind_patterns.items()))
            patterns.update([x[0] for x in patts])


        for patt in patterns:
            group = []
            for s in this.kmp(phones, list(patt)):
                words = []
                for i in range(s, s+len(patt)):
                    words.append(lookup[i])
               
                words = f7(words)
                
                words2 = []
                for x,y in words:
                    words2.append(this.lines[x][y])
                group.append(words2)

            print(group)

    # provides best pronunciation given list of pronunciations
    def best(this, cts, prons):
        if len(prons) > 1:
            scores = []
            for pron in prons:
                score = 0
                for phone in pron:
                    score += cts[phone]
                scores.append(score)
            
            return prons[scores.index(max(scores))]
        elif len(prons) == 1:
            return prons[0]
        else:
            return []


    def find_sublist(sub, bigger):
        if not bigger:
            return -1
        if not sub:
            return 0
        first, rest = sub[0], sub[1:]
        pos = 0
        try:
            while True:
                pos = bigger.index(first, pos) + 1
                if not rest or bigger[pos:pos+len(rest)] == rest:
                    return pos
        except ValueError:
            return -1


    def kmp(this, text, pattern):

        '''Yields all starting positions of copies of the pattern in the text.
    Calling conventions are similar to string.find, but its arguments can be
    lists or iterators, not just strings, it returns all matches, not just
    the first one, and it does not need the whole text in memory at once.
    Whenever it yields, it will have read the text exactly up to and including
    the match that caused the yield.'''

        # allow indexing into pattern and protect against change during yield
        pattern = list(pattern)

        # build table of shift amounts
        shifts = [1] * (len(pattern) + 1)
        shift = 1
        for pos in range(len(pattern)):
            while shift <= pos and pattern[pos] != pattern[pos-shift]:
                shift += shifts[pos-shift]
            shifts[pos+1] = shift

        # do the actual search
        startPos = 0
        matchLen = 0
        for c in text:
            while matchLen == len(pattern) or \
                  matchLen >= 0 and pattern[matchLen] != c:
                startPos += shifts[matchLen]
                matchLen -= shifts[matchLen]
            matchLen += 1
            if matchLen == len(pattern):
                yield startPos


lyr = lyrics(sentence)
