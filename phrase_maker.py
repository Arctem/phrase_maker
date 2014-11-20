import random
import re
import sys

data = {
    #Generic stuff phrases for everything.
    'gen' : {
        'template' : ['this is only so tests don\'t crash'],

        'vowel' : list('aeiouy'),
        'consonant' : list('bcdfghjklmnpqrstvwxyz'),
        'karst' : ['Karst', 'Flannery', 'Flanneroo'],

        'num_either' : ['{number}', '{roman_number}'],
        
        'number' : ['{digit}{number}', '{digit}'],
        'digit' : '1234567890',

        'roman_number' : ['{roman_ones}']*3 + ['{roman_tens}{roman_ones}'],
        'roman_tens' : ['X'],
        'roman_ones' : ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'],
    }
}

def load_module(module):
    new_data = module.data
    for i in new_data.keys():
        if i in data.keys():
            print('Duplicate key {}.'.format(i))
        else:
            data[i] = new_data[i]


#Really stupid method to basically make a format that works better for what I'm doing.
def make(dict_name, name = 'Dudeface', capitalize = True):
    dict = data[dict_name]
    orig = random.choice(dict['template'])
    fixed_data = {}
    #regex = re.compile('{.+?}')
    regex = re.compile('''{.+?}(?:\[.+?\])?''')
    
    orig = replace_vars(dict, orig, regex, name, fixed_data)
    
    orig = fix_articles(orig)
    orig = fix_capitals(orig)
    if capitalize:
        orig = orig.split()
        orig[0] = orig[0].capitalize()
        orig = ' '.join(orig)
    return orig

def replace_vars(dict, orig, regex, name, fixed_data):
    while len(regex.findall(orig)) > 0:
        to_replace = regex.findall(orig)[0]
        field = to_replace.strip('{}')
        field = field.split('}[') #Split if we have the optional arg

        #if we have multiple comma-separated fields, choose one
        if ',' in field[0]:
            field[0] = random.choice(field[0].split(','))

        cap = field[0] != field[0].lower()
        field[0] = field[0].lower()
        word = ''
        
        #Check for existing data.
        if len(field) > 1 and field[1] in fixed_data.keys():
            word = fixed_data[field[1]]
        elif '/' in field[0]:
            field[0] = field[0].split('/')
            word = random.choice(data[field[0][0]][field[0][1]])
            word = word.replace('{', '{' + field[0][0] + '/')
        elif field[0] not in dict.keys():
            if field[0] != 'username':
                print(field[0])
            #orig = orig.replace('{username}', name, 1)
            #orig = orig.replace('{Username}', name.capitalize(), 1)
            word = name
            #continue
        else:
            word = random.choice(dict[field[0]])
 
        #Handle all the extra vars inside the new word before we store it in fixed_data.
        word = replace_vars(dict, word, regex, name, fixed_data)

        if len(field) > 1 and field[1] not in fixed_data.keys():
            fixed_data[field[1]] = word

        if cap:
            word = make_capital(word)
        orig = orig.replace(to_replace, word, 1)
    return orig

def make_capital(orig):
    orig = orig.split()
    for i in range(len(orig)):
        if i is not 0 and orig[i] in ['of', 'the', 'a']:
            continue
        if orig[i][0] == '{':
            orig[i] = orig[i][0] + orig[i][1].capitalize() + orig[i][2:]
        else:
            orig[i] = orig[i][0].capitalize() + orig[i][1:]
    return ' '.join(orig)
    
#Makes sure sentences start with capitals.
def fix_capitals(orig):
    orig = orig.split()
    for i in range(len(orig) - 1):
        if i is 0 or orig[i - 1][-1] in '.?!':
            orig[i] = orig[i].capitalize()
    return ' '.join(orig)

def fix_articles(orig):
    orig = orig.split()
    for i in range(len(orig) - 1):
        if orig[i] == 'a' or orig[i] == 'an':
            if orig[i + 1][0].lower() in 'aeiou':
                orig[i] = 'an'
            else:
                orig[i] = 'a'
    return ' '.join(orig)

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
