T = readtable('../data/CoolSpreadSheet.csv', 'Delimiter',',');

path = 'Crops/*.jpg';
pics = dir(path);
n=0;
wh = [];
whcsv = [];
for pic = pics'
    name = pic.name;
    %figure
    I = imread(name);
    %imshow(I)
    BW = rgb2gray(I);
    BW = imgaussfilt(BW,8);
    regmax = imregionalmax(BW);
    regmin = imregionalmin(BW);
    [height, width] = size(BW);

    % Display surface
    %figure
    h = warp(BW,BW,256);
    Xcoords = get(h, 'XData');
    Ycoords = get(h, 'YData');
    Zcoords = get(h, 'ZData');
    
    Zmax = zeros(height, width);
    Zmin = zeros(height, width);
    for i=1:height
        for j=1:width
            if regmax(i,j)==1
                Zmax(i,j)=Zcoords(i,j);
            end
            if regmin(i,j)==1
                Zmin(i,j)=Zcoords(i,j);
            end
        end
    end
    
    avgMax = mean(nonzeros(Zmax));
    avgMin = mean(nonzeros(Zmin));
    
    waveHeight = avgMax-avgMin;
    
    fname = strcat(extractBetween(string(name),1,length(name)-6),'.jpg');
    for row=1:size(T,1)
        if T{row,1}==fname
            waveHeightCsv = T{row,3};
        end
    end
    
    wh(end+1) = waveHeight;
    whcsv(end+1)= waveHeight/waveHeightCsv;
    ratio = waveHeight/waveHeightCsv;
    
%     figure
%     warp(BW, regmax)
%     figure
%     warp(BW, regmin)

%     method = 'linear';
%     extrap = 'none';
%     S = scatteredInterpolant(Xcoords,Ycoords,Zcoords,method,extrap);

    n=n+1;
    
    if n>1000
        scatter(wh, whcsv);
        break
    end
end