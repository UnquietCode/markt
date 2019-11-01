#!/bin/bash

fonts=$(pyfiglet -l)

IFS=$'\n'
fonts=($fonts)

for font in "${fonts[@]}"; do
  echo "$font\n\n"
  pyfiglet -f "$font" hello
  echo "\n"
done
