#!/usr/bin/env python

from psychopy import visual, event, core
import scipy.misc as smp
import numpy as np
import math
import os
import random
import time
from useful_functions import *
import time
##########################################################################################
############################          SPECIFY PARAMETERS:          #######################
########################################################################################## 
# 1,4,7,10,13,16,19,22,25,28,31,34,37,40,43,46,49,52,55,58,61,64,
SubCode			  = ['S055','S058','S061', 'S064']
BaseImageFileName = "NFD_MC_v1_image_003_Final.png" # The base face (i.e., the background face)

##########################################################################################
#################################          PARAMETERS:          ##########################
########################################################################################## 
NumImages		= 400 # the number of .png to be created and saved
imageSize 		= 256 # pixels, use numbers^2
opacityValue 	= (1/12.0)
faceOpacity		= 0.5
grating_phase 	= [0.0]*6 + [math.pi/2]*6  # i.e., sine or cosine 
orientations 	= range(0,180,30)*2  
grating_hpos	= 0
grating_vpos	= 0

##########################################################################################
########          If SubCode is a list, check the entries are sensible:        ###########
########################################################################################## 
for i in range(0,len(SubCode)):
	if len(SubCode[i]) != 4 or SubCode[i][0] != 'S':
		print ('')	
		print '################################################################################'
		print ('WARNING: There is an issue with the following subject code:')
		print SubCode[i]
		print ('Code aborted')
		print '################################################################################'	
		print ('')	
		core.quit()

##########################################################################################
############          CHECK IF IMAGE ALREADY EXISTS (AND QUIT IF SO):          ###########
########################################################################################## 
# os.chdir('/Users/lewisforder/Dropbox/SharedFolders/LupyanExps/NFD/stimuli/testFaces')
os.chdir('C:/Users/LupyanLab/Pictures/NFD/NFD_v1/testFaces')
for i in range(0,len(SubCode)):
	if  os.path.isfile('NFD_v1_'+SubCode[i]+'_'+str(str(0).zfill(3))+'.png'):
		print ('')
		print '################################################################################'
		print ('WARNING: This subject code already exists:')
		print SubCode[i]
		print ('Code aborted')
		print '################################################################################'	
		print ('')	
		core.quit()
	else:
		print ('')
		print '################################################################################'
		print ('Subject code appears unique, commencing stimulus generation.')
		print '################################################################################'	
		print ('')	
		

##########################################################################################
#############################              FUNCTIONS:               ######################
##########################################################################################

def drawGrating(numTiles,spaFreq,grating_phase,orientations,opacityValue,grating_hpos,grating_vpos,dataSaveNames,outputFile,imageNumber,aperture_hpos,aperture_vpos,BaseImageFileName):
	for i in range(12):
		grating.sf 		 = spaFreq / imageSize
		singleContrast	 = np.random.uniform(-1,1)
		grating.contrast = singleContrast
		grating.phase 	 = grating_phase[i]
		grating.ori 	 = orientations[i]
		grating.opacity  = opacityValue	
		grating.pos 	 = [grating_hpos,grating_vpos]	
		grating.draw()
		data 			 = [SubCode]
		data.extend([imageNumber,numTiles,spaFreq, orientations[i],singleContrast,aperture_hpos,aperture_vpos,BaseImageFileName])
		writeToFile(outputFile,data,writeNewLine=True)


def defineAperture(apertureSize,aperture_posHor,aperture_posVer):
	aperture = visual.Aperture(win, size=apertureSize, pos=(aperture_posHor, aperture_posVer), ori=0, nVert=120, 
						shape='square', units=None, name=None, autoLog=None)
	return aperture


def getAperturePos(numTiles,numCycles):
	aperture_hpos 	= []
	hposIndex 		= range(int(-math.sqrt(numTiles))+1,int(math.sqrt(numTiles))+1,2)
	hposIndex 		= hposIndex[::-1]
	for i in range(int(math.sqrt(numTiles))):
		aperture_hpos.append(-(imageSize/numCycles)*hposIndex[i])
	aperture_hpos = aperture_hpos*int(math.sqrt(numTiles))

	aperture_vpos 		= []
	counter = 0
	vposIndex = range(int(-math.sqrt(numTiles))+1,int(math.sqrt(numTiles))+1,2)
	for i in range(int(math.sqrt(numTiles))):
		aperture_vpos.append(-(imageSize/numCycles)*vposIndex[i])

	positions = np.zeros((numTiles,2))
	counterA = -1
	counterB = 0
	for i in range(numTiles):
		positions[i,0] = aperture_hpos[i]
		positions[i,1] = aperture_vpos[counterB]
		counterA = counterA + 1
		if counterA == int(math.sqrt(numTiles))-1:
			counterB = counterB+1
			counterA = -1

	aperture_hpos = positions[:,0]
	aperture_vpos = positions[:,1]
	
	return(aperture_hpos,aperture_vpos)	
	

def defineAperDrawGrating(numTiles, numCycles,grating_phase,orientations,opacityValue,grating_hpos,grating_vpos,dataSaveNames,outputFile,imageNumber,BaseImageFileName):
	[aperture_hpos,aperture_vpos] = getAperturePos(numTiles,numCycles,)

	for k in range(numTiles):

		aperture = defineAperture(imageSize/(numCycles/2),aperture_hpos[k],aperture_vpos[k])

		win.blendMode = 'add'

		drawGrating(numTiles,float(numCycles),grating_phase,orientations,opacityValue,grating_hpos,grating_vpos,dataSaveNames,outputFile,imageNumber,aperture_hpos[k],aperture_vpos[k],BaseImageFileName)

		del(aperture)
	

##########################################################################################
#############################          CONFIGURE STIMULI:           ######################
##########################################################################################
startTime   = time.time()

for p in range(0,len(SubCode)):
	print 'Commencing'
	print p
	print 'of'
	print len(SubCode)

	winHeight 	= imageSize
	winLength 	= imageSize
	imageData 	= np.zeros((4092,7))
	headerOutputFileName = SubCode[p]+'_HeaderTitles'


	for n in range(NumImages):
		imageNumber    = str(str(n).zfill(3))
		imageSaveNames = 'NFD_v1_'+SubCode[p]+'_'+str(str(n).zfill(3))+'.png'
		dataSaveNames  = 'NFD_v1_'+SubCode[p]+'_'+str(str(n).zfill(3))+'_data'
		outputFile     = open(dataSaveNames+'.txt','w')

		headerTitles   = ['SubCode']
		headerTitles.extend(['imageNumber','numTiles','spaFreq', 'orientation','Contrast','aperture_hpos','aperture_vpos', 'BaseImageFileName'])
		writeToFile(outputFile,headerTitles,writeNewLine=True)

	
		win = visual.Window(
			size=[winLength, winHeight],
			units="pix",
			fullscr=False,
			allowGUI=False,
			allowStencil=True,
			blendMode='add',
			useFBO=True,
			color=[0, 0, 0])

		img = visual.ImageStim(
			win=win,
			image=BaseImageFileName,
			units="pix")

		img.opacity = faceOpacity
		img.draw()

		grating = visual.GratingStim(
			win=win,
			units='pix',
			tex='sin',    
			interpolate=True,
			size=[imageSize*2, imageSize*2])

	
		defineAperDrawGrating(1, 2,grating_phase,orientations,opacityValue,grating_hpos,grating_vpos,dataSaveNames,outputFile,imageNumber,BaseImageFileName)	
		defineAperDrawGrating(4, 4,grating_phase,orientations,opacityValue,grating_hpos,grating_vpos,dataSaveNames,outputFile,imageNumber,BaseImageFileName)
		defineAperDrawGrating(16, 8,grating_phase,orientations,opacityValue,grating_hpos,grating_vpos,dataSaveNames,outputFile,imageNumber,BaseImageFileName)
		defineAperDrawGrating(64, 16,grating_phase,orientations,opacityValue,grating_hpos,grating_vpos,dataSaveNames,outputFile,imageNumber,BaseImageFileName)
		defineAperDrawGrating(256, 32,grating_phase,orientations,opacityValue,grating_hpos,grating_vpos,dataSaveNames,outputFile,imageNumber,BaseImageFileName)


		win.getMovieFrame(buffer='back')
		win.saveMovieFrames(imageSaveNames)

		win.close()

	headerOutputFile = open(headerOutputFileName+'.txt','w')
	headerTitles	 = ['SubCode']
	headerTitles.extend(['imageNumber','numTiles','spaFreq', 'orientation','Contrast','aperture_hpos','aperture_vpos', 'BaseImageFileName'])
	writeToFile(headerOutputFile,headerTitles,writeNewLine=True)

endTime   = time.time()
totalTime = endTime-startTime

print '##########################'
print 'Code complete'
print 'You have generated this many images for each subject:'
print NumImages
print 'And it took this long to complete in minutes:'
print totalTime/60
print '##########################'