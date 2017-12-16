import pronouncing
import string
from collections import Counter
import repeats as rpts
from helper import *

phones = load_phones()

def pron_dict(unique):
    prons = {}
    for word in unique:
        word_phones = map(lambda x: x.split(), pronouncing.phones_for_word(word))
        word_vowels = []
        for phone in word_phones:
            word_vowels.append([x for x in phone if x in phones['vowel']])
        
        prons[word] = word_vowels
    
    cts = Counter(flt(flt(list(prons.values()))))
    
    for word in unique:
        prons[word] = best(cts,prons[word])

    return prons

# provides best pronunciation given list of pronunciation counts
def best(cts, prons):
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


def similarity(set1, set2):
    return (len(set1 - set2) + len(set2 - set1))/(len(set1)+len(set2))



def lyrics_analysis(dirty):
    if type(dirty) is not str:
        return -1
    # Clean up the lyrics, remove capitals and punctuation
    clean = clean_text(dirty)  
    words = clean.split()

    if len(words) < 10:
        return -1
    # Set of unique words
    word_bag = Counter(words) 
    # get unique pronunciations per word
    prons = pron_dict(word_bag.keys())
    

    # Get pronunciation of each word in song
    words_pron = []
    for word in words:
        words_pron.append(prons[word])
    
    # Make lookup tuples of (line, word) to look 
    lookup = []
    phones = []
    for wd_idx, word in enumerate(words_pron):
        for phone in word:
            lookup.append(wd_idx)
            phones.append(phone)

    # Convert phones into character sequence for matching
    keys,ls = to_int_keys_best(phones)
    char_keys = ''.join(list(map(lambda x: chr(97+x),keys)))

    # Find supermaximal repeats
    repeats = rpts.supermax(char_keys,1)
    
    # From repeat locations find words that were rhymed
    rhymes = []
    for locs, length, seq in repeats:
        rhyme = []
        for loc in locs:
            phrase = []
            for i in range(0,length):
                phrase.append(lookup[loc + i])
            phrase = rem_dup(phrase)
            rhyme.append(list(map(lambda x: words[x], phrase)))

        rhymes.append((rhyme,locs,length,seq))

    # Find unique rhymes
    rhymes_diff = []
    for rhyme,locs,length,seq in rhymes:
        sets = []
        for group in rhyme:
            sets.append(set(group))
        
        mask = [1] * len(sets)
        for idx in it.combinations(range(0,len(sets)),2):
            if similarity(sets[idx[0]],sets[idx[1]]) < .5:
                mask[idx[1]] = 0

        rhyme_diff = list(it.compress(rhyme, mask))
        if(len(rhyme_diff) > 1):
            rhymes_diff.append((rhyme_diff,locs,length,seq))

    #print(rhymes_diff)
    
    total = 0
    max_len = 0
    for _,locs,length,_ in rhymes_diff:
        total += length
        if max_len < length:
            max_len = length
    
    denom = len(rhymes_diff)
    if(denom > 0):
        mean = total/len(rhymes_diff)
    else:
        mean = -1

    return {'mean':mean,
            'num_rhymes':denom,
            'word_count':len(words),
            'unique_word_count':len(word_bag.keys())}
        

sentence1 = '''Look
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

sentence2 = '''
Yo, yo, yo, y'all can't stand right here
In his right hand was your man's worst nightmare
Loud enough to burst his right eardrum close-range
The game is not only dangerous, but it's most strange
I sell rhymes like dimes
The one who mostly keep cash but brag about the broker times
Joking rhymes, like the "Is you just happy to see me?" trick
Classical slapstick rappers need Chapstick
A lot of 'em sound like they in a talent show
So I give 'em something to remember like the Alamo
Tally-ho! A high Joker like a Spades game
Came back from five years laying and stayed the same
I'm saying - electromagnetic field it blocks all logic, Spock
And G-Shocks her biological clock
When I hit it, slit it to the shitter, thought I killed her goose
Her Power U was pure Brita water, filtered juice
Keep a pen like a fiend keep a pipe with him
Gentleman who lent a pen to a friend who write with him
Never seen the shit again but he's still my dunny
The only thing that come between us is krill and money
I sell rhymes like dimes
The one who mostly keep cash but brag about the broke times
Better rhymes make for better songs, it matters not
If you got a lot of what it takes just to get along
Surrender now or suffer serious setbacks
Got get-back, connects wet-back, get stacks
Even if you gots to get jet-black, head to toe
To get the dough, battle for bottles of Mo' or 'dro
This fly flow take practice like Tae Bo with Billy Blanks
"Oh, you're too kind!" "Really? Thanks!"
To the gone and lost forever like "Oh My Darling Clementine"
He hold his heart when he telling rhyme
When it's his time, I hope his soul go to Heaven
He nasty like the old time Old No. 7
You still taste it when you chase it with the Coca-Cola
Make 'em wish they could erase it out the Motorola
I told her - no credit for a bag
If you want what they got, then go get it, it's all gak
Only in America could you find a way to earn a healthy buck
And still keep your attitude on self-destruct
I sell rhymes like dimes
The one who mostly keep cash but brag about the broker times
Joking rhymes, like the "Is you just happy to see me?" trick
Classical slapstick rappers need Chapstick
A lot of 'em sound like they in a talent show
So I give 'em something to remember like the Alamo
Tally-ho! A high Joker like a Spades game
Came back from five years laying and stayed the same
I'm saying - electromagnetic field it blocks all logic, Spock
And G-Shocks her biological clock
When I hit it, slit it to the shitter, thought I killed her goose
Her Power U was pure Brita water, filtered juice
Keep a pen like a fiend keep a pipe with him
Gentleman who lent a pen to a friend who write with him
Never seen the shit again but he's still my dunny
The only thing that come between us is krill and money
I sell rhymes like dimes
The one who mostly keep cash but brag about the broke times
'''

sentence3 = '''
So, you've been to school
For a year or two
And you know you've seen it all
In daddy's car
Thinking you'll go far
Back east your type don't crawl
Playing ethnicky jazz
To parade your snazz
On your five-grand stereo
Braggin' that you know
How the niggers feel cold
And the slum's got so much soul
It's time to taste what you most fear
Right Guard will not help you here
Brace yourself, my dear
Brace yourself, my dear
It's a holiday in Cambodia
It's tough, kid, but it's life
It's a holiday in Cambodia
Don't forget to pack a wife
You're a star-belly snitch
You suck like a leech
You want everyone to act like you
Kiss ass while you bitch
So you can get rich
While your boss gets richer off you
Well, you'll work harder
With a gun in your back
For a bowl of rice a day
Slave for soldiers
Till you starve
Then your head is skewered on a stake
Now you can go where the people are one
Now you can go where they get things done
What you need, my son...
What you need, my son...
Is a holiday in Cambodia
Where people are dressed in black
A holiday in Cambodia
Where you'll kiss ass or crack
Pol Pot, Pol Pot, Pol Pot, Pol Pot
It's a holiday in Cambodia
Where you'll do what you're told
It's a holiday in Cambodia
Where the slums got so much soul
Pol Pot
'''


lyr = lyrics_analysis(sentence1)
lyr = lyrics_analysis(sentence2)
lyr = lyrics_analysis(sentence3)
