% NAVIGATE TO MATLABSCRIPTS BEFORE RUNNING THIS FILE
% otherwise the images can't be found in the path

% 'r' for rotate
% 'c' for crop
% 'd' for debug
% 'o' for otsu method
% 'x' to remove bad images
mode = 'x';

if mode=='r'
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
                fname = strcat('Crops/',extractBetween(string(name),1,length(name)-4),'_',int2str(i),'.jpg');
                imwrite(subim,fname,'jpg');
                subim=imresize(subim,[272 479]);
                BW=otsu(fname);
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
end

if mode=='c'
    path = 'Crops/*.jpg';
    pics = dir(path);
    for pic = pics'
        name = pic.name;
        fname = strcat('Crops/',name)
        J = imread(name);
        [h, w] = size(J);

        % Find lines
        BW=otsu(fname);
        BW=rgb2gray(J);
        BW=edge(BW);
        [H,T,R] = hough(BW);
        P  = houghpeaks(H,5,'threshold',ceil(0.3*max(H(:))));

        lines = houghlines(BW,T,R,P,'FillGap',40,'MinLength',200);
        max_len = 0;
        for k = 1:length(lines)
            xy = [lines(k).point1; lines(k).point2];

            % determine the endpoints of the longest line segment 
            len = norm(lines(k).point1 - lines(k).point2);
            if (len > max_len)
                max_len = len;
                xy_long = xy;
            end
        end

        J = imcrop(J,[0 xy_long(1,2) w h]);
        [Jh Jw] = size(J)
        if (Jh>100 && Jh<200)
            imshow(J)
            pause(0.5)
        end
        
        % write to file
        fname = strcat('Crops/',name);
        imwrite(J,fname,'jpg');
    end
end

if mode=='d'
    
end

if mode=='o'
    path = 'Crops/*.jpg';
    pics = dir(path);
    for pic = pics'
        name = pic.name;
        K = imread(name);
        [height, width] = size(K);

        % Find lines
        BW=otsu(strcat('Crops/',name));
        imshow(BW)
        pause(0.5)
    end
end

if mode=='x'
    del = 0;
    count = 0;
    path = 'Crops/*.jpg';
    pics = dir(path);
    for pic = pics'
        name = pic.name;
        K = imread(name);
        [height, width] = size(K);
        if (width<50 || height<50)
            delete(strcat('Crops/',name))
            del = del + 1;
        end
        count = count + 1;
    end
end