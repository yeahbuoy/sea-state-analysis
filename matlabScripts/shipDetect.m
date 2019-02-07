clear;
clc;


I=imread('ship4.png');
%imshow(I)
%hold on

%Filter image
J=imgaussfilt(I,0.4);
K=rangefilt(J);
L=rgb2gray(K);
M=ordfilt2(L,25,true(5));



%Resize to square
I2=imresize(M,[512 512]);

%break into blocks
S = qtdecomp(I2, 0.2);
blocks = repmat(uint8(0),size(S));
for dim = [512 256 128 64 32 16 8 4 2 1];
      numblocks = length(find(S==dim)); 
      if (numblocks > 0)
          values = repmat(uint8(1),[dim dim numblocks]);
          values(2:dim,2:dim,:) = 0;
          blocks = qtsetblk(blocks,S,dim,values);
      end
end
  
blocks(end,1:end) = 1;
blocks(1:end,end) = 1;

%Determine ratios of blocks
S1=find(S==1);
S1=numel(S1);
S2=find(S==2);
S2=numel(S2);
S4=find(S==4);
S4=numel(S4);
S8=find(S==8);
S8=numel(S8);
S16=find(S==16);
S16=numel(S16);
S32=find(S==32);
S32=numel(S32);
S64=find(S==64);
S64=numel(S64);
S128=find(S==2);
S128=numel(S128);
S256=find(S==256);
S256=numel(S256);
S512=find(S==512);
S512=numel(S512);
ratS=S1/(S1+S2+S4+S8+S16+S32+S64+S128+S256+S512)

%Compare and determine if ship
figure
imshow(blocks,[])
%Resize to square
I=imresize(I,[512 512]);
imshowpair(I,blocks,'montage')
if (ratS >= 0.092)
text(550,75,[sprintf('SHIP DETECTED')],'Color','y','FontSize',14,'FontWeight','bold');
else
text(550,75,[sprintf('NO SHIP DETECTED')],'Color','y','FontSize',14,'FontWeight','bold');    
end

