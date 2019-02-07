% Created by:   Casey Fernandez
% Date:         Feb 7, 2019
% Description:	Script to detect the height of the waves in an image. Used
%               to help determine Beaufort scale number.

clear;
clc;

run waveAngle

% edge detection on grayscale image
BW = rgb2gray(K);
BW = edge(BW);
[height, width, dim] = size(BW);

% find straight lines
lines = houghlines(BW,T,R,P,'FillGap',5,'MinLength',7);
%figure, imshow(BW), hold on
max_len = 0;
for k = 1:length(lines)
   xy = [lines(k).point1; lines(k).point2];
   %plot(xy(:,1),xy(:,2),'LineWidth',2,'Color','green');

   % Plot beginnings and ends of lines
   %plot(xy(1,1),xy(1,2),'x','LineWidth',2,'Color','yellow');
   %plot(xy(2,1),xy(2,2),'x','LineWidth',2,'Color','red');

   % Determine the endpoints of the longest line segment
   len = norm(lines(k).point1 - lines(k).point2);
   if ( len > max_len)
      max_len = len;
      xy_long = xy;
   end
end

% crop the image to the horizon
BW = imcrop(BW, [0 xy_long(1,2) width height]);

% dilate the edges
se90 = strel('line', 3, 90);
se0 = strel('line', 3, 0);
BWdil = imdilate(BW, [se90 se0]);

% fill the edges
figure(10)
BWdfill = imfill(BWdil, 'holes');

% remove "islands"
BW2 = bwareaopen(BWdfill, 500);
imshow(BW2, 'Border', 'tight');

% % find peaks
% hold on
% rowSum = sum(1-BW2, 1);
% plot(rowSum)
% 
% % plot peaks
% [peaks, locations, widths, prominences] = findpeaks(smooth(rowSum));
% isPeak = prominences > 50; 
% nPeaks = sum(isPeak);
% plot(locations(isPeak), peaks(isPeak), 'r*');
% hold off

% ----------------------------------------------------------------------- %

% Gaussian Filter stuff
% I=rgb2gray(K); % convert the image to grey 
% A = fft2(double(I)); % compute FFT of the grey image
% A1=fftshift(A); % frequency scaling
% % Gaussian Filter Response Calculation
% [M N]=size(A); % image size
% R=10; % filter size parameter 
% X=0:N-1;
% Y=0:M-1;
% [X Y]=meshgrid(X,Y);
% Cx=0.5*N;
% Cy=0.5*M;
% Lo=exp(-((X-Cx).^2+(Y-Cy).^2)./(2*R).^2);
% Hi=1-Lo; % High pass filter=1-low pass filter
% % Filtered image=ifft(filter response*fft(original image))
% J=A1.*Lo;
% J1=ifftshift(J);
% B1=ifft2(J1);
% K=A1.*Hi;
% K1=ifftshift(K);
% B2=ifft2(K1);
% %----visualizing the results----------------------------------------------
% figure(1)
% imshow(I);colormap gray
% title('original image','fontsize',14)
% figure(2)
% imshow(abs(A1),[-12 300000]), colormap gray
% title('fft of original image','fontsize',14)
% figure(3)
% imshow(abs(B1),[12 290]), colormap gray
% title('low pass filtered image','fontsize',14)
% figure(4)
% imshow(abs(B2),[12 290]), colormap gray
% title('High pass filtered image','fontsize',14)
% figure(5)
%    mesh(X,Y,Lo)
%    axis([ 0 N 0 M 0 1])
%    h=gca; 
%    get(h,'FontSize') 
%    set(h,'FontSize',14)
%    title('Gaussiab LPF H(f)','fontsize',14)
%    
% figure(6)
%    mesh(X,Y,Hi)
%    axis([ 0 N 0 M 0 1])
%    h=gca; 
%    get(h,'FontSize') 
%    set(h,'FontSize',14)
%    title('Gaussian HPF H(f)','fontsize',14)
