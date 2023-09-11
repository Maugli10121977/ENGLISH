#!/usr/bin/env bash

for (( f=$1; f<=$2; f++ )); do
  echo "";
  echo "Lesson $f";
  cat -n ~/ENGLISH/titan_course/$f/dictionary_$f.txt;
done
