% Initialization
f = pwd;
chf = 0; chnf = 0;
fwind = dir(fullfile(f,'*WIND*.csv'));
fwave = dir(fullfile(f,'*WAVE*.csv'));
d = dir(fullfile(f,'41001*.jpg'));
nd = length(d); 
ncpsi = 480; % #columns per subimage
nrvp  = 270; % #valid pixel rows (not footer)
iBlank = false(nd,1);
% Read CSV spreadsheets
delimiter = ',';
startRow = 2;
formatSpec = '%q%f%f%f%f%*s%*s%*s%*s%*s%*s%[^\n\r]';
fileID = fopen(fwind.name,'r');
windArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'TextType', 'string', 'EmptyValue', NaN, 'HeaderLines' ,startRow-1, 'ReturnOnError', false, 'EndOfLine', '\r\n');
datestr = windArray{1}; 
windDnum = datenum(datestr,'mm/dd/yyyy HHMM');
knotsPerMps = 1.94384;
windspeed = windArray{2}*knotsPerMps; 
windspeed10 = windArray{3}*knotsPerMps; 
windspeed20 = windArray{4}*knotsPerMps; 
formatSpec = '%s%f%f%f%f%f%*s%*s%*s%*s%*s%*s%*s%[^\n\r]';
fileID = fopen(fwave.name,'r');
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'TextType', 'string', 'EmptyValue', NaN, 'HeaderLines' ,startRow-1, 'ReturnOnError', false, 'EndOfLine', '\r\n');
datestr = dataArray{1}; 
waveDnum = datenum(datestr,'mm/dd/yyyy HHMM');
signWaveHeight = dataArray{4}; 
windWaveHeight = dataArray{5}; 
aimgDnum = zeros(nd,1);
% Import image files and separate into 6 subimages
for i = 1:nd % For each image
    I = imread(d(i).name);
    if all(I(1:10,1:10,:)<6) % Blank image; skip
        iBlank(i) = true;
    end
    aimgDnum(i) = datenum(d(i).name(7:end-4),'yyyy_mm_dd_HHMM');
end                                             
iValid = find(~iBlank);
nvi = length(iValid); % #valid images
vimgDnum = aimgDnum(iValid);
% for i = 1:nvi
%     idxWave(i) = find(vimgDnum(i) == waveDnum);
%     idxWind(i) = find(vimgDnum(i) == windDnum);
%     if isempty(idxWave) || isempty(idxWind)
%         error('Can''t find datenum');
%     end
% end
J = cell(nvi,6); S = J;
for i = 1:nvi % For each Valid Image
    s = d(iValid(i)).name;
    I = imread(s);
    for j = 1:6 % For each subimage (of 6)
        J{i,j} = I(1:nrvp,((j-1)*ncpsi+1):(j*ncpsi),:);
        K = rgb2gray(J{i,j});
        %[BW1,tc] = edge(K,'Canny');
        [BW,tp] = edge(K,'Prewitt');
        % Compute the Hough transform of the binary image returned by edge to detect lines
        [H,T,R] = hough(BW);
        imshow(H,[],'XData',T,'YData',R,'InitialMagnification','fit');
        xlabel('\theta'), ylabel('\rho');
        axis on, axis normal, hold on;
        % Find the peaks in the Hough transform matrix, H, using the houghpeaks function.
    	P  = houghpeaks(H,5,'threshold',ceil(0.3*max(H(:))));
    	% Superimpose a plot on the image of the transform that identifies the peaks.
    	x = T(P(:,2)); y = R(P(:,1));
    	%plot(x,y,'s','color','white');
    	% Find lines in the image using the houghlines function.
    	lines = houghlines(BW,T,R,P,'FillGap',5,'MinLength',7);
    	% Create a plot that displays the original image with the lines superimposed on it.
    	figure, imshow(K), hold on
    	max_len = 0;
    	for k = 1:length(lines)
        	xy = [lines(k).point1; lines(k).point2];
        	plot(xy(:,1),xy(:,2),'LineWidth',2,'Color','green');
        	% Plot beginnings and ends of lines
        	plot(xy(1,1),xy(1,2),'x','LineWidth',2,'Color','yellow');
        	plot(xy(2,1),xy(2,2),'x','LineWidth',2,'Color','red');
        	% Determine the endpoints of the longest line segment
        	len = norm(lines(k).point1 - lines(k).point2);
        	if ( len > max_len)
            	max_len = len;
            	xy_long = xy;
        	end
    	end
    	%highlight the longest line segment
   	plot(xy_long(:,1),xy_long(:,2),'LineWidth',2,'Color','red');
	J{i,7} = strrep(s(7:end-4),'_','/');
	end
end

