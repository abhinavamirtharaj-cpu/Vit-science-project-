"""
emotion_analyzer.py
Advanced emotion detection using keyword analysis, negation handling, and sentiment scores.
"""

from textblob import TextBlob
from emotion_colors import EMOTION_COLORS, get_emotion_category
import re
from typing import List, Dict, Optional

# Negation words that flip sentiment
NEGATION_WORDS = {'not', 'no', 'never', 'neither', 'nobody', 'nothing', 'nowhere', 
                  'none', 'hardly', 'scarcely', 'barely', 'don\'t', 'doesn\'t', 
                  'didn\'t', 'won\'t', 'wouldn\'t', 'shouldn\'t', 'can\'t', 'cannot',
                  'isn\'t', 'aren\'t', 'wasn\'t', 'weren\'t', 'haven\'t', 'hasn\'t', 'hadn\'t'}

# Contextual phrase patterns (checked FIRST before keywords)
# These are multi-word expressions that have specific emotional meanings
EMOTION_PHRASES = {
    # Anger/Frustration expressions (curse words and euphemisms)
    'anger': [
        r'what the hell',
        r'what the fuck',
        r'wtf',
        r'what the fish',  # Euphemism
        r'what the heck',
        r'what the frick',
        r'are you kidding',
        r'you\'re kidding',
        r'this is bullshit',
        r'this is ridiculous',
        r'pissed off',
        r'fed up',
        r'sick of this',
        r'had enough',
        r'damn it',
        r'dammit',
        r'screw this',
        r'screw that',
        r'fuck this',
        r'fuck that',
        r'mind your words',
        r'watch your mouth',
        r'shut up',
        r'shut the fuck up',
        r'get lost',
        r'go to hell',
        r'fuck off',
        r'piss off',
        r'you\'re an? idiot',
        r'you\'re an? fool',
        r'you\'re an? moron',
        r'you\'re an? bastard',
        r'you\'re an? asshole',
        r'you\'re an? jerk',
        r'you\'re stupid',
        r'you\'re dumb',
        r'you suck',
        r'i hate you',
        r'hate you',
        r'don\'t like you',
        r'dislike you',
        r'can\'t stand you',
    ],
    
    # Frustration
    'frustration': [
        r'give me a break',
        r'for crying out loud',
        r'come on',
        r'seriously\?',
        r'not again',
        r'why me',
        r'why now',
    ],
    
    # Sarcasm (context-dependent phrases)
    'sarcasm': [
        r'oh great',
        r'just great',
        r'just perfect',
        r'wonderful',
        r'fantastic',
        r'yeah right',
        r'sure thing',
        r'obviously',
        r'oh really',
    ],
    
    # Positive expressions
    'joy': [
        r'so happy',
        r'very happy',
        r'i love',
        r'love this',
        r'love it',
        r'best day',
        r'amazing',
        r'awesome',
    ],
    
    # Gratitude
    'gratitude': [
        r'thank you',
        r'thanks',
        r'appreciate it',
        r'appreciate you',
        r'grateful',
    ],
    
    # Confusion (genuine questions, not exclamations)
    'confusion': [
        r'i don\'t understand',
        r'don\'t get it',
        r'makes no sense',
        r'not sure',
        r'unclear',
    ],
}

# Emotion keyword mappings (checked AFTER phrases) - EXPANDED TO 100+ KEYWORDS EACH
EMOTION_KEYWORDS = {
    # Positive emotions (100+ keywords each)
    'joy': ['joy', 'joyful', 'happy', 'delighted', 'cheerful', 'pleased', 'content', 'glad', 'ecstatic', 'elated',
            'overjoyed', 'thrilled', 'blissful', 'euphoric', 'radiant', 'beaming', 'glowing', 'jubilant', 'gleeful',
            'merry', 'jolly', 'bright', 'sunny', 'upbeat', 'lively', 'buoyant', 'chipper', 'peppy', 'perky',
            'animated', 'spirited', 'vivacious', 'exuberant', 'effervescent', 'bubbly', 'sparkling', 'giddy',
            'tickled', 'blessed', 'fortunate', 'lucky', 'wonderful', 'fantastic', 'amazing', 'incredible', 'awesome',
            'brilliant', 'superb', 'excellent', 'magnificent', 'marvelous', 'spectacular', 'phenomenal', 'fabulous',
            'terrific', 'stupendous', 'outstanding', 'exceptional', 'divine', 'heavenly', 'perfect', 'ideal',
            'delightful', 'lovely', 'beautiful', 'gorgeous', 'splendid', 'grand', 'glorious', 'sublime',
            'bliss', 'rapture', 'paradise', 'heaven', 'nirvana', 'utopia', 'cloud nine', 'seventh heaven',
            'walking on air', 'on top of the world', 'over the moon', 'tickled pink', 'pleased as punch'],
    
    'happiness': ['happiness', 'happy', 'happier', 'happiest', 'elated', 'blissful', 'content', 'satisfied', 'fulfilled',
                  'gratified', 'pleased', 'glad', 'cheerful', 'merry', 'joyous', 'jovial', 'gleeful', 'delighted',
                  'thrilled', 'excited', 'enthusiastic', 'upbeat', 'positive', 'optimistic', 'hopeful', 'bright',
                  'sunny', 'radiant', 'glowing', 'beaming', 'smiling', 'grinning', 'laughing', 'giggling',
                  'enjoying', 'loving', 'appreciating', 'savoring', 'relishing', 'basking', 'reveling', 'luxuriating',
                  'comfortable', 'cozy', 'warm', 'peaceful', 'serene', 'tranquil', 'calm', 'relaxed', 'easy',
                  'carefree', 'lighthearted', 'breezy', 'easygoing', 'laid back', 'chill', 'cool', 'sweet',
                  'nice', 'pleasant', 'agreeable', 'enjoyable', 'delightful', 'charming', 'lovely', 'beautiful',
                  'wonderful', 'fantastic', 'great', 'good', 'fine', 'okay', 'alright', 'well', 'better', 'best'],
    
    'love': ['love', 'adore', 'cherish', 'treasure', 'affection', 'fond', 'devoted', 'passionate', 'infatuated',
             'smitten', 'enamored', 'besotted', 'captivated', 'enchanted', 'charmed', 'attracted', 'drawn',
             'attached', 'bonded', 'connected', 'close', 'intimate', 'romantic', 'amorous', 'tender', 'gentle',
             'caring', 'loving', 'affectionate', 'warm', 'heartfelt', 'sincere', 'genuine', 'true', 'real',
             'deep', 'profound', 'intense', 'strong', 'powerful', 'overwhelming', 'all-consuming', 'obsessive',
             'crazy about', 'mad about', 'nuts about', 'wild about', 'head over heels', 'swept off feet',
             'falling for', 'crushing on', 'into', 'dig', 'fancy', 'sweet on', 'keen on', 'taken with',
             'admire', 'respect', 'appreciate', 'value', 'prize', 'esteem', 'honor', 'worship', 'idolize',
             'adulate', 'venerate', 'revere', 'devoted to', 'dedicated to', 'committed to', 'loyal to',
             'faithful to', 'true to', 'dear', 'precious', 'beloved', 'darling', 'sweetheart', 'honey'],
    
    'excitement': ['excited', 'exciting', 'thrilled', 'eager', 'pumped', 'stoked', 'hyped', 'amped', 'fired up',
                   'psyched', 'revved up', 'wound up', 'keyed up', 'worked up', 'stirred up', 'charged',
                   'energized', 'electrified', 'animated', 'stimulated', 'aroused', 'awakened', 'inspired',
                   'motivated', 'driven', 'passionate', 'enthusiastic', 'zealous', 'fervent', 'ardent',
                   'avid', 'keen', 'anxious', 'impatient', 'restless', 'antsy', 'itching', 'dying to',
                   'can\'t wait', 'counting down', 'anticipating', 'looking forward', 'expecting', 'awaiting',
                   'buzzing', 'tingling', 'jittery', 'jumpy', 'nervous', 'on edge', 'wired', 'high',
                   'exhilarated', 'thrilled', 'ecstatic', 'elated', 'euphoric', 'rapturous', 'delirious',
                   'intoxicated', 'drunk', 'giddy', 'dizzy', 'lightheaded', 'breathless', 'gasping',
                   'heart racing', 'pulse pounding', 'adrenaline', 'rush', 'thrill', 'kick', 'buzz'],
    
    'enthusiasm': ['enthusiastic', 'enthusiast', 'passionate', 'keen', 'zealous', 'fervent', 'ardent', 'avid',
                   'devoted', 'dedicated', 'committed', 'engaged', 'involved', 'active', 'participatory',
                   'eager', 'excited', 'animated', 'spirited', 'lively', 'energetic', 'dynamic', 'vibrant',
                   'vigorous', 'robust', 'hearty', 'wholehearted', 'earnest', 'sincere', 'genuine'],
    
    'fun': ['fun', 'funny', 'entertaining', 'enjoyable', 'amusing', 'playful', 'humorous', 'comical', 'hilarious',
            'witty', 'clever', 'silly', 'goofy', 'wacky', 'zany', 'crazy', 'wild', 'ridiculous', 'absurd',
            'laugh', 'giggle', 'chuckle', 'grin', 'smile', 'joke', 'jest', 'tease', 'banter', 'kidding'],
    
    'admiration': ['admire', 'admiration', 'respect', 'appreciate', 'impressive', 'remarkable', 'outstanding', 'excellent',
                   'exceptional', 'extraordinary', 'phenomenal', 'magnificent', 'superb', 'brilliant', 'amazing',
                   'awesome', 'wonderful', 'fantastic', 'incredible', 'marvelous', 'spectacular', 'stunning'],
    
    'amusement': ['hilarious', 'laugh', 'lol', 'haha', 'funny', 'amusing', 'comical', 'humorous', 'witty', 'clever',
                  'entertaining', 'delightful', 'charming', 'engaging', 'captivating', 'enjoyable', 'pleasurable'],
    
    'approval': ['approve', 'agree', 'accept', 'support', 'endorse', 'good', 'great', 'excellent', 'perfect', 'right',
                 'correct', 'accurate', 'true', 'valid', 'sound', 'reasonable', 'sensible', 'logical', 'rational',
                 'wise', 'smart', 'clever', 'intelligent', 'brilliant', 'genius', 'okay', 'alright', 'fine', 'cool'],
    
    'caring': ['care', 'caring', 'compassion', 'concerned', 'thoughtful', 'kind', 'gentle', 'tender', 'loving',
               'affectionate', 'warm', 'nurturing', 'supportive', 'understanding', 'empathetic', 'sympathetic',
               'considerate', 'attentive', 'mindful', 'helpful', 'generous', 'giving', 'selfless', 'devoted'],
    
    'gratitude': ['thank', 'thanks', 'grateful', 'appreciate', 'gratitude', 'thankful', 'obliged', 'indebted',
                  'blessed', 'fortunate', 'lucky', 'privileged', 'honored', 'humbled', 'touched', 'moved'],
    
    'relief': ['relief', 'relieved', 'glad', 'phew', 'finally', 'thank god', 'thank goodness', 'at last',
               'about time', 'breathing easier', 'weight lifted', 'burden lifted', 'stress gone', 'over'],
    
    'pride': ['proud', 'pride', 'accomplished', 'achievement', 'success', 'triumph', 'victory', 'win', 'winner',
              'champion', 'best', 'top', 'first', 'excellent', 'outstanding', 'exceptional', 'impressive'],
    
    'optimism': ['hopeful', 'optimistic', 'positive', 'bright', 'promising', 'encouraging', 'uplifting', 'inspiring',
                 'motivating', 'confident', 'assured', 'certain', 'sure', 'determined', 'resolute', 'steadfast'],
    
    # Neutral emotions
    'neutral': ['okay', 'fine', 'alright', 'whatever', 'meh'],
    'surprise': ['surprise', 'surprised', 'wow', 'whoa', 'omg'],
    'realization': ['realize', 'understand', 'see', 'get it', 'makes sense', 'clear now', 'oh i see'],
    'confusion': ['confused', 'confusing', 'puzzled', 'unclear', 'lost'],
    'curiosity': ['curious', 'wonder', 'interested', 'tell me'],
    
    
    # Negative emotions (100+ keywords each)
    'anger': ['angry', 'anger', 'furious', 'mad', 'irate', 'enraged', 'outraged', 'livid', 'fuming', 'seething',
              'raging', 'incensed', 'infuriated', 'apoplectic', 'wrathful', 'resentful', 'bitter', 'hostile',
              'aggressive', 'violent', 'savage', 'fierce', 'ferocious', 'vicious', 'brutal', 'cruel', 'harsh',
              'irritated', 'annoyed', 'frustrated', 'exasperated', 'aggravated', 'provoked', 'antagonized',
              'pissed', 'pissed off', 'ticked off', 'fed up', 'sick of', 'had enough', 'done with',
              'steaming', 'boiling', 'burning', 'blazing', 'hot', 'heated', 'fired up', 'worked up',
              'bent out of shape', 'up in arms', 'seeing red', 'blood boiling', 'losing it', 'losing temper',
              'blow up', 'explode', 'erupt', 'snap', 'crack', 'lose cool', 'flip out', 'freak out',
              'rage', 'fury', 'wrath', 'ire', 'indignation', 'umbrage', 'offense', 'affront', 'insult',
              'hate', 'hatred', 'loathe', 'detest', 'despise', 'abhor', 'scorn', 'contempt', 'disdain',
              'spite', 'malice', 'venom', 'poison', 'toxic', 'venomous', 'spiteful', 'malicious', 'vindictive',
              'betray', 'betrayed', 'betrayal', 'backstab', 'backstabbed', 'two-faced', 'deceived', 'tricked',
              'lied', 'liar', 'cheated', 'cheater', 'unfaithful', 'disloyal'],
    
    'annoyance': ['annoyed', 'annoying', 'irritated', 'irritating', 'bothered', 'frustrated', 'exasperated',
                  'aggravated', 'irked', 'vexed', 'perturbed', 'peeved', 'miffed', 'nettled', 'riled',
                  'bugged', 'pestered', 'harassed', 'hassled', 'nagged', 'badgered', 'hounded', 'plagued',
                  'disturbed', 'unsettled', 'disquieted', 'troubled', 'upset', 'dismayed', 'displeased',
                  'cross', 'cranky', 'grumpy', 'grouchy', 'crabby', 'testy', 'touchy', 'snappy', 'short',
                  'petty', 'trivial', 'minor', 'small', 'little', 'insignificant', 'negligible', 'trifling'],
    
    'disgust': ['disgusting', 'disgusted', 'gross', 'revolting', 'repulsive', 'repugnant', 'repellent', 'nasty',
                'vile', 'foul', 'putrid', 'rotten', 'rancid', 'fetid', 'stinking', 'stinky', 'smelly',
                'sick', 'sickening', 'nauseating', 'nauseous', 'queasy', 'squeamish', 'vomit', 'puke', 'gag',
                'reprehensible', 'deplorable', 'despicable', 'contemptible', 'detestable', 'abhorrent', 'loathsome',
                'offensive', 'objectionable', 'unpleasant', 'disagreeable', 'distasteful', 'unsavory', 'unpalatable',
                'abominable', 'atrocious', 'appalling', 'horrific', 'horrible', 'horrid', 'hideous', 'ghastly',
                'grotesque', 'monstrous', 'ugly', 'repugnant', 'odious', 'obnoxious', 'insufferable', 'intolerable'],
    
    'disapproval': ['disapprove', 'disapproving', 'disagree', 'disagreeing', 'reject', 'refuse', 'decline', 'deny',
                    'oppose', 'opposing', 'against', 'anti', 'con', 'objection', 'protest', 'resist', 'rebuff',
                    'bad', 'wrong', 'incorrect', 'mistaken', 'erroneous', 'false', 'untrue', 'inaccurate',
                    'inappropriate', 'unsuitable', 'improper', 'unfit', 'unacceptable', 'intolerable', 'impermissible',
                    'condemn', 'censure', 'criticize', 'denounce', 'deplore', 'reproach', 'rebuke', 'reprimand',
                    'scold', 'admonish', 'chastise', 'chide', 'berate', 'castigate', 'lambaste', 'excoriate',
                    'frown', 'disapproving', 'negative', 'unfavorable', 'adverse', 'hostile', 'antagonistic'],
    
    'disappointment': ['disappointed', 'disappointing', 'let down', 'failed', 'failure', 'unsuccessful', 'fell short',
                       'unfortunate', 'unlucky', 'regrettable', 'lamentable', 'deplorable', 'sad', 'unhappy',
                       'disheartened', 'discouraged', 'dismayed', 'disenchanted', 'disillusioned', 'crestfallen',
                       'deflated', 'downcast', 'dejected', 'despondent', 'dismal', 'gloomy', 'bleak', 'dreary',
                       'expectations unmet', 'hopes dashed', 'dreams crushed', 'bubble burst', 'reality check',
                       'anticlimax', 'letdown', 'washout', 'dud', 'flop', 'bust', 'bummer', 'drag', 'shame',
                       'betrayed', 'betrayal', 'let me down', 'broke trust', 'trust broken'],
    
    'sadness': ['sad', 'sadness', 'unhappy', 'down', 'low', 'blue', 'depressed', 'depression', 'miserable', 'wretched',
                'heartbroken', 'broken-hearted', 'devastated', 'crushed', 'shattered', 'destroyed', 'ruined',
                'sorrowful', 'mournful', 'doleful', 'melancholy', 'melancholic', 'gloomy', 'dismal', 'dreary',
                'dejected', 'despondent', 'downcast', 'downhearted', 'forlorn', 'woeful', 'woebegone', 'crestfallen',
                'grief-stricken', 'anguished', 'tormented', 'tortured', 'suffering', 'pain', 'hurt', 'aching',
                'tearful', 'teary', 'crying', 'weeping', 'sobbing', 'wailing', 'bawling', 'blubbering',
                'lonely', 'alone', 'isolated', 'abandoned', 'forsaken', 'rejected', 'unwanted', 'unloved',
                'hopeless', 'despairing', 'desperate', 'suicidal', 'dark', 'black', 'empty', 'hollow', 'void',
                'betrayed', 'hurt', 'wounded', 'broken trust', 'trust issues'],
    
    'grief': ['grief', 'grieving', 'grieve', 'mourning', 'mourn', 'loss', 'lost', 'bereaved', 'devastated',
              'heartbroken', 'anguish', 'agony', 'torment', 'torture', 'suffering', 'pain', 'sorrow', 'sadness',
              'death', 'died', 'dead', 'passed', 'gone', 'departed', 'deceased', 'late', 'funeral', 'burial',
              'miss', 'missing', 'longing', 'yearning', 'pining', 'aching', 'hurting', 'wounded', 'scarred'],
    
    'regret': ['regret', 'regretful', 'sorry', 'apologize', 'apology', 'remorse', 'remorseful', 'contrite', 'penitent',
               'wish I hadn\'t', 'shouldn\'t have', 'should have', 'if only', 'would have', 'could have',
               'mistake', 'error', 'blunder', 'fault', 'blame', 'guilty', 'guilt', 'ashamed', 'shame',
               'embarrassed', 'humiliated', 'mortified', 'chagrined', 'chastened', 'rueful', 'repentant'],
    
    'fear': ['fear', 'afraid', 'scared', 'terrified', 'petrified', 'frightened', 'horrified', 'panicked', 'alarmed',
             'anxious', 'worried', 'concerned', 'apprehensive', 'uneasy', 'nervous', 'jittery', 'jumpy', 'edgy',
             'dread', 'dreading', 'terror', 'horror', 'phobia', 'paranoid', 'paranoia', 'threatened', 'menaced',
             'danger', 'dangerous', 'threatening', 'menacing', 'ominous', 'foreboding', 'sinister', 'eerie',
             'creepy', 'spooky', 'scary', 'frightening', 'terrifying', 'horrifying', 'chilling', 'bone-chilling',
             'nightmare', 'nightmarish', 'haunt', 'haunted', 'haunting', 'ghost', 'demon', 'monster', 'evil'],
    
    'nervousness': ['nervous', 'nervousness', 'jittery', 'jumpy', 'uneasy', 'unease', 'tense', 'tension', 'stressed',
                    'stress', 'anxious', 'anxiety', 'worried', 'worry', 'concern', 'concerned', 'apprehensive',
                    'hesitant', 'uncertain', 'unsure', 'doubtful', 'wary', 'cautious', 'careful', 'guarded',
                    'edgy', 'on edge', 'uptight', 'wound up', 'keyed up', 'worked up', 'rattled', 'shaken',
                    'butterflies', 'stomach churning', 'hands shaking', 'trembling', 'quaking', 'quivering'],
    
    'hate': ['hate', 'hatred', 'loathe', 'loathing', 'detest', 'despise', 'abhor', 'abhorrence', 'revulsion',
             'repugnance', 'aversion', 'antipathy', 'animosity', 'hostility', 'enmity', 'animus', 'rancor',
             'spite', 'malice', 'ill will', 'bad blood', 'grudge', 'resentment', 'bitterness', 'acrimony',
             'vengeance', 'vindictiveness', 'revenge', 'retaliation', 'payback', 'retribution', 'vendetta'],
    
    'worry': ['worried', 'worrying', 'worry', 'worries', 'anxious', 'anxiety', 'concerned', 'concern', 'troubled',
              'troubling', 'distressed', 'distress', 'uneasy', 'unease', 'apprehensive', 'apprehension',
              'nervous', 'nervousness', 'tense', 'tension', 'stressed', 'stress', 'pressure', 'strain',
              'fretting', 'fret', 'brooding', 'brood', 'dwelling', 'obsessing', 'ruminating', 'overthinking'],
    
    'embarrassment': ['embarrassed', 'embarrassment', 'ashamed', 'humiliated', 'mortified', 'chagrined', 'abashed',
                      'sheepish', 'red-faced', 'blushing', 'flushed', 'awkward', 'uncomfortable', 'self-conscious',
                      'exposed', 'naked', 'vulnerable', 'caught', 'busted', 'outed', 'revealed', 'unmasked'],
    
    'shame': ['shame', 'shameful', 'ashamed', 'disgraced', 'disgraceful', 'dishonored', 'tarnished', 'sullied',
              'soiled', 'stained', 'blemished', 'stigmatized', 'branded', 'marked', 'scarred', 'damaged'],
    
    'guilt': ['guilty', 'guilt', 'culpable', 'blameworthy', 'at fault', 'responsible', 'accountable', 'liable',
              'remorseful', 'contrite', 'penitent', 'repentant', 'regretful', 'sorry', 'apologetic'],
    
    'remorse': ['remorse', 'remorseful', 'regret', 'regretful', 'contrite', 'penitent', 'repentant', 'apologetic',
                'sorry', 'rueful', 'compunction', 'self-reproach', 'self-blame', 'self-condemnation'],
    
    # Special emotions (100+ keywords each)
    'sarcasm': ['yeah right', 'sure', 'obviously', 'totally', 'just great', 'wonderful', 'perfect', 'brilliant',
                'fantastic', 'amazing', 'lovely', 'nice try', 'good one', 'real smart', 'genius', 'clever',
                'oh really', 'you don\'t say', 'no kidding', 'go figure', 'imagine that', 'shocking',
                'surprise surprise', 'who would have thought', 'what a shock', 'unbelievable', 'incredible',
                'as if', 'like that\'ll happen', 'in your dreams', 'keep dreaming', 'not likely', 'fat chance',
                'sarcastic', 'ironic', 'sardonic', 'mocking', 'sneering', 'derisive', 'scornful', 'contemptuous'],
    
    'empathy': ['understand', 'feel for you', 'sorry to hear', 'sympathize', 'empathize', 'compassion', 'compassionate',
                'feel your pain', 'in your shoes', 'there for you', 'here for you', 'support you', 'with you',
                'thinking of you', 'praying for you', 'sending love', 'sending thoughts', 'hearts go out',
                'condolences', 'deepest sympathies', 'share your grief', 'share your sorrow', 'share your pain',
                'know how you feel', 'been there', 'relate', 'resonates', 'touches my heart', 'moves me'],
    
    'anxiety': ['anxious', 'anxiety', 'panic', 'panicking', 'panicked', 'overwhelmed', 'stressed out', 'freaking out',
                'losing it', 'can\'t cope', 'can\'t handle', 'too much', 'falling apart', 'breaking down',
                'heart racing', 'can\'t breathe', 'hyperventilating', 'dizzy', 'nauseous', 'shaking',
                'trembling', 'sweating', 'cold sweat', 'nervous breakdown', 'mental breakdown', 'crisis',
                'attack', 'anxiety attack', 'panic attack', 'meltdown', 'frazzled', 'unraveling', 'undone'],
    
    'depression': ['depressed', 'depression', 'hopeless', 'helpless', 'worthless', 'empty', 'numb', 'nothing',
                   'meaningless', 'pointless', 'useless', 'no point', 'why bother', 'what\'s the use',
                   'give up', 'can\'t go on', 'end it all', 'suicidal', 'want to die', 'better off dead',
                   'dark', 'darkness', 'abyss', 'void', 'pit', 'hole', 'drowning', 'suffocating', 'trapped',
                   'stuck', 'paralyzed', 'frozen', 'can\'t move', 'can\'t function', 'broken', 'damaged'],
    
    'stress': ['stressed', 'stressing', 'stress', 'pressure', 'pressured', 'overwhelmed', 'overloaded', 'swamped',
               'buried', 'drowning', 'underwater', 'in over head', 'too much', 'can\'t handle', 'breaking point',
               'burned out', 'burnt out', 'exhausted', 'drained', 'depleted', 'spent', 'running on empty',
               'stretched thin', 'spread thin', 'pulled in directions', 'juggling', 'balancing', 'struggling'],
    
    'frustration': ['frustrated', 'frustrating', 'frustration', 'annoying', 'annoyed', 'aggravating', 'aggravated',
                    'irritating', 'irritated', 'exasperating', 'exasperated', 'maddening', 'infuriating',
                    'trying', 'difficult', 'impossible', 'can\'t', 'unable', 'stuck', 'blocked', 'obstacle',
                    'wall', 'brick wall', 'dead end', 'nowhere', 'going nowhere', 'spinning wheels', 'wasting time'],
    
    'jealousy': ['jealous', 'jealousy', 'envy', 'envious', 'envying', 'covet', 'covetous', 'resentful', 'resentment',
                 'bitter', 'bitterness', 'green with envy', 'green-eyed', 'want what they have', 'not fair',
                 'why them', 'why not me', 'they don\'t deserve', 'I deserve', 'should be mine', 'wish I had',
                 'possessive', 'territorial', 'insecure', 'threatened', 'comparing', 'comparison', 'competing'],
    
    'loneliness': ['lonely', 'loneliness', 'alone', 'isolated', 'isolation', 'solitary', 'solo', 'by myself',
                   'no one', 'nobody', 'abandoned', 'forgotten', 'left behind', 'left out', 'excluded',
                   'outcast', 'outsider', 'misfit', 'loner', 'friendless', 'unloved', 'unwanted', 'invisible',
                   'disconnected', 'detached', 'distant', 'remote', 'far away', 'separate', 'apart', 'divided'],
    
    'boredom': ['bored', 'boring', 'boredom', 'dull', 'tedious', 'monotonous', 'repetitive', 'routine', 'mundane',
                'humdrum', 'tiresome', 'wearisome', 'dreary', 'dry', 'stale', 'flat', 'lifeless', 'dead',
                'uninteresting', 'unexciting', 'uninspiring', 'unstimulating', 'bland', 'insipid', 'vapid',
                'nothing to do', 'nothing happening', 'slow', 'dragging', 'killing time', 'passing time', 'waiting'],
}

# Ambiguous phrases that need context from chat history
AMBIGUOUS_PHRASES = {
    r'oh my god': ['surprise', 'anger', 'shock', 'excitement'],
    r'omg': ['surprise', 'anger', 'shock', 'excitement'],
    r'oh god': ['worry', 'frustration', 'surprise'],
    r'seriously': ['anger', 'surprise', 'sarcasm'],
    r'wow': ['surprise', 'sarcasm', 'excitement'],
    r'great': ['joy', 'sarcasm', 'anger'],
    r'perfect': ['joy', 'sarcasm', 'anger'],
    r'nice': ['approval', 'sarcasm', 'anger'],
}

def analyze_chat_context(history: List[Dict]) -> str:
    """
    Analyze recent chat history to determine the emotional context.
    Returns the dominant emotion from recent messages.
    """
    if not history:
        return 'neutral'
    
    # Look at last 5 messages
    recent = history[-5:]
    emotion_counts = {}
    
    for msg in recent:
        emotion = msg.get('sentiment_category', 'neutral').lower()
        # Map old categories to emotions if needed
        if emotion in ['very negative', 'negative']:
            emotion = 'anger'
        elif emotion in ['very positive', 'positive']:
            emotion = 'joy'
        
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    
    # Return most common emotion
    if emotion_counts:
        return max(emotion_counts, key=emotion_counts.get)
    return 'neutral'

def has_negation(text, keyword):
    """
    Check if a keyword is negated in the text.
    Returns True if the keyword appears within 3 words after a negation word.
    """
    text_lower = text.lower()
    words = text_lower.split()
    
    try:
        keyword_index = None
        for i, word in enumerate(words):
            if keyword in word:
                keyword_index = i
                break
        
        if keyword_index is None:
            return False
        
        # Check 3 words before the keyword
        for i in range(max(0, keyword_index - 3), keyword_index):
            if words[i] in NEGATION_WORDS:
                return True
        
        return False
    except:
        return False

def flip_emotion_for_negation(emotion):
    """
    Flip positive emotions to negative when negated, and vice versa.
    """
    # Positive to negative mappings
    positive_to_negative = {
        'joy': 'sadness',
        'happiness': 'sadness',
        'love': 'hate',
        'excitement': 'disappointment',
        'enthusiasm': 'boredom',
        'fun': 'boredom',
        'admiration': 'disapproval',
        'approval': 'disapproval',
        'gratitude': 'resentment',
        'pride': 'shame',
        'optimism': 'pessimism',
        'caring': 'indifference',
        'relief': 'worry',
    }
    
    # Negative to positive mappings
    negative_to_positive = {
        'sadness': 'happiness',
        'anger': 'calm',
        'fear': 'confidence',
        'hate': 'love',
        'disappointment': 'satisfaction',
        'disapproval': 'approval',
        'disgust': 'appreciation',
        'worry': 'relief',
        'shame': 'pride',
        'guilt': 'innocence',
    }
    
    if emotion in positive_to_negative:
        return positive_to_negative[emotion]
    elif emotion in negative_to_positive:
        return negative_to_positive[emotion]
    else:
        return emotion

def detect_emotion(text, chat_history: Optional[List[Dict]] = None):
    """
    Detect specific emotion from text using contextual phrases first, then keywords.
    Uses chat history to disambiguate ambiguous phrases.
    Handles negation to flip sentiment (e.g., "I don't like you" -> anger/hate)
    Returns emotion label (e.g., 'joy', 'sadness', 'anger')
    """
    text_lower = text.lower().strip()
    
    # Check for common negative phrases FIRST
    negative_phrases = [
        (r'betray(?:ed)? me', 'anger'),
        (r'you betray(?:ed)?', 'anger'),
        (r'betrayal', 'anger'),
        (r'stabbed (?:me )?in (?:the )?back', 'anger'),
        (r'let me down', 'disappointment'),
        (r'broke my trust', 'anger'),
        (r'lied to me', 'anger'),
        (r'cheated on me', 'anger'),
        (r'don\'t like', 'hate'),
        (r'do not like', 'hate'),
        (r'don\'t love', 'dislike'),
        (r'don\'t want', 'rejection'),
        (r'can\'t stand', 'hate'),
        (r'hate you', 'hate'),
        (r'dislike you', 'disapproval'),
        (r'you\'re (?:a |an )?(?:idiot|fool|moron|bastard|asshole|jerk|stupid|dumb|loser|trash|piece of shit)', 'anger'),
        (r'you are (?:a |an )?(?:idiot|fool|moron|bastard|asshole|jerk|stupid|dumb|loser|trash|piece of shit)', 'anger'),
        (r'(?:u|you) (?:r|are) (?:a |an )?(?:idiot|fool|moron|bastard|asshole|jerk|stupid|dumb|loser|trash)', 'anger'),
        (r'you suck', 'anger'),
        (r'this sucks', 'disappointment'),
        (r'fuck you', 'anger'),
        (r'screw you', 'anger'),
        (r'go to hell', 'anger'),
    ]
    
    for pattern, emotion in negative_phrases:
        if re.search(pattern, text_lower):
            return emotion
    
    # Check for ambiguous phrases first
    for pattern, possible_emotions in AMBIGUOUS_PHRASES.items():
        if re.search(pattern, text_lower):
            # Use chat history to determine which emotion
            if chat_history:
                context_emotion = analyze_chat_context(chat_history)
                # If context is negative, lean towards negative interpretation
                if context_emotion in ['anger', 'frustration', 'annoyance', 'sadness']:
                    # Return the negative option
                    for emotion in possible_emotions:
                        if emotion in ['anger', 'frustration', 'worry', 'sarcasm']:
                            return emotion
                elif context_emotion in ['joy', 'excitement', 'happiness']:
                    # Return the positive option
                    for emotion in possible_emotions:
                        if emotion in ['surprise', 'excitement', 'joy']:
                            return emotion
            # Default to first option if no clear context
            return possible_emotions[0]
    
    # STEP 1: Check for contextual phrases FIRST (most important)
    # These are multi-word expressions with specific meanings
    for emotion, patterns in EMOTION_PHRASES.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                # Direct match on a contextual phrase - return immediately
                return emotion
    
    # STEP 2: Check for keywords with negation handling
    emotion_scores = {}
    has_negation_found = False
    
    for emotion, keywords in EMOTION_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in text_lower:
                # Check if negated
                if has_negation(text, keyword):
                    has_negation_found = True
                    # Don't count negated keywords for this emotion
                    continue
                
                # Exact word match gets higher score
                if f' {keyword} ' in f' {text_lower} ':
                    score += 2
                else:
                    score += 1
        
        if score > 0:
            emotion_scores[emotion] = score
    
    # If keywords matched, return emotion with highest score
    # Apply negation flip if negation was found
    if emotion_scores:
        best_emotion = max(emotion_scores, key=emotion_scores.get)
        
        # If negation was detected, flip the emotion
        if has_negation_found:
            best_emotion = flip_emotion_for_negation(best_emotion)
        
        return best_emotion
    
    # STEP 3: Fall back to sentiment polarity analysis
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Map polarity to emotion
        if polarity > 0.5:
            return 'joy' if subjectivity > 0.5 else 'happiness'
        elif polarity > 0.1:
            return 'approval' if subjectivity < 0.5 else 'optimism'
        elif polarity < -0.5:
            return 'anger' if subjectivity > 0.5 else 'sadness'
        elif polarity < -0.1:
            return 'disappointment' if subjectivity > 0.5 else 'annoyance'
        else:
            return 'neutral'
    except:
        return 'neutral'

def analyze_emotion(text, chat_history: Optional[List[Dict]] = None):
    """
    Complete emotion analysis returning detailed results.
    Includes chat history context for better accuracy.
    """
    emotion = detect_emotion(text, chat_history)
    
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
    except:
        polarity = 0.0
        subjectivity = 0.5
    
    return {
        'emotion': emotion,
        'polarity': polarity,
        'subjectivity': subjectivity,
        'category': get_emotion_category(emotion)
    }

if __name__ == '__main__':
    # Test emotion detection
    test_cases = [
        "I'm so happy today!",
        "This makes me really sad",
        "I'm absolutely furious",
        "I'm terrified",
        "Wow this is amazing!",
        "I really appreciate your help",
        "I'm so worried",
        "This is frustrating",
        "I feel so lonely",
        "You're the best!",
        "I'm feeling anxious",
        "This is disgusting",
        "I'm embarrassed",
        "I feel guilty",
        "Yeah right, like that'll happen",
        "Hello",
        "Thanks"
    ]
    
    print("="*60)
    print("EMOTION DETECTION TEST")
    print("="*60)
    
    for text in test_cases:
        result = analyze_emotion(text)
        print(f"\nText: {text}")
        print(f"Emotion: {result['emotion']}")
        print(f"Category: {result['category']}")
        print(f"Polarity: {result['polarity']:.2f}")
