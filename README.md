Laurdan quantification – Python Script (laurdanfinal.py)

Usage:
Open the script in FIJI.
Change the folder name (line 10) to the folder you want to save the images in.
(see below for path format for Windows and MacOS)
For Windows: Make sure all forward slashes (/) are backslashes (\)
Click “Run”.
In the pop-up window, select the golgi, Laurdan 440, and Laurdan 490 images, input the stack number, then click “OK”.
Midway through the script, a pop-up window titled "Multiply" will appear; input the 
G-value here, then click “OK”.
After this, you can see if the files have been saved and the GP histogram will appear.

Notes:
The script will save a total of eight (8) .tif files (names and descriptions below)
golgi255: Result of running Process---Binary
golgibinary: Result of dividing golgi255 by 255, will only have 0 and 1
I440: Result of multiplying Laurdan 440 x golgibinary
GI490: Result of multiplying G-value to the result of Laurdan 490 x golgibinary 
sub: Result of I440 – GI490
add: Result of I440 + GI490
GP: Final GP image
histogram: Histogram of GP
The stack number allows us to keep track of which stack each image/file came from
For example, the filename of the final GP image of stack 7 will be called “7_GP”

