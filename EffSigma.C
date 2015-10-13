//effsigma function from Chris
#include <TH1.h>
#include <iostream>
Double_t EffSigma(TH1 * hist)
{

  TAxis *xaxis = hist->GetXaxis();
  Int_t nb = xaxis->GetNbins();
  if(nb < 10) {
    cout << "effsigma: not enough bins. nbins = " << nb << endl;
    return 0.;
  }
  
  Double_t bwid = xaxis->GetBinWidth(1);
  if(bwid == 0) {
    cout << "effsigma: binwidth is zero. bwid = " << bwid << endl;
    return 0.;
  }
  //Double_t xmax = xaxis->GetXmax();//Not used
  Double_t xmin = xaxis->GetXmin();
  Double_t ave = hist->GetMean();
  Double_t rms = hist->GetRMS();

  Double_t total=0.;
  for(Int_t i=0; i<nb+2; i++) {
    total+=hist->GetBinContent(i);
  }
//   if(total < 100.) {
//     cout << "effsigma: Too few entries " << total << endl;
//     return 0.;
//   }
  Int_t ierr=0;//flag for errors
  Int_t ismin=999;
  
  Double_t rlim=0.683*total;
  Int_t nrms=rms/(bwid);    // Set scan size to +/- rms
  if(nrms > nb/10) nrms=nb/10; // Could be tuned...

  Double_t effSigma=9999999.;//initial crazy value
  for(Int_t iscan=-nrms;iscan<nrms+1;iscan++) { // Scan window centre
    Int_t ibm=(ave-xmin)/bwid +1+iscan;
    Double_t x=(ibm-0.5)*bwid +xmin;
    Double_t x_right=x;
    Double_t x_left=x;
    Int_t j_right=ibm;
    Int_t j_left=ibm;
    Double_t bin=hist->GetBinContent(ibm);//bin=#events nel punto di scan
    total=bin;
    for(Int_t j=1;j<nb;j++){//right direction
      if(j_right < nb) {
        j_right++;
        x_right+=bwid;
        bin=hist->GetBinContent(j_right);
        total+=bin;
        if(total > rlim) break;
      }
      else ierr=1;
      
      if(j_left > 0) {//left direction
        j_left--;
        x_left-=bwid;
        bin=hist->GetBinContent(j_left);
        total+=bin;
        if(total > rlim) break;
      }
      else ierr=2;

    }

    Double_t dxf=(total-rlim)*bwid/bin;//bin=#events nell'ultimo x toccato
    //cout<<"x_right "<<x_right<<" x_left "<<x_left<<endl;
    //cout<<"dxf is "<<dxf<<endl;
    //cout<<"bwid is "<<bwid<<endl;
    Double_t wid=(x_right-x_left+bwid-dxf)*0.5;
    //cout<<"wid is "<<wid<<endl;
    if(wid < effSigma) {
      effSigma=wid;
      ismin=iscan;
    }
  }//chiude lo scan su iscan
  if(ismin == nrms || ismin == -nrms) ierr=3;
  if(ierr != 0) cout << "effsigma: Error of type " << ierr << endl;
  
  return effSigma;
  
}
