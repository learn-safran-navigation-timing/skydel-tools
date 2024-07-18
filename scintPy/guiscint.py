import math
import time
import scintModel04
from scintModel04 import Model04
import genUAF2
from genUAF2 import genUAF2
import numpy as np
import scipy.io as sio

class mainWindpws:

    def __init__(self):
        # Nspb is the number of sub-samples per accumulation
        self.Nspa = 8
        fnh = 'helvetica'
        fnt = 'times new roman'
        self.Tb = 0.02
        # Initial values
        self.ivS4 = 0.5
        self.ivtau0 = 1
        self.ivC_N0 = 45
        self.ivTsim = 300
        # Extreme values
        self.minS4 = 0
        self.maxS4 = 1
        self.mintau0 = -1
        self.maxtau0 = 0.3010
        self.minC_N0 = 35
        self.maxC_N0 = 55
        self.minTsim = 10
        self.maxTsim = 1000
        # The range of Te that will be plotted (logarithmically) on the graph
        self.TeLow = 0.626
        self.TeHigh = 3600 * 20
        self.PeLow = self.Tb / self.TeHigh
        self.PeHigh = self.Tb / self.TeLow
        self.PeLowLog = math.log(self.PeLow)
        self.PeHighLog = math.log(self.PeHigh)
        # self.Levels = {'Negligible','Weak', 'Moderate', 'Severe', ...
        #         'Catastrophic'}
        # self.mLevels = len(self.Levels)

        self.hTA = 10

    """----- Initialize and hide the GUI as it is being constructed.
    f =figure('Visible','off','menubar','none','Position',[360,500,396,320])
    
    
    %----- Construct the console frames
    xConsole = 230; wConsole = 154; xTitles = 233;
    hConsole1 =uicontrol( ...
        'Style','frame', ...
        'Position',[xConsole,170,wConsole,146], ...
        'BackgroundColor',[0.50 0.50 0.50]);
    htConsole1  = uicontrol('style','text','string','Scintillation Parameters',...
                            'Position',[xTitles,300,145,10], ...
                            'BackgroundColor',[0.50 0.50 0.50],... 
                            'foregroundColor',[0,0,0.5],'fontweight','bold',...
                            'fontname',fnh);
    hConsole2 =uicontrol( ...
        'Style','frame', ...
        'Position',[xConsole,102,wConsole,64], ...
        'BackgroundColor',0.5*[1,1,1]);
    htConsole2   = uicontrol('style','text','string','Expected Nominal C/N0',...
                             'Position',[xTitles,152,145,12], ...
                             'BackgroundColor',0.5*[1,1,1],... 
                             'foregroundColor',[0,0,0.5],'fontweight','bold',...
                             'fontname',fnh);
    
    hConsole3 =uicontrol( ...
        'Style','frame', ...
        'Position',[xConsole,4,wConsole,94], ...
        'BackgroundColor',0.5*[1,1,1]);
    htConsole3   = uicontrol('style','text','string','Simulation Settings',...
                             'Position',[xTitles,84,145,12], ...
                             'BackgroundColor',0.5*[1,1,1],... 
                             'foregroundColor',[0,0,0.5],'fontweight','bold',...
                             'fontname',fnh);
    
    %----- Construct the components.
    xSlider = 244;wSlider = 125;hSlider = 15;wEdit = 50;xEdit = 279;
    hS4      = uicontrol('Style','slider','min',minS4,'max',maxS4,...
                         'value',ivS4,...
                         'position',[xSlider,260,wSlider,hSlider],...
                         'sliderstep',[0.05,0.1],...
                         'callback', {@S4sliderCallback});
    ivtau0Log10 = log10(ivtau0);
    htau0    = uicontrol('Style','slider','min',mintau0,'max',maxtau0,...
                         'value',ivtau0Log10,...
                         'position',[xSlider,200,wSlider,hSlider],...
                         'sliderstep',[0.05,0.1],...
                         'callback', {@tau0sliderCallback});
    hC_N0    = uicontrol('Style','slider','min',minC_N0,'max',maxC_N0,...
                         'value',ivC_N0,...
                         'position',[xSlider,130,wSlider,hSlider],...
                         'sliderstep',[0.05,0.1],...
                         'callback', {@C_N0sliderCallback});
    htS4     = uicontrol('style','text','string','S4 Index',...
                         'Position',[330-56,280,60,10], ...
                         'BackgroundColor',[0.50 0.50 0.50],... 
                         'foregroundColor',[0,0,0],'fontweight','bold',...
                         'fontname',fnh);
    httau0   = uicontrol('style','text','string','tau0',...
                         'Position',[274,220,60,10], ...
                         'BackgroundColor',[0.50 0.50 0.50],... 
                         'foregroundColor',[0,0,0],'fontweight','bold',...
                         'fontname',fnh);
    httau0U  = uicontrol('style','text','string','sec',...
                         'Position',[332,183,20,12], ...
                         'BackgroundColor',[0.50 0.50 0.50],... 
                         'foregroundColor',[0,0,0],'fontname',fnh);
    self.heS4     = uicontrol('style','edit','position',[xEdit,243,wEdit,hSlider],...
                         'value',ivS4,'string',num2str(ivS4),...
                         'callback', {@S4editCallback});
    self.hetau0   = uicontrol('style','edit','position',[xEdit,183,wEdit,hSlider],...
                         'value',ivtau0,'string',num2str(ivtau0),...
                         'callback', {@tau0editCallback});
    heC_N0   = uicontrol('style','edit','position',[xEdit,113,wEdit,hSlider],...
                         'value',ivC_N0,'string',num2str(ivC_N0),...
                         'callback', {@C_N0editCallback});
    htC_N0U  = uicontrol('style','text','string','dB-Hz',...
                         'Position',[332,113,35,12], ...
                         'BackgroundColor',[0.50 0.50 0.50],... 
                         'foregroundColor',[0,0,0],'fontname',fnh);
    
    hTa = uicontrol('Style','popupmenu',...
               'String',{'10','20'},...
               'Position',[244,60,40,20], 'value', 1);
    htTa   = uicontrol('style','text','string','Ta (ms)',...
                       'Position',[284,65,50,12], ...
                       'BackgroundColor',[0.50 0.50 0.50],... 
                       'foregroundColor',[0,0,0],'fontweight','bold',...
                       'fontname',fnh);
    self.heTsim   = uicontrol('style','edit','position',[244,25,40,hSlider],...
                       'value',ivTsim,'string',ivTsim,... 
                       'callback', {@TsimeditCallback});
    hteTsim   = uicontrol('style','text','string','Length (sec)',...
                       'Position',[290,25,70,12], ...
                       'BackgroundColor',[0.50 0.50 0.50],... 
                       'foregroundColor',[0,0,0],'fontweight','bold',...
                       'fontname',fnh);
    hSim = uicontrol('Style','pushbutton',...
                     'String','Simulate','Position',[45,5,60,25],...
                     'callback', {@SimCallback});
    htSim   = uicontrol('style','text','string',...
                        'Data written to scintDat.mat',...
                        'Position',[120,4,80,25], ...
                        'BackgroundColor',[0.8 0.8 0.8],... 
                        'foregroundColor',[0,0,0],...
                        'fontname',fnh, 'visible', 'off');
    
    %----- The axis and its labels
    hAxis = axes('Units','pixels','Position',[50,40,50,260],...
                 'visible', 'off');
    htAxis = uicontrol('style','text','string','Te = 10 sec',...
                       'Position',[35,300,80,12], ...
                       'foregroundColor',[0,0,0.5],...
                       'backgroundColor',0.8*[1,1,1],...
                       'fontname',fnh,'visible', 'off');
    hLevelVec = zeros(NLevels,1);
    ybase = 33;
    dy = 62;
    for ii=1:NLevels
      str = Levels{ii};
      ylab = ybase + dy*(ii-1);
      M = hot;
      clr = M((ii-1)*6 + 1,:);
      hLevelVec(ii) = uicontrol('style','text','string',str,...
                                'Position',[103,ylab,80,20], ...
                                'foregroundColor',clr,...
                                'backgroundColor',0.8*[1,1,1],...
                                'fontname',fnh,...
                                'fontweight','bold','fontsize',10,...
                                'horizontalalignment', 'left');
    end
    
    %align([htConsole1,httau0],'Center','None');
    
    %----- Initialize the GUI.
    % Change units to normalized so components resize automatically.
    handleVec = [f,hConsole1,htConsole1,hConsole2,htConsole2,hConsole3, ...
                 htConsole3,hS4,htau0,hC_N0,htS4,httau0,self.heS4,self.hetau0,heC_N0, ...
                 hTa,htTa,self.heTsim,hteTsim,hSim,hAxis,httau0U,htC_N0U,...
                 htAxis,htSim,hLevelVec'];
    set(handleVec,'Units','normalized');
    % Assign the GUI a name to appear in the window title.
    set(f,'Name','Equatorial Scintillation Simulator')
    movegui(f,'northeast')
    % Make the GUI visible.
    set(f,'Visible','on')
    updateGraph
    
    %----- Program the Callbacks
    function S4sliderCallback(hObject,eventdata) 
    v = get(hObject,'value');
    v = fix(100*v)/100;
    set(self.heS4,'value',v,'string',num2str(v));
    updateGraph
    end
    
    function tau0sliderCallback(hObject,eventdata) 
    v = get(hObject,'value');
    v = 10^v; v = round(100*v)/100;
    set(self.hetau0,'value',v,'string',num2str(v));
    updateGraph
    end
    
    function C_N0sliderCallback(hObject,eventdata)
    v = get(hObject,'value');
    set(heC_N0,'value',v,'string',num2str(v));
    updateGraph
    end
    
    function S4editCallback(hObject,eventdata)
    vstring = get(hObject,'string');
    v = eval(vstring);
    v = fix(100*v)/100;
    if(v < minS4) v = minS4; end
    if(v > maxS4) v = maxS4; end
    set(hS4,'value',v);
    set(self.heS4,'value',v, 'string', num2str(v));
    updateGraph
    end
    
    function tau0editCallback(hObject,eventdata)
    vstring = get(hObject,'string');
    v = (eval(vstring));
    v = round(100*v)/100; v = log10(v);
    if(v < mintau0) v = mintau0; end
    if(v > maxtau0) v = maxtau0; end
    v = 10^v;
    set(self.hetau0,'value',v,'string',num2str(v));
    set(htau0,'value',log10(v));
    updateGraph
    end
    
    function C_N0editCallback(hObject,eventdata) 
    vstring = get(hObject,'string');
    v = eval(vstring);
    v = round(10*v)/10;
    if(v < minC_N0) v = minC_N0; end
    if(v > maxC_N0) v = maxC_N0; end
    set(hC_N0,'value',v);
    set(heC_N0,'value',v,'string',num2str(v));
    updateGraph
    end
    
    
    function TsimeditCallback(hObject,eventdata) 
    vstring = get(hObject,'string');
    v = fix(eval(vstring));
    v = round(v);
    if(v < minTsim) v = minTsim; end
    if(v > maxTsim) v = maxTsim; end
    set(self.heTsim,'string',num2str(v),'value',v);
    end
    """

    def SimCallback(self):
        # set(htSim,'visible','off')
        # str = get(hSim,'string')
        self.hTA = 10
        # if(strcmp(str,'Simulate')):
        # set(hSim,'string', 'Busy', 'enable', 'off')
        mode = "Simulate"

        if mode == "Simulate":
            time.sleep(0.01)
            # v = get(hTa,'value')
            """self.v = self.hTA
            #vstr = get(hTa,'string')
            vstr = str(self.v)
            #Ta = eval(vstr{v})/1000
            self.Ta = self.v/1000
            #tau0 = get(self.hetau0,'value')
            self.tau0 = self.hetau0
            #S4 = get(self.heS4,'value')

            self.S4 = self.heS4

            self.m = max(1,1/(self.S4^2))
            self.K = math.sqrt(self.m^2 - self.m)/(self.m - math.sqrt(self.m^2 - self.m))
            #Tsim = get(self.heTsim,'value')
            self.Tsim = self.heTsim
            self.Napb = self.Tb/self.Ta
            self.Nt = self.Napb*round(self.Tsim/self.Tb)"""
            self.Tsim = 300
            self.Tb  = 0.02
            self.Ta = 0.0100
            self.tau0 = 1
            self.S4 = 0.5
            self.m = max(1, 1/(self.S4*self.S4))
            self.K = math.sqrt(self.m**2-self.m)/(self.m-math.sqrt(self.m**2 - self.m))
            self.Napb = self.Tb/self.Ta
            self.Nspa = 8
            self.Nt = self.Napb*round(self.Tsim/self.Tb)

            print("Ta:", self.Ta)
            print("Nt:", self.Nt)
            print("tau0:", self.tau0)
            print("K:", self.K)
            print("Nspa:", self.Nspa)

            algo = Model04()

            [zskhist, zkhist, tkhist] = algo.model_scint(self.Ta, self.Nt, self.tau0, self.K, self.Nspa)
            scintPyDat = {'time': tkhist, 'data': zkhist}
            sio.savemat('scintPyDat.mat', scintPyDat)

            [zskhist, zkhist, tkhist] = algo.model_scint(self.Ta, self.Nt, self.tau0, self.K, self.Nspa)
            scintPyDat_L2 = {'time': tkhist, 'data': zkhist}
            sio.savemat('scintPyDat_L2.mat', scintPyDat_L2)

main = mainWindpws()
main.SimCallback()
