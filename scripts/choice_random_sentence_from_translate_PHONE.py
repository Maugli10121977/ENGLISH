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
    print('\t--measure-speed Измерять скорость печати.')
    print('\t--show-time-every-sentence Показывать время, затраченное на ввод каждого предложения (этот параметр должен применяться совместно с --measure-speed).')
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
counter_wrong_answers = 0
number_lesson = int(start_lesson)
history_mistakes = {}
measure_speed_result_time = 0
counter_input_symbols = 0

root_directory = '/data/data/com.termux/files/home/ENGLISH/titan_course'
if f'training_history.txt' not in os.listdir(f'{root_directory}/docs/'):
    training_history = open(f'{root_directory}/docs/training_history.txt','w')
    training_history.close(); del training_history

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
                    if '*' not in en:
                        dict_all_sentences[f'{ru}'] = [f'{file}',f'{en}',f'{number_string_in_file}']
    number_lesson += 1

try:
    training_history = open(f'{root_directory}/docs/training_history.txt', 'a')
    if (('--help' in sys.argv) or (('--start' and '--stop') not in sys.argv)):
        training_history.close()
        h()
    else:
        all_ru_sentences = list(dict_all_sentences.keys())
        shuffle(all_ru_sentences)
        print(f'Найдено {len(all_ru_sentences)} предложений (уроки с {start_lesson} по {stop_lesson}).')
        print(f'Переведёшь {count} из них? =)')
        print('')
        date_time = datetime.now()
        training_history.writelines('*' * 40 + '\n')
        training_history.writelines(f'{date_time.strftime("%Y-%m-%d %H:%M:%S")} (уроки с {start_lesson} по {stop_lesson})\n\n')
        training_history.flush()
        for ru_sentence in all_ru_sentences:
            if counter <= count:
                counter += 1
                en_sentence = dict_all_sentences[ru_sentence][1]
                if en_sentence:
                    if '--measure-speed' in sys.argv:
                        t1 = datetime.now().timestamp()
                    answer = input("{0} \u001b[38;5;7m\033[03m\033[02m{1}\033[00m - ".format(counter, ru_sentence)) # counter, ru_sentence
                    if '--measure-speed' in sys.argv:
                        t2 = datetime.now().timestamp()
                    if answer not in en_sentence.split(' / '):
                        print("")
                        print("\033[93m{0}\033[06m\033[00m\033[00m".format(f"IT'S WRONG! ({len(all_ru_sentences)} выбраны, {count} предложены, {counter} решены)"))
                        print("{0} - \033[91m{1}\033[05m\033[00m".format(ru_sentence, answer))
                        print("Правильный ответ:    ")
                        print(f"{dict_all_sentences[ru_sentence][0]} ({dict_all_sentences[ru_sentence][2]})")
                        print("{0} - \033[92m{1}\033[03m\033[00m".format(ru_sentence, en_sentence))
                        w = input(f'\033[96m{"Записать в историю?    "}\033[00m') # только 'y'
                        if w == 'y':
                            counter_wrong_answers += 1
                            training_history.writelines(f"IT'S WRONG! ({counter_wrong_answers} из ({len(all_ru_sentences)} выбранных, {count} предложенных, {counter} решённых))\n")
                            training_history.writelines(f"{ru_sentence} - {answer}\n")
                            training_history.writelines("Правильный ответ:\n")
                            training_history.writelines(f"{dict_all_sentences[ru_sentence][0]} ({dict_all_sentences[ru_sentence][2]})\n")
                            training_history.writelines(f"{ru_sentence} - {en_sentence}\n\n")
                            training_history.flush()
                            history_mistakes[f'{counter_wrong_answers}'] = [f'WRONG - {answer}', f'{ru_sentence}', f'{en_sentence}']
                else:
                    if '--measure-speed' in sys.argv:
                        t1 = datetime.now().timestamp()
                    answer = input("{0} \u001b[38;5;8m\033[03m\033[02m{1}\033[00m - ".format(counter,ru_sentence)) # counter, ru_sentence
                    if '--measure-speed' in sys.argv:
                        t2 = datetime.now().timestamp()
                counter_input_symbols += len(answer)
                measure_speed_result_time += (t2 - t1)
                if '--show-time-every-sentence' in sys.argv:
                    print(f'Количество символов:   {len(answer)}')
                    print(f'На ввод затрачено сек.:   {round((t2 - t1), ndigits=2)}')
                    print('')
            if counter == count:
                training_history.writelines(f'Из {len(all_ru_sentences)} выбранных, {count} предложенных и {counter} решённых предложений {len(history_mistakes)} НЕВЕРНЫ!\n')
                training_history.writelines(f'Общее количество введённых символов:   {counter_input_symbols}\n')
                training_history.writelines(f'Общее количество затраченного времени на печать:   {round(measure_speed_result_time, ndigits=1)} сек.\n')
                training_history.flush()
                print('\nУпражнение окончено.')
                print(f'Из {len(all_ru_sentences)} выбранных, {count} предложенных и {counter} решённых предложений {len(history_mistakes)} НЕВЕРНЫ!')
                print(f'Общее количество введённых символов:   {counter_input_symbols}\n')
                print(f'Общее количество затраченного времени на печать:   {round(measure_speed_result_time, ndigits=1)} сек.\n')
                exit()
            sleep(1)
except (KeyboardInterrupt, EOFError): # ^C или ^D
    training_history.writelines(f'Из {len(all_ru_sentences)} выбранных, {count} предложенных и {counter} решённых предложений {len(history_mistakes)} НЕВЕРНЫ!\n')
    training_history.writelines(f'Общее количество введённых символов:   {counter_input_symbols}\n')
    training_history.writelines(f'Общее количество затраченного времени на печать:   {round(measure_speed_result_time, ndigits=1)} сек.\n')
    training_history.flush()
    print('\n\nВыполнение упражнения прервано.')
    print(f'Из {len(all_ru_sentences)} выбранных, {count} предложенных и {counter} решённых предложений {len(history_mistakes)} НЕВЕРНЫ!')
    if '--measure-speed' in sys.argv:
        print(f'Общее количество введённых символов:   {counter_input_symbols}')
        print(f'Общее количество затраченного времени на печать:   {round(measure_speed_result_time, ndigits=1)} сек.')
except (IndexError, ValueError) as error:
    h()
finally:
    #print('Урок окончен.')
    training_history.close(); del training_history
