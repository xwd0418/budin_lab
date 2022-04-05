from ij import IJ
from ij.io import FileSaver
import os
from os import path
from ij.process import ImageProcessor
from ij.plugin import ImageCalculator

"""
0. Select folder and test if the folder exists
IMPORTANT: Path format is different for different operating systems
Note: Make sure folder name is in quotes (" ")
"""
folder = "C:\" # INSERT FOLDER NAME HERE

if path.exists(folder) and path.isdir(folder):
	print "folder exists:", folder
else:
	print "Folder does not exist or it's not a folder!"

"""
1. Select Images
	1.1 Create parameters to select files
	1.2 Select/assign Golgi marker (golgi), Laurdan 440 (l440), and Laurdan 490 (l490) images
"""

# 1.1 Create parameters
#@ File(label='golgi image') golgi
#@ File(label='laurdan 440 image') l440
#@ File(label='laurdan 490 image') l490
#@ String(label='Stack', description='Enter stack number') stack


# 1.2 Assign images to variables
golgi = IJ.openImage(golgi.getAbsolutePath())
l440 = IJ.openImage(l440.getAbsolutePath())
l490 = IJ.openImage(l490.getAbsolutePath())

"""
2. Create mask (
	2.1 Make binary, then save as golgi255
	2.2 Divide by 255 to get only 0 and 1, save as golgibinary
"""
# 2.1
golgi.show()
IJ.run("Convert to Mask")

# Test if golgi255 exists before attempting to save the image
filepath = folder + "\" + stack + "_golgi255.tif" # Operating System-specific
if path.exists(filepath):
	print "File exists! Not saving the image, would overwrite a file!"
elif FileSaver(golgi).saveAsTiff(filepath): # Format: "name of save function".saveAsTiff
	print "File saved successfully at ", filepath

# 2.2
golgi255name = stack + "_golgi255.tif"
golgi255 = IJ.openImage(os.path.join(folder, golgi255name))

IJ.run(golgi255, "Divide...", "value=255.000")

# Test if golgibinary exists before attempting to save the image:
filepath = folder + "\" + stack + "_golgibinary.tif"
if path.exists(filepath):
	print "File exists! Not saving the image, would overwrite a file!"
elif FileSaver(golgi255).saveAsTiff(filepath):
	print "File saved successfully at ", filepath

binaryname = stack + "_golgibinary.tif"
golgibinary = IJ.openImage(os.path.join(folder, binaryname))

"""
3. Apply Laurdan images to mask
	3.1 Multiply mask (golgibinary) by l440, then save
	3.2 Multiply mask by l490, use in the next step
"""

# 3.1
createI440 = ImageCalculator().run("Multiply create", golgibinary, l440)

# Test if the image exists before attempting to save the image:
filepath = folder + "\" + stack + "_I440.tif" # CHECK NAME
if path.exists(filepath):
	print "File exists! Not saving the image, would overwrite a file!"
elif FileSaver(createI440).saveAsTiff(filepath): # CHECK SAVE FUNCTION NAME
	print "File saved successfully at ", filepath

I440name = stack + "_I440.tif"
I440 = IJ.openImage(os.path.join(folder, I440name))

# 3.2
createI490 = ImageCalculator().run("Multiply create", golgibinary, l490)

"""
4. Calculate GP
	4.1 Multiply I490 by G value (input manually), save as GI490
	4.2 Find top part of GP (I440 - GI490), save as sub
	4.3 Find bottom part of GP (I440 + GI490), save as add
	4.4 Divide sub by add, save final result as GP
"""

#4.1
createI490.show()
IJ.run("Multiply...")

# Test if the image exists before attempting to save the image:
filepath = folder + "\" + stack + "_GI490.tif" # CHECK NAME
if path.exists(filepath):
	print "File exists! Not saving the image, would overwrite a file!"
elif FileSaver(createI490).saveAsTiff(filepath): # CHECK SAVE FUNCTION NAME
	print "File saved successfully at ", filepath

GI490name = stack + "_GI490.tif"
GI490 = IJ.openImage(os.path.join(folder, GI490name))

# 4.2
GP_top = ImageCalculator().run("Subtract create", I440, GI490)

# Test if sub exists before attempting to save the image:
filepath = folder + "\" + stack + "_sub.tif"
if path.exists(filepath):
	print "File exists! Not saving the image, would overwrite a file!"
elif FileSaver(GP_top).saveAsTiff(filepath):
	print "File saved successfully at ", filepath

subname = stack + "_sub.tif"
sub = IJ.openImage(os.path.join(folder, subname))

# 4.3
GP_bottom = ImageCalculator().run("Add create", I440, GI490)

# Test if add exists before attempting to save the image:
filepath = folder + "\" + stack + "_add.tif"
if path.exists(filepath):
	print "File exists! Not saving the image, would overwrite a file!"
elif FileSaver(GP_bottom).saveAsTiff(filepath):
	print "File saved successfully at ", filepath

addname = stack + "_add.tif"
add = IJ.openImage(os.path.join(folder, addname))

# 4.4 Divide top by bottom
createGP = ImageCalculator().run("Divide create 32-bit", sub, add)

# Test if GP exists before attempting to save the image:
filepath = folder + "\" + stack + "_GP.tif"
if path.exists(filepath):
	print "File exists! Not saving the image, would overwrite a file!"
elif FileSaver(createGP).saveAsTiff(filepath):
	print "File saved successfully at ", filepath

GPname = stack + "_GP.tif"
GPfinal = IJ.openImage(os.path.join(folder, GPname))

"""
5. Display & save histogram
"""
IJ.run(GPfinal, "Histogram", "bins=256 use x_min=0 x_max=0.46 y_max=Auto")

imphist = IJ.getImage()

filepath = folder + "\" + stack + "_histogram.tif" # CHECK NAME
if path.exists(filepath):
	print "File exists! Not saving the image, would overwrite a file!"
elif FileSaver(imphist).saveAsTiff(filepath): # CHECK SAVE FUNCTION NAME
	print "File saved successfully at ", filepath