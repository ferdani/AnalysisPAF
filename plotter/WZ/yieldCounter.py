import ROOT
import os

nolepMVA,veryLoose,loose,medium,tight,veryTight,extraTight,top = range(8)
TIsSR,TIsCRTT,TIsCRDY = range(3)
leptonIDs = ["nolepMVA","veryLoose","loose","medium","tight","veryTight","extraTight","top"]
var = ["TIsSR","TIsCRTT","TIsCRDY"]
#leptonIDs = ["nolepMVA"]
#var = ["TIsSR"]

emptyYields = []

theLumi = 35900.

for i in leptonIDs:
	tempList = []	
	for j in var:
			tempList.append(-1)
	emptyYields.append(tempList)	

class sample():
	def __init__(self, fileName, name, group):
		self.fName = fileName
		self.name  = name
		self.yields = []
		self.stats  = []

		for i in leptonIDs:
			tempList1 = []	
			tempList2 = []	
			for j in var:
				tempList1.append(-1)
				tempList2.append(-1)
			self.yields.append(tempList1)
			self.stats.append(tempList2)

		group.append(self)
		print "Getting yields for... " + str(self.name) + " ......"
		for i in leptonIDs:
			print i + " ......"
			for j in var:
				self.GetYields(i,j)

	def GetYields(self, leptonID, var):
		os.system("root -l -q -b 'yieldCounter.C(\"%s\",\"%s\",\"%s\")' >> temp.txt"%(self.name,leptonID,var))
		inFile = open("temp.txt","r")
		inFile.readline()
		inFile.readline()
		self.yields[eval(leptonID)][eval(var)] = float(inFile.readline())*theLumi
		self.stats[eval(leptonID)][eval(var)]  = ((float(inFile.readline()))**0.5)*theLumi
		inFile.close()
		os.system("rm temp.txt")

Signal      = []
Fakes_DY    = []
Fakes_t     = []
Prompt_ttX  = []
Prompt_VV   = []
Conversions = []



WZ = sample("Tree_WZTo3LNu.root", "WZTo3LNu", Signal)

DY_1 = sample("Tree_DYJetsToLL_M50_MLM.root", "DYJetsToLL_M50_MLM", Fakes_DY)
DY_2 = sample("Tree_DYJetsToLL_M5to50_MLM.root", "DYJetsToLL_M5to50_MLM", Fakes_DY)
DY_3 = sample("Tree_WJetsToLNu_MLM.root", "WJetsToLNu_MLM", Fakes_DY)

TT_1 = sample("Tree_TW_noFullyHadr.root", "TW_noFullyHadr", Fakes_t) 
TT_2 = sample("Tree_TbarW_noFullyHadr.root", "TbarW_noFullyHadr", Fakes_t) 
TT_3 = sample("Tree_Tbar_tch.root", "Tbar_tch", Fakes_t) 
TT_4 = sample("Tree_T_tch.root", "T_tch", Fakes_t) 
TT_5 = sample("Tree_TToLeptons_sch_amcatnlo.root", "TToLeptons_sch_amcatnlo", Fakes_t) 
TT_6 = sample("Tree_TTbar_Powheg.root", "TTbar_Powheg", Fakes_t) 
 

TTX_1 = sample("Tree_TTZToLLNuNu.root", "TTZToLLNuNu", Prompt_ttX) 
TTX_2 = sample("Tree_TTZToLL_M1to10.root", "TTZToLL_M1to10", Prompt_ttX) 
TTX_3 = sample("Tree_TTWToLNu.root", "TTWToLNu", Prompt_ttX) 
TTX_4 = sample("Tree_TTHNonbb.root", "TTHNonbb", Prompt_ttX) 
TTX_5 = sample("Tree_TTTT.root", "TTTT", Prompt_ttX) 
TTX_6 = sample("Tree_tZq_ll.root", "tZq_ll", Prompt_ttX)

VV_1 = sample("Tree_WpWpJJ.root", "WpWpJJ", Prompt_VV) 
VV_2 = sample("Tree_WWTo2L2Nu.root", "WWTo2L2Nu", Prompt_VV) 
VV_3 = sample("Tree_VHToNonbb_amcatnlo.root", "VHToNonbb_amcatnlo", Prompt_VV) 
VV_4 = sample("Tree_ZZZ.root", "ZZZ", Prompt_VV) 
VV_5 = sample("Tree_WZZ.root", "WZZ", Prompt_VV) 
VV_6 = sample("Tree_WWZ.root", "WWZ", Prompt_VV) 
VV_7 = sample("Tree_WWW.root", "WWW", Prompt_VV) 
VV_8 = sample("Tree_WWTo2L2Nu_DoubleScat.root", "WWTo2L2Nu_DoubleScat", Prompt_VV) 
VV_9 = sample("Tree_ZZTo4L.root", "ZZTo4L", Prompt_VV) 

                                                                                                                         
Convs_1 = sample("Tree_WGToLNuG.root", "WGToLNuG", Conversions) 
Convs_2 = sample("Tree_WZG_amcatnlo.root", "WZG_amcatnlo", Conversions) 
Convs_3 = sample("Tree_TTGJets.root", "TTGJets", Conversions) 
Convs_4 = sample("Tree_TGJets.root", "TGJets", Conversions) 
Convs_5 = sample("Tree_ZGTo2LG.root", "ZGTo2LG", Conversions) 
Convs_6 = sample("Tree_WWG_amcatnlo.root", "WWG_amcatnlo", Conversions) 

ALLBKG = Fakes_DY + Fakes_t + Prompt_ttX + Prompt_VV + Conversions

for i in range(len(leptonIDs)):
	for j in range(len(var)):
		print leptonIDs[i], var[j], "Conversions", sum([sam.yields[i][j] for sam in Conversions]),  sum([sam.stats[i][j]**2 for sam in Conversions])**0.5
		print leptonIDs[i], var[j], "Fakes_DY", sum([sam.yields[i][j] for sam in Fakes_DY]),  sum([sam.stats[i][j]**2 for sam in Fakes_DY])**0.5
		print leptonIDs[i], var[j], "Fakes_TT", sum([sam.yields[i][j] for sam in Fakes_t]),  sum([sam.stats[i][j]**2 for sam in Fakes_t])**0.5
		print leptonIDs[i], var[j], "Prompt_ttX", sum([sam.yields[i][j] for sam in Prompt_ttX]),  sum([sam.stats[i][j]**2 for sam in Prompt_ttX])**0.5
		print leptonIDs[i], var[j], "Prompt_VV", sum([sam.yields[i][j] for sam in Prompt_VV]),  sum([sam.stats[i][j]**2 for sam in Prompt_VV])**0.5
		print leptonIDs[i], var[j], "Background", sum([sam.yields[i][j] for sam in ALLBKG]),  sum([sam.stats[i][j]**2 for sam in ALLBKG])**0.5	
		print leptonIDs[i], var[j], "Signal", sum([sam.yields[i][j] for sam in Signal]),  sum([sam.stats[i][j]**2 for sam in Signal])**0.5
		print leptonIDs[i], var[j], "S/B", sum([sam.yields[i][j] for sam in Signal])/(sum([sam.yields[i][j] for sam in ALLBKG])), (sum([sam.stats[i][j]**2 for sam in Signal])**0.5)/(sum([sam.yields[i][j] for sam in ALLBKG])) + sum([sam.stats[i][j]**2 for sam in ALLBKG])**0.5 *sum([sam.yields[i][j] for sam in Signal])/(sum([sam.yields[i][j] for sam in ALLBKG])**2)

print "______________________________"
print "______________________________"
print "______________________________"
print "______________________________"
print "______________________________"

for i in range(len(leptonIDs)):
	for j in range(len(var)):
		for k in range(len(Conversions)):
			print leptonIDs[i], var[j], Conversions[k].name, Conversions[k].yields[i][j]
print "______________________________"

for i in range(len(leptonIDs)):
	for j in range(len(var)):
		for k in range(len(Fakes_DY)):
			print leptonIDs[i], var[j], Fakes_DY[k].name, Fakes_DY[k].yields[i][j]

print "______________________________"

for i in range(len(leptonIDs)):
	for j in range(len(var)):
		for k in range(len(Fakes_t)):
			print leptonIDs[i], var[j], Fakes_t[k].name, Fakes_t[k].yields[i][j]

print "______________________________"

for i in range(len(leptonIDs)):
	for j in range(len(var)):
		for k in range(len(Prompt_ttX)):
			print leptonIDs[i], var[j], Prompt_ttX[k].name, Prompt_ttX[k].yields[i][j]

print "______________________________"

for i in range(len(leptonIDs)):
	for j in range(len(var)):
		for k in range(len(Prompt_VV)):
			print leptonIDs[i], var[j], Prompt_VV[k].name, Prompt_VV[k].yields[i][j]

