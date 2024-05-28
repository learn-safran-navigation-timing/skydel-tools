%% Clean up the environment first =========================================

clear; close all; clc;
%% Insert GPS Satellites Elevation and Azimuth =========

SatNo = input('  How many GPS satellites that you wish to simulate? ');
prn = 1:SatNo;
for i = 1:SatNo
    fprintf('Please insert elevation angle (in degrees) of Satellite No. %d', i); satEl(i) = input('= ');
    fprintf('Please insert azmith angle (in degrees) of Satellite No. %d', i); satAz(i) = input(' = ');
end

%% Plot Skyplot

figure
for i=1:SatNo
    labelStr = sprintf( '%02d', prn(i) );
    SkyView(deg2rad( satAz(1,i) ), deg2rad( satEl(1,i)), labelStr, 'o', ...
        'MarkerSize', 24, 'Linewidth', 6, 'MarkerFaceColor', 'c', 'MarkerEdgeColor', 'c')
    grid off; hold on;
end
legend( 'GPS','Location', 'Best');

%% Generate Keplerian Parameters

for i=1:SatNo
    [gpsKeplerian] = select_sat_based_on_el_az(satEl(i),satAz(i),i)
    T(1,i) = gpsKeplerian;
end

%% Export CSV File
Output = struct2table(T)
writetable(Output)