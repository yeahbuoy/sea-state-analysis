clear;
clc;

I=imread('ship7.png');
I=imresize(I,[272 479]);
figure, imshow(I, 'Border', 'tight')
%PSF = fspecial('gaussian',60,10);
%edgesTapered = edgetaper(I,PSF);
BW=rgb2gray(I);
%BW=imadjust(BW,[0.0 1],[]);
%BW=rangefilt(BW);
BW=edge(BW);
figure, imshow(BW, 'Border', 'tight')


      [H,T,R] = hough(BW);
      %imshow(H,[],'XData',T,'YData',R,'InitialMagnification','fit');
      %xlabel('\theta'), ylabel('\rho');
      %axis on, axis normal, hold on;
      P  = houghpeaks(H,5,'threshold',ceil(0.3*max(H(:))));
      %x = T(P(:,2)); 
      %y = R(P(:,1));
      %plot(x,y,'s','color','white');

      % Find lines and plot them
      lines = houghlines(BW,T,R,P,'FillGap',40,'MinLength',200);
      figure, imshow(I, 'Border', 'tight'), hold on
      max_len = 0;
      for k = 1:length(lines)
        xy = [lines(k).point1; lines(k).point2];
        %plot(xy(:,1),xy(:,2),'LineWidth',2,'Color','green');

        % plot beginnings and ends of lines
        %plot(xy(1,1),xy(1,2),'x','LineWidth',2,'Color','yellow');
        %plot(xy(2,1),xy(2,2),'x','LineWidth',2,'Color','red');

        % determine the endpoints of the longest line segment 
        len = norm(lines(k).point1 - lines(k).point2);
        if ( len > max_len)
          max_len = len;
          xy_long = xy;
          plot(xy(:,1),xy(:,2),'LineWidth',2,'Color','green');
          plot(xy(1,1),xy(1,2),'x','LineWidth',2,'Color','yellow');
          plot(xy(2,1),xy(2,2),'x','LineWidth',2,'Color','red');
        end
      end
       
        %xy_long(1,1)
        %xy_long(1,2)
        %xy_long(2,1)
        %xy_long(2,2)
      xLength = xy_long(2,1) - xy_long(1,1);
      yLength = xy_long(1,2) - xy_long(2,2);
    
      theta = atan(yLength/xLength);
      theta=rad2deg(theta);
      text(250,125,[sprintf('%1.3f',theta),'{\circ}'],'Color','y','FontSize',14,'FontWeight','bold');
     
      J=imRotateCrop(I, -theta);
      K=imresize(J,[272 479]);
     
      figure, imshow(K, 'Border', 'tight')
      % highlight the longest line segment
      %plot(xy_long(:,1),xy_long(:,2),'LineWidth',2,'Color','cyan');
     
