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

dict_all_sentences = dict()
start_lesson = 1
stop_lesson = len(os.listdir())-2 # все уроки
if '--start' in sys.argv:
    start_lesson = int(sys.argv[sys.argv.index('--start')+1])
if '--stop' in sys.argv:
    stop_lesson = int(sys.argv[sys.argv.index('--stop')+1])
count = 80
if '--count' in sys.argv:
    count = int(sys.argv[sys.argv.index('--count')+1])
counter = 0
number_lesson = int(start_lesson)

root_directory = '/data/data/com.termux/files/home/ENGLISH/titan_source'
if 'training_history.txt' not in os.listdir(f'{root_directory}/docs/'):
    training_history = open(f'{root_directory}/docs/training_history.txt','w')
    training_history.close()

while number_lesson <= stop_lesson:
    for file in os.listdir(f'{root_directory}/{number_lesson}'):
        if 'translate' in file:
            with open(f'{root_directory}/{number_lesson}/{file}', 'r') as f:
                list_sentences_one_file = f.readlines()
                number_string_in_file = 0
                for sentence in list_sentences_one_file:
                    number_string_in_file += 1
                    ru = sentence.split(' - ')[0]
                    en = sentence.split(' - ')[-1].rstrip('\n')
                    dict_all_sentences[f'{ru}'] = [f'{file}',f'{en}',f'{number_string_in_file}']
    number_lesson += 1

try:
    training_history = open(f'{root_directory}/docs/training_history.txt', 'a')
    if ((sys.argv[1] == '--help') or (('--start' and '--stop') not in sys.argv)):
        training_history.close()
        h()
    else:
        #counter = 0
        all_ru_sentences = list(dict_all_sentences.keys())
        shuffle(all_ru_sentences)
        print(f'Найдено {len(all_ru_sentences)} предложений.')
        print(f'Переведёшь {count} из них? =)')
        print('')
        date_time = datetime.now()
        training_history.writelines('*' * 40 + '\n')
        training_history.writelines(date_time.strftime("%Y-%m-%d %H:%M:%S\n\n"))
        training_history.flush()
        for ru_sentence in all_ru_sentences:
            if counter <= count:
                counter += 1
                en_sentence = dict_all_sentences[ru_sentence][1]
                if en_sentence:
                    answer = input("{0} \u001b[38;5;7m\033[03m\033[02m{1}\033[00m\033[01m - ".format(counter, ru_sentence)) # counter, ru_sentence
                    if answer not in en_sentence.split(' / '):
                        training_history.writelines("НЕВЕРНО!\n")
                        training_history.writelines(f"{ru_sentence} - {answer}\n")
                        training_history.writelines("Правильный ответ:\n")
                        training_history.writelines(f"{dict_all_sentences[ru_sentence][0]} ({dict_all_sentences[ru_sentence][2]})\n")
                        training_history.writelines(f"{ru_sentence} - {en_sentence}\n\n")
                        training_history.flush()
                        print("")
                        print("\033[93m{0}\033[06m\033[00m\033[01m".format("НЕВЕРНО!"))
                        print("{0} - \033[91m{1}\033[05m\033[00m\033[01m".format(ru_sentence, answer))
                        print("Правильный ответ:    ")
                        print(f"{dict_all_sentences[ru_sentence][0]} ({dict_all_sentences[ru_sentence][2]})")
                        print("{0} - \033[92m{1}\033[03m\033[00m\033[01m".format(ru_sentence, en_sentence))
                        print("")
                    #continue
                else:
                    answer = input("{0} \u001b[38;5;8m\033[03m\033[02m{1}\033[00m\033[01m - ".format(counter,ru_sentence)) # counter, ru_sentence
                    #continue
            if counter == count:
                exit()
            sleep(1)
except (KeyboardInterrupt, EOFError): # ^C
    print('\nВыполнение прервано.')
except IndexError:
    h()
except ValueError:
    h()
finally:
    #print('Урок окончен.')
    print('\n')
    training_history.close()
