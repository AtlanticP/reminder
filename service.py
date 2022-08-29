import string 
import random
from hinting import Fieldnames

PATTERN_TIME = '%Y-%m-%d %H:%M:%S'
FIELDNAMES: Fieldnames = ("start", "text")

def get_text()-> str:
    """get random text"""
    
    s = string.ascii_lowercase + string.digits
    n_letters = lambda: random.randint(1, 10)
    n_words = random.randint(1, 20)
    get_word = lambda : ''.join(random.sample(s, n_letters()))
    text: str = ' '.join(get_word() for _ in range(n_words))

    return text + "\n" 

