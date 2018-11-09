clc
clear all
close all

vid=videoinput('winvideo',1);

I = getsnapshot(vid);
imshow(I)
figure();
rotI_gray=rgb2gray(I);
BW = edge(rotI_gray,'canny',0.85);
imshow(BW);
figure();
[x y]= find(BW==1);
scatter(y,-x,'b*')