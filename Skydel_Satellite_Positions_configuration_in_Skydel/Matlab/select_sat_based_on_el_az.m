function [gpsKeplerian] = select_sat_based_on_el_az(el,az,prn) 

% Initial parameters from input
azimute = az;
elevation = el;

% Conditions
if (azimute > 180)
    azimute = (azimute-360);
end

if (azimute >=0) && (azimute <=90)
    
    % Recompute elevation/azimute
    azimute = 90-azimute;
    elevation = elevation - 90;
    
    % Ascending node
    omega_0 = 0;
    
    % Define semi-major axes
    sqrtA = 5153;
    
    % Eccentricity
    e = 0;
    
    % Argument of perigee
    omega = pi/2;
    
    % Compute M0
    R_earth = 6378137.0;
    R_sat = sqrtA^2;
    phi_a = asin(R_earth*sin(elevation/180*pi)/R_sat);
    phi_a = pi-phi_a;
    M0_deg = 180 - (90+elevation + phi_a/pi*180);
    M_0 = M0_deg/180*pi;
    
    % Inclination    
    i_0 = azimute/180*pi;

end

if (azimute > -180) && (azimute <= -90)
    
    % Recompute elevation/azimute
    azimute = 180 + azimute;
    azimute = 90-azimute;    
    elevation = 90 - elevation;
    
    % Ascending node
    omega_0 = 0;
    
    % Semi-major acces
    sqrtA = 5153;
    
    % Eccentricity
    e = 0;
    
    % Argument of perigee
    omega = pi/2;
    
    % Compute M0
    R_earth = 6378137.0;
    R_sat = sqrtA^2;
    phi_a = asin(R_earth*sin(elevation/180*pi)/R_sat);
    phi_a = pi-phi_a;
    M0_deg = 180 - (90+elevation + phi_a/pi*180);
    M_0 = M0_deg/180*pi;
    
    % Inclination
    i_0 = azimute/180*pi;

end

if (azimute > -90) && (azimute < 0)
    
    % Recompute elevation/azimute
    azimute = 90 + azimute;
    elevation = 90 - elevation;
    
    % Ascending node
    omega_0 = pi;
    
    % Semi-major acces
    sqrtA = 5153;
    
    % Eccentricity
    e = 0;
    
    % Argument of perigee
    omega = pi/2;
    
    % Compute M0
    R_earth = 6378137.0;
    R_sat = sqrtA^2;
    phi_a = asin(R_earth*sin(elevation/180*pi)/R_sat);
    phi_a = pi-phi_a;
    M0_deg = 180 - (90+elevation + phi_a/pi*180);
    M0_deg = (M0_deg - 180);
    M_0 = M0_deg/180*pi;
    
    % Inclination
    i_0 = azimute/180*pi;

end

if (azimute > 90) && (azimute <= 180)
    
    % Recompute elevation/azimute
    azimute = azimute - 90;
    elevation = elevation - 90;
    
    % Ascending node
    omega_0 = pi;
    
    % Semi-major acces
    sqrtA = 5153;
    
    % Eccentricity
    e = 0;
    
    % Argument of perigee
    omega = pi/2;
    
    % Compute M0
    R_earth = 6378137.0;
    R_sat = sqrtA^2;
    phi_a = asin(R_earth*sin(elevation/180*pi)/R_sat);
    phi_a = pi-phi_a;
    M0_deg = 180 - (90+elevation + phi_a/pi*180);
    M0_deg = (M0_deg - 180);
    M_0 = M0_deg/180*pi;
    
    % Inclination
    i_0 = azimute/180*pi;

end
gpsKeplerian.PRN = prn;
gpsKeplerian.t_oc = 0;
gpsKeplerian.t_oe = 0;

gpsKeplerian.sqrtA = sqrtA;
gpsKeplerian.e = e;
gpsKeplerian.omega = omega;

if M_0 < -pi
    M_0 = 2*pi + M_0;
end

if M_0 > pi
    M_0 = -2*pi + M_0;
end

% Semi-cercles
gpsKeplerian.M_0 = M_0/pi;
gpsKeplerian.i_0 = i_0/pi;
gpsKeplerian.omega_0 = omega_0/pi;
gpsKeplerian.omega = omega/pi;
gpsKeplerian.omega_dot = 0;
gpsKeplerian.i_dot = 0;
gpsKeplerian.delta_n = 0;

% Radians
% gpsKeplerian.M_0 = M_0;
% gpsKeplerian.i_0 = i_0;
% gpsKeplerian.omega_0 = omega_0;
% gpsKeplerian.omega_dot = 0;
% gpsKeplerian.i_dot = 0;
% gpsKeplerian.delta_n = 0;

end
