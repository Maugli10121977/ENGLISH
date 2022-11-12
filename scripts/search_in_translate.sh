#!/usr/bin/env bash
# Скрипт должен быть вызван с параметром в виде искомого слова

for f in `ls -R ~/ENGLISH/ | grep 'translate' | grep 'txt'`; do
  file=`cat --number ~/ENGLISH/*/*/*/"$f"`;
  sentence=`echo "$file" | grep "$1"`;
  if [[ "$sentence" ]]; then
    echo "";
    echo ~/ENGLISH/*/*/*/"$f" && echo "$sentence";
  fi
done
