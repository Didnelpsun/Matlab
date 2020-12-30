clear;clc;
x = [] ;
slide = 10000;
for i = 1:slide-1
    value = i / slide;
    x = [x, value];
end
clear i value;
y = - ( x .* log2(x) + (1-x) .* log2(1-x));
plot(x,y);
title("信息熵");
