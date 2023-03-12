#!/usr/bin/env bash
# Скрипт должен быть вызван с параметром в виде искомого слова

for f in `ls -R ~/ENGLISH/ | grep 'dictionary' | grep 'txt'`; do
  file=`cat --number ~/ENGLISH/*/*/"$f"`;
  word=`echo "$file" | grep "$1"`;
  if [[ "$word" ]]; then
    echo ~/ENGLISH/*/*/"$f" && echo "$word";
  fi
done
