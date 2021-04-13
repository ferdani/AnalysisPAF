# ====================
# FAKES ===> FROM DATA
# ====================


# ====================
# PROMPT
# ====================
# ttX
root -l -b -q 'RunAnalyserPAF.C("TTWToLNu_ext1 & TTWToLNu_ext2"     ,"WZ",   32)' #
root -l -b -q 'RunAnalyserPAF.C("TTZToLLNuNu_ext1 & TTZToLLNuNu_ext2", "WZ",  8, -4)'
root -l -b -q 'RunAnalyserPAF.C("TTZToLL_M1to10", "WZ",32)' #
root -l -b -q 'RunAnalyserPAF.C("TTHNonbb"                          , "WZ",  32)' #
root -l -b -q 'RunAnalyserPAF.C("tZq_ll"                            , "WZ", 8, -10, -1)' #
root -l -b -q 'RunAnalyserPAF.C("TTTT"   , "WZ",8)' #

#Di and tri bosons => DONE
root -l -b -q 'RunAnalyserPAF.C("ZZTo4L"   ,   "WZ", 8 , -4)' #
root -l -b -q 'RunAnalyserPAF.C("WWTo2L2Nu"   ,"WZ", 8)'  #
root -l -b -q 'RunAnalyserPAF.C("ZZZ"      ,"WZ",  8)' #
root -l -b -q 'RunAnalyserPAF.C("WZZ"      ,"WZ",  8)' #
root -l -b -q 'RunAnalyserPAF.C("WWZ"      ,"WZ",  8)' #
root -l -b -q 'RunAnalyserPAF.C("WWW"      ,"WZ",  8)' #
root -l -b -q 'RunAnalyserPAF.C("WpWpJJ"   ,"WZ", 8)' #
root -l -b -q 'RunAnalyserPAF.C("VHToNonbb_amcatnlo"   ,"WZ", 8)' #
root -l -b -q 'RunAnalyserPAF.C("WWTo2L2Nu_DoubleScat"   ,"WZ", 8)' # 

# ====================
# CONVERSIONS => DONE
# ====================
root -l -b -q 'RunAnalyserPAF.C("TGJets & TGJets_ext"  , "WZ",8)' #
root -l -b -q 'RunAnalyserPAF.C("TTGJets & TTGJets_ext", "WZ",8)' #
root -l -b -q 'RunAnalyserPAF.C("WGToLNuG"             , "WZ",8)' #
root -l -b -q 'RunAnalyserPAF.C("ZGTo2LG"              , "WZ",8)' #
root -l -b -q 'RunAnalyserPAF.C("WZG_amcatnlo"   , "WZ",8)' #
root -l -b -q 'RunAnalyserPAF.C("WWG_amcatnlo"   , "WZ",8)' #

# ====================
# SIGNAL => DONE
# ====================
#
root -l -b -q 'RunAnalyserPAF.C("WZTo3LNu"   , "WZ", 8 )' #

# ====================
# DATA === > WRONG!!
# ====================
root -l -b -q 'RunAnalyserPAF.C("MuonEG"    , "WZ",60)' #
root -l -b -q 'RunAnalyserPAF.C("DoubleMuon", "WZ",60)' #
root -l -b -q 'RunAnalyserPAF.C("DoubleEG"  , "WZ",60)' #
root -l -b -q 'RunAnalyserPAF.C("SingleElec", "WZ",60)' #
root -l -b -q 'RunAnalyserPAF.C("SingleMuon", "WZ",60)' #
