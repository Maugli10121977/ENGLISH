#!/usr/bin/env bash

for (( f=$1; f<=$2; f++ )); do
  echo "********************************";
  echo "Урок $f";
  cat ~/ENGLISH/titan_course/$f/README_$f.txt;
  echo "";
done
