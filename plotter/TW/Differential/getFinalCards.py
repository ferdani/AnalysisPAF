import ROOT     as r
import varList  as vl
import warnings as wr
import sys, os, copy
from array import array
from multiprocessing import Pool
###################################################

pathToTree  = ""
NameOfTree  = "Mini1j1t";

systlist    = vl.GiveMeTheExpNamesWOJER(vl.varList["Names"]["ExpSysts"])
#systlist    = ""

StandardCut = "(Tpassreco == 1)"
opts        = ''

r.gROOT.SetBatch(True)
r.gROOT.LoadMacro('../../Histo.C+')
r.gROOT.LoadMacro('../../Looper.C+')
r.gROOT.LoadMacro('../../Plot.C+')
r.gROOT.LoadMacro('../../PlotToPy.C+')
r.gROOT.LoadMacro('../../PlotToPyC.C+')
r.gROOT.LoadMacro('../../PDFunc.C+')

############ NOTE: we are using for the tw+ttbar fiducial as nominal ttbar powheg + ttbar2l powheg, but for the resp. mat. only ttbar2l

def GiveMeMyHistos(var):
    binning = array('f', vl.varList[var]['recobinning']) # For some reason, PyROOT requires that you create FIRST this object, then put it inside the PlotToPyC.
    p = r.PlotToPyC(r.TString(vl.varList[var]['var']), r.TString(StandardCut), r.TString('ElMu'), int(len(vl.varList[var]['recobinning']) - 1), binning, r.TString(var), r.TString(vl.varList[var]['xaxis']))
    p.SetPath(pathToTree); p.SetTreeName(NameOfTree);
    p.SetLimitFolder('./temp/{var}_/'.format(var = var))
    p.SetPlotFolder('./temp/{var}_/'.format(var = var))
    p.SetPathSignal(pathToTree);
    p.SetTitleY("Events")
    p.SetLumi(vl.Lumi)
    p.verbose = True
    p.SetWeight(vl.nominal_weight)

    #if "twttbar" not in var.lower():
        #p.AddSample("TTbar_Powheg",          "ttbar",    r.itBkg, 633, systlist, opts)
    #else:
        #p.AddSample('TTbar2L_powheg',        'ttbar',    r.itBkg, 633, systlist, opts)
    
    if "twttbar" not in var.lower():
        specialweight = vl.n_ttbar/vl.sigma_ttbar/(vl.n_ttbar/vl.sigma_ttbar + vl.n_dilep/vl.sigma_dilep)
        p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
        p.AddSample('TTbar_Powheg',          'ttbar',    r.itBkg, 633, systlist, opts)
        specialweight = vl.n_dilep/vl.sigma_dilep/(vl.n_ttbar/vl.sigma_ttbar + vl.n_dilep/vl.sigma_dilep)
        p.SetWeight(vl.nominal_weight + '*' + str(specialweight))
        p.AddSample('TTbar2L_powheg',        'ttbar',    r.itBkg, 633, systlist, opts)
        p.SetWeight(vl.nominal_weight)
    else:
        p.AddSample('TTbar2L_powheg',        'ttbar',    r.itBkg, 633, systlist, opts)

    #p.AddSample('TTbar_Powheg',          'ttbar',    r.itBkg, 633, systlist, opts)
    
    p.AddSample("TTbar_PowhegSemi",      "Non-WorZ", r.itBkg, 413, systlist, opts)
    p.AddSample("WJetsToLNu_MLM",        "Non-WorZ", r.itBkg, 413, systlist, opts)

    p.AddSample("WZ",                    "VVttbarV", r.itBkg, 390, systlist, opts)
    p.AddSample("WW",                    "VVttbarV", r.itBkg, 390, systlist, opts)
    p.AddSample("ZZ",                    "VVttbarV", r.itBkg, 390, systlist, opts)
    p.AddSample("TTWToLNu",              "VVttbarV", r.itBkg, 390, systlist, opts)
    p.AddSample("TTWToQQ" ,              "VVttbarV", r.itBkg, 390, systlist, opts)
    p.AddSample("TTZToQQ" ,              "VVttbarV", r.itBkg, 390, systlist, opts)
    p.AddSample("TTZToLLNuNu",           "VVttbarV", r.itBkg, 390, systlist, opts)
    p.AddSample("TTGJets",               "VVttbarV", r.itBkg, 390, systlist, opts)

    p.AddSample("DYJetsToLL_M5to50_MLM", "DY",       r.itBkg, 852, systlist, opts)
    p.AddSample("DYJetsToLL_M50_MLM",    "DY",       r.itBkg, 852, systlist, opts)
    #p.AddSample("DYJetsToLL_M10to50_aMCatNLO","DY",  r.itBkg, 852, systlist, opts)
    #p.AddSample("DYJetsToLL_M50_aMCatNLO","DY",      r.itBkg, 852, systlist, opts)
    
    #p.AddSample("TW",                    "tW",       r.itBkg, r.TColor.GetColor("#ffcc33"), systlist, opts)
    #p.AddSample("TbarW",                 "tW",       r.itBkg, r.TColor.GetColor("#ffcc33"), systlist, opts)

    specialweight = vl.n_tw/vl.sigma_tw/(vl.n_tw/vl.sigma_tw + vl.n_twnohad/vl.sigma_twnohad)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TW',                     'tW',      r.itBkg, r.TColor.GetColor("#ffcc33"), systlist, opts)
    specialweight = vl.n_twnohad/vl.sigma_twnohad/(vl.n_tw/vl.sigma_tw + vl.n_twnohad/vl.sigma_twnohad)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TW_noFullyHadr',         'tW',      r.itBkg, r.TColor.GetColor("#ffcc33"), systlist, opts)
    specialweight = vl.n_tbarw/vl.sigma_tw/(vl.n_tbarw/vl.sigma_tw + vl.n_tbarwnohad/vl.sigma_twnohad)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TbarW',                  'tW',      r.itBkg, r.TColor.GetColor("#ffcc33"), systlist, opts)
    specialweight = vl.n_tbarwnohad/vl.sigma_twnohad/(vl.n_tbarw/vl.sigma_tw + vl.n_tbarwnohad/vl.sigma_twnohad)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TbarW_noFullyHadr',      'tW',      r.itBkg, r.TColor.GetColor("#ffcc33"), systlist, opts)
    p.SetWeight(vl.nominal_weight)

    # Data (or Asimov)
    if not vl.asimov:
        p.SetWeight("TWeight")
        p.AddSample("MuonEG",            "Data",     r.itData, 0, '', opts)
        p.AddSample("SingleMuon",        "Data",     r.itData, 0, '', opts)
        p.AddSample("SingleElec",        "Data",     r.itData, 0, '', opts)
        p.SetWeight(vl.nominal_weight)
    else:
        hData=r.Histo(p.GetHisto('tW').Clone("Data"))
        for proc in ['ttbar', 'VVttbarV', "DY", "Non-WorZ"]:
            hData.Add( p.GetHisto(proc) )
        hData.SetProcess("Data")
        hData.SetTag("Data")
        hData.SetType(r.itData)
        hData.SetColor(r.kBlack)
        p.AddToHistos(hData)
    
    # Modelling systematics
    p.AddSample("TW"                           , "tW",           r.itSys, 1, "JERUp");
    p.AddSample("TW_noFullyHadr_isrUp"         , "tW",           r.itSys, 1, "isrUp");
    p.AddSample("TW_noFullyHadr_isrDown"       , "tW",           r.itSys, 1, "isrDown");
    p.AddSample("TW_noFullyHadr_fsrUp"         , "tW",           r.itSys, 1, "fsrUp");
    p.AddSample("TW_noFullyHadr_fsrDown"       , "tW",           r.itSys, 1, "fsrDown");
    p.AddSample("TW_noFullyHadr_MEscaleUp"     , "tW",           r.itSys, 1, "tWMEUp");
    p.AddSample("TW_noFullyHadr_MEscaleDown"   , "tW",           r.itSys, 1, "tWMEDown");
    p.AddSample("TW_noFullyHadr_mtop1755"      , "tW",           r.itSys, 1, "mtopUp");
    p.AddSample("TW_noFullyHadr_mtop1695"      , "tW",           r.itSys, 1, "mtopDown");

    p.AddSample("TbarW"                        , "tW",           r.itSys, 1, "JERUp");
    p.AddSample("TbarW_noFullyHadr_isrUp"      , "tW",           r.itSys, 1, "isrUp");
    p.AddSample("TbarW_noFullyHadr_isrDown"    , "tW",           r.itSys, 1, "isrDown");
    p.AddSample("TbarW_noFullyHadr_fsrUp"      , "tW",           r.itSys, 1, "fsrUp");
    p.AddSample("TbarW_noFullyHadr_fsrDown"    , "tW",           r.itSys, 1, "fsrDown");
    p.AddSample("TbarW_noFullyHadr_MEscaleUp"  , "tW",           r.itSys, 1, "tWMEUp");
    p.AddSample("TbarW_noFullyHadr_MEscaleDown", "tW",           r.itSys, 1, "tWMEDown");
    p.AddSample("TbarW_noFullyHadr_mtop1755"   , "tW",           r.itSys, 1, "mtopUp");
    p.AddSample("TbarW_noFullyHadr_mtop1695"   , "tW",           r.itSys, 1, "mtopDown");

    p.AddSample("TW_noFullyHadr_DS",             "tW",           r.itSys, 1, "DSUp");
    p.AddSample("TbarW_noFullyHadr_DS",          "tW",           r.itSys, 1, "DSUp");
    p.AddSymmetricHisto("tW",  "DSUp");
    p.AddSymmetricHisto("tW",  "JERUp");

    p.AddSample("TTbar_Powheg",                 "ttbar",     r.itSys, 1, "JERUp");

    specialweight = vl.nUEUp_ttbar/vl.sigma_ttbar/(vl.nUEUp_ttbar/vl.sigma_ttbar + vl.nUEUp_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar_Powheg_ueUp",            "ttbar",     r.itSys, 1, "UEUp");
    specialweight = vl.nUEUp_dilep/vl.sigma_dilep/(vl.nUEUp_ttbar/vl.sigma_ttbar + vl.nUEUp_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar2L_Powheg_ueUp",          "ttbar",     r.itSys, 1, "UEUp");
    specialweight = vl.nUEDown_ttbar/vl.sigma_ttbar/(vl.nUEDown_ttbar/vl.sigma_ttbar + vl.nUEDown_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar_Powheg_ueDown",          "ttbar",     r.itSys, 1, "UEDown");
    specialweight = vl.nUEDown_dilep/vl.sigma_dilep/(vl.nUEDown_ttbar/vl.sigma_ttbar + vl.nUEDown_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar2L_Powheg_ueDown",        "ttbar",     r.itSys, 1, "UEDown");
    specialweight = vl.nhDampUp_ttbar/vl.sigma_ttbar/(vl.nhDampUp_ttbar/vl.sigma_ttbar + vl.nhDampUp_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar_Powheg_hdampUp",         "ttbar",     r.itSys, 1, "hDampUp");
    specialweight = vl.nhDampUp_dilep/vl.sigma_dilep/(vl.nhDampUp_ttbar/vl.sigma_ttbar + vl.nhDampUp_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar2L_Powheg_hdampUp",       "ttbar",     r.itSys, 1, "hDampUp");
    specialweight = vl.nhDampDown_ttbar/vl.sigma_ttbar/(vl.nhDampDown_ttbar/vl.sigma_ttbar + vl.nhDampDown_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar_Powheg_hdampDown",       "ttbar",     r.itSys, 1, "hDampDown");
    specialweight = vl.nhDampDown_dilep/vl.sigma_dilep/(vl.nhDampDown_ttbar/vl.sigma_ttbar + vl.nhDampDown_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar2L_Powheg_hdampDown",     "ttbar",     r.itSys, 1, "hDampDown");
    p.SetWeight(vl.nominal_weight);

    p.AddSample("TTbar_Powheg_isrUp"          , "ttbar",     r.itSys, 1, "isrUp");
    p.AddSample("TTbar_Powheg_isrDown"        , "ttbar",     r.itSys, 1, "isrDown");
    p.AddSample("TTbar_Powheg_fsrUp"          , "ttbar",     r.itSys, 1, "fsrUp");
    p.AddSample("TTbar_Powheg_fsrDown"        , "ttbar",     r.itSys, 1, "fsrDown");
    p.AddSample("TTbar_Powheg_mtop1755"       , "ttbar",     r.itSys, 1, "mtopUp");
    p.AddSample("TTbar_Powheg_mtop1695"       , "ttbar",     r.itSys, 1, "mtopDown");

    specialweight = vl.nGluonMoveCRTune_ttbar/vl.sigma_ttbar/(vl.nGluonMoveCRTune_ttbar/vl.sigma_ttbar + vl.nGluonMoveCRTune_dilep/vl.sigma_dilep)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TTbar_GluonMoveCRTune',        'ttbar',     r.itSys, 1, "GluonMoveCRTune")
    specialweight = vl.nGluonMoveCRTune_dilep/vl.sigma_dilep/(vl.nGluonMoveCRTune_ttbar/vl.sigma_ttbar + vl.nGluonMoveCRTune_dilep/vl.sigma_dilep)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TTTo2L2Nu_GluonMoveCRTune',    'ttbar',     r.itSys, 1, "GluonMoveCRTune")
    specialweight = vl.nPowhegerdON_ttbar/vl.sigma_ttbar/(vl.nPowhegerdON_ttbar/vl.sigma_ttbar + vl.nPowhegerdON_dilep/vl.sigma_dilep)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TTbar_Powheg_erdON',           'ttbar',     r.itSys, 1, "PowhegerdON")
    specialweight = vl.nPowhegerdON_dilep/vl.sigma_dilep/(vl.nPowhegerdON_ttbar/vl.sigma_ttbar + vl.nPowhegerdON_dilep/vl.sigma_dilep)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TTTo2L2Nu_Powheg_erdON',       'ttbar',     r.itSys, 1, "PowhegerdON")
    specialweight = vl.nQCDbasedCRTuneerdON_ttbar/vl.sigma_ttbar/(vl.nQCDbasedCRTuneerdON_ttbar/vl.sigma_ttbar + vl.nQCDbasedCRTuneerdON_dilep/vl.sigma_dilep)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TTbar_GluonMoveCRTune_erdON',  'ttbar',     r.itSys, 1, "QCDbasedCRTuneerdON")
    specialweight = vl.nQCDbasedCRTuneerdON_dilep/vl.sigma_dilep/(vl.nQCDbasedCRTuneerdON_ttbar/vl.sigma_ttbar + vl.nQCDbasedCRTuneerdON_dilep/vl.sigma_dilep)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TTTo2L2Nu_QCDbasedCRTune_erdON','ttbar',    r.itSys, 1, "QCDbasedCRTuneerdON")
    p.SetWeight(vl.nominal_weight)

    p.AddSample("TTbar_GluonMoveCRTune_erdON" , "ttbar",     r.itSys, 1, "GluonMoveCRTuneerdON");
    p.UseEnvelope("ttbar", "GluonMoveCRTune,GluonMoveCRTuneerdON,PowhegerdON,QCDbasedCRTuneerdON", "ColorReconnection");
    p.AddSymmetricHisto("ttbar",  "JERUp");


    pdf     = r.PDFToPyC(r.TString(pathToTree), r.TString("TTbar_Powheg"), r.TString(NameOfTree), r.TString(StandardCut), r.TString("ElMu"), r.TString(vl.varList[var]['var']), len(vl.varList[var]['recobinning']) - 1, binning, r.TString(''));
    pdf.verbose = False
    pdf.verbose = True
    pdf.SetLumi(vl.Lumi * 1000)
    pdf.SetWeight(vl.nominal_weight)

    hPDFUp  = pdf.GetSystHisto("up","pdf").CloneHisto();
    hPDFDown= pdf.GetSystHisto("Down","pdf").CloneHisto();
    hMEUp   = pdf.GetSystHisto("up","ME").CloneHisto();
    hMEDown = pdf.GetSystHisto("Down","ME").CloneHisto();
    p.PrepareHisto(hPDFUp,   "TTbar_Powheg", "ttbar", r.itSys, 0, "pdfUp");
    p.PrepareHisto(hPDFDown, "TTbar_Powheg", "ttbar", r.itSys, 0, "pdfDown");
    p.PrepareHisto(hMEUp,    "TTbar_Powheg", "ttbar", r.itSys, 0, "ttbarMEUp");
    p.PrepareHisto(hMEDown,  "TTbar_Powheg", "ttbar", r.itSys, 0, "ttbarMEDown");
    p.AddToSystematicLabels("pdf");
    p.AddToSystematicLabels("ttbarME");
    del pdf


    p.doUncInLegend = True;
    p.SetRatioMin( 0.6 );
    p.SetRatioMax( 1.4 );
    p.SetPadPlotMargins(vl.margins)
    p.SetPadRatioMargins(vl.marginsratio)

    p.SetCMSlabel("CMS");
    p.SetCMSmodeLabel("Preliminary");
    p.SetLegendPosition(0.7, 0.45, 0.93, 0.92)
    p.doYieldsInLeg = False;
    p.doSetLogy     = False;
    #p.doData        = False;
    p.doSignal      = False;
    p.SetTitleY(r.TString(vl.varList[var]['yaxis']))

    p.PrintYields("", "", "", "txt,tex")
    p.PrintSystYields()
    p.NoShowVarName = True;
    p.SetOutputName("forCards_{var}".format(var = var));
    p.SaveHistograms();
    del p
    if vl.asimov: del hData
    return


def GiveMeMyGoodHistosToShowThem(var):
    nbins    = int(20) if "ndescbins" not in vl.varList[var] else int(vl.varList[var]['ndescbins'])
    lowedge  = float(vl.varList[var]['recobinning'][0]) if "descbinning" not in vl.varList[var] else float(vl.varList[var]['descbinning'][0])
    highedge = float(vl.varList[var]['recobinning'][-1]) if "descbinning" not in vl.varList[var] else float(vl.varList[var]['descbinning'][1])
    width    = (highedge - lowedge)/nbins

    p = r.PlotToPy(r.TString(vl.varList[var]['var']), r.TString(StandardCut), r.TString('ElMu'), nbins, lowedge, highedge, r.TString(var), r.TString(vl.varList[var]['xaxis']))
    p.SetPath(pathToTree); p.SetTreeName(NameOfTree);
    p.SetLimitFolder('./temp/{var}_/'.format(var = var))
    p.SetPlotFolder('./temp/{var}_/'.format(var = var))
    p.SetPathSignal(pathToTree);
    p.SetTitleY("Events")
    p.SetLumi(vl.Lumi)
    p.verbose = True
    p.SetWeight(vl.nominal_weight)

    #if "twttbar" not in var.lower():
        #p.AddSample("TTbar_Powheg",          "ttbar",    r.itBkg, 633, systlist, opts)
    #else:
        #p.AddSample('TTbar2L_powheg',        'ttbar',    r.itBkg, 633, systlist, opts)

    if "twttbar" not in var.lower():
        specialweight = vl.n_ttbar/vl.sigma_ttbar/(vl.n_ttbar/vl.sigma_ttbar + vl.n_dilep/vl.sigma_dilep)
        p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
        p.AddSample('TTbar_Powheg',          'ttbar',    r.itBkg, 633, systlist, opts)
        specialweight = vl.n_dilep/vl.sigma_dilep/(vl.n_ttbar/vl.sigma_ttbar + vl.n_dilep/vl.sigma_dilep)
        p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
        p.AddSample('TTbar2L_powheg',        'ttbar',    r.itBkg, 633, systlist, opts)
        p.SetWeight(vl.nominal_weight)
    else:
        p.AddSample('TTbar2L_powheg',        'ttbar',    r.itBkg, 633, systlist, opts)

    #p.AddSample('TTbar_Powheg',          'ttbar',    r.itBkg, 633, systlist, opts)

    p.AddSample("TTbar_PowhegSemi",      "Non-WorZ", r.itBkg, 413, systlist, opts)
    p.AddSample("WJetsToLNu_MLM",        "Non-WorZ", r.itBkg, 413, systlist, opts)

    p.AddSample("WZ",                    "VVttbarV", r.itBkg, 390, systlist, opts)
    p.AddSample("WW",                    "VVttbarV", r.itBkg, 390, systlist, opts)
    p.AddSample("ZZ",                    "VVttbarV", r.itBkg, 390, systlist, opts)
    p.AddSample("TTWToLNu",              "VVttbarV", r.itBkg, 390, systlist, opts)
    p.AddSample("TTWToQQ" ,              "VVttbarV", r.itBkg, 390, systlist, opts)
    p.AddSample("TTZToQQ" ,              "VVttbarV", r.itBkg, 390, systlist, opts)
    p.AddSample("TTZToLLNuNu",           "VVttbarV", r.itBkg, 390, systlist, opts)
    p.AddSample("TTGJets",               "VVttbarV", r.itBkg, 390, systlist, opts)

    p.AddSample("DYJetsToLL_M5to50_MLM", "DY",       r.itBkg, 852, systlist, opts)
    p.AddSample("DYJetsToLL_M50_MLM",    "DY",       r.itBkg, 852, systlist, opts)
    #p.AddSample("DYJetsToLL_M10to50_aMCatNLO","DY",  r.itBkg, 852, systlist, opts)
    #p.AddSample("DYJetsToLL_M50_aMCatNLO","DY",      r.itBkg, 852, systlist, opts)

    #p.AddSample("TW",                    "tW",       r.itBkg, r.TColor.GetColor("#ffcc33"), systlist, opts)
    #p.AddSample("TbarW",                 "tW",       r.itBkg, r.TColor.GetColor("#ffcc33"), systlist, opts)

    specialweight = vl.n_tw/vl.sigma_tw/(vl.n_tw/vl.sigma_tw + vl.n_twnohad/vl.sigma_twnohad)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TW',                     'tW',      r.itBkg, r.TColor.GetColor("#ffcc33"), systlist, opts)
    specialweight = vl.n_twnohad/vl.sigma_twnohad/(vl.n_tw/vl.sigma_tw + vl.n_twnohad/vl.sigma_twnohad)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TW_noFullyHadr',         'tW',      r.itBkg, r.TColor.GetColor("#ffcc33"), systlist, opts)
    specialweight = vl.n_tbarw/vl.sigma_tw/(vl.n_tbarw/vl.sigma_tw + vl.n_tbarwnohad/vl.sigma_twnohad)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TbarW',                  'tW',      r.itBkg, r.TColor.GetColor("#ffcc33"), systlist, opts)
    specialweight = vl.n_tbarwnohad/vl.sigma_twnohad/(vl.n_tbarw/vl.sigma_tw + vl.n_tbarwnohad/vl.sigma_twnohad)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TbarW_noFullyHadr',      'tW',      r.itBkg, r.TColor.GetColor("#ffcc33"), systlist, opts)
    p.SetWeight(vl.nominal_weight)

    # Data (or Asimov)
    if not vl.asimov:
        p.SetWeight("TWeight")
        p.AddSample("MuonEG",            "Data",     r.itData, 0, '', opts)
        p.AddSample("SingleMuon",        "Data",     r.itData, 0, '', opts)
        p.AddSample("SingleElec",        "Data",     r.itData, 0, '', opts)
        p.SetWeight(vl.nominal_weight)
    else:
        hData=r.Histo(p.GetHisto('tW').Clone("Data"))
        for proc in ['ttbar', 'VVttbarV', "DY", "Non-WorZ"]:
            hData.Add( p.GetHisto(proc) )
        hData.SetProcess("Data")
        hData.SetTag("Data")
        hData.SetType(r.itData)
        hData.SetColor(r.kBlack)
        p.AddToHistos(hData)

    # Modelling systematics
    p.AddSample("TW"                           , "tW",           r.itSys, 1, "JERUp");
    p.AddSample("TW_noFullyHadr_isrUp"         , "tW",           r.itSys, 1, "isrUp");
    p.AddSample("TW_noFullyHadr_isrDown"       , "tW",           r.itSys, 1, "isrDown");
    p.AddSample("TW_noFullyHadr_fsrUp"         , "tW",           r.itSys, 1, "fsrUp");
    p.AddSample("TW_noFullyHadr_fsrDown"       , "tW",           r.itSys, 1, "fsrDown");
    p.AddSample("TW_noFullyHadr_MEscaleUp"     , "tW",           r.itSys, 1, "tWMEUp");
    p.AddSample("TW_noFullyHadr_MEscaleDown"   , "tW",           r.itSys, 1, "tWMEDown");
    p.AddSample("TW_noFullyHadr_mtop1755"      , "tW",           r.itSys, 1, "mtopUp");
    p.AddSample("TW_noFullyHadr_mtop1695"      , "tW",           r.itSys, 1, "mtopDown");

    p.AddSample("TbarW"                        , "tW",           r.itSys, 1, "JERUp");
    p.AddSample("TbarW_noFullyHadr_isrUp"      , "tW",           r.itSys, 1, "isrUp");
    p.AddSample("TbarW_noFullyHadr_isrDown"    , "tW",           r.itSys, 1, "isrDown");
    p.AddSample("TbarW_noFullyHadr_fsrUp"      , "tW",           r.itSys, 1, "fsrUp");
    p.AddSample("TbarW_noFullyHadr_fsrDown"    , "tW",           r.itSys, 1, "fsrDown");
    p.AddSample("TbarW_noFullyHadr_MEscaleUp"  , "tW",           r.itSys, 1, "tWMEUp");
    p.AddSample("TbarW_noFullyHadr_MEscaleDown", "tW",           r.itSys, 1, "tWMEDown");
    p.AddSample("TbarW_noFullyHadr_mtop1755"   , "tW",           r.itSys, 1, "mtopUp");
    p.AddSample("TbarW_noFullyHadr_mtop1695"   , "tW",           r.itSys, 1, "mtopDown");

    p.AddSample("TW_noFullyHadr_DS",             "tW",           r.itSys, 1, "DSUp");
    p.AddSample("TbarW_noFullyHadr_DS",          "tW",           r.itSys, 1, "DSUp");
    p.AddSymmetricHisto("tW", "DSUp");
    p.AddSymmetricHisto("tW", "JERUp");

    p.AddSample("TTbar_Powheg",                 "ttbar",     r.itSys, 1, "JERUp");

    specialweight = vl.nUEUp_ttbar/vl.sigma_ttbar/(vl.nUEUp_ttbar/vl.sigma_ttbar + vl.nUEUp_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar_Powheg_ueUp",            "ttbar",     r.itSys, 1, "UEUp");
    specialweight = vl.nUEUp_dilep/vl.sigma_dilep/(vl.nUEUp_ttbar/vl.sigma_ttbar + vl.nUEUp_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar2L_Powheg_ueUp",          "ttbar",     r.itSys, 1, "UEUp");
    specialweight = vl.nUEDown_ttbar/vl.sigma_ttbar/(vl.nUEDown_ttbar/vl.sigma_ttbar + vl.nUEDown_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar_Powheg_ueDown",          "ttbar",     r.itSys, 1, "UEDown");
    specialweight = vl.nUEDown_dilep/vl.sigma_dilep/(vl.nUEDown_ttbar/vl.sigma_ttbar + vl.nUEDown_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar2L_Powheg_ueDown",        "ttbar",     r.itSys, 1, "UEDown");
    specialweight = vl.nhDampUp_ttbar/vl.sigma_ttbar/(vl.nhDampUp_ttbar/vl.sigma_ttbar + vl.nhDampUp_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar_Powheg_hdampUp",         "ttbar",     r.itSys, 1, "hDampUp");
    specialweight = vl.nhDampUp_dilep/vl.sigma_dilep/(vl.nhDampUp_ttbar/vl.sigma_ttbar + vl.nhDampUp_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar2L_Powheg_hdampUp",       "ttbar",     r.itSys, 1, "hDampUp");
    specialweight = vl.nhDampDown_ttbar/vl.sigma_ttbar/(vl.nhDampDown_ttbar/vl.sigma_ttbar + vl.nhDampDown_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar_Powheg_hdampDown",       "ttbar",     r.itSys, 1, "hDampDown");
    specialweight = vl.nhDampDown_dilep/vl.sigma_dilep/(vl.nhDampDown_ttbar/vl.sigma_ttbar + vl.nhDampDown_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar2L_Powheg_hdampDown",     "ttbar",     r.itSys, 1, "hDampDown");
    p.SetWeight(vl.nominal_weight);

    p.AddSample("TTbar_Powheg_isrUp"          , "ttbar",     r.itSys, 1, "isrUp");
    p.AddSample("TTbar_Powheg_isrDown"        , "ttbar",     r.itSys, 1, "isrDown");
    p.AddSample("TTbar_Powheg_fsrUp"          , "ttbar",     r.itSys, 1, "fsrUp");
    p.AddSample("TTbar_Powheg_fsrDown"        , "ttbar",     r.itSys, 1, "fsrDown");
    p.AddSample("TTbar_Powheg_mtop1755"       , "ttbar",     r.itSys, 1, "mtopUp");
    p.AddSample("TTbar_Powheg_mtop1695"       , "ttbar",     r.itSys, 1, "mtopDown");

    specialweight = vl.nGluonMoveCRTune_ttbar/vl.sigma_ttbar/(vl.nGluonMoveCRTune_ttbar/vl.sigma_ttbar + vl.nGluonMoveCRTune_dilep/vl.sigma_dilep)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TTbar_GluonMoveCRTune',        'ttbar',     r.itSys, 1, "GluonMoveCRTune")
    specialweight = vl.nGluonMoveCRTune_dilep/vl.sigma_dilep/(vl.nGluonMoveCRTune_ttbar/vl.sigma_ttbar + vl.nGluonMoveCRTune_dilep/vl.sigma_dilep)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TTTo2L2Nu_GluonMoveCRTune',    'ttbar',     r.itSys, 1, "GluonMoveCRTune")
    specialweight = vl.nPowhegerdON_ttbar/vl.sigma_ttbar/(vl.nPowhegerdON_ttbar/vl.sigma_ttbar + vl.nPowhegerdON_dilep/vl.sigma_dilep)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TTbar_Powheg_erdON',           'ttbar',     r.itSys, 1, "PowhegerdON")
    specialweight = vl.nPowhegerdON_dilep/vl.sigma_dilep/(vl.nPowhegerdON_ttbar/vl.sigma_ttbar + vl.nPowhegerdON_dilep/vl.sigma_dilep)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TTTo2L2Nu_Powheg_erdON',       'ttbar',     r.itSys, 1, "PowhegerdON")
    specialweight = vl.nQCDbasedCRTuneerdON_ttbar/vl.sigma_ttbar/(vl.nQCDbasedCRTuneerdON_ttbar/vl.sigma_ttbar + vl.nQCDbasedCRTuneerdON_dilep/vl.sigma_dilep)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TTbar_GluonMoveCRTune_erdON',  'ttbar',     r.itSys, 1, "QCDbasedCRTuneerdON")
    specialweight = vl.nQCDbasedCRTuneerdON_dilep/vl.sigma_dilep/(vl.nQCDbasedCRTuneerdON_ttbar/vl.sigma_ttbar + vl.nQCDbasedCRTuneerdON_dilep/vl.sigma_dilep)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TTTo2L2Nu_QCDbasedCRTune_erdON','ttbar',    r.itSys, 1, "QCDbasedCRTuneerdON")
    p.SetWeight(vl.nominal_weight)

    p.AddSample("TTbar_GluonMoveCRTune_erdON" , "ttbar",     r.itSys, 1, "GluonMoveCRTuneerdON");
    p.UseEnvelope("ttbar", "GluonMoveCRTune,GluonMoveCRTuneerdON,PowhegerdON,QCDbasedCRTuneerdON", "ColorReconnection");
    p.AddSymmetricHisto("ttbar",  "JERUp");


    pdf     = r.PDFToPy(r.TString(pathToTree), r.TString("TTbar_Powheg"), r.TString(NameOfTree), r.TString(StandardCut), r.TString("ElMu"), r.TString(vl.varList[var]['var']), nbins, lowedge, highedge);
    pdf.verbose = False
    pdf.verbose = True
    pdf.SetLumi(vl.Lumi * 1000)
    pdf.SetWeight(vl.nominal_weight)

    hPDFUp  = pdf.GetSystHisto("up","pdf").CloneHisto();
    hPDFDown= pdf.GetSystHisto("Down","pdf").CloneHisto();
    hMEUp   = pdf.GetSystHisto("up","ME").CloneHisto();
    hMEDown = pdf.GetSystHisto("Down","ME").CloneHisto();
    p.PrepareHisto(hPDFUp,   "TTbar_Powheg", "ttbar", r.itSys, 0, "pdfUp");
    p.PrepareHisto(hPDFDown, "TTbar_Powheg", "ttbar", r.itSys, 0, "pdfDown");
    p.PrepareHisto(hMEUp,    "TTbar_Powheg", "ttbar", r.itSys, 0, "ttbarMEUp");
    p.PrepareHisto(hMEDown,  "TTbar_Powheg", "ttbar", r.itSys, 0, "ttbarMEDown");
    p.AddToSystematicLabels("pdf");
    p.AddToSystematicLabels("ttbarME");
    del pdf


    p.doUncInLegend = True;
    p.SetRatioMin( 0.6 );
    p.SetRatioMax( 1.4 );
    p.SetPadPlotMargins(vl.margins)
    p.SetPadRatioMargins(vl.marginsratio)

    p.SetCMSlabel("CMS");
    p.SetCMSmodeLabel("Preliminary");
    p.SetLegendPosition(0.7, 0.45, 0.93, 0.92)
    p.doYieldsInLeg = False;
    p.doSetLogy     = False;
    #p.doData        = False;
    p.doSignal      = False;
    p.SetTitleY(r.TString(vl.varList[var]['yaxis']))

    p.PrintYields("", "", "", "txt,tex")
    p.PrintSystYields()
    p.NoShowVarName = True;
    p.SetOutputName("forBeautifulPlots_{var}".format(var = var));
    p.SaveHistograms();
    del p
    if vl.asimov: del hData
    return


def GiveMeMyAsimovHistos(var):
    binning = array('f', vl.varList[var]['recobinning']) # For some reason, PyROOT requires that you create FIRST this object, then put it inside the PlotToPyC.
    p = r.PlotToPyC(r.TString(vl.varList[var]['var']), r.TString(StandardCut), r.TString('ElMu'), int(len(vl.varList[var]['recobinning']) - 1), binning, r.TString(var), r.TString(vl.varList[var]['xaxis']))
    p.SetPath(pathToTree); p.SetTreeName(NameOfTree);
    p.SetLimitFolder('./temp/{var}_/'.format(var = var))
    p.SetPlotFolder('./temp/{var}_/'.format(var = var))
    p.SetPathSignal(pathToTree);
    p.SetTitleY("Events")
    p.SetLumi(vl.Lumi)
    p.verbose = True
    p.SetWeight(vl.nominal_weight)

    #if "twttbar" not in var.lower():
        #p.AddSample("TTbar_Powheg",          "ttbar",    r.itBkg, 633, systlist, opts)
    #else:
        #p.AddSample('TTbar2L_powheg',        'ttbar',    r.itBkg, 633, systlist, opts)
    
    if "twttbar" not in var.lower():
        specialweight = vl.n_ttbar/vl.sigma_ttbar/(vl.n_ttbar/vl.sigma_ttbar + vl.n_dilep/vl.sigma_dilep)
        p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
        p.AddSample('TTbar_Powheg',          'ttbar',    r.itBkg, 633, systlist, opts)
        specialweight = vl.n_dilep/vl.sigma_dilep/(vl.n_ttbar/vl.sigma_ttbar + vl.n_dilep/vl.sigma_dilep)
        p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
        p.AddSample('TTbar2L_powheg',        'ttbar',    r.itBkg, 633, systlist, opts)
        p.SetWeight(vl.nominal_weight)
    else:
        p.AddSample('TTbar2L_powheg',        'ttbar',    r.itBkg, 633, systlist, opts)
    
    #p.AddSample('TTbar_Powheg',          'ttbar',    r.itBkg, 633, systlist, opts)
    
    p.AddSample("TTbar_PowhegSemi",      "Non-WorZ", r.itBkg, 413, "", opts)
    p.AddSample("WJetsToLNu_MLM",        "Non-WorZ", r.itBkg, 413, "", opts)

    p.AddSample("WZ",                    "VVttbarV", r.itBkg, 390, "", opts)
    p.AddSample("WW",                    "VVttbarV", r.itBkg, 390, "", opts)
    p.AddSample("ZZ",                    "VVttbarV", r.itBkg, 390, "", opts)
    p.AddSample("TTWToLNu",              "VVttbarV", r.itBkg, 390, "", opts)
    p.AddSample("TTWToQQ" ,              "VVttbarV", r.itBkg, 390, "", opts)
    p.AddSample("TTZToQQ" ,              "VVttbarV", r.itBkg, 390, "", opts)
    p.AddSample("TTZToLLNuNu",           "VVttbarV", r.itBkg, 390, "", opts)
    p.AddSample("TTGJets",               "VVttbarV", r.itBkg, 390, "", opts)

    p.AddSample("DYJetsToLL_M5to50_MLM", "DY",       r.itBkg, 852, "", opts)
    p.AddSample("DYJetsToLL_M50_MLM",    "DY",       r.itBkg, 852, "", opts)
    #p.AddSample("DYJetsToLL_M10to50_aMCatNLO","DY",  r.itBkg, 852, "", opts)
    #p.AddSample("DYJetsToLL_M50_aMCatNLO","DY",      r.itBkg, 852, "", opts)
    
    #p.AddSample('TbarW',                  'tW',      r.itBkg, r.TColor.GetColor("#ffcc33"), "", opts) # HI HA UNA MAGIA AQUI QUE FLIPES, NUN CAMUDES EL ORDEN NI AUNQUE TE PAGUEN
    #p.AddSample('TW',                     'tW',      r.itBkg, r.TColor.GetColor("#ffcc33"), "", opts)
    
    specialweight = vl.n_tw/vl.sigma_tw/(vl.n_tw/vl.sigma_tw + vl.n_twnohad/vl.sigma_twnohad)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TW',                     'tW',      r.itBkg, r.TColor.GetColor("#ffcc33"), "", opts)
    specialweight = vl.n_twnohad/vl.sigma_twnohad/(vl.n_tw/vl.sigma_tw + vl.n_twnohad/vl.sigma_twnohad)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TW_noFullyHadr',         'tW',      r.itBkg, r.TColor.GetColor("#ffcc33"), "", opts)
    specialweight = vl.n_tbarw/vl.sigma_tw/(vl.n_tbarw/vl.sigma_tw + vl.n_tbarwnohad/vl.sigma_twnohad)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TbarW',                  'tW',      r.itBkg, r.TColor.GetColor("#ffcc33"), "", opts)
    specialweight = vl.n_tbarwnohad/vl.sigma_twnohad/(vl.n_tbarw/vl.sigma_tw + vl.n_tbarwnohad/vl.sigma_twnohad)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TbarW_noFullyHadr',      'tW',      r.itBkg, r.TColor.GetColor("#ffcc33"), "", opts)
    p.SetWeight(vl.nominal_weight)
    
    hData = r.Histo(copy.deepcopy(p.GetHisto('tW').Clone("hData")))
    for proc in ['ttbar', 'VVttbarV', "DY", "Non-WorZ"]:
        tmph = copy.deepcopy(p.GetHisto(proc).Clone(proc + "_tmp"))
        hData.Add( tmph )
        del tmph
    hData.SetProcess("Data")
    hData.SetTag("Data")
    hData.SetType(r.itData)
    hData.SetColor(r.kBlack)
    p.AddToHistos(hData)
    
    p.doUncInLegend = True;
    p.SetRatioMin( 0.6 );
    p.SetRatioMax( 1.4 );
    p.SetPadPlotMargins(vl.margins)
    p.SetPadRatioMargins(vl.marginsratio)

    p.SetCMSlabel("CMS");
    p.SetCMSmodeLabel("Preliminary");
    p.SetLegendPosition(0.7, 0.45, 0.93, 0.92)
    p.doYieldsInLeg = False;
    p.doSetLogy     = False;
    #p.doData        = False;
    p.doSignal      = False;
    p.SetTitleY(r.TString(vl.varList[var]['yaxis']))
    p.NoShowVarName = True;
    p.SetOutputName("forCards_{var}_asimov".format(var = var));
    p.SaveHistograms();
    del p, hData
    return


def GiveMeMyGoodAsimovHistos(var):
    binning = array('f', vl.varList[var]['recobinning']) # For some reason, PyROOT requires that you create FIRST this object, then put it inside the PlotToPyC.
    p = r.PlotToPyC(r.TString(vl.varList[var]['var']), r.TString(StandardCut), r.TString('ElMu'), int(len(vl.varList[var]['recobinning']) - 1), binning, r.TString(var), r.TString(vl.varList[var]['xaxis']))
    p.SetPath(pathToTree); p.SetTreeName(NameOfTree);
    p.SetLimitFolder('./temp/{var}_/'.format(var = var))
    p.SetPlotFolder('./temp/{var}_/'.format(var = var))
    p.SetPathSignal(pathToTree);
    p.SetTitleY("Events")
    p.SetLumi(vl.Lumi)
    p.verbose = True
    p.SetWeight(vl.nominal_weight)

    #if "twttbar" not in var.lower():
        #p.AddSample("TTbar_Powheg",          "ttbar",    r.itBkg, 633, systlist, opts)
    #else:
        #p.AddSample('TTbar2L_powheg',        'ttbar',    r.itBkg, 633, systlist, opts)
    
    if "twttbar" not in var.lower():
        specialweight = vl.n_ttbar/vl.sigma_ttbar/(vl.n_ttbar/vl.sigma_ttbar + vl.n_dilep/vl.sigma_dilep)
        p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
        p.AddSample('TTbar_Powheg',          'ttbar',    r.itBkg, 633, systlist, opts)
        specialweight = vl.n_dilep/vl.sigma_dilep/(vl.n_ttbar/vl.sigma_ttbar + vl.n_dilep/vl.sigma_dilep)
        p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
        p.AddSample('TTbar2L_powheg',        'ttbar',    r.itBkg, 633, systlist, opts)
        p.SetWeight(vl.nominal_weight)
    else:
        p.AddSample('TTbar2L_powheg',        'ttbar',    r.itBkg, 633, systlist, opts)
    
    #p.AddSample('TTbar_Powheg',          'ttbar',    r.itBkg, 633, systlist, opts)
    
    p.AddSample("TTbar_PowhegSemi",      "Non-WorZ", r.itBkg, 413, "", opts)
    p.AddSample("WJetsToLNu_MLM",        "Non-WorZ", r.itBkg, 413, "", opts)

    p.AddSample("WZ",                    "VVttbarV", r.itBkg, 390, "", opts)
    p.AddSample("WW",                    "VVttbarV", r.itBkg, 390, "", opts)
    p.AddSample("ZZ",                    "VVttbarV", r.itBkg, 390, "", opts)
    p.AddSample("TTWToLNu",              "VVttbarV", r.itBkg, 390, "", opts)
    p.AddSample("TTWToQQ" ,              "VVttbarV", r.itBkg, 390, "", opts)
    p.AddSample("TTZToQQ" ,              "VVttbarV", r.itBkg, 390, "", opts)
    p.AddSample("TTZToLLNuNu",           "VVttbarV", r.itBkg, 390, "", opts)
    p.AddSample("TTGJets",               "VVttbarV", r.itBkg, 390, "", opts)

    p.AddSample("DYJetsToLL_M5to50_MLM", "DY",       r.itBkg, 852, "", opts)
    p.AddSample("DYJetsToLL_M50_MLM",    "DY",       r.itBkg, 852, "", opts)
    #p.AddSample("DYJetsToLL_M10to50_aMCatNLO","DY",  r.itBkg, 852, "", opts)
    #p.AddSample("DYJetsToLL_M50_aMCatNLO","DY",      r.itBkg, 852, "", opts)
    
    #p.AddSample('TbarW',                  'tW',      r.itBkg, r.TColor.GetColor("#ffcc33"), "", opts) # HI HA UNA MAGIA AQUI QUE FLIPES, NUN CAMUDES EL ORDEN NI AUNQUE TE PAGUEN
    #p.AddSample('TW',                     'tW',      r.itBkg, r.TColor.GetColor("#ffcc33"), "", opts)
    
    specialweight = vl.n_tw/vl.sigma_tw/(vl.n_tw/vl.sigma_tw + vl.n_twnohad/vl.sigma_twnohad)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TW',                     'tW',      r.itBkg, r.TColor.GetColor("#ffcc33"), "", opts)
    specialweight = vl.n_twnohad/vl.sigma_twnohad/(vl.n_tw/vl.sigma_tw + vl.n_twnohad/vl.sigma_twnohad)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TW_noFullyHadr',         'tW',      r.itBkg, r.TColor.GetColor("#ffcc33"), "", opts)
    specialweight = vl.n_tbarw/vl.sigma_tw/(vl.n_tbarw/vl.sigma_tw + vl.n_tbarwnohad/vl.sigma_twnohad)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TbarW',                  'tW',      r.itBkg, r.TColor.GetColor("#ffcc33"), "", opts)
    specialweight = vl.n_tbarwnohad/vl.sigma_twnohad/(vl.n_tbarw/vl.sigma_tw + vl.n_tbarwnohad/vl.sigma_twnohad)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TbarW_noFullyHadr',      'tW',      r.itBkg, r.TColor.GetColor("#ffcc33"), "", opts)
    p.SetWeight(vl.nominal_weight)
    
    hData = r.Histo(copy.deepcopy(p.GetHisto('tW').Clone("hData")))
    for proc in ['ttbar', 'VVttbarV', "DY", "Non-WorZ"]:
        tmph = copy.deepcopy(p.GetHisto(proc).Clone(proc + "_tmp"))
        hData.Add( tmph )
        del tmph
    hData.SetProcess("Data")
    hData.SetTag("Data")
    hData.SetType(r.itData)
    hData.SetColor(r.kBlack)
    p.AddToHistos(hData)
    
    # Modelling systematics
    p.AddSample("TW"                           , "tW",           r.itSys, 1, "JERUp");
    p.AddSample("TW_noFullyHadr_isrUp"         , "tW",           r.itSys, 1, "isrUp");
    p.AddSample("TW_noFullyHadr_isrDown"       , "tW",           r.itSys, 1, "isrDown");
    p.AddSample("TW_noFullyHadr_fsrUp"         , "tW",           r.itSys, 1, "fsrUp");
    p.AddSample("TW_noFullyHadr_fsrDown"       , "tW",           r.itSys, 1, "fsrDown");
    p.AddSample("TW_noFullyHadr_MEscaleUp"     , "tW",           r.itSys, 1, "tWMEUp");
    p.AddSample("TW_noFullyHadr_MEscaleDown"   , "tW",           r.itSys, 1, "tWMEDown");
    p.AddSample("TW_mtop1755"                  , "tW",           r.itSys, 1, "mtopUp");
    p.AddSample("TW_mtop1695"                  , "tW",           r.itSys, 1, "mtopDown");

    p.AddSample("TbarW"                        , "tW",           r.itSys, 1, "JERUp");
    p.AddSample("TbarW_noFullyHadr_isrUp"      , "tW",           r.itSys, 1, "isrUp");
    p.AddSample("TbarW_noFullyHadr_isrDown"    , "tW",           r.itSys, 1, "isrDown");
    p.AddSample("TbarW_noFullyHadr_fsrUp"      , "tW",           r.itSys, 1, "fsrUp");
    p.AddSample("TbarW_noFullyHadr_fsrDown"    , "tW",           r.itSys, 1, "fsrDown");
    p.AddSample("TbarW_noFullyHadr_MEscaleUp"  , "tW",           r.itSys, 1, "tWMEUp");
    p.AddSample("TbarW_noFullyHadr_MEscaleDown", "tW",           r.itSys, 1, "tWMEDown");
    p.AddSample("TbarW_noFullyHadr_mtop1755"   , "tW",           r.itSys, 1, "mtopUp");
    p.AddSample("TbarW_noFullyHadr_mtop1695"   , "tW",           r.itSys, 1, "mtopDown");

    p.AddSample("TW_noFullyHadr_DS",             "tW",           r.itSys, 1, "DSUp");
    p.AddSample("TbarW_noFullyHadr_DS",          "tW",           r.itSys, 1, "DSUp");
    p.AddSymmetricHisto("tW",  "DSUp");
    p.AddSymmetricHisto("tW",  "JERUp");

    p.AddSample("TTbar_Powheg",                 "ttbar",     r.itSys, 1, "JERUp");

    specialweight = vl.nUEUp_ttbar/vl.sigma_ttbar/(vl.nUEUp_ttbar/vl.sigma_ttbar + vl.nUEUp_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar_Powheg_ueUp",            "ttbar",     r.itSys, 1, "UEUp");
    specialweight = vl.nUEUp_dilep/vl.sigma_dilep/(vl.nUEUp_ttbar/vl.sigma_ttbar + vl.nUEUp_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar2L_Powheg_ueUp",          "ttbar",     r.itSys, 1, "UEUp");
    specialweight = vl.nUEDown_ttbar/vl.sigma_ttbar/(vl.nUEDown_ttbar/vl.sigma_ttbar + vl.nUEDown_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar_Powheg_ueDown",          "ttbar",     r.itSys, 1, "UEDown");
    specialweight = vl.nUEDown_dilep/vl.sigma_dilep/(vl.nUEDown_ttbar/vl.sigma_ttbar + vl.nUEDown_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar2L_Powheg_ueDown",        "ttbar",     r.itSys, 1, "UEDown");
    specialweight = vl.nhDampUp_ttbar/vl.sigma_ttbar/(vl.nhDampUp_ttbar/vl.sigma_ttbar + vl.nhDampUp_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar_Powheg_hdampUp",         "ttbar",     r.itSys, 1, "hDampUp");
    specialweight = vl.nhDampUp_dilep/vl.sigma_dilep/(vl.nhDampUp_ttbar/vl.sigma_ttbar + vl.nhDampUp_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar2L_Powheg_hdampUp",       "ttbar",     r.itSys, 1, "hDampUp");
    specialweight = vl.nhDampDown_ttbar/vl.sigma_ttbar/(vl.nhDampDown_ttbar/vl.sigma_ttbar + vl.nhDampDown_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar_Powheg_hdampDown",       "ttbar",     r.itSys, 1, "hDampDown");
    specialweight = vl.nhDampDown_dilep/vl.sigma_dilep/(vl.nhDampDown_ttbar/vl.sigma_ttbar + vl.nhDampDown_dilep/vl.sigma_dilep);
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight));
    p.AddSample("TTbar2L_Powheg_hdampDown",     "ttbar",     r.itSys, 1, "hDampDown");
    p.SetWeight(vl.nominal_weight);

    p.AddSample("TTbar_Powheg_isrUp"          , "ttbar",     r.itSys, 1, "isrUp");
    p.AddSample("TTbar_Powheg_isrDown"        , "ttbar",     r.itSys, 1, "isrDown");
    p.AddSample("TTbar_Powheg_fsrUp"          , "ttbar",     r.itSys, 1, "fsrUp");
    p.AddSample("TTbar_Powheg_fsrDown"        , "ttbar",     r.itSys, 1, "fsrDown");
    p.AddSample("TTbar_Powheg_mtop1755"       , "ttbar",     r.itSys, 1, "mtopUp");
    p.AddSample("TTbar_Powheg_mtop1695"       , "ttbar",     r.itSys, 1, "mtopDown");

    specialweight = vl.nGluonMoveCRTune_ttbar/vl.sigma_ttbar/(vl.nGluonMoveCRTune_ttbar/vl.sigma_ttbar + vl.nGluonMoveCRTune_dilep/vl.sigma_dilep)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TTbar_GluonMoveCRTune',        'ttbar',     r.itSys, 1, "GluonMoveCRTune")
    specialweight = vl.nGluonMoveCRTune_dilep/vl.sigma_dilep/(vl.nGluonMoveCRTune_ttbar/vl.sigma_ttbar + vl.nGluonMoveCRTune_dilep/vl.sigma_dilep)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TTTo2L2Nu_GluonMoveCRTune',    'ttbar',     r.itSys, 1, "GluonMoveCRTune")
    specialweight = vl.nPowhegerdON_ttbar/vl.sigma_ttbar/(vl.nPowhegerdON_ttbar/vl.sigma_ttbar + vl.nPowhegerdON_dilep/vl.sigma_dilep)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TTbar_Powheg_erdON',           'ttbar',     r.itSys, 1, "PowhegerdON")
    specialweight = vl.nPowhegerdON_dilep/vl.sigma_dilep/(vl.nPowhegerdON_ttbar/vl.sigma_ttbar + vl.nPowhegerdON_dilep/vl.sigma_dilep)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TTTo2L2Nu_Powheg_erdON',       'ttbar',     r.itSys, 1, "PowhegerdON")
    specialweight = vl.nQCDbasedCRTuneerdON_ttbar/vl.sigma_ttbar/(vl.nQCDbasedCRTuneerdON_ttbar/vl.sigma_ttbar + vl.nQCDbasedCRTuneerdON_dilep/vl.sigma_dilep)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TTbar_GluonMoveCRTune_erdON',  'ttbar',     r.itSys, 1, "QCDbasedCRTuneerdON")
    specialweight = vl.nQCDbasedCRTuneerdON_dilep/vl.sigma_dilep/(vl.nQCDbasedCRTuneerdON_ttbar/vl.sigma_ttbar + vl.nQCDbasedCRTuneerdON_dilep/vl.sigma_dilep)
    p.SetWeight(vl.nominal_weight + "*" + str(specialweight))
    p.AddSample('TTTo2L2Nu_QCDbasedCRTune_erdON','ttbar',    r.itSys, 1, "QCDbasedCRTuneerdON")
    p.SetWeight(vl.nominal_weight)

    p.AddSample("TTbar_GluonMoveCRTune_erdON" , "ttbar",     r.itSys, 1, "GluonMoveCRTuneerdON");
    p.UseEnvelope("ttbar", "GluonMoveCRTune,GluonMoveCRTuneerdON,PowhegerdON,QCDbasedCRTuneerdON", "ColorReconnection");
    p.AddSymmetricHisto("ttbar",  "JERUp");


    pdf     = r.PDFToPyC(r.TString(pathToTree), r.TString("TTbar_Powheg"), r.TString(NameOfTree), r.TString(StandardCut), r.TString("ElMu"), r.TString(vl.varList[var]['var']), len(vl.varList[var]['recobinning']) - 1, binning, r.TString(''));
    pdf.verbose = False
    pdf.verbose = True
    pdf.SetLumi(vl.Lumi * 1000)
    pdf.SetWeight(vl.nominal_weight)

    hPDFUp  = pdf.GetSystHisto("up","pdf").CloneHisto();
    hPDFDown= pdf.GetSystHisto("Down","pdf").CloneHisto();
    hMEUp   = pdf.GetSystHisto("up","ME").CloneHisto();
    hMEDown = pdf.GetSystHisto("Down","ME").CloneHisto();
    p.PrepareHisto(hPDFUp,   "TTbar_Powheg", "ttbar", r.itSys, 0, "pdfUp");
    p.PrepareHisto(hPDFDown, "TTbar_Powheg", "ttbar", r.itSys, 0, "pdfDown");
    p.PrepareHisto(hMEUp,    "TTbar_Powheg", "ttbar", r.itSys, 0, "ttbarMEUp");
    p.PrepareHisto(hMEDown,  "TTbar_Powheg", "ttbar", r.itSys, 0, "ttbarMEDown");
    p.AddToSystematicLabels("pdf");
    p.AddToSystematicLabels("ttbarME");
    del pdf

    p.doUncInLegend = True;
    p.SetRatioMin( 0.6 );
    p.SetRatioMax( 1.4 );
    p.SetPadPlotMargins(vl.margins)
    p.SetPadRatioMargins(vl.marginsratio)

    p.SetCMSlabel("CMS");
    p.SetCMSmodeLabel("Preliminary");
    p.SetLegendPosition(0.7, 0.45, 0.93, 0.92)
    p.doYieldsInLeg = False;
    p.doSetLogy     = False;
    #p.doData        = False;
    p.doSignal      = False;
    p.SetTitleY(r.TString(vl.varList[var]['yaxis']))
    p.NoShowVarName = True;
    p.SetOutputName("forCards_{var}_goodasimov".format(var = var));
    p.SaveHistograms();
    del p, hData
    return

def lazyoptimisation(tsk):
    var, ty = tsk
    if   ty == "histos":    return GiveMeMyHistos(var)
    elif ty == "asihist":   return GiveMeMyAsimovHistos(var)
    elif ty == "beautiful": return GiveMeMyGoodHistosToShowThem(var)
    else:                   return GiveMeMyGoodAsimovHistos(var)
    return


if __name__=="__main__":
    print "===== Variable's histograms procedure.\n"
    vl.SetUpWarnings()
    
    if (len(sys.argv) > 1):
        varName     = sys.argv[1]
        print "> Chosen variable:", varName, "\n"
        if (len(sys.argv) > 2):
            nCores      = int(sys.argv[2])
            print ('> Parallelization will be done with ' + str(nCores) + ' cores')
            if (len(sys.argv) > 3):
                if sys.argv[3] == 'last':
                    pathToTree    = vl.GetLastFolder(vl.storagepath)
                else:
                    pathToTree    = vl.storagepath + sys.argv[3] + "/"
            else:
                pathToTree  = vl.minipath
            print "> Minitrees will be read from:", pathToTree, "\n"
        else:
            print '> Sequential execution mode chosen'
            nCores      = 1
            pathToTree  = vl.minipath
    else:
        print "> Default choice of variable and minitrees\n"
        varName     = 'LeadingLepEta'
        pathToTree  = vl.minipath
        nCores      = 1

    print "> Beginning to produce histograms", "\n"
    tasks = []
    if varName == 'All':
        for vr in vl.varList['Names']['Variables']:
            for ty in ["histos", "asihist", "goodasihist", "beautiful"]:
                if not vl.asimov:      tasks.append( (vr, ty) )
                elif (ty == "histos"): tasks.append( (vr, ty) )
    else:
        for ty in ["histos", "asihist", "goodasihist"]:
            if not vl.asimov:      tasks.append( (varName, ty) )
            elif (ty == "histos"): tasks.append( (varName, ty) )

    pool    = Pool(nCores)
    pool.map(lazyoptimisation, tasks)
    pool.close()
    pool.join()
    del pool

    print "> Done!", "\n"
