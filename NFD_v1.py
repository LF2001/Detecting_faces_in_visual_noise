#!/usr/bin/env python

############################
#  Import various modules  #
############################
from psychopy import core, visual, prefs, event
from baseDefsPsychoPy import *
from useful_functions import * 
from stimPresPsychoPy import *
import webbrowser as web
import socket
import os
############################
#  		Parameters         #
############################
BkgroundRGBs    = [0.0,0.0,0.0]
win				= visual.Window([1680,1050], monitor='testMonitor', color= BkgroundRGBs, units='pix', fullscr=False) #grey background
numTrials       = 400 
takeBreakEvery	= 100 # take a break every .. trials
IntroTextheight = 20
fixCrossTime	= 0.5
faceTime		= 1
ISI 			= 0.25 # interStimInverval
textheight 		= 30
cuePositions   = [[-250,0],[250,0]]
comparisonFacesDict = {'manSmile':'NFDv1_Man_smile_1', 'manNoSmile':'NFDv1_Man_nonSmile_1', 'womanSmile':'NFDv1_Woman_smile_1', 'womanNoSmile':'NFDv1_Woman_nonSmile_1', 'ratingScale': 'NFDv1_RatingScale'}
myPath         = os.getcwd()
############################
#  		Instructions       #
############################
instructions = '''
\n Thank you for participating. In this task you will be viewing pictures of faces that are very difficult to make out because they are embedded in visual noise.
\n For each image, you should indicate if you think it looks more like a male or a female face.
\n Following each response you will be asked to indicate your confidence from just guessing to completely sure.
\n If you have any questions you can ask the researcher now.
\n Please tell the researcher when you are ready and they will start the experiment.'''	

breakText = ''' Please take a break if you want to.
\n Press the RETURN key to resume'''

thankYou = ''' Thank you very much for taking part.
\n You have completed the main part of the study.
\n We would like you to answer some questions about this study.
\n This will take you a couple of minutes.
\n After you have completed the questionnaire you have finished this study.
\n Please press the RETURN key to open the questionnaire.'''

class NoiseFaceDetection:
	def __init__(self):
		expName = 'NFD_v1'
		self.validResponses = {'0':'escape','1':'left', '2':'right', '3':'return', '4':'1', '5':'2', '6':'3', '7':'4'}
		while True:
			runTimeVarOrder 	= ['subjCode', 'seed', 'gender', 'age', 'isWord', 'isML', 'isMH']
			self.runTimeVars 	= getRunTimeVars({'subjCode':'NFD_v1_S000', 'seed':999, 'gender':'male', 'age':0, 'isWord': ['Choose', '0','1'], 'isML': ['Choose', '0','1'], 'isMH': ['Choose', '0','1','2']},runTimeVarOrder,expName)
			if 'Choose' in self.runTimeVars.values():
				popupError('Need to choose a value from a dropdown box')
			else:
				self.outputFile = openOutputFile('data/'+self.runTimeVars['subjCode'],'')
				if self.outputFile:
					break

		self.surveyURL = 'https://docs.google.com/forms/d/e/1FAIpQLScT35xnV4omcOylW4aw4gZ2SlktJdMR1N-mHjWedL7eUrWn8w/viewform'
		self.runTimeVars['room'] = socket.gethostname().upper()
		self.surveyURL += '?entry.900342216=%s&entry.142747125=%s' % (self.runTimeVars['subjCode'], self.runTimeVars['room'])

        
        def RunExperiment(self):
                win                  = visual.Window([1680,1050], monitor='testMonitor', color= BkgroundRGBs, units='pix', fullscr=True) #grey background
		SubjectCodeStr 	     = exp.runTimeVars['subjCode']
		headerOutputFileName = SubjectCodeStr+'_dataHeaders'
		stimuliBaseFileName  = exp.runTimeVars['subjCode']+'*'
		os.chdir('C:/Users/LupyanLab/Pictures/NFD/NFD_v1')
		stimuli              = loadFiles('testFaces','.png','image', win=win,whichFiles=stimuliBaseFileName) # load stimuli png files specific to the subject code
		print stimuli
		comparisonFaces      = loadFiles('comparisonFaces','.png','image', win=win,whichFiles=u'NFDv1*') # load comparison faces (used if condition isWord==0)
		os.chdir(myPath)
		textMan              = visual.TextStim(win, pos = cuePositions[0],text = 'man',   height = textheight, color = 'black', units = 'pix')	
		textWoman            = visual.TextStim(win, pos = cuePositions[1],text = 'woman', height = textheight, color = 'black', units = 'pix')

		headerOutputFile = open(headerOutputFileName+'.txt','w')
		headerTitles	 = ['SubCode']
		headerTitles.extend(['seed','trialNum', 'imageFileName', 'isWord', 'isManLeft',
		 'isManHappy', 'keyPress', 'choiceStr', 'RT', 'ratingScore', 'ratingRT'])
		writeToFile(headerOutputFile,headerTitles,writeNewLine=True)	

		presentInstrucs = newText(win,instructions,pos=[0,0],color="black",scale=0.8)	
		presentInstrucs.draw()
		win.flip()
		getKeyboardResponse('return')
		win.flip()

		for i in range(numTrials):
			if (i+1) % takeBreakEvery==0:
				presentBreakText =newText(win,breakText,pos=[0,0],color="black",scale=0.8)					
				presentBreakText.draw()
				win.flip()
				getKeyboardResponse('return')

			core.wait(ISI)
			presentFixCross = newText(win,'+',pos=[0,0],color="black",scale=1.0)
			presentFixCross.draw()
			win.flip()
			core.wait(fixCrossTime)
			event.clearEvents()
			core.wait(ISI)

			imageFileName = SubjectCodeStr+'_'+str(str(i).zfill(3))
			stimuli[str(imageFileName)]['stim'].draw()	
			
 			if exp.runTimeVars['isWord'] == '1': # display words
 				if exp.runTimeVars['isML'] == '1':
 					textMan.pos   = cuePositions[0]
 					textWoman.pos = cuePositions[1]
 				elif exp.runTimeVars['isML'] == '0':
 					textMan.pos   = cuePositions[1]
 					textWoman.pos = cuePositions[0]

 			elif exp.runTimeVars['isWord'] == '0': # display images
 				if exp.runTimeVars['isMH'] == '1':
					if exp.runTimeVars['isML'] == '1':
						comparisonFaces[comparisonFacesDict['manSmile']]['stim'].setPos(cuePositions[0])
						comparisonFaces[comparisonFacesDict['womanNoSmile']]['stim'].setPos(cuePositions[1])
					elif exp.runTimeVars['isML'] == '0':
						comparisonFaces[comparisonFacesDict['manSmile']]['stim'].setPos(cuePositions[1])
						comparisonFaces[comparisonFacesDict['womanNoSmile']]['stim'].setPos(cuePositions[0])
 				elif exp.runTimeVars['isMH'] == '0':
					if exp.runTimeVars['isML'] == '1':
						comparisonFaces[comparisonFacesDict['manNoSmile']]['stim'].setPos(cuePositions[0])
						comparisonFaces[comparisonFacesDict['womanSmile']]['stim'].setPos(cuePositions[1])
					elif exp.runTimeVars['isML'] == '0':
						comparisonFaces[comparisonFacesDict['manNoSmile']]['stim'].setPos(cuePositions[1])
						comparisonFaces[comparisonFacesDict['womanSmile']]['stim'].setPos(cuePositions[0])
			win.flip()
			core.wait(faceTime)
			win.flip()
			
			if exp.runTimeVars['isWord'] == '1':
				textMan.draw()
				textWoman.draw()
			elif exp.runTimeVars['isWord'] == '0':
				if exp.runTimeVars['isMH'] == '1':
					comparisonFaces[comparisonFacesDict['manSmile']]['stim'].draw()
					comparisonFaces[comparisonFacesDict['womanNoSmile']]['stim'].draw()

				elif exp.runTimeVars['isMH'] == '0':
					comparisonFaces[comparisonFacesDict['manNoSmile']]['stim'].draw()
					comparisonFaces[comparisonFacesDict['womanSmile']]['stim'].draw()

			win.flip()
			(response,rt) = getKeyboardResponse(['left','right','escape'])
			if response == 'escape':
				win.close()
				core.quit()
			comparisonFaces[comparisonFacesDict['ratingScale']]['stim'].draw()
			win.flip()
			(rating,rtRating) = getKeyboardResponse(['1','2','3','4'])
			win.flip()

			
			if exp.runTimeVars['isML'] == '1' and response == 'left' or exp.runTimeVars['isML'] == '0' and response == 'right':
					choiceStr = 'male'
			elif exp.runTimeVars['isML'] == '0' and response == 'left' or exp.runTimeVars['isML'] == '1' and response == 'right':
					choiceStr = 'female'


			if exp.runTimeVars['isWord'] == '1':
				isMHappy = 999
			else:
				isMHappy = 	exp.runTimeVars['isMH']
			
			responses =[SubjectCodeStr]
			responses.extend([exp.runTimeVars['seed'],i, imageFileName, exp.runTimeVars['isWord'], 
			exp.runTimeVars['isML'], isMHappy, response, choiceStr, rt*1000, rating, rtRating*1000])
			writeToFile(self.outputFile,responses,writeNewLine=True)

		sayThankyou = newText(win,thankYou,pos=[0,0],color="black",scale=0.6)
		sayThankyou.draw()
		win.flip()
		getKeyboardResponse('return')


exp = NoiseFaceDetection()
exp.RunExperiment()
win	= visual.Window([1680,1050], monitor='testMonitor', color= BkgroundRGBs, units='pix', fullscr=False) #grey background
win.flip()
web.open(exp.surveyURL)
win.close()
core.quit()