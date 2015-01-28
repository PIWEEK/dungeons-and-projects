#!/bin/sh
dia -t png -s 400x -O . architecture.dia
convert architecture.png -gravity center -extent 105%x105% architecture.png

