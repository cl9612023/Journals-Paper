clear;clc;
mkdir('100picture17');
bb=zeros(5000,10);
x = -1000:1:1000;
[X,Y] = meshgrid(x,x);
[theta,r] = cart2pol(X,Y);
maxr=max(max(r))*0.7;
rnew=r./maxr;
thetanew=-1.*theta;
rnew(rnew>1)=nan;
h=figure('visible','off');
hold off;
for i=10000:14999
    i=i+1;
    c=rand(1,10)*2-1;
%     c=[1 1 1 1 1 1 1 1 1 1];
    % c=[1 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5]
    % c=[1 0.1386 0.1493 0.2575 0.8407 0.2543 0.8143 0.2435 0.9293 0.350];
    % c=[1 7 10 6 6 5 5 10 8 8];
    Phi=c(1)*1+c(2)*2*rnew.*cos(thetanew)...%Piston+Tilt X
        +c(3)*2*rnew.*sin(thetanew)...%Tilt Y
        +c(4)*sqrt(6)*rnew.^2 .*cos(2.*thetanew)...Astigmatism X
        +c(5)*sqrt(3)*(2.*rnew.^2 - 1)...%Defocus
        +c(6)*sqrt(6)*rnew.^2 .* sin(2.*thetanew)...%Astigmatism Y
        +c(7)*sqrt(8)*rnew.^3 .* sin(3.*thetanew)...%Trefoil Y
        +c(8)*sqrt(8)*(3.*rnew.^3 - 2.*rnew) .* sin(thetanew)... %Coma Y
        +c(9)*sqrt(8)*(3.*rnew.^3 - 2.*rnew).*cos(thetanew)...%Coma X
        +c(10)*sqrt(8)*rnew.^3 .* cos(3.*thetanew);%Trefoil X
    B= 4.*cos(Phi*pi/ 2).^2;

    %maxB = max(max(B));
    minB = min(min(B));
    newB=B-minB;
    maxnewB = max(max(newB));
    %minnewB = min(min(newB));
    NCLevels = 255;
    Br = (newB /maxnewB).*NCLevels;
    %maxBr=max(max(Br));
    %minBr=min(min(Br));
    imshow(Br,[min(Br(:)) max(Br(:))],'border','tight','initialmagnification','fit');
    set (gcf,'Position',[400,400,512,512])
    colormap(gray(NCLevels));
    axis square;
    set(gca,'xtick',[],'ytick',[]);
    bb(i-10000,:)=c;
%     f=getframe(gcf);
%     imwrite(f.cdata,['E:\±ç¦ö¸Û\ÃèÀY_virtuallab\100picture\',int2str(i),'.png']);
    print('-dpng',['E:\±ç¦ö¸Û\ÃèÀY_virtuallab\100picture17\',int2str(i)]);
end
csvwrite('E:\±ç¦ö¸Û\ÃèÀY_virtuallab\100picture17\26.csv',bb)