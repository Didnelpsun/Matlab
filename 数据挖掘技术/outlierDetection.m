clc;clear;
num = xlsread("data\catering_sale.xls");
sales=num(1:end, 1);
rows=size(sales, 1);
% 异常值检查
% 箱图上下界
q_ = prctile(sales, [25, 75]) ;
p25=q_ (1, 1);
p75=q_ (1, 2);
upper = p75+1.5* (p75-p25);
lower = p25-1.5* (p75-p25);
upper_indexes = sales(sales>upper);
lower_indexes = sales(sales<lower) ;
indexes =[upper_indexes; lower_indexes];
indexes = sort(indexes);
% 箱图绘制
figure;
hold on;
boxplot(sales, 'whisker', 1.5 ,'outliersize' , 6) ;
rows = size(indexes, 1);
flag =0;
for i =1:rows
    if flag ==0
        text(1+0.01, indexes(i, 1), num2str(indexes(i, 1)));
        flag=1;
    else
        text(1-0.017*length(num2str(indexes(i, 1))), indexes(i, 1), num2str(indexes(i, 1)));
        flag=0;
    end
end
hold off;
disp('餐饮销量数据缺失值异常值检查完成!');