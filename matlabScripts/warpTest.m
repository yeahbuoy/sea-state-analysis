% Unit tests for warpImage.m
% Test files
I = imread('Crops/41001_2016_03_11_1310_2.jpg');
BW = rgb2gray(I);
data = warp(BW,BW,256);
[height, width] = size(BW);

csv = readtable('../data/CoolSpreadSheet.csv', 'Delimiter',',');

%% Test 1: Get data from warp
X = get(data, 'XData');
Y = get(data, 'YData');
Z = get(data, 'ZData');
assert(mean(Z,'all') ~= 0);

%% Test 2: Get regional max and min
max = imregionalmax(BW);
min = imregionalmin(BW);
assert(mean(max,'all') ~= mean(min,'all'));

%% Test 3: Remove non max/min values from Z data
Zmax = zeros(height, width);
Zmin = zeros(height, width);
Z = get(data, 'ZData');
for i=1:height
    for j=1:width
        if max(i,j)==1
            Zmax(i,j)=Z(i,j);
        end
        if min(i,j)==1
            Zmin(i,j)=Z(i,j);
        end
    end
end
assert(mean(Zmax,'all') ~= 0);
assert(mean(Zmin,'all') ~= 0);

%% Test 4: Read .csv
waveHeightCsv = csv{:,3};
assert(length(waveHeightCsv) > 0);