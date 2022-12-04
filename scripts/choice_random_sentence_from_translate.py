#!/usr/bin/env python
import os
#import sys
from datetime import datetime
from random import shuffle
from time import sleep

root_directory = '/data/data/com.termux/files/home/ENGLISH/titan_source/part_0'
if 'training_history.txt' not in os.listdir(root_directory):
    training_history = open(f'{root_directory}/training_history.txt','w')
    training_history.close()
os.chdir(root_directory)

list_sentences = []
count = 0

for directory in os.listdir():
    if os.path.isdir(directory):
        for file in os.listdir(directory):
            if 'translate' in file:
                with open(f'{directory}/{file}', 'r') as f:
                    list_sentences += f.readlines()

shuffle(list_sentences)

try:
    training_history = open(f'{root_directory}/training_history.txt', 'a')
    while True:
        date_time = datetime.now()
        training_history.writelines('*' * 40 + '\n')
        training_history.writelines(date_time.strftime("%Y-%m-%d %H:%M:%S\n\n"))
        training_history.flush()
        print(f"Найдено {len(list_sentences)} предложений.")
        for i in list_sentences:
            count += 1
            if '*' not in i:
                ru_sentence = i.split(' - ')[0]
                en_sentence = i.split(' - ')[-1].rstrip('\n')
                answer = input(f"{count} {ru_sentence} - ")
                if en_sentence and answer not in en_sentence.split(' / '):
                    training_history.writelines("НЕВЕРНО!\n")
                    training_history.writelines(f"{ru_sentence} - {answer}\n")
                    training_history.writelines("Правильный ответ:\n")
                    training_history.writelines(f"{ru_sentence} - {en_sentence}\n\n")
                    training_history.flush()
                    print("")
                    print("\033[93m{0}\033[06m\033[00m".format("НЕВЕРНО!"))
                    print("{0} - \033[91m{1}\033[05m\033[00m".format(ru_sentence, answer))
                    print("Правильный ответ:    ")
                    print("{0} - \033[92m{1}\033[03m\033[00m".format(ru_sentence, en_sentence))
                    print("")
                sleep(1)
except KeyboardInterrupt: # ^C
    print('\nВыполнение прервано.')
finally:
    print('\nУрок окончен =)')
    training_history.close()
    exit()
