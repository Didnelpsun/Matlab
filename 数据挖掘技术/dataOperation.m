clc;
clear;
X = xlsread('data\normaliz_data.xls');
X;
[Y,PS] = mapminmax(X);
Y;
X=mapminmax('reverse',Y,PS);
X;
clc;
clear;


data = xlsread('data\discretization_data.xls');
% 分为4类
k = 4;
min = min(data);
max = max(data);
section = (max-min)/k;
variable = min;
rules = zeros(1,k+1);
for i=1:k+1
    rules(i) = variable;
    variable = variable + section;
end
rules;
clear i min max section variable;
rows = size(data,1);
width_data = zeros(k, rows);
for i=1:k
    vardata = data(find(data(1:end,1)>=rules(i)&data(1:end,1)<rules(i+1)));
    if(i==k)
        vardata = [vardata;data([find(data(1:end) == rules(i+1))])];
    end
    for j=1:size(vardata)
        width_data(i,j) = vardata(j);
    end
end
clear i j vardata;
sort_data = sort(data);
row = floor(rows/k);
if(row*k==rows)
    frequancy_data = [k, row];
else
    row = row + 1;
    frequancy_data = [k, row];
end
for i=1:k
    for j=1:row
        if((i-1)*row+j<=rows)
            frequancy_data(i,j) = sort_data((i-1)*row+j);
        end
    end
end
clear i j row sort_data rows rules;
X11 = width_data(1, find(width_data(1,:)));
X12 = width_data(2, find(width_data(2,:)));
X13 = width_data(3, find(width_data(3,:)));
X14 = width_data(4, find(width_data(4,:)));
X21 = frequancy_data(1, find(frequancy_data(1,:)));
X22 = frequancy_data(2, find(frequancy_data(2,:)));
X23 = frequancy_data(3, find(frequancy_data(3,:)));
X24 = frequancy_data(4, find(frequancy_data(4,:)));
Y11 = ones(size(find(width_data(1,:)))) * 1;
Y12 = ones(size(find(width_data(2,:)))) * 2;
Y13 = ones(size(find(width_data(3,:)))) * 3;
Y14 = ones(size(find(width_data(4,:)))) * 4;
Y21 = ones(size(find(frequancy_data(1,:)))) * 1;
Y22 = ones(size(find(frequancy_data(2,:)))) * 2;
Y23 = ones(size(find(frequancy_data(3,:)))) * 3;
Y24 = ones(size(find(frequancy_data(4,:)))) * 4;
subplot(1,2,1);
plot(X11,Y11, 'or');
hold on;
plot(X12,Y12, 'og');
hold on;
plot(X13,Y13, 'ob');
hold on;
plot(X14,Y14, 'om');
title("等宽离散化");
subplot(1,2,2);
plot(X21,Y21, 'or');
hold on;
plot(X22,Y22, 'og');
hold on;
plot(X23,Y23, 'ob');
hold on;
plot(X24,Y24, 'om');
title("等频离散化");
clc;
clear;
