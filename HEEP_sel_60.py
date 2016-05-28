def HEEP_ID_60(tree,Z_leg_index):
    #Z_leg_index =>tree.Zee_i1[i]

    if(tree.gsf_isEB[Z_leg_index]):
        pass_sel=(tree.gsf_pt[Z_leg_index]>35)*\
            (tree.gsf_ecaldrivenSeed[Z_leg_index]==1)*\
            (abs(tree.gsf_deltaEtaSeedClusterTrackAtCalo[Z_leg_index])<0.004)*\
            (abs(tree.gsf_deltaPhiSeedClusterTrackAtCalo[Z_leg_index])<0.06)*\
            (tree.gsf_hadronicOverEm[Z_leg_index] < (1./tree.gsf_caloEnergy[Z_leg_index] + 0.05))*\
            (tree.gsf_scE2x5Max[Z_leg_index]/tree.gsf_scE5x5[Z_leg_index] > 0.94 or tree.gsf_scE1x5[Z_leg_index]/tree.gsf_scE5x5[Z_leg_index] > 0.83 )*\
            (tree.gsf_hcalDepth1OverEcal[Z_leg_index] < 2 +0.03*tree.gsf_pt[Z_leg_index] + 0.28*tree.ev_fixedGridRhoFastjetAll)*\
            (tree.gsf_nLostInnerHits[Z_leg_index]<2)*\
            (abs(tree.gsf_dxy[Z_leg_index])<0.02)

        
    elif(tree.gsf_isEE[Z_leg_index]):
        pass_sel=(tree.gsf_pt[Z_leg_index]>35)*\
            (tree.gsf_ecaldrivenSeed[Z_leg_index]==1)*\
            (abs(tree.gsf_deltaEtaSeedClusterTrackAtCalo[Z_leg_index])<0.006)*\
            (abs(tree.gsf_deltaPhiSeedClusterTrackAtCalo[Z_leg_index])<0.06)


#    if(tree.gsf_isEB[Z_leg_index]):
#        pass_sel=(tree.gsf_pt[Z_leg_index]>35)*\
#            (tree.gsf_ecaldrivenSeed[Z_leg_index]==1)*\
#            (abs(tree.gsf_deltaEtaSeedClusterTrackAtCalo[Z_leg_index])<0.004)*\
#            (abs(tree.gsf_deltaPhiSeedClusterTrackAtCalo[Z_leg_index])<0.06)*\
#            (tree.gsf_hadronicOverEm[Z_leg_index] < (1./tree.gsf_caloEnergy[Z_leg_index] + 0.05))*\
#            (tree.gsf_scE2x5Max[Z_leg_index]/tree.gsf_scE5x5[Z_leg_index] > 0.94 or tree.gsf_scE1x5[Z_leg_index]/tree.gsf_scE5x5[Z_leg_index] > 0.83 )*\
#            (gsf_hcalDepth1OverEcal[Z_leg_index] < 2 +0.03*tree.gsf_pt[Z_leg_index] + 0.28*tree.ev_fixedGridRhoFastjetAll[Z_leg_index])*\
#            (tree.gsf_nLostInnerHits[Z_leg_index]<2)*\
#            (abs(tree.gsf_dxy[Z_leg_index]<0.02))
#            #trackPT,5\
#    elif(tree.gsf_isEE[Z_leg_index]):
#        pass_sel=(tree.gsf_pt[Z_leg_index]>35)*\
#            (tree.gsf_ecaldrivenSeed[Z_leg_index]==1)*\
#            (abs(tree.gsf_deltaEtaSeedClusterTrackAtCalo[Z_leg_index])<0.006)*\
#            (abs(tree.gsf_deltaPhiSeedClusterTrackAtCalo[Z_leg_index])<0.06)
#

    return pass_sel