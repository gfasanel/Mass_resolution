import ROOT
tree= ROOT.TChain("IIHEAnalysis")
tree.Add('/user/aidan/public/HEEP/samples/RunIISpring15DR74/RunIISpring15DR74_DYToEE_50_25ns/outfile_1.root')
tree.Print()

