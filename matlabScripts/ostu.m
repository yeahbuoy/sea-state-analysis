function BW = ostu(imname)
% Converts an image to binary using the ostu algorithm for determining global image threshold
% imname is the name of the image we want to convert to binary
% BW is the converted image

I = imread(imname);
I=imresize(I,[272 479]);
I = rgb2gray(I);
avg = filter2(fspecial('average',7),I)/255;

% use oshu algorithm to find the threshold
level = graythresh(avg);

% convert the image to binary using the threshold
BW = imbinarize(avg, level);

% show image
imshowpair(avg, BW, 'montage')
end

