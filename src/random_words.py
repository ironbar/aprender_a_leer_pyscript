import random

from pyodide import create_proxy


def download_data():
    # had to remove this because it does not work on pyscript
    # page = urllib.request.urlopen('https://raw.githubusercontent.com/mazyvan/most-common-spanish-words/master/most-common-spanish-words-v5.txt').read().decode()
    # words = page.split('\n')
    with open('most-common-spanish-words-v5.txt', 'r') as f:
        words = f.read().split('\n')
    len_to_words = {}
    for word in words:
        if len(word) not in len_to_words:
            len_to_words[len(word)] = [word]
        else:
            len_to_words[len(word)].append(word)
    len_to_words[2] = get_syllabes()
    return len_to_words


def get_syllabes():
    syllabes = set()
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    for consonant in consonants:
        for vowel in vowels:
            if consonant in 'gq' and vowel in 'ei':
                syllabes.add(consonant + 'u' + vowel)
            else:
                syllabes.add(consonant + vowel)
    remove = ['qu', 'qa', 'qi', 'qo', 'qu']
    syllabes = sorted(list(syllabes.difference(remove)))
    # print(syllabes)
    return syllabes


def get_random_word(n_letters, forbidden_letters='', required_letters=''):
    random.shuffle(LEN_TO_WORDS[n_letters])
    for word in LEN_TO_WORDS[n_letters]:
        lower_word = word.lower()
        if any(letter in lower_word for letter in forbidden_letters.lower()):
            continue
        if required_letters:
            if all(letter in lower_word for letter in required_letters.lower()):
                return word
        else:
            return word


LEN_TO_WORDS = download_data()


def on_click(event):
    n_letters = int(Element("n_letters").value)
    forbidden_letters = Element('forbidden_letters').value
    required_letters = Element('required_letters').value
    output = Element("output")
    output.write(get_random_word(n_letters, forbidden_letters, required_letters))
    update_slider_value()


def update_slider_value():
    Element('n_letters_value').write(Element("n_letters").value)


update_slider_value()

button = document.querySelector("button")
button.addEventListener("click", create_proxy(on_click))


for key in ['n_letters', 'forbidden_letters', 'required_letters']:
    element = document.querySelector('#%s' % key)
    element.onchange = create_proxy(on_click)
