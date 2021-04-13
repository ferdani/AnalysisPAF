#include "WZAnalysis.h"



#define IF_JEC_UP if (VAR == 0)
#define IF_JEC_DO if (VAR == 1)
#define IF_BTG_UP if (VAR == 2)
#define IF_BTG_DO if (VAR == 3)
#define IF_NORMAL if (VAR == 4)


ClassImp(WZAnalysis);

bool GreaterThan(float i, float j){ return (i > j);}

WZAnalysis::WZAnalysis() : PAFChainItemSelector() {
  fhDummy = 0;
  passMETfilters = 0;
  passTrigger    = 0;
}
void WZAnalysis::Summary(){}

void WZAnalysis::Initialise(){
  gIsData      = GetParam<Bool_t>("IsData");
  gSelection   = GetParam<Int_t>("iSelection");
  gSampleName  = GetParam<TString>("sampleName");
  localPath    = GetParam<TString>("WorkingDir");
  gDoSyst      = GetParam<Bool_t>("doSyst");
  gIsTTbar     = false;
  gIsLHE       = false;
  if (gSampleName.Contains("TTbar") || gSampleName.Contains("TTJets")) gIsTTbar = true;
  if (gSampleName == "TTbar_Powheg") gIsLHE = true;
  leptonSFtop = new LeptonSF(localPath + "/InputFiles/");
  leptonSFEWKM = new LeptonSF(localPath + "/InputFiles/");
  leptonSFEWKVT = new LeptonSF(localPath + "/InputFiles/");

  if (!gIsData){
    leptonSFtop->loadHisto(iMuonId,   iTight);          //Only top
    leptonSFtop->loadHisto(iMuonIsoTightId,   iTight);//Only top
    leptonSFtop->loadHisto(iElecId,   iTight);        //Only top
    leptonSFEWKM->loadHisto(iMuonEWKinoID);//Only MVA
    leptonSFEWKM->loadHisto(iMuonEWKinomvaM);//Only MVA
    leptonSFEWKM->loadHisto(iElecEWKinoID);//Only MVA
    leptonSFEWKM->loadHisto(iElecEWKinomvaM);//Only MVA
    leptonSFEWKVT->loadHisto(iMuonEWKinoID);//Only MVA
    leptonSFEWKVT->loadHisto(iMuonEWKinomvaVT);//Only MVA
    leptonSFEWKVT->loadHisto(iElecEWKinoID);//Only MVA
    leptonSFEWKVT->loadHisto(iElecEWKinomvaVT);//Only MVA
  }
  makeTree = true;
  makeHistos = true;
  if(makeTree){
    for(int i = 0; i < nWPoints; i++){
      fTree[i]   = CreateTree(sWPoints[i],"Created with PAF");
      SetLeptonVariables(fTree[i]);
      SetJetVariables(fTree[i]);
      SetEventVariables(fTree[i]);
    }
  }
  InitHistos();
}


void WZAnalysis::InsideLoop(){
  // Vectors with the objects
  genLeptons  = GetParam<vector<Lepton>>("genLeptons");
  genParticles= GetParam<vector<Lepton>>("genParticles");
  selLeptons  = GetParam<vector<Lepton>>("selLeptons");
  foLeptons = GetParam<vector<Lepton>>("vetoLeptons");
  looseLeptons = GetParam<vector<Lepton>>("looseLeptons");
  selJets     = GetParam<vector<Jet>>("selJets");
  selJetsJecUp   = GetParam<vector<Jet>>("selJetsJecUp");
  selJetsJecDown = GetParam<vector<Jet>>("selJetsJecDown");
  Jets15      = GetParam<vector<Jet>>("Jets15");
  vetoJets    = GetParam<vector<Jet>>("vetoJets");
  genJets     = GetParam<vector<Jet>>("genJets");
  mcJets      = GetParam<vector<Jet>>("mcJets");
  // Weights and SFs
  NormWeight = GetParam<Float_t>("NormWeight");
  TrigSF       = GetParam<Float_t>("TriggerSF");
  TrigSFerr    = GetParam<Float_t>("TriggerSFerr");
  PUSF         = GetParam<Float_t>("PUSF");
  PUSF_Up      = GetParam<Float_t>("PUSF_Up");
  PUSF_Down    = GetParam<Float_t>("PUSF_Down");


  // Event variables
  gChannel       = GetParam<Int_t>("gChannel");
  passMETfilters = GetParam<Bool_t>("METfilters");
  passTrigger    = GetParam<Bool_t>("passTrigger");
  TEvtNum        = Get<ULong64_t>("evt");

  //std::cout << "test 0 " << std::endl;




  //std::cout << "evtNum: " << TEvtNum << std::endl;






  for (int VAR = 0; VAR < 5; VAR ++) // The Great Bucle
  {
    // 0 -> JEC up
    // 1 -> JEC down
    // 2 -> BTag up
    // 3 -> BTag down
    // 4 -> Nothing special
  for (int wP = 0; wP < nWPoints; wP++)
  {
    // Leptons and Jets
    //std::cout << "Create vectors\n";
      tightLeptons = {};
      fakeableLeptons = {};
      GetLeptonsByWP(wP);
    //std::cout << "Get Tight/FO\n";
      GetLeptonVariables(tightLeptons, fakeableLeptons, looseLeptons);
    //std::cout << "Get Lepton\n";
      /*IF_NORMAL */GetJetVariables(selJets, Jets15, VAR);
      //IF_JEC_UP GetJetVariables(selJetsJecUp, Jets15);
      //IF_JEC_DO GetJetVariables(selJetsJecDown, Jets15);     // estas tuplas no sirven
      //, cua pTJESUp   = p.Pt();, etc y tira con selJets 
    //std::cout << "Get Jet\n";
      GetGenJetVariables(genJets, mcJets);
    //std::cout << "Get GenVariables\n";

      GetMET(VAR);

    //std::cout << "Match gen/reco\n";
    //fakeableLeptons = getMatchGenSelLeptons(fakeableLeptons, genLeptons, 0.3, true); // Match gen and sel Leptons, require same Id
    //fakeableLeptons = getMatchGenSelLeptons(fakeableLeptons, genParticles, 0.3, false); // Match gen particles and sel Leptons, do not require same Id (allow for taus)
    //std::cout << "test 1 " << std::endl;




    //std::cout << TNOSSF<< " " << passTrigger<< " "<< passMETfilters<< " "<< std::endl;






    if((TNFOLeps >= 3) && TNOSSF > 0  && passTrigger && passMETfilters){ 
    //if(TNFOLeps < 3 && TNOSSF > 0  && passTrigger && passMETfilters){ // trilepton event with OSSF + l, passes trigger and MET filters

    // Deal with weights:
    //std::cout << "Pass 3FO\n";
      Float_t lepSF   = fakeableLeptons.at(0).GetSF(0)*fakeableLeptons.at(1).GetSF(0)*fakeableLeptons.at(2).GetSF(0);
      Float_t ElecSF = 1; Float_t MuonSF = 1;
      Float_t ElecSFUp = 1; Float_t ElecSFDo = 1; Float_t MuonSFUp = 1; Float_t MuonSFDo = 1;
      Float_t stat = 0; 
      //For muons
      //https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonReferenceEffsRun2
      //Additional 1% for ID + 0.5% for Isolation + 0.5% single muon triggers
  
      if(TChannel == iElElEl){
        ElecSF   = fakeableLeptons.at(0).GetSF( 0)*fakeableLeptons.at(1).GetSF( 0)*fakeableLeptons.at(2).GetSF( 0);
        ElecSFUp = fakeableLeptons.at(0).GetSF( 1)*fakeableLeptons.at(1).GetSF( 1)*fakeableLeptons.at(2).GetSF( 1);
        ElecSFDo = fakeableLeptons.at(0).GetSF(-1)*fakeableLeptons.at(1).GetSF(-1)*fakeableLeptons.at(2).GetSF(-1);
        MuonSFUp = 1; MuonSFDo = 1; MuonSF = 1;
      }
      else if(TChannel == iMuMuMu){
        MuonSF   = fakeableLeptons.at(0).GetSF( 0)*fakeableLeptons.at(1).GetSF( 0)*fakeableLeptons.at(2).GetSF( 0);
        MuonSFUp = fakeableLeptons.at(0).GetSF( 1)*fakeableLeptons.at(1).GetSF( 1)*fakeableLeptons.at(2).GetSF( 1);
        MuonSFDo = fakeableLeptons.at(0).GetSF(-1)*fakeableLeptons.at(1).GetSF(-1)*fakeableLeptons.at(2).GetSF(-1);
        ElecSFUp = 1; ElecSFDo = 1; ElecSF = 1;
      }
      else{
        MuonSFUp = 1; MuonSFDo = 1; MuonSF = 1;ElecSFUp = 1; ElecSFDo = 1; ElecSF = 1;
        for (int i = 0; i <3; i ++){
          if (fakeableLeptons.at(i).isMuon){
            MuonSF   *= fakeableLeptons.at(i).GetSF( 0);
            MuonSFUp *= fakeableLeptons.at(i).GetSF( 1);
            MuonSFDo *= fakeableLeptons.at(i).GetSF(-1);
          } 
          else{
            ElecSF   *= fakeableLeptons.at(i).GetSF( 0);
            ElecSFUp *= fakeableLeptons.at(i).GetSF( 1);
            ElecSFDo *= fakeableLeptons.at(i).GetSF(-1);        
          }
        }
      }
  
      TWeight = NormWeight*ElecSF*MuonSF*TrigSF*PUSF;

      TWeight_PUSF_Up = NormWeight*ElecSF*MuonSF*TrigSF*PUSF_Up;
      TWeight_PUSF_Down = NormWeight*ElecSF*MuonSF*TrigSF*PUSF_Down;

      TWeight_ElecSFUp = NormWeight*ElecSFUp*MuonSF*TrigSF*PUSF;
      TWeight_ElecSFDown = NormWeight*ElecSFDo*MuonSF*TrigSF*PUSF;

      TWeight_MuonSFUp = NormWeight*ElecSF*MuonSFUp*TrigSF*PUSF;
      TWeight_MuonSFDown = NormWeight*ElecSF*MuonSFDo*TrigSF*PUSF;


      IF_NORMAL TIsSRVBS   = false;
      IF_JEC_UP TIsSRVBS_JEC_UP   = false;
      IF_JEC_DO TIsSRVBS_JEC_DO   = false;
      IF_BTG_UP TIsSRVBS_BTG_UP   = false;
      IF_BTG_DO TIsSRVBS_BTG_DO   = false;

      TIsSR   = false;
      TIsSRVBS = false;
      passMandEtaRequieriments = false;
      passEtaFilters = false;
      TIsCRDY = false;
      TIsCRTT = false;  

      // one region for each cut
      TIsCRVBS_0 = false; TIsCRVBS_1 = false, TIsCRVBS_2 = false;
      TIsCRVBS_3 = false; TIsCRVBS_4 = false, TIsCRVBS_5 = false;
      TIsCRVBS_6 = false; TIsCRVBS_7 = false, TIsCRVBS_8 = false;
      TIsCRVBS_9 = false; TIsCRVBS_10 = false, TIsCRVBS_11 = false;
      TIsCRVBS_12 = false; TIsCRVBS_13 = false;




      TIsCRtop = false;  
      TIsCRConv = false;
      TIsCRZZ = false;

      TIsNewCRDY = false;
      TIsNewCRTT = false;  
      if(gIsData)
      {
        TWeight = 1;
        TWeight_PUSF_Up = 1;
        TWeight_PUSF_Down = 1;
        TWeight_ElecSFUp = 1;
        TWeight_ElecSFDown = 1;
        TWeight_MuonSFUp = 1;
        TWeight_MuonSFDown = 1;
      }
      // Event Selection
      // ===================================================================================================================
      TM3l  = -999;
      TMtWZ = -999;
      IF_JEC_UP TMtWZ_JEC_UP = -999;
      IF_JEC_DO TMtWZ_JEC_DO = -999;
      TMtW  = -999;
      IF_JEC_UP TMtW_JEC_UP = -999;
      IF_JEC_DO TMtW_JEC_DO = -999;
      TMll  = -999;
      TMZ1W = -999;
      TMZ2W = -999;
      //std::cout << "ASSIGNS\n";
      std::vector<Lepton> tempLeps = AssignWZLeptons(fakeableLeptons);
      tempLeps = getMatchGenSelLeptons(tempLeps, tightLeptons, 0.4, true);

      lepZ1 = tempLeps.at(0);
      lepZ2 = tempLeps.at(1);
      lepW  = tempLeps.at(2);

      TLep_SFerrZ1 = tempLeps.at(0).GetSF( 1);
      TLep_SFerrZ2 = tempLeps.at(1).GetSF( 1);
      TLep_SFerrW = tempLeps.at(2).GetSF( 1);

      TLep_PtZ1 = lepZ1.Pt();
      TLep_EtaZ1 = lepZ1.Eta();
      TLep_PhiZ1 = lepZ1.Phi();
      TLep_EZ1 = lepZ1.E();
      TLep_ChargeZ1 = lepZ1.charge;
      TLep_IsTightZ1 =  (lepZ1.lepMatch == 0) ? 0 : 1;
      TLep_pdgIdZ1 = lepZ1.type;

      TLep_PtZ2 = lepZ2.Pt();
      TLep_EtaZ2 = lepZ2.Eta();
      TLep_PhiZ2 = lepZ2.Phi();
      TLep_EZ2 = lepZ2.E();
      TLep_ChargeZ2 = lepZ2.charge;
      TLep_IsTightZ2 =  (lepZ2.lepMatch == 0) ? 0 : 1;
      TLep_pdgIdZ2 = lepZ2.type;

      TLep_PtW = lepW.Pt();
      TLep_EtaW = lepW.Eta();
      TLep_PhiW = lepW.Phi();
      TLep_EW = lepW.E();
      TLep_ChargeW = lepW.charge;
      TLep_IsTightW =  (lepW.lepMatch == 0) ? 0 : 1;
      TLep_pdgIdW = lepW.type;

      //std::cout << "REMATCHES\n";
      TLep_IsPromptW = lepW.idDecayMode;
      TLep_IsPromptZ2 = lepZ2.idDecayMode;
      TLep_IsPromptZ1 = lepZ1.idDecayMode;
      
      
      //std::cout << "test 3 " << std::endl;


      for(Int_t i = 0; i < TNFOLeps; i++){
        TLep_isConvVeto[i]  = tempLeps.at(i).isConvVeto;
      }
      TLorentzVector metVector = TLorentzVector();

      IF_NORMAL metVector.SetPtEtaPhiM(TMET, TMET_Phi, 0., 0.);
      IF_BTG_UP metVector.SetPtEtaPhiM(TMET, TMET_Phi, 0., 0.);
      IF_BTG_DO metVector.SetPtEtaPhiM(TMET, TMET_Phi, 0., 0.);
      IF_JEC_UP metVector.SetPtEtaPhiM(TMET_JEC_UP, TMET_Phi_JEC_UP, 0., 0.);
      IF_JEC_DO metVector.SetPtEtaPhiM(TMET_JEC_DO, TMET_Phi_JEC_DO, 0., 0.);

      TM3l = (lepZ1.p + lepZ2.p + lepW.p).M();

      IF_NORMAL TMtWZ = (lepZ1.p + lepZ2.p + lepW.p + metVector).Mt();
      IF_BTG_UP TMtWZ = (lepZ1.p + lepZ2.p + lepW.p + metVector).Mt();
      IF_BTG_DO TMtWZ = (lepZ1.p + lepZ2.p + lepW.p + metVector).Mt();
      IF_JEC_UP TMtWZ_JEC_UP = (lepZ1.p + lepZ2.p + lepW.p + metVector).Mt();
      IF_JEC_DO TMtWZ_JEC_DO = (lepZ1.p + lepZ2.p + lepW.p + metVector).Mt();

      IF_NORMAL TMtW  = (lepW.p + metVector).Mt(); 
      IF_BTG_UP TMtW  = (lepW.p + metVector).Mt(); 
      IF_BTG_DO TMtW  = (lepW.p + metVector).Mt(); 
      IF_JEC_UP TMtW_JEC_UP  = (lepW.p + metVector).Mt();
      IF_JEC_DO TMtW_JEC_DO  = (lepW.p + metVector).Mt();

      TMll  = (lepZ1.p + lepZ2.p).M();
      TMZ1W  = (lepZ1.p + lepW.p).M();
      TMZ2W  = (lepZ2.p + lepW.p).M();


      //WZ VBS region
      // >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      Bool_t tooManyLeps = false; // TODO: move me to the header
      if (TNFOLeps >= 3 && (passesMCTruth(fakeableLeptons,1,TNFOLeps)))
      {
        TIsCRVBS_13 = true;

        // extra leps must have pt < 10 GeV
        for (int a = 3; a < TNFOLeps; a++)
        {
          if (tempLeps.at(a).Pt() > 10)
          {
            tooManyLeps = true;
          }
        }
        
        if (lepZ1.Pt() > 25 && lepZ2.Pt() > 15 && lepW.Pt() > 20) {
          TIsCRVBS_11 = true;
          }
        if (tooManyLeps == false) {TIsCRVBS_12 = true;}
        

        if (lepZ1.Pt() > 25 && lepZ2.Pt() > 15 && lepW.Pt() > 20 && tooManyLeps == false)
        {
          if (TMath::Abs(TMll - nomZmass) < 15.) {TIsCRVBS_8 = true;}
          if (TMinMll > 4) {TIsCRVBS_9 = true;}
          if (TM3l > 90.) {TIsCRVBS_10 = true;} //====

          IF_NORMAL MllnomMZ = TMath::Abs(TMll - nomZmass);
          IF_BTG_UP MllnomMZ = TMath::Abs(TMll - nomZmass);
          IF_BTG_DO MllnomMZ = TMath::Abs(TMll - nomZmass);
          IF_JEC_UP MllnomMZ_JEC_UP = TMath::Abs(TMll - nomZmass); 
          IF_JEC_DO MllnomMZ_JEC_DO = TMath::Abs(TMll - nomZmass);

          if (TMath::Abs(TMll - nomZmass) < 15. && TMinMll > 4. && TM3l > 90.) // ====
          {
            TIsCRVBS_7 = true;
            passEtaFilters = true;
            for (int a  = 0; a < TNFOLeps; a++)
            { 
              if ((tempLeps.at(a).isMuon && abs(tempLeps.at(a).Eta()) >= 2.4) || 
                  (tempLeps.at(a).isElec && abs(tempLeps.at(a).Eta()) >= 2.5))
                  {passEtaFilters = false; break;}
            }

              if (TMET > 30) {TIsCRVBS_5 = true;}
              if (passEtaFilters) {TIsCRVBS_6 = true;}

            if (passEtaFilters && TMET > 10)  // TMET > 30
            {
              TIsCRVBS_4 = true;
              badBJets = false; // B jets with pt > 30 & eta < 4.7 
              numGoodJets = 0; // pt > 50 GeV y eta < 4.7, 2 MIN.
              std::vector <Int_t> indexes = {}; // where are the good jets

              for (int a = 0; a < TNJets; a++)
              {
                if (TJet_Pt[a] > 30 && TJet_Eta[a] < 4.7 && TJet_isBJet[a])
                {
                  badBJets = true; break;
                }

                if (TJet_Pt[a] > 50 && TJet_Eta[a] < 4.7)
                {
                  numGoodJets ++;
                  indexes.push_back(a);
                }
              }
              
              passMandEtaRequieriments = false;
              //bool passMandEtaRequieriments = false; // mjj > 500 GeV, Deta > 2.5
              
              if (!badBJets) {TIsCRVBS_3 = true;}
              if (numGoodJets >= 2) {TIsCRVBS_2 = true;}

              //if (!badBJets && numGoodJets >= 2)
              if (numGoodJets >= 2)
              {
                TIsCRVBS_1 = true;

                TLorentzVector jet1;
                TLorentzVector jet2;

                for (unsigned int r = 0; r < indexes.size(); r++)
                {
                  for (unsigned int s = 0; s < indexes.size(); s++)
                  {
                    if (r != s)
                    {
                      jet1.SetPxPyPzE(TJet_Px[r], TJet_Py[r], TJet_Pz[r], TJet_E[r]);
                      jet2.SetPxPyPzE(TJet_Px[s], TJet_Py[s], TJet_Pz[s], TJet_E[s]);

                      goodDiJetM.push_back((jet1 + jet2).M());
                      goodDiJetDeltaEta.push_back(abs(TJet_Eta[r] - TJet_Eta[s]));
                      if ((jet1 + jet2).M() > 500 && \
                          abs(TJet_Eta[r] - TJet_Eta[s]) > 2.5)
                      {
                        passMandEtaRequieriments = true; break;
                      }
                    }
                  }
                }

                if (passMandEtaRequieriments)
                {
                  TIsCRVBS_0 = true;
                  TLorentzVector sum3l = tempLeps.at(0).p + tempLeps.at(1).p + tempLeps.at(2).p;
                  
                  finalVar = TMath::Abs(sum3l.Eta() - 0.5*(jet1.Eta() + jet2.Eta()));

                  //if (TMath::Abs(sum3l.Eta() - 0.5*(jet1.Eta() + jet2.Eta())) < 2.5) // =====
                  if (TMath::Abs(sum3l.Eta() - 0.5*(jet1.Eta() + jet2.Eta())) < 4)
                  {
                    //std::cout << "peanut" << std::endl;
                    IF_NORMAL TIsSRVBS = true;
                    IF_JEC_UP TIsSRVBS_JEC_UP = true;
                    IF_JEC_DO TIsSRVBS_JEC_DO = true;
                    IF_BTG_UP TIsSRVBS_BTG_UP = true;
                    IF_BTG_DO TIsSRVBS_BTG_DO = true;
                  }
                }
              }
            }
          }
        }
      }
      goodDiJetMSize = goodDiJetM.size();
      goodDiJetDeltaEtaSize = goodDiJetDeltaEta.size();
 


      // <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

      // Let's define here the CRZZ region
      if (TNFOLeps == 4 && passesMCTruth(fakeableLeptons,1,4))
      {
        lepExtra = tempLeps.at(3); 
        TLep_PtExtra = lepExtra.Pt();

        {
          {
            if(TNBtags == 0)
            {
              if(TMET > 30.)
              {
                TIsCRZZ = true;
              }
            }
          }
        }
      }      


      if(passesMCTruth(fakeableLeptons,1,3) && TNFOLeps == 3){
        //std::cout << "test 4 " << std::endl;


        // Let's define here the CRConv region
        if (lepZ1.Pt() > 25 && lepZ2.Pt() > 10 && lepW.Pt() > 25)
        {
          if(TMath::Abs(TMll - nomZmass) > 15. && TMinMll > 4. && TM3l < 100.  )
          {
            if(TNBtags == 0)
            {
              if(TMET <= 30.)
              {
                TIsCRConv = true;
              }
            }
          }
        }  

        // Let's define here the CRtop region
        if (lepZ1.Pt() > 25 && lepZ2.Pt() > 10 && lepW.Pt() > 25)
        {
          if(TMath::Abs(TMll - nomZmass) > 5. && TMinMll > 4. && TM3l > 100.  )
          {
            if(TNBtags > 0)
            {
              if(TMET > 30.)
              {
                TIsCRtop = true;
              }
            }
          }
        }




        //std::cout << "Pass 3Tight, hasOS,passMC\n";
        if (lepZ1.Pt() > 25 && lepZ2.Pt() > 10 && lepW.Pt() > 25){//3 lepton, has OSSF, leptons assigned to W and Z. Fill histos from here onwards
          //std::cout << "test 5 " << std::endl;

          if(TMath::Abs(TMll - nomZmass)< 15. && TMinMll > 4. && TM3l > 100.  ){ //  Z window + exlcude low masses + M_3l selection 
            //std::cout << "test ------6 " << std::endl;

            // The last two cuts define the Control/Signal regions
            
            // Signal Region
            if(TMET > 30.){   // MET > 30 always
              //std::cout << "test -------7 " << std::endl;

              if(TNBtags == 0){ //Exactly 0 btags
                TIsSR   = true;
              }
              else if(TNBtags > 0 && (TNOSSF == 0 || (TNOSSF > 0 && TMath::Abs(TM3l - nomZmass) > 5))){ //1 or more btags
                TIsCRTT = true ;
              }
            }
            else if (TMET < 30. && TNBtags == 0){
              TIsCRDY = true ;
            }

          }
          if (TMath::Abs(TMll - nomZmass)< 15. && TMinMll > 4. && TMET < 30.){
            TIsNewCRDY = true;
          }
          if (TMath::Abs(TMll - nomZmass)> 15. && TMath::Abs(TM3l - nomZmass) > 5 &&  TMinMll > 4. && (lepZ1.p + lepZ2.p + lepW.p).M() > 100. && TMET > 30.){
            TIsNewCRTT = true;
          } 
        }
      }
    //std::cout << "test FIN " << std::endl;

    }
    IF_NORMAL fTree[wP] -> Fill();  //Skimming for 3 FO; remember to use TNTightLeptons == 3 for plotting!!!
  } // End of the wP bucle
  } // End of the Great Bucle

}




//#####################################################################
// Initialize histograms/Minitrees
//------------------------------------------------------------------
void WZAnalysis::InitHistos(){
}

void WZAnalysis::SetLeptonVariables(TTree* iniTree){
  iniTree->Branch("TNFOLeps",     &TNFOLeps,     "TNFOLeps/I");
  iniTree->Branch("TNTightLeps",     &TNTightLeps,     "TNTightLeps/I");

  iniTree->Branch("TLep_PtZ1",     &TLep_PtZ1,     "TLep_PtZ1/F");
  iniTree->Branch("TLep_PtZ2",     &TLep_PtZ2,     "TLep_PtZ2/F");
  iniTree->Branch("TLep_PtW",      &TLep_PtW,     "TLep_PtW/F");

  iniTree->Branch("TLep_EtaZ1",     &TLep_EtaZ1,     "TLep_EtaZ1/F");
  iniTree->Branch("TLep_EtaZ2",     &TLep_EtaZ2,     "TLep_EtaZ2/F");
  iniTree->Branch("TLep_EtaW",      &TLep_EtaW,     "TLep_EtaW/F");

  iniTree->Branch("TLep_PhiZ1",     &TLep_PhiZ1,     "TLep_PhiZ1/F");
  iniTree->Branch("TLep_PhiZ2",     &TLep_PhiZ2,     "TLep_PhiZ2/F");
  iniTree->Branch("TLep_PhiW",      &TLep_PhiW,     "TLep_PhiW/F");

  iniTree->Branch("TLep_EZ1",     &TLep_EZ1,     "TLep_EZ1/F");
  iniTree->Branch("TLep_EZ2",     &TLep_EZ2,     "TLep_EZ2/F");
  iniTree->Branch("TLep_EW",      &TLep_EW,     "TLep_EW/F");

  iniTree->Branch("TLep_ChargeZ1",     &TLep_ChargeZ1,     "TLep_ChargeZ1/F");
  iniTree->Branch("TLep_ChargeZ2",     &TLep_ChargeZ2,     "TLep_ChargeZ2/F");
  iniTree->Branch("TLep_ChargeW",      &TLep_ChargeW,     "TLep_ChargeW/F");

  iniTree->Branch("TChannel",      &TChannel,      "TChannel/I");
  iniTree->Branch("TMll",        &TMll,      "TMll/F");
  iniTree->Branch("TMZ1W",        &TMZ1W,      "TMZ1W/F");
  iniTree->Branch("TMZ2W",        &TMZ2W,      "TMZ2W/F");
  iniTree->Branch("TM3l",        &TM3l,      "TM3l/F");
  iniTree->Branch("TNOSSF",      &TNOSSF,      "TNOSSF/I");
  iniTree->Branch("TMinMll",      &TMinMll,      "TMinMll/F");
  iniTree->Branch("TConvNumber",      &TConvNumber,      "TConvNumber/I");
  iniTree->Branch("TFakeNumber",      &TFakeNumber,      "TFakeNumber/I");

  iniTree->Branch("TLep_IsTightZ1",     &TLep_IsTightZ1,     "TLep_IsTightZ1/F");
  iniTree->Branch("TLep_IsTightZ2",     &TLep_IsTightZ2,     "TLep_IsTightZ2/F");
  iniTree->Branch("TLep_IsTightW",      &TLep_IsTightW,     "TLep_IsTightW/F");

  iniTree->Branch("TLep_IsPromptZ1",     &TLep_IsPromptZ1,     "TLep_IsPromptZ1/F");
  iniTree->Branch("TLep_IsPromptZ2",     &TLep_IsPromptZ2,     "TLep_IsPromptZ2/F");
  iniTree->Branch("TLep_IsPromptW",      &TLep_IsPromptW,     "TLep_IsPromptW/F");

  iniTree->Branch("TLep_pdgIdZ1",     &TLep_pdgIdZ1,     "TLep_pdgIdZ1/F");
  iniTree->Branch("TLep_pdgIdZ2",     &TLep_pdgIdZ2,     "TLep_pdgIdZ2/F");
  iniTree->Branch("TLep_pdgIdW",      &TLep_pdgIdW,     "TLep_pdgIdW/F");
  iniTree->Branch("TLep_isConvVeto",   &TLep_isConvVeto, "TLep_isConvVeto[TNFOLeps]/I");

  // Dependent JEC / Btag branches 

  iniTree->Branch("TLep_SFerrZ1", &TLep_SFerrZ1, "TLep_SFerrZ1/F");
  iniTree->Branch("TLep_SFerrZ2", &TLep_SFerrZ2, "TLep_SFerrZ2/F");
  iniTree->Branch("TLep_SFerrW", &TLep_SFerrW, "TLep_SFerrW/F");

  iniTree->Branch("TMtWZ", &TMtWZ, "TMtWZ/F");
  iniTree->Branch("TMtWZ_JEC_UP", &TMtWZ_JEC_UP, "TMtWZ_JEC_UP/F");
  iniTree->Branch("TMtWZ_JEC_DO", &TMtWZ_JEC_DO, "TMtWZ_JEC_DO/F");

  iniTree->Branch("TMtW", &TMtW, "TMtW/F");
  iniTree->Branch("TMtW_JEC_UP", &TMtW_JEC_UP, "TMtW_JEC_UP/F");
  iniTree->Branch("TMtW_JEC_DO", &TMtW_JEC_DO, "TMtW_JEC_DO/F");
}

void WZAnalysis::SetJetVariables(TTree* iniTree){
  iniTree->Branch("TNJets",           &TNJets,         "TNJets/I");
  iniTree->Branch("TNBtags",       &TNBtags,     "TNBtags/I");
  iniTree->Branch("TNBtags_BTG_UP",       &TNBtags_BTG_UP,     "TNBtags_BTG_UP/I");
  iniTree->Branch("TNBtags_BTG_DO",       &TNBtags_BTG_DO,     "TNBtags_BTG_DO/I");
  iniTree->Branch("TJet_isBJet",       TJet_isBJet,       "TJet_isBJet[TNJets]/I");
  iniTree->Branch("TJet_Pt",           TJet_Pt,           "TJet_Pt[TNJets]/F");
  iniTree->Branch("TJet_Pt_JEC_UP",           TJet_Pt_JEC_UP,           "TJet_Pt[TNJets]/F");
  iniTree->Branch("TJet_Pt_JEC_DO",           TJet_Pt_JEC_DO,           "TJet_Pt[TNJets]/F");
  iniTree->Branch("TJet_Px",           TJet_Px,           "TJet_Px[TNJets]/F");
  iniTree->Branch("TJet_Py",           TJet_Py,           "TJet_Py[TNJets]/F");
  iniTree->Branch("TJet_Pz",           TJet_Pz,           "TJet_Pz[TNJets]/F");
  iniTree->Branch("TJet_Eta",           TJet_Eta,           "TJet_Eta[TNJets]/F");
  iniTree->Branch("TJet_Phi",           TJet_Phi,           "TJet_Phi[TNJets]/F");
  iniTree->Branch("TJet_E",            TJet_E,            "TJet_E[TNJets]/F");
  iniTree->Branch("THT",          &THT,          "THT/F");
}

void WZAnalysis::SetEventVariables(TTree* iniTree){



  iniTree->Branch("TWeight",      &TWeight,      "TWeight/F");

  iniTree->Branch("TWeight_PUSF_Up",      &TWeight_PUSF_Up,      "TWeight_PUSF_Up/F");
  iniTree->Branch("TWeight_PUSF_Down",      &TWeight_PUSF_Down,      "TWeight_PUSF_Down/F");
  iniTree->Branch("TWeight_ElecSFUp",      &TWeight_ElecSFUp,      "TWeight_ElecSFUp/F");
  iniTree->Branch("TWeight_ElecSFDown",      &TWeight_ElecSFDown,      "TWeight_ElecSFDown/F");
  iniTree->Branch("TWeight_MuonSFUp",      &TWeight_MuonSFUp,      "TWeight_MuonSFUp/F");
  iniTree->Branch("TWeight_MuonSFDown",      &TWeight_MuonSFDown,      "TWeight_MuonSFDown/F");

  iniTree->Branch("TIsSR"  ,      &TIsSR  ,      "TIsSR/B"  );

  /*
  float goodDiJetMList[goodDiJetM.size()];
  float goodDiJetDeltaEtaList[goodDiJetDeltaEta.size()];

  for (int unsigned m = 0; m < goodDiJetM.size(); m++){
    goodDiJetMList[m] = goodDiJetM[m];
  }        
  //else std::fill_n(goodDiJetMList, 40, -999); 

  for (int unsigned m = 0; m < goodDiJetDeltaEta.size(); m++){
    goodDiJetDeltaEtaList[m] = goodDiJetDeltaEta[m];
  }    
  //else std::fill_n(goodDiJetDeltaEtaList, 40, -999);   
  lenM = goodDiJetM.size();  lenEta = goodDiJetDeltaEta.size();
  iniTree->Branch("lenM"  ,      lenM  ,      "lenM/I"  );
  iniTree->Branch("lenEta"  ,      lenEta  ,      "lenEta/I"  );
  iniTree->Branch("goodDiJetMList", goodDiJetMList, "goodDiJetMList[lenM]/F");
  iniTree->Branch("goodDiJetDeltaEtaList", goodDiJetDeltaEtaList, "goodDiJetDeltaEtaList[lenEta]/F"  );
  */
  iniTree->Branch("finalVar"  ,      &finalVar  ,      "finalVar/F"  );
  iniTree->Branch("passMandEtaRequieriments", &passMandEtaRequieriments, "passMandEtaRequieriments/B");
  iniTree->Branch("badBJets"  ,      &badBJets  ,      "badBJets"  );
  iniTree->Branch("numGoodJets"  ,      &numGoodJets  ,      "numGoodJets/I"  );
  iniTree->Branch("passEtaFilters"  ,      &passEtaFilters  ,      "passEtaFilters/O"  );
  // TMET (ya esta)
  // TMinMll ta esta, y tm3l TLep_PtZ1, z2 t W.




  //the new two branches:
  iniTree->Branch("TIsCRtop"  ,      &TIsCRtop  ,      "TIsCRtop/B"  );
  iniTree->Branch("TIsCRZZ"  ,      &TIsCRZZ  ,      "TIsCRZZ/B"  );
  iniTree->Branch("TIsCRConv"  ,      &TIsCRConv  ,      "TIsCRConv/B"  );

  iniTree->Branch("TIsCRVBS_0"  ,      &TIsCRVBS_0  ,      "TIsCRVBS_0/B"  );
  iniTree->Branch("TIsCRVBS_1"  ,      &TIsCRVBS_1  ,      "TIsCRVBS_1/B"  );
  iniTree->Branch("TIsCRVBS_2"  ,      &TIsCRVBS_2  ,      "TIsCRVBS_2/B"  );
  iniTree->Branch("TIsCRVBS_3"  ,      &TIsCRVBS_3  ,      "TIsCRVBS_3/B"  );
  iniTree->Branch("TIsCRVBS_4"  ,      &TIsCRVBS_4  ,      "TIsCRVBS_4/B"  );
  iniTree->Branch("TIsCRVBS_5"  ,      &TIsCRVBS_5  ,      "TIsCRVBS_5/B"  );
  iniTree->Branch("TIsCRVBS_6"  ,      &TIsCRVBS_6  ,      "TIsCRVBS_6/B"  );
  iniTree->Branch("TIsCRVBS_7"  ,      &TIsCRVBS_7  ,      "TIsCRVBS_7/B"  );
  iniTree->Branch("TIsCRVBS_8"  ,      &TIsCRVBS_8  ,      "TIsCRVBS_8/B"  );
  iniTree->Branch("TIsCRVBS_9"  ,      &TIsCRVBS_9  ,      "TIsCRVBS_9/B"  );
  iniTree->Branch("TIsCRVBS_10"  ,      &TIsCRVBS_10  ,      "TIsCRVBS_10/B"  );
  iniTree->Branch("TIsCRVBS_11"  ,      &TIsCRVBS_11  ,      "TIsCRVBS_11/B"  );
  iniTree->Branch("TIsCRVBS_12"  ,      &TIsCRVBS_12  ,      "TIsCRVBS_12/B"  );
  iniTree->Branch("TIsCRVBS_13"  ,      &TIsCRVBS_13  ,      "TIsCRVBS_13/B"  );
  
  iniTree->Branch("TIsCRTT",      &TIsCRTT,      "TIsCRTT/B");
  iniTree->Branch("TIsCRDY",      &TIsCRDY,      "TIsCRDY/B");
  iniTree->Branch("TIsNewCRTT",      &TIsNewCRTT,      "TIsNewCRTT/B");
  iniTree->Branch("TIsNewCRDY",      &TIsNewCRDY,      "TIsNewCRDY/B");
  iniTree->Branch("TLHEWeight",        TLHEWeight,         "TLHEWeight[254]/F");
  iniTree->Branch("TEvtNum",         &TEvtNum,         "TEvtNum/l");

  // Dependent JEC / Btag branches 
  iniTree->Branch("TMET", &TMET, "TMET/F");
  iniTree->Branch("TMET_JEC_UP", &TMET_JEC_UP, "TMET_JEC_UP/F");
  iniTree->Branch("TMET_JEC_DO", &TMET_JEC_DO, "TMET_JEC_DO/F");
  
  iniTree->Branch("TMET_Phi", &TMET_Phi, "TMET_Phi/F");
  iniTree->Branch("TMET_Phi_JEC_UP", &TMET_Phi_JEC_UP, "TMET_Phi_JEC_UP/F");
  iniTree->Branch("TMET_Phi_JEC_DO", &TMET_Phi_JEC_DO, "TMET_Phi_JEC_DO/F");
  
  iniTree->Branch("TGenMET", &TGenMET, "TGenMET/F");
  iniTree->Branch("TGenMET_JEC_UP", &TGenMET_JEC_UP, "TGenMET_JEC_UP/F");
  iniTree->Branch("TGenMET_JEC_DO", &TGenMET_JEC_DO, "TGenMET_JEC_DO/F"); 

  iniTree->Branch("MllnomMZ", &MllnomMZ, "MllnomMZ/F"  );
  iniTree->Branch("MllnomMZ_JEC_UP", &MllnomMZ_JEC_UP, "MllnomMZ_JEC_UP/F"  );
  iniTree->Branch("MllnomMZ_JEC_DO", &MllnomMZ_JEC_DO, "MllnomMZ_JEC_DO/F"  );

  iniTree->Branch("TIsSRVBS", &TIsSRVBS, "TIsSRVBS/B"  );
  iniTree->Branch("TIsSRVBS_JEC_UP" , &TIsSRVBS_JEC_UP, "TIsSRVBS_JEC_UP/B"  );
  iniTree->Branch("TIsSRVBS_JEC_DO" , &TIsSRVBS_JEC_DO, "TIsSRVBS_JEC_DO/B"  );
  iniTree->Branch("TIsSRVBS_BTG_UP" , &TIsSRVBS_BTG_UP, "TIsSRVBS_BTG_UP/B"  );
  iniTree->Branch("TIsSRVBS_BTG_DO" , &TIsSRVBS_BTG_DO, "TIsSRVBS_BTG_DO/B"  );
}

Bool_t WZAnalysis::passesMCTruth(std::vector<Lepton> sLep, Int_t addConvs = 1, Int_t requiredLeps = 3){
  Int_t passes = 0;
  Int_t convs = 0;
  Int_t otherfakes = 0;
  for (unsigned int i = 0; i < sLep.size(); i++){
    if (gIsData) passes++;
    else{
      Int_t theID = sLep.at(i).idDecayMode;
      Int_t theGammaID = sLep.at(i).decayMode;
      if (theID != 0){//Is prompt (parent is not fake, might be gamma)
        passes++;
      }
      else if (theID == 0 && theGammaID == 1){//Is conversion (parent is a fake gamma)
        convs++;
      }
      else if (theID == 0 && theGammaID != 1){//Other fakes
        otherfakes++;
      } 
    }
  }
/*  if (!gIsData){
    for (int i = 0; i < sLep.size(); i++){
      //std::cout << "LepMatch " << sLep.at(i).lepMatch << std::endl;
      if (sLep.at(i).isPrompt > 0) passes++; //MC hard prompt lepton
      else if (sLep.at(i).lepMatch == 0) continue;//No matching gen/reco is a fail
      else {
        Lepton theLep = sLep.at(i);
        Lepton genMatch = *sLep.at(i).lepMatch;
        Int_t theTypepdgId = (theLep.type == 1) ? 11 : 13;
        Int_t theMotherId  = TMath::Abs(genMatch.decayMode);
        Int_t theGrandMotherId  = TMath::Abs(genMatch.idDecayMode);
        if (genMatch.isPrompt) passes++; //MC hard prompt lepton
        else if (((theTypepdgId == TMath::Abs(genMatch.type) || TMath::Abs(genMatch.type) == 15) && ( (theMotherId == 23 || theMotherId == 24 || theMotherId == 25) || (theMotherId == 15 && (theGrandMotherId == 23 || theGrandMotherId == 24 || theGrandMotherId == 25))))) passes++; //Either a decay from a tau, Z, W or H including tau decays from the later
        else if (genMatch.type == 22 || (theMotherId == 22 && TMath::Abs(genMatch.type) == theTypepdgId)) isConv++; //For conversions
      } 
    }
  }
  if (gIsData){ passes++;}*/
  TConvNumber = convs; //Used to cut conversions in non-conversion samples
  TFakeNumber = otherfakes;
  return (passes + addConvs*(convs+ otherfakes)) == requiredLeps; //Count Prompt leptons and conversions and add up to the required lepton number
}

//#####################################################################
// Get Variables
//------------------------------------------------------------------

void WZAnalysis::GetLeptonsByWP(Int_t wPValue){
  Int_t nFakeableLeptons = foLeptons.size();
  Int_t nTightLeptons = selLeptons.size();

  if (sWPoints[wPValue] == "top"){
    for (int k = 0; k < nTightLeptons; k++){ // No FO for top ID
      if (selLeptons.at(k).idMVA >= 10){
        tightLeptons.push_back(selLeptons.at(k));
        fakeableLeptons.push_back(selLeptons.at(k));
        tightLeptons.back().SetSF(selLeptons.at(k).GetSF(0)*leptonSFtop->GetLeptonSF(selLeptons.at(k).Pt(), selLeptons.at(k).Eta(), selLeptons.at(k).type));
        fakeableLeptons.back().SetSF(selLeptons.at(k).GetSF(0)*leptonSFtop->GetLeptonSF(selLeptons.at(k).Pt(), selLeptons.at(k).Eta(), selLeptons.at(k).type));
      }
    }
  }
  else {
    Int_t nFO = 0;
    for (int k = 0; k < nFakeableLeptons; k++){
      if (foLeptons.at(k).idMVA%10 > WPointVal[wPValue]){
        //std::cout << k << std::endl;
        fakeableLeptons.push_back(foLeptons.at(k));
        if (WPointVal[wPValue] == 5){//VT SF
          fakeableLeptons.back().SetSF(foLeptons.at(k).GetSF(0)*leptonSFEWKVT->GetLeptonSF(foLeptons.at(k).Pt(), foLeptons.at(k).Eta(), foLeptons.at(k).type));
          fakeableLeptons.back().SetSFerr(leptonSFEWKVT->GetLeptonSFerror(foLeptons.at(k).Pt(), foLeptons.at(k).Eta(), foLeptons.at(k).type));
        }
        else { //M SF
          fakeableLeptons.back().SetSF(foLeptons.at(k).GetSF(0)*leptonSFEWKM->GetLeptonSF(foLeptons.at(k).Pt(), foLeptons.at(k).Eta(), foLeptons.at(k).type));
          fakeableLeptons.back().SetSFerr(leptonSFEWKM->GetLeptonSFerror(foLeptons.at(k).Pt(), foLeptons.at(k).Eta(), foLeptons.at(k).type));
        }
        nFO++;
      }
    }

    for (int k = 0; k < nTightLeptons; k++){
      if (selLeptons.at(k).idMVA%10 > WPointVal[wPValue]){
        tightLeptons.push_back(selLeptons.at(k));
        if (WPointVal[wPValue] == 5){//VT SF
          tightLeptons.back().SetSF(selLeptons.at(k).GetSF(0)*leptonSFEWKVT->GetLeptonSF(selLeptons.at(k).Pt(), selLeptons.at(k).Eta(), selLeptons.at(k).type));
          tightLeptons.back().SetSFerr(leptonSFEWKVT->GetLeptonSFerror(selLeptons.at(k).Pt(), selLeptons.at(k).Eta(), selLeptons.at(k).type));
        }
        else { //M SF
          tightLeptons.back().SetSF(selLeptons.at(k).GetSF(0)*leptonSFEWKM->GetLeptonSF(selLeptons.at(k).Pt(), selLeptons.at(k).Eta(), selLeptons.at(k).type));
        }
      }
    }
  }
}

void WZAnalysis::GetLeptonVariables(std::vector<Lepton> tightLeptons, std::vector<Lepton> foLeptons, std::vector<Lepton> looseLeptons){
  TNTightLeps = tightLeptons.size();
  Int_t nVetoLeptons = foLeptons.size();
  TNFOLeps = nVetoLeptons;
  //std::cout << "NLeps:" << TNFOLeps << ", NTight:" << TNTightLeps << std::endl;
  //Require exactly 3 leptons 
  if(TNFOLeps != 3 ) gChannel = -1;
  //Charge compatibility with WZ production
  else if(TMath::Abs(fakeableLeptons.at(0).charge + fakeableLeptons.at(1).charge + fakeableLeptons.at(2).charge) != 1) gChannel = -1;
  //Combinatory of posible final leptons
  else if(fakeableLeptons.at(0).isMuon && fakeableLeptons.at(1).isMuon && fakeableLeptons.at(2).isMuon) gChannel = iMuMuMu;
  else if(fakeableLeptons.at(0).isMuon && fakeableLeptons.at(1).isMuon && fakeableLeptons.at(2).isElec) gChannel = iElMuMu;
  else if(fakeableLeptons.at(0).isMuon && fakeableLeptons.at(1).isElec && fakeableLeptons.at(2).isMuon) gChannel = iElMuMu;
  else if(fakeableLeptons.at(0).isMuon && fakeableLeptons.at(1).isElec && fakeableLeptons.at(2).isElec) gChannel = iElElMu;
  else if(fakeableLeptons.at(0).isElec && fakeableLeptons.at(1).isMuon && fakeableLeptons.at(2).isMuon) gChannel = iElMuMu;
  else if(fakeableLeptons.at(0).isElec && fakeableLeptons.at(1).isMuon && fakeableLeptons.at(2).isElec) gChannel = iElElMu;
  else if(fakeableLeptons.at(0).isElec && fakeableLeptons.at(1).isElec && fakeableLeptons.at(2).isMuon) gChannel = iElElMu;
  else if(fakeableLeptons.at(0).isElec && fakeableLeptons.at(1).isElec && fakeableLeptons.at(2).isElec) gChannel = iElElEl;
  //std::cout << "Channel Set\n";
  TMinMll = 100000;
  TNOSSF = 0;
  for(Int_t i = 0; i < TNFOLeps; i++){
    for(Int_t j = i+1; j < TNFOLeps; j++){
      if (fakeableLeptons.at(j).isMuon && fakeableLeptons.at(i).isMuon && fakeableLeptons.at(i).charge*fakeableLeptons.at(j).charge == -1)           TNOSSF++;
      if (fakeableLeptons.at(j).isElec && fakeableLeptons.at(i).isElec && fakeableLeptons.at(i).charge*fakeableLeptons.at(j).charge == -1)           TNOSSF++;
      Float_t hypMll = (fakeableLeptons.at(j).p + fakeableLeptons.at(i).p).M();
      if (hypMll < TMinMll) TMinMll = hypMll;
    }
  }
  //std::cout << "Mass computed\n";
  TChannel = gChannel;
  gChannel = gChannel -1; // gchannel used for chan index of histograms
}

void WZAnalysis::GetJetVariables(std::vector<Jet> selJets, std::vector<Jet> cleanedJets15, int VAR, Float_t ptCut){
  TNJets = selJets.size(); THT = 0;
  TNBtags = 0;

  IF_BTG_UP TNBtags_BTG_UP = 0;
  IF_BTG_DO TNBtags_BTG_DO = 0;
  for(Int_t i = 0; i < TNJets; i++){
    IF_NORMAL TJet_Pt[i]     = selJets.at(i).Pt();
    IF_BTG_UP TJet_Pt[i]     = selJets.at(i).Pt();
    IF_BTG_DO TJet_Pt[i]     = selJets.at(i).Pt();
    IF_JEC_UP TJet_Pt[i]     = selJets.at(i).pTJESUp;
    IF_JEC_UP TJet_Pt_JEC_UP[i] = selJets.at(i).pTJESUp;
    IF_JEC_DO TJet_Pt[i]     = selJets.at(i).pTJESDown;
    IF_JEC_DO TJet_Pt_JEC_DO[i] = selJets.at(i).pTJESDown;

    TJet_Eta[i]    = selJets.at(i).Eta();
    TJet_Phi[i]    = selJets.at(i).Phi();
    TJet_E[i]      = selJets.at(i).E();
    TJet_isBJet[i] = selJets.at(i).isBtag;
    
    IF_NORMAL {TJet_isBJet[i] = selJets.at(i).isBtag;}
    IF_JEC_UP {TJet_isBJet[i] = selJets.at(i).isBtag;}
    IF_JEC_DO {TJet_isBJet[i] = selJets.at(i).isBtag;}
    IF_BTG_UP {TJet_isBJet[i] = selJets.at(i).isBtag_BtagUp;}
    IF_BTG_DO {TJet_isBJet[i] = selJets.at(i).isBtag_BtagDown;}
    
    THT += TJet_Pt[i];
    
    IF_NORMAL {if(selJets.at(i).isBtag) TNBtags++;}
    IF_JEC_UP {if(selJets.at(i).isBtag) TNBtags++;}
    IF_JEC_DO {if(selJets.at(i).isBtag) TNBtags++;}
    IF_BTG_UP {if(selJets.at(i).isBtag_BtagUp) {TNBtags++; TNBtags_BTG_UP ++;}}
    IF_BTG_DO {if(selJets.at(i).isBtag_BtagDown) {TNBtags++; TNBtags_BTG_DO ++;}}
  }
  SetParam("THT",THT);
}

void WZAnalysis::GetGenJetVariables(std::vector<Jet> genJets, std::vector<Jet> mcJets){
  if(gIsData) return;
  nFiduJets = 0; nFidubJets = 0; 
  Int_t nGenJets = genJets.size();
  Int_t nmcJets = mcJets.size();
  for(Int_t i = 0; i < nGenJets; i++) if(genJets.at(i).p.Pt() > 50 && TMath::Abs(genJets.at(i).p.Eta()) < 4.7)                         nFiduJets++;
  for(Int_t i = 0; i <  nmcJets; i++) if(mcJets.at(i).p.Pt()  > 50 && TMath::Abs(mcJets.at(i).Eta())    < 4.7 && mcJets.at(i).isBtag)  nFidubJets++;
}

void WZAnalysis::GetMET(int VAR){
  IF_NORMAL TMET = Get<Float_t>("met_pt");
  IF_BTG_UP TMET = Get<Float_t>("met_pt");
  IF_BTG_DO TMET = Get<Float_t>("met_pt");
  IF_JEC_UP TMET_JEC_UP = Get<Float_t>("met_jecUp_pt");
  IF_JEC_DO TMET_JEC_DO = Get<Float_t>("met_jecDown_pt");
  
  IF_NORMAL TMET_Phi    = Get<Float_t>("met_phi");  // MET phi
  IF_BTG_UP TMET_Phi    = Get<Float_t>("met_phi");  // MET phi
  IF_BTG_DO TMET_Phi    = Get<Float_t>("met_phi");  // MET phi
  IF_JEC_UP TMET_Phi_JEC_UP    = Get<Float_t>("met_jecUp_phi");  // MET phi
  IF_JEC_DO TMET_Phi_JEC_DO    = Get<Float_t>("met_jecDown_phi");  // MET phi

  if(gIsData) return;
  
  IF_NORMAL TGenMET     = Get<Float_t>("met_genPt");
  IF_BTG_UP TGenMET     = Get<Float_t>("met_genPt");
  IF_BTG_DO TGenMET     = Get<Float_t>("met_genPt");
  IF_JEC_UP TGenMET_JEC_UP     = Get<Float_t>("met_jecUp_genPt");
  IF_JEC_DO TGenMET_JEC_DO     = Get<Float_t>("met_jecDown_genPt");

  if(gIsLHE)  for(Int_t i = 0; i < Get<Int_t>("nLHEweight"); i++)   TLHEWeight[i] = Get<Float_t>("LHEweight_wgt", i);
}

//#####################################################################
// Fill histograms/Minitrees
//------------------------------------------------------------------

void WZAnalysis::FillDYHistos(Int_t ch){
}

void WZAnalysis::FillHistos(Int_t ch, Int_t cut){
  if(!makeHistos) return;
  Int_t sys = 0;
}
