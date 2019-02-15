function BW = otsu(imname)
% Converts an image to binary using the otsu algorithm for determining global image threshold
% imname is the name of the image we want to convert to binary
% BW is the converted image

I = imread(imname);
I=imresize(I,[272 479]);
I = rgb2gray(I);
avg = filter2(fspecial('average',7),I)/255;

% use otsu algorithm to find the threshold
level = graythresh(avg);

% convert the image to binary using the threshold
BW = imbinarize(avg, level);

% show image
imshowpair(avg, BW, 'montage')
end

