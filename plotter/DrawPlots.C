#include "Histo.h"
#include "Looper.h"
#include "Plot.h"
R__LOAD_LIBRARY(Histo.C+)
R__LOAD_LIBRARY(Looper.C+)
R__LOAD_LIBRARY(TResultsTable.C+)
R__LOAD_LIBRARY(Plot.C+)


void DrawPlot(TString var, TString cut, TString chan, Int_t nbins, Float_t bin0, Float_t binN, TString Xtitle, TString varName="", TString cutName="", TString outFolder="");
TString NameOfTree = "top";
TString pathToTree = "/mnt_pool/ciencias_users/user/carlosec/AnalysisPAF/WZ_temp/";

bool doSync = false;


void DrawPlots(){
 DrawPlot("TMET", "TIsSR==1", "All",       8, 0, 200, "Jet Multiplicity", "nJets");
 gApplication->Terminate();
}

void DrawPlot(TString var, TString cut, TString chan, Int_t nbins, Float_t bin0, Float_t binN, TString Xtitle, TString varName, TString cutName, TString outFolder){
  Plot* p = new Plot(var, cut, chan, nbins, bin0, binN, "Title", Xtitle);
  if(outFolder!="") p->SetPlotFolder(outFolder);
	std::cout << "PATH SET\n";
  p->SetPath(pathToTree);
	std::cout << "NAME SET\n";
  p->SetTreeName(NameOfTree);
  p->verbose = true;

  if(varName != "") p->SetVarName(varName);
  if(cutName != "") p->SetOutputName(cutName);
	std::cout << "ADD SAMPLE\n";
	//Signal  
  //p->AddSample("WZTo3LNu",                                        "WZ",       itSignal, kYellow);    // WZ
	std::cout << "SAMPLE ADDED\n";
	//Drell-Yan
  //p->AddSample("DYJetsToLL_M50_MLM, DYJetsToLL_M5to50_MLM",         "DY",       itBkg, kOrange);  // DY
  //p->AddSample("WJetsToLNu_MLM",         "WJets",       itBkg, kOrange-3);  												// WJets

  //p->AddSample("WWTo2L2Nu, WpWpJJ, WWTo2L2Nu_DoubleScat",         "WW",       itBkg, kBlue + 10);  // WW
	
  p->AddSample("WWW, WWZ, WZZ, ZZZ, VHToNonbb_amcatnlo","VVV",  itBkg, kGreen-9); // VVV

  //p->AddSample("TGJets, TTGJets, WGToLNuG, ZGTo2LG, WWG_amcatnlo, WZG_amcatnlo", "X+#gamma", itBkg, kViolet+2);  // X+gamma 

  //p->AddSample("TTZToLL_M1to10, TTZToLLNuNu, TTWToLNu, TTTT, TTHNonbb", "tt+X", itBkg, kRed-10);  // X+gamma 

//  p->AddSample("TTbar_Powheg", "tt", itBkg, kRed);  // tt

//  p->AddSample("TW_noFullyHadr, T_tch, Tbar_tch, TbarW_noFullyHadr, TToLeptons_sch_amcatnlo", "t", itBkg, kRed);  // tt	 

// p->AddSample("tZq_ll", "tZq", itBkg, kGreen);  // tt	 

  //p->AddSample("ZZTo4L", "ZZ", itBkg, kCyan-5);  // ZZ	 

	//p->AddSample("MuonEG, DoubleEG, DoubleMuon",                     "Data",  itData);             // Data

  p->SetSignalProcess("WZ");
  //p->ScaleSignal(10);
  p->SetSignalStyle("SM");

	std::cout << "SET SIGNAL STYLE\n";

  p->SetRatioMin(0.2);
  p->SetRatioMax(1.8);
	std::cout << "SET RATIOS\n";

  //p->AddSystematic("JES,Btag,MisTag,LepEff,PU");
  p->AddSystematic("stat");

	std::cout << "ADDED SYSTEMATICS\n";
  cout << "Selection = " << varName << endl;
  cout << "Corresponding to cut: " << cut << endl;
  p->PrintYields();
  //p->PrintSamples();
  p->doSetLogy = false;
  p->DrawStack("0", 1);
  //p->doSetLogy = true;
  //p->DrawStack("log", 1);
  //p->PrintSystYields();
  delete p;
}

