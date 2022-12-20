# Random Music Generator and Visualizer

This is the project for ECE-GY 6183 DSP Lab.  <br />
Generates a random music clip under specific rules.
Opens a generated music clip randomly or a local .wav file,  displays the circulated plot in the visualizer.

## Prerequisites
This project is written in Python 3.10. <br />
Libraries used: [Librosa](https://librosa.org/), [MIDIUtil](https://github.com/MarkCWirt/MIDIUtil), [Mido](https://mido.readthedocs.io/en/latest/),
[NumPy](https://numpy.org/), [PyDub](https://github.com/jiaaro/pydub), [PyGame](https://github.com/pygame/pygame),
[tkinter](https://docs.python.org/3/library/tkinter.html).
Could be installed using ```pip``` or ```homebrew```.

## Run the program
Simply run ```main.py```. <br />
A standard MIDI file will be generated and then converted to a wav file in the *music_clips* folder. The filename is output_{date}.mid. <br />
A dialog window would appear, asking the user to *Open a wav file* or *Play a random clip*.  <br />
Close the dialog window, the music visualizer would appear and play the previously chosen wav file or randomly picked music clip. <br /><br />
The music visualizer looks like the following, the figure in the [PyGame](https://github.com/pygame/pygame) window would change simultaneously with the output of the signal. <br />
![Screenshot 2022-12-07 at 11 02 41 AM](https://user-images.githubusercontent.com/77599569/208757991-df9c22b6-2bcb-4058-b81b-f05e67b66034.png)

## Structure of the project
####  ```config/notes.json```
*config/notes.json* is the JSON file that defines the attributes of the music note that we later generate in the *note_generator.py*. <br />
<br />
*degrees*: the octave that the music clip is based on.<br />MIDI notes for the C5 octave are 84(C5), 74(D4), 76(E4), 77(F4), 79(G4), 81(A4), 83(B4)
<br /><br />

*chords*: note sequences that form chords for the music clip.
The Major C chord has Major C, E, and G music notes. 
We used two Major C chords, one is C4(72), E3(64), G3(67), the other is C4(72), E4(76), G4(79). Notes in each array would be played simultaneously.
<br /><br />

*tones*: the rhythm pattern. <br/>
Rhythm combines strong beats and weak beats. 
Strong beats include the first beat of each measure (the downbeat) and other heavily accented beats. 
The music combines strong beats and weak beats to create rhythmic patterns. 
The numbers are in beats (quarter notes) and 0.25, 0.5, and 1 represent quarter notes, half notes, and whole notes, respectively.
<br /><br />

*upper*: the upper bound of the interval of music notes
<br /><br />
*lower*: the lower bound of the interval of music notes
<br /><br />
*beats*: the beats per minute (BPM), indicating the number of beats in one minute. Define the BPM for strong, moderate, and weak beats.

####  ```config/settings.json```
Parameters (duration, tempo, and volume) for the music clip.

####  ```note_generator.py```
```note_generator.py``` generates a list of notes randomly according to the parameters given in the ```config/notes.json```.
It creates a class ```Note```. The ```Note``` object has three attributes: ```octave```, ```lower``` and ```upper```. 
The octave attribute is the octave for this note. The three attributes match the degrees, lower and upper fields in the config/notes.json, respectively.
The ```Note``` class has two functions, one for generating a single note and appending it to the list, and one for initializing a new note.


####  ```music_generator.py```
```music_generator.py``` generates a music clip, using the ```Note``` class from the ```note_generator.py```. <br/>
It creates the class ```MusicClip``` with a number of functions.  <br/>
The ```create_sequence()``` function adds the attributes of the pitch and the duration of each note inside a list.  <br/>
The ```initialize_single_track()``` function assigns the track name, adds a tempo, and a program change event.  <br/>
The ```create_basic_track()``` function generates a track with strong, moderate, and weak beats to form a rhythm.  <br/>
The ```create_chord_track()``` function generates a chord. <br/>
The ```create_midi_file()``` function calls the ```create_basic_track()``` and  ```create_chord_track()``` functions and adds these two tracks 
and writes the MIDI file that contains the music clip. 



####  ```converter.py```
```converter.py``` converts a MIDI file to a wav file according to the MIDI tuning standard. <br/>
After the data format is changed, the output wav file is written to the folder *music_clips* with a suffix of the date the wav file was created. <br/>
 

####  ```player_dialog.py```
```player_dialog.py``` creates a dialog user interface using [tkinter](https://docs.python.org/3/library/tkinter.html). <br/>
It has two buttons on the GUI window, one for the user to choose to open a wav file locally or play a random music clip that our project has generated. The root of the window is initialized in the ```main.py```. <br/>
The event listener of opening a local wav file button limits the file type to wav files only and uses functions provided by the filedialog from [tkinter](https://docs.python.org/3/library/tkinter.html) to open this file. <br/>


####  ```visualizer_components.py```
```visualizer_components.py``` creates classes of ```MusicAnalyzer```, ```BasicBar```, ```SimpleBar```, ```RotatedBar```, and ```Rectangle```.
<br/>```BasicBar``` creates a basic bar. Each bar represents a frequency, and the height represents the amplitude of the frequency.
<br/>```SimpleBar``` groups a number of ```BasicBar``` objects together. Given a small time difference, we could get the new decibel after the small time difference and update the shape of the bar.
<br/>```RotatedBar``` inherits the attributes of ```SimpleBar```, and is built around a circle, with angles specified. Thus, we need the bars to rotate for an angle so they can root at the circle.
<br/>```Rectangle``` is the shape of the ```RotatedBar```, and the width and height are updated to match the audio signal. The rotation of the rectangle is also updated.
<br/>```MusicAnalyzer``` analyzes the piece of audio with the library [librosa](https://librosa.org/) by generating a decibel-based spectrogram so that the decibel of a specific timestamp and frequency could be retrieved.



####  ```music_visualizer.py```
```music_visualizer.py``` uses [PyGame](https://github.com/pygame/pygame) to generate the music visualizer window.
<br />It takes the ```MusicAnalyzer``` class from ```visualizer_components.py``` for audio signal processing. 
<br />It contains parameters for setting up the window and  creates custom frequency patterns for the bars as a technique to show the frequency bars differently. 


####  ```main.py```
```main.py``` uses the class objects and functions from the above python files. <br />
It first creates a random music clip, then opens the music player dialog for the user to choose a local wav file or play a music clip randomly from the *music_clips* folder. After the dialog window is closed, the music visualizer window would appear, displaying real-time signals and playing the music simultaneously.


