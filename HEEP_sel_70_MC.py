#I had to remove the ecaldrivenSeed because there is something fishy with this only variable
#Z_leg_index  0
#ecaldrivenSeed  <ROOT._Bit_reference object at 0x68c3c80>
def HEEP_ID_70(tree,Z_leg_index):
    if(tree.gsf_isEB[Z_leg_index]):
        pass_sel=(tree.gsf_pt[Z_leg_index]>35)*\
            (abs(tree.gsf_deltaEtaSeedClusterTrackAtCalo[Z_leg_index])<0.004)*\
            (abs(tree.gsf_deltaPhiSuperClusterTrackAtVtx[Z_leg_index])<0.06)*\
            (tree.gsf_hadronicOverEm[Z_leg_index] < (1./tree.gsf_caloEnergy[Z_leg_index] + 0.05))*\
            (tree.gsf_full5x5_e2x5Max[Z_leg_index]/tree.gsf_full5x5_e5x5[Z_leg_index] > 0.94 or tree.gsf_full5x5_e1x5[Z_leg_index]/tree.gsf_full5x5_e5x5[Z_leg_index] > 0.83 )*\
            (tree.gsf_dr03EcalRecHitSumEt[Z_leg_index] + tree.gsf_dr03HcalDepth1TowerSumEt[Z_leg_index] < 2 +0.03*tree.gsf_pt[Z_leg_index] + 0.28*tree.ev_fixedGridRhoFastjetAll)*\
            (tree.gsf_dr03TkSumPtHEEP7[Z_leg_index]<5)*\
            (tree.gsf_nLostInnerHits[Z_leg_index]<2)*\
            (abs(tree.gsf_dxy_firstPVtx[Z_leg_index])<0.02)
        
    elif(tree.gsf_isEE[Z_leg_index]):
        pass_sel=(tree.gsf_pt[Z_leg_index]>35)*\
            (abs(tree.gsf_deltaEtaSeedClusterTrackAtCalo[Z_leg_index])<0.006)*\
            (abs(tree.gsf_deltaPhiSuperClusterTrackAtVtx[Z_leg_index])<0.06)*\
            (tree.gsf_hadronicOverEm[Z_leg_index] < (5./tree.gsf_caloEnergy[Z_leg_index] + 0.05))*\
            (tree.gsf_full5x5_sigmaIetaIeta[Z_leg_index] < 0.03)*\
            (tree.gsf_dr03EcalRecHitSumEt[Z_leg_index] + tree.gsf_dr03HcalDepth1TowerSumEt[Z_leg_index] < (tree.gsf_pt[Z_leg_index]<50)*(2.5 + 0.28*tree.ev_fixedGridRhoFastjetAll) + (tree.gsf_pt[Z_leg_index]>50)*(2.5 + 0.03*(tree.gsf_pt[Z_leg_index] - 50) + 0.28*tree.ev_fixedGridRhoFastjetAll))*\
            (tree.gsf_dr03TkSumPtHEEP7[Z_leg_index]<5)*\
            (tree.gsf_nLostInnerHits[Z_leg_index]<2)*\
            (abs(tree.gsf_dxy_firstPVtx[Z_leg_index])<0.05)


    return pass_sel
