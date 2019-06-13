import re
from emoji.unicode_codes import UNICODE_EMOJI

__BYTES_TABLE = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f                0123456789       ABCDEFGHIJKLMNOPQRSTUVWXYZ      abcdefghijklmnopqrstuvwxyz    \x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'

#replace '_' (95) with space (32) and remove other punctuation
#__STRING_TABLE = {95: 32, 33: None, 34: None, 35: None, 36: None, 37: None, 38: None, 9: None, 40: None, 41: None, 42: None, 43: None, 44: None, 45: None, 46: None, 47: None, 58: None, 59: None, 60: None, 61: None, 62: None, 63: None, 64: None, 91: None, 92: None, 93: None, 94: None, 96: None, 23: None, 124: None, 125: None, 126: None}

__STRING_TABLE = {95: 32, 33: 32, 34: 32, 35: 32, 36: 32, 37: 32, 38: 32, 9: 32, 40: 32, 41: 32, 42: 32, 43: 32, 44: 32, 45: 32, 46: 32, 47: 32, 58: 32, 59: 32, 60: 32, 61: 32, 62: 32, 63: 32, 64: 32, 91: 32, 92: 32, 93: 32, 94: 32, 96: 32, 23: 32, 124: 32, 125: 32, 126: 32}

def remove_punctuaction(x):
    x = x.lower()
    if type(x) == bytes:
        return b' '.join(x.translate(__BYTES_TABLE).split()).decode('utf-8')
    else:
        return ' '.join(x.translate(__STRING_TABLE).split())

def preprocess_no_variables(text):
    text = preprocess_text(text)
    text = re.sub('url', '', text)
    text = re.sub('uservariable', '', text) # remove usernames
    return text
    
def preprocess_text(text):
    text = re.sub(r'(.)\1+', r'\1\1', text)
    text = convert_emojis(text)
    text = text.replace(":)"," happy ")
    text = text.replace(":("," unhappy ")
    text = text.replace(":-)"," happy ")
    text = text.replace(";D"," funny ")
    text = text.replace(" XD "," funny ")
    text = text.replace("<3"," love ")
    text = re.sub('@[^\s]+', 'USERVARIABLE', text) # remove usernames
    text = re.sub(r'#([^\s]+)', r' ', text) # remove the # in #hashtag
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)
    text = remove_whitespace(deEmojify(clean_numbers(remove_punctuaction(replace_typical_misspell(text.strip().lower())))))  
    return text if len(text) > 0 else 'neutral'

def preprocess_text_without_emojis(text):
    text = re.sub(r'(.)\1+', r'\1\1', text)
    text = text.replace(":)"," happy ")
    text = text.replace(":("," unhappy ")
    text = text.replace(":-)"," happy ")
    text = text.replace(" XD "," funny ")
    text = text.replace("<3"," love ")
    text = re.sub('@[^\s]+', 'USERVARIABLE', text) # remove usernames
    text = re.sub(r'#([^\s]+)', r' ', text) # remove the # in #hashtag
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)
    text = remove_whitespace(deEmojify(clean_numbers(remove_punctuaction(replace_typical_misspell(text.strip().lower())))))  
    return text if len(text) > 0 else 'neutral'

def is_emoji(s):
    return s in UNICODE_EMOJI

def convert_emojis(text):
    return ''.join([' '+UNICODE_EMOJI[char].strip(':').replace('_',' ')+' ' if is_emoji(char) else char for char in text])

def remove_whitespace(text):
    return ' '.join(text.split())

def _get_mispell(mispell_dict):
    mispell_re = re.compile('(%s)' % '|'.join(mispell_dict.keys()))
    return mispell_dict, mispell_re

def replace_typical_misspell(text):
    mispellings, mispellings_re = _get_mispell(mispell_dict)
    def replace(match):
        return mispellings[match.group(0)]
    return mispellings_re.sub(replace, text)

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

def clean_numbers(x):
    x = re.sub('[0-9]{5,}', '#####', x)
    x = re.sub('[0-9]{4}', '####', x)
    x = re.sub('[0-9]{3}', '###', x)
    x = re.sub('[0-9]{2}', '##', x)
    x = re.sub('[0-9]{1}', '#', x)
    #x = re.sub('[0-9]{1}', '#', x)
    return x

mispell_dict = {"0":"zero","1":"one","hearteyes":"heart eyes","xoxo":" kisses ","!":" exclamation ","perrrrfect":"perfect"," ur ":" your "," u ": " you ","ain't": "is not", "aren't": "are not","can't": "cannot", "'cause": "because", "could've": "could have", "couldn't": "could not", "didn't": "did not",  "doesn't": "does not", "don't": "do not", "hadn't": "had not", "hasn't": "has not", "haven't": "have not", "he'd": "he would","he'll": "he will", "he's": "he is", "how'd": "how did", "how'd'y": "how do you", "how'll": "how will", "how's": "how is",  "I'd": "I would", "I'd've": "I would have", "I'll": "I will", "I'll've": "I will have","I'm": "I am", "I've": "I have", "i'd": "i would", "i'd've": "i would have", "i'll": "i will",  "i'll've": "i will have","i'm": "i am", "i've": "i have", "isn't": "is not", "it'd": "it would", "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have","it's": "it is", "let's": "let us", "ma'am": "madam", "mayn't": "may not", "might've": "might have","mightn't": "might not","mightn't've": "might not have", "must've": "must have", "mustn't": "must not", "mustn't've": "must not have", "needn't": "need not", "needn't've": "need not have","o'clock": "of the clock", "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not", "sha'n't": "shall not", "shan't've": "shall not have", "she'd": "she would", "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have", "she's": "she is", "should've": "should have", "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have","so's": "so as", "this's": "this is","that'd": "that would", "that'd've": "that would have", "that's": "that is", "there'd": "there would", "there'd've": "there would have", "there's": "there is", "here's": "here is","they'd": "they would", "they'd've": "they would have", "they'll": "they will", "they'll've": "they will have", "they're": "they are", "they've": "they have", "to've": "to have", "wasn't": "was not", "we'd": "we would", "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", "we're": "we are", "we've": "we have", "weren't": "were not", "what'll": "what will", "what'll've": "what will have", "what're": "what are",  "what's": "what is", "what've": "what have", "when's": "when is", "when've": "when have", "where'd": "where did", "where's": "where is", "where've": "where have", "who'll": "who will", "who'll've": "who will have", "who's": "who is", "who've": "who have", "why's": "why is", "why've": "why have", "will've": "will have", "won't": "will not", "won't've": "will not have", "would've": "would have", "wouldn't": "would not", "wouldn't've": "would not have", "y'all": "you all", "y'all'd": "you all would","y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have","you'd": "you would", "you'd've": "you would have", "you'll": "you will", "you'll've": "you will have", "you're": "you are", "you've": "you have", 'colour': 'color', 'centre': 'center', 'favourite': 'favorite', 'travelling': 'traveling', 'counselling': 'counseling', 'theatre': 'theater', 'cancelled': 'canceled', 'labour': 'labor', 'organisation': 'organization', 'wwii': 'world war 2', 'citicise': 'criticize', 'youtu ': 'youtube ', 'Qoura': 'Quora', 'sallary': 'salary', 'Whta': 'What', 'narcisist': 'narcissist', 'howdo': 'how do', 'whatare': 'what are', 'howcan': 'how can', 'howmuch': 'how much', 'howmany': 'how many', 'whydo': 'why do', 'doI': 'do I', 'theBest': 'the best', 'howdoes': 'how does', 'mastrubation': 'masturbation', 'mastrubate': 'masturbate', "mastrubating": 'masturbating', 'pennis': 'penis', 'Etherium': 'Ethereum', 'narcissit': 'narcissist', 'bigdata': 'big data', '2k17': '2017', '2k18': '2018', 'qouta': 'quota', 'exboyfriend': 'ex boyfriend', 'airhostess': 'air hostess', "whst": 'what', 'watsapp': 'whatsapp', 'demonitisation': 'demonetization', 'demonitization': 'demonetization', 'demonetisation': 'demonetization'}


