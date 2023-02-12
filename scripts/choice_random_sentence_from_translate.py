#!/usr/bin/env python
import os
import sys
from datetime import datetime
from random import shuffle
from time import sleep

def h():
    print('Параметры:')
    print('\t--help Показать эту справку и выйти.')
    print('\t--count Количество предложений для занятия.')
    print('\t--start Первый урок для включения предложений в список.')
    print('\t--stop Последний урок для включения предложений в список.')

list_sentences = []
counter = 0
start_lesson = 1
stop_lesson = len(os.listdir())-1 # 50
if ('--start' and '--stop') in sys.argv:
    start_lesson = int(sys.argv[sys.argv.index('--start')+1])
    stop_lesson = int(sys.argv[sys.argv.index('--stop')+1])
count = 80
if '--count' in sys.argv:
    count = int(sys.argv[sys.argv.index('--count')+1])
number_lesson = int(start_lesson)

root_directory = '/data/data/com.termux/files/home/ENGLISH/titan_source/part_0'
if 'training_history.txt' not in os.listdir(root_directory):
    training_history = open(f'{root_directory}/training_history.txt','w')
    training_history.close()
os.chdir(root_directory)

while number_lesson <= stop_lesson:
    for file in os.listdir(f'{root_directory}/{number_lesson}'):
        if 'translate' in file:
            with open(f'{root_directory}/{number_lesson}/{file}', 'r') as f:
                list_sentences += f.readlines()
    number_lesson += 1

shuffle(list_sentences)

try:
    training_history = open(f'{root_directory}/training_history.txt', 'a')
    if sys.argv[1] == '--help' or ('--start' and '--stop') not in sys.argv:
        training_history.close()
        h()
        exit()
    else:
        date_time = datetime.now()
        training_history.writelines('*' * 40 + '\n')
        training_history.writelines(date_time.strftime("%Y-%m-%d %H:%M:%S\n\n"))
        training_history.flush()
        print(f"Найдено {len(list_sentences)} предложений.")
        print(f"Переведёшь {count} из них? =)")
        print("")
        for i in list_sentences:
            if '*' not in i:
                if counter != count:
                    counter += 1
                    ru_sentence = i.split(' - ')[0]
                    en_sentence = i.split(' - ')[-1].rstrip('\n')
                    if not en_sentence:
                        answer = input("{0} \u001b[38;5;8m\033[03m\033[02m{1}\033[00m\033[01m - ".format(counter,ru_sentence)) # counter, ru_sentence
                    else:
                        answer = input("{0} \u001b[38;5;7m\033[03m\033[02m{1}\033[00m\033[01m - ".format(counter,ru_sentence)) # counter, ru_sentence
                    if en_sentence and answer not in en_sentence.split(' / '):
                        training_history.writelines("НЕВЕРНО!\n")
                        training_history.writelines(f"{ru_sentence} - {answer}\n")
                        training_history.writelines("Правильный ответ:\n")
                        training_history.writelines(f"{ru_sentence} - {en_sentence}\n\n")
                        training_history.flush()
                        print("")
                        print("\033[93m{0}\033[06m\033[00m\033[01m".format("НЕВЕРНО!"))
                        print("{0} - \033[91m{1}\033[05m\033[00m\033[01m".format(ru_sentence, answer))
                        print("Правильный ответ:    ")
                        print("{0} - \033[92m{1}\033[03m\033[00m\033[01m".format(ru_sentence, en_sentence))
                        print("")
                    sleep(1)
            else:
                continue
except KeyboardInterrupt: # ^C
    print('\nВыполнение прервано.')
    exit()
except ValueError:
    h()
    exit()
finally:
    #print('Урок окончен.')
    print('\n')
    training_history.close()
    exit()
