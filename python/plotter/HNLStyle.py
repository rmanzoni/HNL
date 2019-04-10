from ROOT import TColor, kViolet, kBlue, kRed, kCyan, kAzure, kGreen, kMagenta, kYellow, kOrange

class Style:

    def __init__(self,
                 markerStyle=8,
                 markerColor=1,
                 markerSize=1,
                 lineStyle=1,
                 lineColor=1,
                 lineWidth=2,
                 fillColor=None,
                 fillStyle=1001,
                 drawAsData=False):
        self.markerStyle = markerStyle
        self.markerColor = markerColor
        self.markerSize = markerSize
        self.lineStyle = lineStyle
        self.lineColor = lineColor
        self.lineWidth = lineWidth
        if fillColor is None:
            self.fillColor = lineColor
        else:
            self.fillColor = fillColor
        self.fillStyle = fillStyle
        self.drawAsData = drawAsData

    def formatHisto(self, hist, title=None):
        hist.SetMarkerStyle(self.markerStyle)
        hist.SetMarkerColor(self.markerColor)
        hist.SetMarkerSize(self.markerSize)
        hist.SetLineStyle(self.lineStyle)
        hist.SetLineColor(self.lineColor)
        hist.SetLineWidth(self.lineWidth)
        hist.SetFillColor(self.fillColor)
        hist.SetFillStyle(self.fillStyle)
        if title != None:
            hist.SetTitle(title)
        return hist

# the following standard files are defined and ready to be used.
# more standard styles can be added on demand.
# user defined styles can be created in the same way in any python module

sBlack = Style()
sData = Style(fillStyle=0, markerSize=1.3, drawAsData=True)
sBlue = Style(markerColor=4, fillColor=4)
sGreen = Style(markerColor=8, fillColor=8)
sRed = Style(markerColor=2, fillColor=2)
sYellow = Style(lineColor=1, markerColor=5, fillColor=5)
sViolet = Style(lineColor=1, markerColor=kViolet, fillColor=kViolet)

# John's colours
qcdcol = TColor.GetColor(250,202,255)
dycol =  TColor.GetColor(248,206,104)
dylowcol =  kYellow+1
dybbcol =  kYellow
wcol = TColor.GetColor(222,90,106)
ttcol = TColor.GetColor(155,152,204)
tcol = kMagenta+2
zlcol = TColor.GetColor(100,182,232)
dibosoncol = kBlue+2 #TColor.GetColor(222,90,106)
tribosoncol = kCyan #TColor.GetColor(222,90,106)
ttvcol = kCyan+2 #TColor.GetColor(222,90,106)
zzcol = kGreen+2 #TColor.GetColor(222,90,106)
singleTcol = kCyan 
DDEcol_singlefake = kGreen-3 
DDEcol_doublefake = kBlue-6 
ConversionCol = kMagenta-9

# Backgrounds
sHNL_QCD = Style(lineColor=qcdcol, markerColor=qcdcol, fillColor=qcdcol)
sHNL_DYJets = Style(lineColor=dycol, markerColor=dycol, fillColor=dycol)
sHNL_DYJets_low = Style(lineColor=dylowcol, markerColor=dylowcol, fillColor=dylowcol)
sHNL_DYJets_bb = Style(lineColor=dybbcol, markerColor=dybbcol, fillColor=dybbcol)
sHNL_WJets = Style(lineColor=wcol, markerColor=wcol, fillColor=wcol)
sHNL_TTJets = Style(lineColor=ttcol, markerColor=ttcol, fillColor=ttcol)
sHNL_ZL = Style(lineColor=zlcol, markerColor=zlcol, fillColor=zlcol)
sHNL_VV = Style(lineColor=dibosoncol, markerColor=dibosoncol, fillColor=dibosoncol)
sHNL_TTV = Style(lineColor=ttvcol, markerColor=ttvcol, fillColor=ttvcol)
sHNL_rare = Style(lineColor=tribosoncol, markerColor=tribosoncol, fillColor=tribosoncol)
sHNL_ZZ = Style(lineColor=zzcol, markerColor=zzcol, fillColor=zzcol)
sHNL_Conversion = Style(lineColor = ConversionCol, markerColor = ConversionCol, fillColor=ConversionCol)
sHNL_SingleT = Style(lineColor = singleTcol, markerColor = singleTcol, fillColor=singleTcol)
sHNL_DDE_doublefake = Style(lineColor = DDEcol_doublefake, markerColor = DDEcol_doublefake, fillColor=DDEcol_doublefake)
sHNL_DDE_singlefake = Style(lineColor = DDEcol_singlefake, markerColor = DDEcol_singlefake, fillColor=DDEcol_singlefake)
# Signals
sHNL_HN  = Style(lineColor=kBlue   , markerColor=0, lineStyle=2, fillColor=0, lineWidth=3)
sHNL_HN2 = Style(lineColor=kAzure+8, markerColor=0, lineStyle=3, fillColor=0, lineWidth=3)


sBlackSquares = Style(markerStyle=21)
sBlueSquares  = Style(lineColor=4, markerStyle=21, markerColor=4)
sGreenSquares = Style(lineColor=8, markerStyle=21, markerColor=8)
sRedSquares   = Style(lineColor=2, markerStyle=21, markerColor=2)


styleSet = [sBlue, sGreen, sRed, sYellow, sViolet, sBlackSquares, sBlueSquares, sGreenSquares, sRedSquares]
iStyle = 0


def nextStyle():
    global iStyle
    style = styleSet[iStyle]
    iStyle = iStyle+1
    if iStyle >= len(styleSet):
        iStyle = 0
    return style

histPref = {}
histPref['HN*'] = {'style':sHNL_HN, 'layer':2999, 'legend':'#splitline{M = 3GeV, #sigma = 90fb}{c#tau = 14.6cm}'}#times 300}{c#tau = 14.6cm}'}
histPref['Data*'] = {'style':sData, 'layer':2999, 'legend':'Observed'}
histPref['data_*'] = {'style':sData, 'layer':2999, 'legend':'Observed'}
histPref['ZTT*'] = {'style':sHNL_DYJets, 'layer':4, 'legend':'Z#rightarrow#tau#tau'}
histPref['DY*'] = {'style':sHNL_DYJets, 'layer':4, 'legend':'DY'}
# histPref['DYJets'] = {'style':sHNL_DYJets, 'layer':4, 'legend':'DYM50'}
# histPref['DYJets_ext'] = {'style':sHNL_DYJets, 'layer':4, 'legend':'DYM50'}
# histPref['DYJetsToLL_M10to50*'] = {'style':sHNL_DYJets_low, 'layer':4, 'legend':'DYM10'}
# histPref['DYBB'] = {'style':sHNL_DYJets_bb, 'layer':4, 'legend':'DYBB'}
histPref['Conversion*'] = {'style':sHNL_Conversion, 'layer':5, 'legend':'Conversion'}
histPref['embed_*'] = {'style':sViolet, 'layer':4.1, 'legend':None}
histPref['TTJets*'] = {'style':sHNL_TTJets, 'layer':1, 'legend':'t#bar{t}'} 
histPref['T*tW*'] = {'style':sHNL_SingleT, 'layer':1, 'legend':'Single t'} 
histPref['TTo*'] = {'style':sHNL_SingleT, 'layer':1, 'legend':'Single t'} 
histPref['TBarTo*'] = {'style':sHNL_SingleT, 'layer':1, 'legend':'Single t'} 
histPref['ST*'] = {'style':sHNL_SingleT, 'layer':1, 'legend':'Single t'} 
histPref['single t*'] = {'style':sHNL_SingleT, 'layer':1, 'legend':'Single t'} 
histPref['Single t'] = {'style':sHNL_SingleT, 'layer':1, 'legend':'Single t'} 
histPref['WWTo*'] = {'style':sHNL_VV, 'layer':0.9, 'legend':'Diboson'} 
histPref['WZTo*'] = {'style':sHNL_VV, 'layer':0.8, 'legend':'Diboson'} 
# histPref['ZZTo*'] = {'style':sHNL_VV, 'layer':0.7, 'legend':'Diboson'} 
# histPref['ZZTo*'] = {'style':sHNL_VV, 'layer':0.7, 'legend':'ZZ'} 
histPref['ZZTo*'] = {'style':sHNL_ZZ, 'layer':0.7, 'legend':'ZZ'} 
histPref['WW'] = {'style':sHNL_VV, 'layer':0.9, 'legend':'Diboson'} 
histPref['WZ'] = {'style':sHNL_VV, 'layer':0.9, 'legend':'Diboson'} 
histPref['ZZ'] = {'style':sHNL_VV, 'layer':0.9, 'legend':'Diboson'} 
histPref['Diboson'] = {'style':sHNL_VV, 'layer':0.7, 'legend':'Diboson'} 
histPref['TTZ*'] = {'style':sHNL_TTV, 'layer':1, 'legend':'t#bar{t}Z'} 
histPref['TTW*'] = {'style':sHNL_TTV, 'layer':1, 'legend':'t#bar{t}W'} 
histPref['ttV'] = {'style':sHNL_TTV, 'layer':1, 'legend':'t#bar{t}V'} 
histPref['WGG*'] = {'style':sHNL_rare, 'layer':0.7, 'legend':'Triboson'} 
histPref['WWW*'] = {'style':sHNL_rare, 'layer':0.7, 'legend':'Triboson'} 
histPref['WZZ*'] = {'style':sHNL_rare, 'layer':0.7, 'legend':'Triboson'} 
histPref['WWZ*'] = {'style':sHNL_rare, 'layer':0.7, 'legend':'Triboson'} 
histPref['ZZZ*'] = {'style':sHNL_rare, 'layer':0.7, 'legend':'Triboson'} 
histPref['Triboson'] = {'style':sHNL_rare, 'layer':0.7, 'legend':'Triboson'} 
# histPref['VV*'] = {'style':sHNL_VV, 'layer':0.7, 'legend':'Diboson'} 
histPref['VV*'] = {'style':sHNL_ZZ, 'layer':0.7, 'legend':'ZZ'} 
histPref['ggZZ*'] = {'style':sHNL_ZZ, 'layer':0.7, 'legend':'ZZ'} 
histPref['Electroweak'] = {'style':sHNL_VV, 'layer':0.7, 'legend':'Electroweak'} 
# histPref['QCD'] = {'style':sHNL_QCD, 'layer':2, 'legend':'QCD multijet'}
histPref['QCD*'] = {'style':sHNL_QCD, 'layer':2, 'legend':'QCD multijet'}
histPref['W'] = {'style':sHNL_WJets, 'layer':3, 'legend':'W+jets'}  
histPref['WJ*'] = {'style':sHNL_WJets, 'layer':3, 'legend':'W+jets'}  
histPref['W+Jets'] = {'style':sHNL_WJets, 'layer':3, 'legend':'W+jets'}  
histPref['W1J*'] = {'style':sHNL_WJets, 'layer':3, 'legend':'W+jets'}  
histPref['W2J*'] = {'style':sHNL_WJets, 'layer':3, 'legend':'W+jets'}  
histPref['W3J*'] = {'style':sHNL_WJets, 'layer':3, 'legend':'W+jets'}  
histPref['W4J*'] = {'style':sHNL_WJets, 'layer':3, 'legend':'W+jets'}  
#histPref['W*Jets*'] = {'style':sHNL_WJets, 'layer':3, 'legend':'W+jets'}  
histPref['EWK'] = {'style':sHNL_WJets, 'layer':3, 'legend':'EWK'}  
histPref['ElectroWeak'] = {'style':sHNL_WJets, 'layer':3, 'legend':'ElectroWeak'}  
histPref['ZJ*'] = {'style':sHNL_DYJets, 'layer':3.1, 'legend':'Z#rightarrow#tau#tau/Z#rightarrow ll, j#rightarrow#tau'}
histPref['ZL*'] = {'style':sHNL_ZL, 'layer':3.2, 'legend':'Z#rightarrow ll'}
histPref['WLL*'] = {'style':sHNL_ZL, 'layer':3.2, 'legend':'W#rightarrow ll'}
histPref['Zl0jet*'] = {'style':sHNL_ZL, 'layer':3.2, 'legend':'Z#rightarrow ll + 0 jets'}
histPref['Zl1jet*'] = {'style':sHNL_DYJets, 'layer':3.2, 'legend':'Z#rightarrow ll + 1 jet'}
histPref['Zl2jet*'] = {'style':sHNL_HN, 'layer':3.2, 'legend':'Z#rightarrow ll + #geq 2 jets'}
histPref['ZLL'] = {'style':sHNL_ZL, 'layer':3.2, 'legend':'Z#rightarrow ll'}
histPref['Ztt_TL'] = {'style':sViolet, 'layer':4.1, 'legend':'Z#rightarrow#tau#tau/Z#rightarrow ll, j#rightarrow#tau'}
histPref['HiggsGGH125'] = {'style':sHNL_HN, 'layer':1001, 'legend':'H_{125}#rightarrow#tau#tau (ggH)'}
histPref['HiggsVBF125'] = {'style':sHNL_HN2, 'layer':1001, 'legend':'H_{125}#rightarrow#tau#tau (VBF)'}
histPref['ggH*'] = {'style':sHNL_HN, 'layer':1001, 'legend':None}
histPref['bbH*'] = {'style':sHNL_HN, 'layer':1001, 'legend':None}
histPref['SMS*'] = {'style':sHNL_HN, 'layer':1001, 'legend':None}
# histPref['DDE*'] = {'style':sHNL_DDE, 'layer':1001, 'legend':'nonprompt'}
histPref['*doublefake*'] = {'style':sHNL_DDE_doublefake, 'layer':900, 'legend':'DF'}
histPref['*singlefake*'] = {'style':sHNL_DDE_singlefake, 'layer':900, 'legend':'SF'}
