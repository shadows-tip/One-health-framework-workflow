% 定义符号变量
syms A lambdas us deltats d1 betas betaws foais ks

% 定义Ss
Ss = (A*(lambdas + us))/(deltats*us + lambdas*us + us^2);

% 原始表达式，使用Ss的定义
original_expr = ((Ss*d1*(Ss*d1*betas^2 + 4*betaws*foais*ks + 4*betaws*ks*us))^(1/2) + Ss*betas*d1)/(2*(d1*foais + d1*us));

% 化简表达式
simplified_expr = simplify(original_expr);

% 显示化简后的结果
disp(simplified_expr);

a = latex(simplified_expr);
