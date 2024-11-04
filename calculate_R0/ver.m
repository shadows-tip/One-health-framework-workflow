syms betas Ss Is betaws Ws us foais ks d1 betash Sh betawsh gammah Iah sigmah uh Ich
eq1 = betas*Ss*Is + betaws*Ss*Ws;
eq2 = ks*Is;
eq3 = betash*Sh*Is + betawsh*Sh*Ws;
eq4 = 0;
J1 = jacobian([eq1,eq2,eq3,eq4], [Is,Ws,Iah,Ich]);
eq5 = (us + foais)*Is;
eq6 = d1*Ws;
eq7 = (gammah + sigmah + uh)*Iah;
eq8 = uh*Ich - sigmah*Iah;
J2 = jacobian([eq5,eq6,eq7,eq8], [Is,Ws,Iah,Ich]);
R0 = J1*inv(J2);
[V,D] = eig(R0);
diag(D)

