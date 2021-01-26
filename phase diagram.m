clear;clc;
mkdir('100wavefrontbk');
M = csvread('E:\±ç¦ö¸Û\ÃèÀY_virtuallab\100picture17\26.csv');
x = -1000:1:1000;
[X,Y] = meshgrid(x,x);
[theta,r] = cart2pol(X,Y);
maxr=max(max(r))*0.7;
rnew=r./maxr;
rnew(rnew>1)=nan;
thetanew=-1.*theta;
h=figure('visible','off');
hold off;
for i=10001:15000
    c = M(i-10000,:);
    % c=[1 1 1 1 1 1 1 1 1 1];
    % c=[1 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5];
    % c=[1 0.1386 0.1493 0.2575 0.8407 0.2543 0.8143 0.2435 0.9293 0.350];
    % c=[1 7 10 6 6 5 5 10 8 8];
    % c=[-285.41 0 -0.032322 0 0.018651 0 0 0 0 0.16777];
    Phi=c(1)*1+c(2)*2*rnew.*cos(thetanew)...%Piston+Tilt X
        +c(3)*2*rnew.*sin(thetanew)...%Tilt Y
        +c(4)*sqrt(6)*rnew.^2 .*cos(2.*thetanew)...Astigmatism X
        +c(5)*sqrt(3)*(2.*rnew.^2 - 1)...%Defocus
        +c(6)*sqrt(6)*rnew.^2 .* sin(2.*thetanew)...%Astigmatism Y
        +c(7)*sqrt(8)*rnew.^3 .* sin(3.*thetanew)...%Trefoil Y
        +c(8)*sqrt(8)*(3.*rnew.^3 - 2.*rnew) .* sin(thetanew)... %Coma Y
        +c(9)*sqrt(8)*(3.*rnew.^3 - 2.*rnew).*cos(thetanew)...%Coma X
        +c(10)*sqrt(8)*rnew.^3 .* cos(3.*thetanew);%Trefoil X
    %maxb = max(max(Phi));
    minb = min(min(Phi));
    rarB=Phi-minb;
    maxrarB = max(max(rarB));
    %minrarB =min(min(rarB));
    NCLevels = 255;
    Br = (rarB./maxrarB).*NCLevels;

%     [c,li]=contourf(x,x,Br,80);
%     colormap(jet(NCLevels));
%     set(li,'lineColor','no')
    imshow(Br,[min(Br(:)) max(Br(:))],'border','tight','initialmagnification','fit');
%     imshow[pic,'border','tight','initialmagnification','fit');
    set (gcf,'Position',[400,400,512,512])
    colormap(gca, gray(256))
    
    axis square;
    set(gca,'xtick',[],'ytick',[]);
%     set(gca,'box','off');
    %     f=getframe(gcf);
%     imwrite(h,['E:\±ç¦ö¸Û\ÃèÀY_virtuallab\test\',int2str(i),'.png']);
    print(h,'-dpng',['E:\±ç¦ö¸Û\ÃèÀY_virtuallab\100wavefrontbk\',int2str(i)]);
end
