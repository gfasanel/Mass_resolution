import ROOT
tree= ROOT.TChain("IIHEAnalysis")
tree.Add('/pnfs/iihe/cms/store/user/wenxing/ZToEE_NNPDF30_13TeV-powheg_M_50_120/crab_ZToEE_NNPDF30_13TeV-powheg_M_50_120_RunIISpring16DR80/160517_090136/0000/outfile_1.root ')
tree.Print()

