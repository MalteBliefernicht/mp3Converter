# mp3Converter

A very simple app that converts mp4, m4a, flac, ogg and wav files to mp3.
In the past I had trouble finding a reliable free program for this task and I also wanted to work with audio files.
The main challenge was finding a way to get the audiosegment module to work with all types of characters.
Simply decoding them wouldn't work.
In the end I resorted to decoding the names of the files I wanted to convert, copying them into a temp folder,
using those files for the conversion and then deleting the temp folder.
Probably not very efficient, but at least reliable.
