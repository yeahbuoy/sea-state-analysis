% NAVIGATE TO MATLABSCRIPTS BEFORE RUNNING THIS FILE
% otherwise the images can't be found in the path

path = '../data/Pictures/*.jpg';
pics = dir(path);
for pic = pics'
    name = pic.name;
    I = imread(name);
    [height, width] = size(I);
    I = imcrop(I, [0 0 width 270]);
       
    for i=0:5
        subim = imcrop(I, [i*480 0 480 height]);
        %imshow(subim)
        if (median(subim,'all')>50)
%             fname = strcat('../../matlabScripts/Crops/',extractBetween(string(name),1,length(name)-4),'_',int2str(i),'.jpg');
%             imwrite(subim,fname,'jpg');
            subim=imresize(subim,[272 479]);
            BW=rgb2gray(subim);
            BW=edge(BW);           
            [H,T,R] = hough(BW);
            P  = houghpeaks(H,5,'threshold',ceil(0.3*max(H(:))));

            % Find lines and plot them
            lines = houghlines(BW,T,R,P,'FillGap',40,'MinLength',200);
            max_len = 0;
            for k = 1:length(lines)
                xy = [lines(k).point1; lines(k).point2];

                % determine the endpoints of the longest line segment 
                len = norm(lines(k).point1 - lines(k).point2);
                if ( len > max_len)
                    max_len = len;
                    xy_long = xy;
                end
            end
            xLength = xy_long(2,1) - xy_long(1,1);
            yLength = xy_long(1,2) - xy_long(2,2);

            theta = atan(yLength/xLength);
            theta=rad2deg(theta);
            text(250,125,[sprintf('%1.3f',theta),'{\circ}'],'Color','y','FontSize',14,'FontWeight','bold');

            J=imRotateCrop(subim, -theta);
            K=imresize(J,[272 479]);
            imshow(K)
            pause(0.5)
        end
    end
end