# -*- coding: latin-1 -*-

import random
import re
import sys

data = {
    #Some general use phrases.
    'gen' : {
        'template' : ['this is only so tests don\'t crash'],

        'username' : ['{.}[username]'],

        'vowel' : list('aeiouy'),
        'consonant' : list('bcdfghjklmnpqrstvwxyz'),
        'karst' : ['Karst', 'Flannery', 'Flanneroo'],

        'num_either' : ['{number}', '{roman_number}'],

        'number' : ['{multidigit}', '{digit}'],
        'multidigit' : ['{number,nonzero}{digit}'],
        'digit' : '1234567890',
        'nonzero' : '123456789',

        'roman_number' : ['{roman_ones}']*3 + ['{roman_tens}{roman_ones}'],
        'roman_tens' : ['X'],
        'roman_ones' : ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'],

        'weekday' : ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday'],
    }
}

_library_match = '(?:([!,{}]+?)/)'
_book_match = _library_match + '?(.+?)'
_books_match = '(?P<books>' + _book_match + '(?:,' + _book_match + ')*)'
_name_match = '''\[(?P<name>.+?)\]'''

_search_string = '{' + _books_match + '}' + '(?:' + _name_match + ')?'

TAG_REGEX = re.compile(_search_string)

def load_module(module):
    new_data = module.data
    for i in new_data.keys():
        if i in data.keys():
            print('Duplicate key {}.'.format(i))
        else:
            data[i] = new_data[i]


#Constructs a full random string using the named library.
def make(lib_name, name = 'Dudeface', capitalize = True):
    orig = random.choice(data[lib_name]['template'])
    fixed_data = {'username': name}

    orig = replace_tags(lib_name, orig, fixed_data)

    orig = fix_articles(orig)
    orig = fix_capitals(orig)
    if capitalize:
        lines = orig.split('\n')
        for i in range(len(lines)):
            line = lines[i].split(' ', 1)
            line[0] = line[0].capitalize()
            lines[i] = ' '.join(line)
        orig = '\n'.join(lines)
    orig = fix_punctuation(orig)
    return orig

def replace_tags(lib_name, orig, fixed_data):
    while TAG_REGEX.search(orig) is not None:
        to_replace = TAG_REGEX.search(orig)
        books = to_replace.group('books')
        name = to_replace.group('name')

        #if we have multiple comma-separated fields, choose one
        #TODO: add weights based on number of elements
        book = random.choice(books.split(','))

        capitalize = book[0] != book[0].lower()
        book = book.lower()

        if '/' in book:
            library, book = book.split('/', 1)
        else:
            library = lib_name

        if name and name in fixed_data:
            word = fixed_data[name]
        else:
            word = random.choice(data[library][book])

        #Handle all the extra vars inside the new word before we store it in fixed_data.
        word = replace_tags(library, word, fixed_data)

        if name and name not in fixed_data:
            fixed_data[name] = word

        if capitalize:
            word = make_capital(word)
        orig = TAG_REGEX.sub(word, orig, 1)
    return orig

def make_capital(orig):
    for char in ' \n':
        orig = orig.split(char)
        for i in range(len(orig)):
            if i is not 0 and orig[i] in ['of', 'the', 'a']:
                continue
            if orig[i][0] == '{':
                orig[i] = orig[i][0] + orig[i][1].capitalize() + orig[i][2:]
            else:
                orig[i] = orig[i][0].capitalize() + orig[i][1:]
        orig = char.join(orig)
    return orig

#Makes sure sentences start with capitals.
def fix_capitals(orig):
    for char in ' \n':
        orig = orig.split(char)
        for i in range(1, len(orig) - 1):
            if orig[i - 1][-1] in '.?!':
                orig[i] = orig[i][0].upper() + orig[i][1:]
        orig = char.join(orig)
    return orig

def fix_articles(orig):
    orig = orig.split(' ')
    for i in range(len(orig) - 1):
        if orig[i] == 'a' or orig[i] == 'an':
            if orig[i + 1][0].lower() in 'aeiou':
                orig[i] = 'an'
            else:
                orig[i] = 'a'
    return ' '.join(orig)

def fix_punctuation(orig):
    #find_punc = re.compile('''[.!?][.!?]+''')

    #reduce sequences of . to 3 max
    while orig.count('....'):
        orig = orig.replace('....', '...')

    #now temporarily convert '...' into a temp unicode char (…) to preserve it
    orig = orig.replace('...', u'…')

    #get rid of ..
    orig = orig.replace('..', '.')

    #let ! override .
    orig = orig.replace('!.', '!').replace('.!', '!')

    #let ? override .
    orig = orig.replace('?.', '?').replace('.?', '?')

    #standardize !? and ?!
    orig = orig.replace('!?', '!?').replace('?!', '!?')

    #undo the previous substitution

    orig = orig.replace(u'…', '...')
    return orig

def get_categories(dict_name):
    if dict_name in data.keys():
        return '{}'.format(sorted(data[dict_name].keys()))
    else:
        return 'No database by that name.'

def main():
    if 'test' in sys.argv:
        test()
    elif 'demo' in sys.argv:
        demo()
    elif len(sys.argv) > 1:
        for i in range(5):
            print(make(sys.argv[1]))
    else:
        print(make('movie'))

def test():
    for key in sorted(data.keys()):
        print('Testing {}'.format(key))
        for i in range(10000):
            make(key)

def demo():
    for key in sorted(data.keys()):
        print('{}: {}'.format(key, make(key)))


if __name__ == '__main__':
    main()
