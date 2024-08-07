function hpol = SkyView (az,el,label,varargin)

%SkyPlot Azimuth Elevation plot based on POLAR
labelq=1;
if nargin < 2
    error('Requires at least 3 input arguments.')
elseif nargin == 3
    if isstr(el)
        line_style = label;
        label = el;
        el = az;
        [mr,nr] = size(el);
        if mr == 1
            az = 1:nr;
        else
            th = (1:mr)';
            az = th(:,ones(1,nr));
        end
    else
        line_style = 'auto';
    end
elseif nargin == 2
    line_style = 'auto';
    label = '';
    labelq=0;
    el = az;
    [mr,nr] = size(el);
    if mr == 1
        az = 1:nr;
    else
        th = (1:mr)';
        az = th(:,ones(1,nr));
    end
end
if isstr(az) | isstr(el)
    error('Input arguments must be numeric.');
end
if ~isequal(size(az),size(el))
    error('AZ and EL must be the same size.');
end


theta = az;

rho = el.*(180/pi);

% get hold state
cax = newplot;
next = lower(get(cax,'NextPlot'));
hold_state = ishold;

% get x-axis text color so grid is in same color
tc = get(cax,'xcolor');
ls = get(cax,'gridlinestyle');

% Hold on to current Text defaults, reset them to the
% Axes' font attributes so tick marks use them.
fAngle  = get(cax, 'DefaultTextFontAngle');
fName   = get(cax, 'DefaultTextFontName');
fSize   = get(cax, 'DefaultTextFontSize');
fWeight = get(cax, 'DefaultTextFontWeight');
fUnits  = get(cax, 'DefaultTextUnits');
set(cax, 'DefaultTextFontAngle',  get(cax, 'FontAngle'), ...
    'DefaultTextFontName',   get(cax, 'FontName'), ...
    'DefaultTextFontSize',   get(cax, 'FontSize'), ...
    'DefaultTextFontWeight', get(cax, 'FontWeight'), ...
    'DefaultTextUnits','data')

% only do grids if hold is off
if ~hold_state
    
    % make a radial grid
    hold on;
    maxrho = 90;
    
    hhh=plot([-maxrho -maxrho maxrho maxrho],[-maxrho maxrho maxrho -maxrho]);
    set(gca,'dataaspectratio',[1 1 1],'plotboxaspectratiomode','auto')
    v = [get(cax,'xlim') get(cax,'ylim')];
    ticks = sum(get(cax,'ytick')>=0);
    delete(hhh);
    rmin = 0;
    rmax = 90;
    rticks = 6;
    
    % define a circle
    th = 0:pi/50:2*pi;
    xunit = cos(th);
    yunit = sin(th);
    % now really force points on x/y axes to lie on them exactly
    inds = 1:(length(th)-1)/4:length(th);
    xunit(inds(2:2:4)) = zeros(2,1);
    yunit(inds(1:2:5)) = zeros(3,1);
    % plot background if necessary
    if ~isstr(get(cax,'color')),
        patch('xdata',xunit*rmax,'ydata',yunit*rmax, ...
            'edgecolor',tc,'facecolor',get(gca,'color'),...
            'handlevisibility','off');
    end
    
    % draw radial circles
    c82 = cos(-8*pi/180);
    s82 = sin(-8*pi/180);
    rinc = (rmax-rmin)/rticks;
    for i=(rmax-rinc):-rinc:rmin+rinc
        hhh = plot(xunit*i,yunit*i,ls,'color',tc,'linewidth',1,...
            'handlevisibility','off');
        text((i+rinc/20)*c82,(i+rinc/20)*s82, ...
            ['  ' num2str(rmax - i)],'verticalalignment','bottom',...
            'handlevisibility','off')
    end
    
    % plot spokes
    th = (1:6)*2*pi/12;
    cst = cos(th); snt = sin(th);
    cs = [-cst; cst];
    sn = [-snt; snt];
    plot(rmax*cs,rmax*sn,ls,'color',tc,'linewidth',1,...
        'handlevisibility','off')
    
    % annotate spokes in degrees
    rt = 1.1*rmax;
    for i = 1:length(th)
        text(rt*cst(i),-rt*snt(i),int2str(i*30),...
            'horizontalalignment','center',...
            'handlevisibility','off');
        if i == length(th)
            loc = int2str(0);
        else
            loc = int2str(180+i*30);
        end
        text(-rt*cst(i),rt*snt(i),loc,'horizontalalignment','center',...
            'handlevisibility','off')
    end
    
    % set view to 2-D
    view(2);
    % Rotate so North is up COD
    view([-90 90])
    % set axis limits
    axis(rmax*[-1 1 -1.15 1.15]);
end

% Reset defaults.
set(cax, 'DefaultTextFontAngle', fAngle , ...
    'DefaultTextFontName',   fName , ...
    'DefaultTextFontSize',   fSize, ...
    'DefaultTextFontWeight', fWeight, ...
    'DefaultTextUnits',fUnits );

% transform data to Cartesian coordinates.
xx = (90-rho).*cos(theta);
yy = (90-rho).*sin(theta);

tmp = find(el>0);

xx = xx(tmp);
yy = yy(tmp);

% plot data on top of grid
q = plot(xx,-yy, varargin{:});

% Put label on
dy = 0;
if labelq==1
    text(xx+dy,-yy,['\bf' label], 'HorizontalAlignment', 'Center');
end
if nargout > 0
    hpol = q;
end
if ~hold_state
    set(gca,'dataaspectratio',[1 1 1]), axis off; set(cax,'NextPlot',next);
end
set(get(gca,'xlabel'),'visible','on')
set(get(gca,'ylabel'),'visible','on')