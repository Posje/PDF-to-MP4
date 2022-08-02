#!/usr/bin/bash

pdftoppm frames.pdf -png frame
ffmpeg -r 8 -i frame-%01d.png video.mp4
