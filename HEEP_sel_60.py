def HEEP_ID_60(tree,Z_leg_index):
    #Z_leg_index =>tree.Zee_i1[i]

    if(tree.gsf_isEB[Z_leg_index]):
        pass_sel=(tree.gsf_pt[Z_leg_index]>35)*\
            (tree.gsf_ecaldrivenSeed[Z_leg_index]==1)*\
            (abs(tree.gsf_deltaEtaSeedClusterTrackAtVtx[Z_leg_index])<0.004)*\
            (abs(tree.gsf_deltaPhiSeedClusterTrackAtVtx[Z_leg_index])<0.06)*\
            (tree.gsf_hadronicOverEm[Z_leg_index] < (1./tree.gsf_caloEnergy[Z_leg_index] + 0.05))*\
            (tree.gsf_e2x5Max[Z_leg_index]/tree.gsf_eE5x5[Z_leg_index] > 0.94 or tree.gsf_eE1x5[Z_leg_index]/tree.gsf_eE5x5[Z_leg_index] > 0.83 )*\
            (gsf_dr03EcalRecHitSumEt[Z_leg_index] + gsf_dr03HcalDepth1TowerSumEt[Z_leg_index] < 2 +0.03*tree.gsf_pt[Z_leg_index] + 0.28*tree.ev_fixedGridRhoFastjetAll)*\
            (tree.gsf_dr03TkSumPtCorrected[Z_leg_index]<5)*\
            (tree.gsf_nLostInnerHits[Z_leg_index]<2)*\
            (abs(tree.gsf_dxy_firstPVtx[Z_leg_index])<0.02)

        
    elif(tree.gsf_isEE[Z_leg_index]):
        #(abs(tree.gsf_deltaEtaSeedClusterTrackAtVtx[Z_leg_index])<0.006)*\ => removed to be safe
        pass_sel=(tree.gsf_pt[Z_leg_index]>35)*\
            (tree.gsf_ecaldrivenSeed[Z_leg_index]==1)*\
            (abs(tree.gsf_deltaPhiSeedClusterTrackAtVtx[Z_leg_index])<0.06)*\
            (tree.gsf_hadronicOverEm[Z_leg_index] < (5./tree.gsf_caloEnergy[Z_leg_index] + 0.05))*\
            (tree.gsf_sigmaIetaIeta[Z_leg_index] < 0.03)*\
            (gsf_dr03EcalRecHitSumEt[Z_leg_index] + gsf_dr03HcalDepth1TowerSumEt[Z_leg_index] < (tree.gsf_pt[Z_leg_index]<50)*(2.5 + 0.28*tree.ev_fixedGridRhoFastjetAll) + (tree.gsf_pt[Z_leg_index]>50)*(2.5 + 0.03*(tree.gsf_pt[Z_leg_index] - 50) + 0.28*tree.ev_fixedGridRhoFastjetAll))*\
            (tree.gsf_dr03TkSumPtCorrected[Z_leg_index]<5)*\
            (tree.gsf_nLostInnerHits[Z_leg_index]<2)*\
            (abs(tree.gsf_dxy_firstPVtx[Z_leg_index])<0.05)


    return pass_sel
