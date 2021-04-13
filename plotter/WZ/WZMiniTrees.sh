#
#Di and tri bosons
#





#root -l -b -q 'RunAnalyserPAF.C("WZTo3LNu"   , "WZ", 32, -4)' #
#root -l -b -q 'RunAnalyserPAF.C("WWTo2L2Nu"   ,"WZ", 32)' #
#root -l -b -q 'RunAnalyserPAF.C("ZZZ"      ,"WZ",  32)' #
#root -l -b -q 'RunAnalyserPAF.C("WZZ"      ,"WZ",  32)' #
#root -l -b -q 'RunAnalyserPAF.C("WWZ"      ,"WZ",  32)' #
#root -l -b -q 'RunAnalyserPAF.C("WWW"      ,"WZ",  32)' #
#root -l -b -q 'RunAnalyserPAF.C("WpWpJJ"   ,"WZ", 32)' #
#root -l -b -q 'RunAnalyserPAF.C("VHToNonbb_amcatnlo"   ,"WZ", 32)' #
#root -l -b -q 'RunAnalyserPAF.C("WWTo2L2Nu_DoubleScat"   ,"WZ", 32)' #
#root -l -b -q 'RunAnalyserPAF.C("ZZTo4L"   ,   "WZ", 32)'
# ====================
# CONVERSIONS
# ====================
#root -l -b -q 'RunAnalyserPAF.C("TGJets & TGJets_ext"  , "WZ",32)' #
#root -l -b -q 'RunAnalyserPAF.C("TTGJets & TTGJets_ext", "WZ",32)' #
#root -l -b -q 'RunAnalyserPAF.C("WGToLNuG"             , "WZ",32)' #
#root -l -b -q 'RunAnalyserPAF.C("ZGTo2LG"              , "WZ",32)' #
#root -l -b -q 'RunAnalyserPAF.C("WZG_amcatnlo"   , "WZ",32)'  #
#root -l -b -q 'RunAnalyserPAF.C("WWG_amcatnlo"   , "WZ",32)'  #
#   
# ====================
# DATA
# ====================
#root -l -b -q 'RunAnalyserPAF.C("MuonEG"    , "WZ",32)'  #
#root -l -b -q 'RunAnalyserPAF.C("DoubleMuon", "WZ",32)'  #
#root -l -b -q 'RunAnalyserPAF.C("DoubleEG"  , "WZ",32)'  # 
#root -l -b -q 'RunAnalyserPAF.C("SingleElec", "WZ",32)'  #
#root -l -b -q 'RunAnalyserPAF.C("SingleMuon", "WZ",32)'  #
#   
#   # ====================
#   # FAKES
#   # ====================
#   
# DY, WJets
#root -l -b -q 'RunAnalyserPAF.C("WJetsToLNu_MLM & WJetsToLNu_MLM_ext2"           , "WZ",  32)' #
#root -l -b -q 'RunAnalyserPAF.C("DYJetsToLL_M5to50_MLM"                           , "WZ", 32)' #
root -l -b -q 'RunAnalyserPAF.C("DYJetsToLL_M50_MLM_ext & DYJetsToLL_M50_MLM_ext2", "WZ", 32, -8)' #
#
## ttbar, single-t
#root -l -b -q 'RunAnalyserPAF.C("TTbar_Powheg"           ,"WZ", 32)' #
#root -l -b -q 'RunAnalyserPAF.C("T_tch"                  ,"WZ", 32)' #
#root -l -b -q 'RunAnalyserPAF.C("Tbar_tch"               ,"WZ", 32)' #
#root -l -b -q 'RunAnalyserPAF.C("TToLeptons_sch_amcatnlo","WZ", 32)' #
#root -l -b -q 'RunAnalyserPAF.C("TbarW_noFullyHadr & TbarW_noFullyHadr_ext & TbarW_noFullyHadr_ext2"   ,"WZ", 32)' #
#root -l -b -q 'RunAnalyserPAF.C("TW_noFullyHadr & TW_noFullyHadr_ext & TW_noFullyHadr_ext2"            ,"WZ", 32)' #
#    
#    
#   Inclusive samples, not dileptonic...
#   ====================
#   PROMPT
#   ==================== 
#   ttX
#root -l -b -q 'RunAnalyserPAF.C("TTWToLNu_ext1 & TTWToLNu_ext2"     ,"WZ",   32)'  #
#root -l -b -q 'RunAnalyserPAF.C("TTZToLLNuNu_ext1 & TTZToLLNuNu_ext2", "WZ",  32, -6)' #
#root -l -b -q 'RunAnalyserPAF.C("TTZToLL_M1to10", "WZ",32)' #
#root -l -b -q 'RunAnalyserPAF.C("TTHNonbb"                          , "WZ",  32)'  #
#root -l -b -q 'RunAnalyserPAF.C("TTTT"   , "WZ",32)'  #
#root -l -b -q 'RunAnalyserPAF.C("tZq_ll"                            , "WZ", 32,-6)'#, -1)'