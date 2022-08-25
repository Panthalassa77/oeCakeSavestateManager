import dataclasses
import OSM as OSM
from tkinter import filedialog as fd 


#tags
oeHeaderV2 		= '# OctaveEngine Casual (Jul 14 2008)\r\nversion 2'
oeHeaderV4 		= '# OctaveEngine Casual (May 27 2008)\r\nversion 4'
oeHeaderv10		= ''
activeHeader 	= oeHeaderV2

oecVersionA		= '1.1.2b'
oecVersionB		= '1.1.4'
fileIn:			str
parsedTempContent = []
rawContent:		str

#@dataclass()
#class oeFileContent:

#define	Octave Engine file structure + setup for calling	
@dataclasses.dataclass
class contentComment:
	content:		str = ''
	identifier:		str = '#'
	fileIndex: 		int = 0
comment: contentComment = contentComment()
	
@dataclasses.dataclass
class contentHeader:
	identifier:		str	= 'v'
	defaultHeader		= activeHeader
	content:		str	= ''
	fileIndex: 		int = 0
header: contentHeader	= contentHeader()

@dataclasses.dataclass
class	contentParticle:
	identifier:	str		='p'
	material:	int		= 0
	index:		int		= 0
	layer:		int		= 0xff
	color:		int		= 0xffffffff
	xPos:		float	= 0.0
	yPos:		float	= 0.0
	xVel:		float	= 0.0
	yVel:		float	= 0.0
	xOrg:		float	= 0.0
	yOrg:		float	= 0.0
	angle:		float	= 0.0
	angVel:		float	= 0.0
	pressure:	int		= 0
	content:	str		= ''
	fileIndex: int 	= 0
particle: contentParticle = contentParticle()

@dataclasses.dataclass
class contentJoin:
	identifier:	str		= 'j'
	index:		int		= 0
	a:			int		= 0
	b:			int		= 0
	proximity:	float	= 0.0
	offset:		float	= 0.0
	Xanchor:	float	= 0.0
	Yanchor:	float	= 0.0
	rot:		float	= 0.0
	unknown:	int		= 0
	content:	str		= ''
	fileIndex: int 	= 0
join: contentJoin = contentJoin()

@dataclasses.dataclass
class contentParameter:
	identifier:	str	= '@'
	variable:	str	= ''
	value			= None
	content:	str	= ''
	fileIndex: int = 0
parameter: contentParameter =	contentParameter()

@dataclasses.dataclass
class contentTexture:
	identifier:	str	= 'texture'
	index:		int	= 0
	name:		str	= ''
	a:			int	= 0
	b:			int	= 0
	c:			int	= 0
	d:			int	= 0
	content:	str	= ''
	fileIndex: int = 0
texture: contentTexture = contentTexture()

@dataclasses.dataclass
class contentScript:
	identifier:str = 's'
	content:	str	= ''
	fileIndex: 	int = 0
script: contentScript = contentScript()

#oeFile Functions
def parseFile(fileIn):
	#consts
	fileSize	=	len(fileIn)
	newLine		=	"\r\n"
	spaceChar	=	"\s"

	#vars
	line:			str = []
	lineList:		int = []
	lineFlag:		bool= 0
	lineIter:		int = 0
	lineCount:		int = 0
	currentChar:	str = ''
	charIter:		int = 0
	variableContent:str= []
	variableCount:	int = 0
	combFlag: 		bool= 0

#	oecFileContent = oeFileContent()
	

	#sanity	check
	if fileIn[fileSize-1] != newLine:
		fileIn = fileIn + newLine

	#iterate through fileIn character by character
	while charIter<fileSize:
		#parse by	newline
		currentChar	  = fileIn[charIter]
		if currentChar ==	newLine:
			#count + record locations of materials containing Elastic or Viscous
			line.append(currentChar)
			lineList.append(charIter)
			#analyze materials
#			if line[0] == oeFileContent.comment.identifier:
			if line[0] == particle.identifier:
				#parse material content
				lineIter = 0
				binMaterial: None
				while	lineIter < len(line):
					if line[lineIter] != spaceChar:
						variableContent.append(line[lineIter])
					else:
						variableCount	+=1
						if variableCount == 2:
							binMaterial	= bin(int(variableContent, 16))[2:].zfill(32)
							if binMaterial[4] == 1:
								combFlag = 1
							if binMaterial[21] == 1:
								combFlag = 1
						variableContent =	None
					lineIter+=1
			#prep iters	for	next line
			lineCount+=1
			charIter+=1
			line = []
		else:
			#concatonate chars into line
			line.append(currentChar)
			charIter+=1
	return (lineCount)

def readFile():
	eol 		= "\n"
	whiteSpace = ' '
	word 		= None
	wordCount: 	int = 0
	lineCount 	= 0
	global rawContent
	fileContent = rawContent
	
	#file content lists
	headerList 		= []
	particleList 	= []
	joinList 		= []
	parameterList 	= []
	textureList 	= []
	commentList 	= []
	scriptList 		= []
	
	fileStructure 	= []
	
	#prepare line
	line 			= ""
	wordCount 		= 0
	fileIter 		= 0
	
	while fileIter<len(fileContent):
		
		#input content
		if fileContent[fileIter] != eol:
			line = line + fileContent[fileIter]
		else:
			#do line stuff
			line = line + fileContent[fileIter]
			lineCount+=1
			
			#copy header content as-is
			if lineCount == 1:
				headerList.append(dataclasses.replace(header)) #creates new instance of header object and appends to list
				headerList[len(headerList) - 1].fileIndex = lineCount
				headerList[len(headerList) - 1].content = line
				line = ''
			elif lineCount == 2:
				headerList.append(dataclasses.replace(header)) #creates new instance of header object and appends to list
				headerList[len(headerList) - 1].fileIndex = lineCount
				headerList[len(headerList) - 1].content = line
				line = ''

			#parse remaining line content
			else:
				charCounter: int = 0
				wordCount = 0
				#parse Particle lines
				if line[0] == particle.identifier:
					#add new particle to list
					particleList.append(dataclasses.replace(particle)) #creates new instance of `particle` object and appends to list
					particleList[len(particleList) - 1].fileIndex = lineCount
					
					#word reader
					word = ""
					while charCounter < len(line):
						wordTemp = ""
						if line[charCounter] != whiteSpace and line[charCounter] != eol:
							tempChar = line[charCounter]
							wordTemp = word + tempChar
							word = wordTemp
							charCounter+=1
						else:
							wordCount+=1
							charCounter+=1
							if wordCount == 2:
								particleList[len(particleList) -  1].material = word
							elif wordCount == 3:
								particleList[len(particleList) -  1].index = word
							elif wordCount == 4:
								particleList[len(particleList) -  1].layer = word
							elif wordCount == 5:
								particleList[len(particleList) -  1].color = word
							elif wordCount == 6:
								particleList[len(particleList) -  1].xPos = word
							elif wordCount == 7:
								particleList[len(particleList) -  1].yPos = word
							elif wordCount == 8:
								particleList[len(particleList) -  1].xVel = word
							elif wordCount == 9:
								particleList[len(particleList) -  1].yVel = word
							elif wordCount == 10:
								particleList[len(particleList) -  1].xOrg = word
							elif wordCount ==11:
								particleList[len(particleList) -  1].yOrg = word
							elif wordCount == 12:
								particleList[len(particleList) -  1].angle = word
							elif wordCount == 13:
								particleList[len(particleList) -  1].angVel = word
							elif wordCount == 14:
								particleList[len(particleList) -  1].pressure = word
							word = ""
					
				#parse Join lines
				elif line[0] == join.identifier:
					#add new join to list
					joinList.append(dataclasses.replace(join))
					joinList[len(joinList) - 1].fileIndex = lineCount
					
					#word reader
					word = ""
					while charCounter < len(line):
						wordTemp = ""
						if line[charCounter] != whiteSpace and line[charCounter] != eol:
							tempChar = line[charCounter]
							wordTemp = word + tempChar
							word = wordTemp
							charCounter+=1
						else:
							wordCount+=1
							charCounter+=1
							if wordCount == 2:
								joinList[len(joinList) -  1].index = word
							elif wordCount == 3:
								joinList[len(joinList) -  1].a = word
							elif wordCount == 4:
								joinList[len(joinList) -  1].b = word
							elif wordCount == 5:
								joinList[len(joinList) -  1].proximity = word
							elif wordCount == 6:
								joinList[len(joinList) -  1].offset = word
							elif wordCount == 7:
								joinList[len(joinList) -  1].Xanchor = word
							elif wordCount == 8:
								joinList[len(joinList) -  1].Yanchor = word
							elif wordCount == 9:
								joinList[len(joinList) -  1].rot = word
							elif wordCount == 10:
								joinList[len(joinList) -  1].unknown = word
							word = ""
					
				#parse Parameter lines
				elif line[0] == parameter.identifier:
					#add parameter to list
					parameterList.append(dataclasses.replace(parameter))
					parameterList[len(parameterList) - 1].fileIndex = lineCount
					
					#word reader
					word = ""
					while charCounter < len(line):
						wordTemp = ""
						if line[charCounter] != whiteSpace and line[charCounter] != eol:
							tempChar = line[charCounter]
							wordTemp = word + tempChar
							word = wordTemp
							charCounter+=1
						else:
							wordCount+=1
							charCounter+=1
							if wordCount == 2:
								parameterList[len(parameterList) -  1].variable = word
							elif wordCount == 3:
								parameterList[len(parameterList) -  1].value = word
							word = ""
					
				#parse Texture lines
				elif line[0:7] == texture.identifier:
					#add texture to list
					textureList.append(dataclasses.replace(texture))
					textureList[len(textureList) - 1].fileIndex = lineCount
					
					#word reader
					word = ""
					while charCounter < len(line):
						wordTemp = ""
						if line[charCounter] != whiteSpace and line[charCounter] != eol:
							tempChar = line[charCounter]
							wordTemp = word + tempChar
							word = wordTemp
							charCounter+=1
						else:
							wordCount+=1
							charCounter+=1
							if wordCount == 2:
								textureList[len(textureList) -  1].index = word
							elif wordCount == 3:
								textureList[len(textureList) -  1].name = word
							elif wordCount == 4:
								textureList[len(textureList) -  1].a = word
							elif wordCount == 5:
								textureList[len(textureList) -  1].b = word
							elif wordCount == 6:
								textureList[len(textureList) -  1].c = word
							elif wordCount == 7:
								textureList[len(textureList) -  1].d = word
							word = ""
					
				#parse Comment lines
				elif line[0] == comment.identifier:
					#add comment to list
					commentList.append(dataclasses.replace(comment))
					commentList[len(commentList) - 1].fileIndex = lineCount
					#copy comment content directly
					commentList[len(commentList) -  1].content = line
					
				#parse all unsigned lines
				else:
					scriptList.append(dataclasses.replace(script))
					scriptList[len(scriptList) - 1].fileIndex = lineCount
					scriptList[len(scriptList) - 1].content = line
					
				line = ""
		fileIter+=1
#		print('H:',len(headerList),' P:',len(particleList),' J:',len(joinList),' C:',len(commentList),' P:',len(parameterList),' T:',len(textureList),' S:',len(scriptList))
		
	#concatonate all structures for export
	fileStructure.append(headerList)
	fileStructure.append(particleList)
	fileStructure.append(joinList)
	fileStructure.append(parameterList)
	fileStructure.append(textureList)
	fileStructure.append(commentList)
	fileStructure.append(scriptList)
	
	#make parsed content global
	global parsedTempContent
	parsedTempContent = fileStructure

def printFile():
	
	global parsedTempContent
	saveFileTo = None
	lineOutTotal = len(parsedTempContent[0]) + len(parsedTempContent[1]) + len(parsedTempContent[2]) + len(parsedTempContent[3]) + len(parsedTempContent[4]) + len(parsedTempContent[5]) + len(parsedTempContent[6])
	
	finalList = [0] * lineOutTotal

	#iterate through each line entry per list type, concat data to oec compliant str
	for listType in parsedTempContent:
		for entry in listType:
			if entry.identifier == 'v':
				line = (f"{entry.content}")
				finalList[entry.fileIndex - 1] = line
				
			elif entry.identifier == 'p':
				line = (f"{entry.identifier} "
						f"{entry.material} "
						f"{entry.index} "
						f"{entry.layer} "
						f"{entry.color} "
						f"{entry.xPos} "
						f"{entry.yPos} "
						f"{entry.xVel} "
						f"{entry.yVel} "
						f"{entry.xOrg} "
						f"{entry.yOrg} "
						f"{entry.angle} "
						f"{entry.angVel} "
						f"{entry.pressure} \r\n")
				finalList[entry.fileIndex - 1] = line
				
			elif entry.identifier == 'j':
				line = (f"{entry.identifier} "
						f"{entry.index} "
						f"{entry.a} "
						f"{entry.b} "
						f"{entry.proximity} "
						f"{entry.offset} "
						f"{entry.Xanchor} "
						f"{entry.Yanchor} "
						f"{entry.rot} "
						f"{entry.unknown}\r\n")
				finalList[entry.fileIndex - 1] = line
				
			elif entry.identifier == 'texture':
				line = (f"{entry.identifier} "
						f"{entry.index} "
						f"{entry.name} "
						f"{entry.a} "
						f"{entry.b} "
						f"{entry.c} "
						f"{entry.d}\r\n")
				finalList[entry.fileIndex - 1] = line
				
			elif entry.identifier == '@':
				line = (f"{entry.identifier} "
						f"{entry.variable} "
						f"{entry.value}\r\n")
				finalList[entry.fileIndex - 1] = line
				
			elif entry.identifier == '#':
				line = entry.content
				finalList[entry.fileIndex - 1] = line
				
			elif entry.identifier == 's':
				line = entry.content
				finalList[entry.fileIndex - 1] = line
	
	#write file
	saveFileTo = fd.askopenfilename(title="Save As:")
	with open(saveFileTo, 'w') as toSave:
		for line in finalList:
			toSave.write(line)

def combFile(fileIn):
	#input file
	global rawContent
	rawContent = fileIn
	readFile()
	
	#process file
	global parsedTempContent
	
	for entry in parsedTempContent[1]:
		binRep = bin(int(entry.material, 16))[2:].zfill(32)
		if int(binRep[31 - 4]) == 1:
			entry.angle = 0
			entry.angVel = 0
	
	#output file
	printFile()
