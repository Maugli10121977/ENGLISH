#!/usr/bin/env python
import os
import sys
import time
import random

root_directory = '/data/data/com.termux/files/home/ENGLISH/titan_source'

need_files = []
def get_need_files():
    for d in os.listdir(root_directory):
        if os.path.isdir(f'{root_directory}/{d}'):
            for f in os.listdir(f'{root_directory}/{d}'):
                if os.path.isfile(f'{root_directory}/{d}/{f}') and 'translate' in f:
                    need_files.append(f'{root_directory}/{d}/{f}')
get_need_files()

def read_all_files():
    pairs_all_sentences = []
    for file in need_files:
        with open(file, 'r') as f:
            sentences_of_one_file = f.readlines()
            for pair in sentences_of_one_file:
                sentence = pair.strip().split(' - ')
                if len(sentence) > 1:
                    pairs_all_sentences.append(sentence)
    return pairs_all_sentences

pairs_all_sentences = read_all_files()
random.shuffle(pairs_all_sentences)
answers_with_mistakes = []

def say_for_writing(pairs_all_sentences):
    for sentence in pairs_all_sentences:
        en_elem = sentence[1]
        ru_elem = sentence[0]
        os.system(f'termux-tts-speak -p 0.7 -r 0.7 {en_elem}')
        answer = input('Your answer:   ')
        while answer == '-':
            os.system(f'termux-tts-speak -p 0.6 -r 0.7 {en_elem}')
            answer = input('Question repeated   ')
        if answer == en_elem:
            continue
        else:
            answers_with_mistakes.append(sentence)

def h():
    print(f'Help about \'{sys.argv[0]}\'')
    print('Описание:')
    print('''\tЭтот скрипт озвучивает в рандомном порядке 
\tанглийские предложения из всех файлов \'translate*.txt\', 
\tи ожидает их письменного перевода. В финале выводит 
\tсписок предложений, переведённых с ошибками.''')
    print('Параметры:')
    print('\t-h Показать эту справку и выйти')
    exit()

def main():
    if '-h' in sys.argv:
        h()
    else:
        print(f'В упражнениях из всех уроков найдено {len(pairs_all_sentences)} предложений.')
        say_for_writing(pairs_all_sentences)

try:
    main()
except (KeyboardInterrupt, EOFError):
    exit()
finally:
    if '-h' not in sys.argv:
        print('')
        print('Learn again )))')
        print(answers_with_mistakes)
