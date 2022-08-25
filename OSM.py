import tkinter as tk
from tkinter import filedialog as fd 
from tkinter import SUNKEN, RAISED, END
import oeFile as oeF
oeFileData = oeF

spagheterationLevel	= '0.0.3'


#window	and	memory init
class osmMain(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self._frame	= None
		self.switch_frame(mainWindow)

	def switch_frame(self, frame_class):
		new_frame =	frame_class(self)
		if self._frame is not None:
			self._frame.destroy()
		self._frame	= new_frame
		self._frame.pack()

	#globals
	saveFileFrom			= None
	saveFileFromContent	= None
	saveFileTo				= None
	saveFileToContent		= None
	saveFileIntermediate	= None
	fileContent 			= None

#start page
class mainWindow(tk.Frame):
	def __init__(self,master):
		tk.Frame.__init__(self,master)
		tk.Label(self, text="Welcome!").						pack(side="top", fill="x",	pady=10)
		tk.Button(self,	text="About",					command=lambda: master.switch_frame(aboutWindow)).pack()
		tk.Button(self,	text="Copy",					command=lambda: master.switch_frame(copyWindow)).pack()
		tk.Button(self,	text="Comb",					command=lambda: master.switch_frame(combWindow)).pack()

#background
class aboutWindow(tk.Frame):
	def __init__(self,master):
		tk.Frame.__init__(self,master)
		tk.Label(self, text="OE-Cake Save Manager\nOSM\n\nOSM is intended to make OE-Cake more accessible\nby offloading the tedious, difficult, and error-prone advanced\ntechniques that allow it to be so much more than a\nsimple physics sandbox").pack(side="top", fill="x", pady=10)
		tk.Button(self,	text="Main Menu",				command=lambda: master.switch_frame(mainWindow)).pack()

#basic copy
class copyWindowDesc(tk.Frame):
	def __init__(self,master):
		tk.Frame.__init__(self,master)
		tk.Label(self, text="The \"Copy\" function is a quick and dirty way\nto move simple arrangements of particles from\n one save to another. It preserves joins in the To\nsave but is not capable of copying Elastic or Rigid safely at this time.").pack(side="top", fill="x", pady=10)
		tk.Button(self,	text="Back",					command=lambda:	master.switch_frame(copyWindow)).pack()
		
class copyWindow(tk.Frame):
	def __init__(self,master):
		tk.Frame.__init__(self,master)

		self.openFrom =	tk.Button(self, text="From",	command = self.openFileFrom)
		self.openFrom.pack(side="left")

		self.openTo	= tk.Button(self, text="To",			command = self.openFileTo)
		self.openTo.pack(side="right")

		self.printD	= tk.Button(self, text="Copy",		command = self.printD)
		self.printD.pack(side="bottom",fill="x")

		tk.Button(self,	text="About",					command=lambda: master.switch_frame(copyWindowDesc)).pack(side="top")
		tk.Button(self,	text="Main Menu",				command=lambda: master.switch_frame(mainWindow)).pack(side="top")

	#open	from
	def openFileFrom(self):
		osmMain.saveFileFrom = fd.askopenfilename(title="From:")
		with open(osmMain.saveFileFrom, "r") as fileFrom:
			osmMain.saveFileFromContent = fileFrom.read()

	#open	to
	def openFileTo(self):
		osmMain.saveFileTo = fd.askopenfilename(title="To:")
		with open(osmMain.saveFileTo, "r+") as fileTo:
			osmMain.saveFileToContent = fileTo.read()

#simple copy
	def printD(self):
		
		#lists
		particleListA	= []
		joinListA		= []
		parameterListA	= []
		commentListA	= []
		scriptListA		= []
		lineCountA		= 0
		lineListA		= []

		particleListB	= []
		joinListB		= []
		parameterListB	= []
		commentListB	= []
		scriptListB		= []
		lineCountB		= 0
		lineListB		= []

		#shorthand
		profileContent			= copyWindow.profileContent
		saveFileFromContent	= osmMain.saveFileFromContent
		saveFileToContent		= osmMain.saveFileToContent
		saveFileTo				= osmMain.saveFileTo
		
		#misc
		newLine			= "\n"

		#catch characterizations
		try:
			particleListA,joinListA,parameterListA,commentListA,scriptListA,lineCountA,lineListA = profileContent(mainWindow,saveFileFromContent)
		except IndexError:
				mainWindow.feedback.configure(text="File: From is empty!")
		try:
			particleListB,joinListB,parameterListB,commentListB,scriptListB,lineCountB,lineListB = profileContent(mainWindow,saveFileToContent)
		except IndexError:
				mainWindow.feedback.configure(text="File: To is	empty!")

		newSize = lineCountB + len(particleListA)

		#stringOut = ('%s %d %s' % ('Done:',parameterListB,'lines.'))
		#stringOut = lineCountA
		#mainWindow.display.configure(text=lineListB[3])

		#write file
		with open(saveFileTo, 'w') as toSave:

			#vars
			charIterA		= 0
			charIterB		= 0
			lineCountOut	= 0
			lineCountA		= 0
			lineCountB		= 0
			lineBufferA		= []
			lineBufferB		= []

			charIterA	= lineListA[1]+1

			#write lines to new file
			while	lineCountOut < newSize:

				#insert	header and particles from target
				if lineCountOut	<= len(particleListB)+1: #copy up to end of	particles
					if charIterB <= lineListB[len(particleListB)+1]:
						if saveFileToContent[charIterB]	!= newLine:
							lineBufferB+=saveFileToContent[charIterB]
						else:
							lineBufferB+=saveFileToContent[charIterB]
							toSave.write(''.join(lineBufferB))
							lineBufferB =[]
							lineCountOut+=1
						charIterB+=1

				#insert	particles from source
				if lineCountOut > len(particleListB)+1 and lineCountOut <= (len(particleListB)+2+len(particleListA)):

#					print('a',ord(saveFileFromContent[lineListA[len(particleListA)+1]]))
					if (charIterA > lineListA[1]) and (charIterA <= lineListA[len(particleListA)+1]+1): #skip	header,	then copy particles	only
						if saveFileFromContent[charIterA] != newLine:
							lineBufferA+=saveFileFromContent[charIterA]
						else:
							lineBufferA+=saveFileFromContent[charIterA]
							toSave.write(''.join(lineBufferA))
							lineBufferA = []
							lineCountOut+=1
						charIterA+=1
					elif charIterA <= lineListA[1]:#seek to start
						charIterA = lineListA[1]+1

				#insert	remainder of data from target
				if lineCountOut	>= (len(particleListB)+2+len(particleListA)) and lineCountOut <	newSize:
					if charIterB >= lineListB[len(particleListB)+1] and charIterB	<= lineListB[len(lineListB)-1]:	#copies	starting at	first join till	end
						if saveFileToContent[charIterB]	!= newLine:
							lineBufferB+=saveFileToContent[charIterB]
						else:
							lineBufferB+=saveFileToContent[charIterB]
							toSave.write(''.join(lineBufferB))
							lineBufferB = []
							lineCountOut+=1
						charIterB+=1
					elif charIterB < lineListB[len(particleListB)+2]:#seek to	start
						charIterB = lineListB[len(particleListB)+2]

	#basic characterization
	def profileContent(mainWindow,fileIn):
		#counters
		particleCount	= 0
		joinCount		= 0
		parameterCount	= 0
		commentCount	= 0
		scriptCount		= 0
		lineCount		= 0

		#lists
		particleList	= []
		joinList		= []
		parameterList	= []
		commentList		= []
		scriptList		= []
		lineList		= []
		stringOut		= ""

		###profile da lines mon
		##parse	line structure
		#vars
		line:		str	= []
		lineList:	int = []
		lineFlag:	bool= 0
		currentChar:str	= ''
		charIter:	int = 0

		#consts
		fileSize	=	len(fileIn)
		newLine		=	"\n"

		#sanity	check
		if fileIn[fileSize-1] != newLine:
			fileIn = fileIn +	newLine

		#iterate through fileIn	character by character
		while charIter<fileSize:

			#parse by	newline
			currentChar		= fileIn[charIter]
			if currentChar	==	newLine:

				#count + record	newline	locations, flag	complete lines
				line.append(currentChar)
				lineList.append(charIter)

				#analyze complete lines
				if line[0] == oeFileData.comment.identifier:
					commentCount +=1
					commentList.append(lineCount)
				elif line[0] ==	oeFileData.particle.identifier:
					particleCount	+=1
					particleList.append(lineCount)
				elif line[0] ==	oeFileData.join.identifier:
					joinCount	+=1
					joinList.append(lineCount)
				elif line[0] ==	oeFileData.parameter.identifier:
					parameterCount +=1
					parameterList.append(lineCount)
				else:
					if lineCount != 0	and	lineCount != 1:
						scriptCount	+=1
						scriptList.append(lineCount)

				#prep iters	for	next line
				lineCount	+=1
				charIter	+=1
				line		=[]

			else:
				#concatonate chars into	line
				line.append(currentChar)
				charIter+=1

			#end charIter
		return (particleList,joinList,parameterList,commentList,scriptList,lineCount,lineList)

#robert's comb
class combWindowDesc(tk.Frame):
	def __init__(self,master):
		tk.Frame.__init__(self,master)
		tk.Label(self,	text="The \"Comb\" function repairs spin-charged Elastic\nwhile preserving the original lattice structure.\nFor the time being this function can only comb Elastic.\nThe process is ~~slow~~ so pls be patient, visual feedback will be added in the future.").pack(side="top", fill="x", pady=10)
		tk.Button(self,text="Back"	,command=lambda:	master.switch_frame(combWindow)).pack()

class combWindow(tk.Frame):
	#environment vars
	elasticList:		int = []
	viscousList:		int = []
	fileIn:				str
	flagEB=flagV=flagAll = 0

	def __init__(self,master):
		tk.Frame.__init__(self,master)

		#configure inputs
		self.About 				= tk.Button(self, text="About"					,command=lambda:	master.switch_frame(combWindowDesc))
		self.About.pack()

		self.main 				= tk.Button(self, text="Main Menu"				,command=lambda: master.switch_frame(mainWindow))
		self.main.pack()

		self.select				= tk.Button(self, text="Select File"				,command=self.targetFile)
		self.select.pack()

		self.combFile 			= tk.Button(self, text="Comb!"					,command=self.combFile)
		self.combFile.pack()

	#target file
	def targetFile(self):
		osmMain.saveFileTo = fd.askopenfilename(title="Target File:")
		with open(osmMain.saveFileTo, "r+") as fileTarget:
			combWindow.fileIn=osmMain.fileContent = fileTarget.read()
			oeF.parseFile(combWindow.fileIn)
			

	#combing procedure 
	def combFile(self):
		oeF.combFile(osmMain.fileContent)
		
#main loop
if __name__	== "__main__":
	osm =	osmMain()
	osm.title("OctaveEngine Save Manager")
	osm.mainloop()

