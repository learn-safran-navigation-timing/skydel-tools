clear all,
clc,


% Specify files to open
% Bin file
[filen, pathname] = uigetfile('C:\Users\iurie\Documents\Skydel-SDX\*.iq');
file1 = [pathname filen];

% Open file
fid1 = fopen(file1, 'r', 'l');

% Initial parameters
L1 = 1575.42e6;
speed_light = 299792458;
LAM = speed_light/L1;
Nblock = 1; % blocks to analyse
Fs = 25e6; % sample frequency
W = 1/4*1e-2*1e3; % frequency resolution
offset = 200*Fs/1000*4; % bytes to skip 
% offset = 8*1000*Fs/1000*4; % bytes to skip 
N = 64; % itterations for spectrum average

% Offset from the origin 
fseek(fid1, offset, -1);

% Block length
Nsamples = round(Fs/W);
% Nsamples = 2^12;

t = linspace(0,0.001, Fs/1000);
f = -0.518e3;
for k = 1:Nblock
    
    % Read I/Q data in int16 format  
    dataIQ_16_1 = fread(fid1, Nsamples*2, 'int16');

    % Convert to complex double
    data_complex = double(dataIQ_16_1(1:2:2*Nsamples-1)) + j.*double(dataIQ_16_1(2:2:2*Nsamples));
    
    
    % Construct a Welch spectrum object.
    h = spectrum.welch('hamming',length(data_complex));

    h.WindowName = 'Blackman';
%   h.WindowName = 'Kaiser';

    hpsd5 = psd(h,data_complex,'Fs',Fs);
    Pxx5 = hpsd5.Data;
    Pxx5_shift = circshift(Pxx5,floor(length(Pxx5)/2));

    % Average spectrum     
    if k <=N
        averageData(:,k) = Pxx5_shift; 
        mean_averageData = mean(averageData, 2);
    else
        averageData = circshift(averageData,[0 -1]);
        averageData(:,N) = Pxx5_shift;
    end
    
    mean_averageData = mean(averageData, 2);
    hpsd = dspdata.psd([mean_averageData],linspace(-Fs/2,Fs/2,length(Pxx5_shift)),'Fs',Fs);
       
%     figure (2),
%     plot(hpsd);
%     axis([-Fs/2*1e-6 Fs/2*1e-6 -100 70]),
%     drawnow,
    
%     figure (5),
%     plot(real(data_complex(1:1000)), imag(data_complex(1:1000)), '*'), grid on, axis([-1200 1200 -1200 1200]),
%     drawnow,


 