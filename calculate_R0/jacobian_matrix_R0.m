syms beta_h1 beta_h2 beta_h3 beta_h4 beta_c beta_s1 beta_s2 beta_f Sh1 Sh2 Sh3 Sh4
syms Sc Ss Sf If Ic Is mu_h mu_d mu_c mu_s mu_f mu_k gamma1 Ih1 Ih2 Ih3 Ih4 
eq1 = beta_h1 * Sh1 * If;
eq2 = beta_h2 * Sh2 * If;
eq3 = beta_h3 * Sh3 * If;
eq4 = beta_h4 * Sh4 * If;
eq5 = beta_c * Sc * If;
eq6 = beta_s1 * Ss * sum([Ih1, Ih2, Ih3, Ih4]) + beta_s2 * Ss * Ic;
eq7 = beta_f * Sf * Is;
J1 = jacobian([eq1,eq2,eq3,eq4,eq5,eq6,eq7], [Ih1,Ih2,Ih3,Ih4,Ic,Is,If]);
eq8 = -(- mu_h * Ih1 - mu_d * Ih1 - gamma1 * Ih1);
eq9 = -(- mu_h * Ih2 - mu_d * Ih2 - gamma1 * Ih2);
eq10 = -(- mu_h * Ih3 - mu_d * Ih3 - gamma1 * Ih3);
eq11 = -(- mu_h * Ih4 - mu_d * Ih4 - gamma1 * Ih4);
eq12 = -(- (mu_c + mu_d) * Ic - gamma1 * Ic);
eq13 = -(- mu_s * Is);
eq14 = -(- mu_f * If - mu_k * If);
J2 = jacobian([eq8,eq9,eq10,eq11,eq12,eq13,eq14], [Ih1,Ih2,Ih3,Ih4,Ic,Is,If]);
R0 = J1*inv(J2);
[V,D] = eig(R0);
diag(D)

%%%% R0 = ((Sc*Sf*Ss*beta_c*beta_f*beta_s2*gamma1 + Sf*Sh1*Ss*beta_f*beta_h1*beta_s1*gamma1 + Sc*Sf*Ss*beta_c*beta_f*beta_s2*mu_d + Sc*Sf*Ss*beta_c*beta_f*beta_s2*mu_h + Sf*Sh1*Ss*beta_f*beta_h1*beta_s1*mu_c + Sf*Sh1*Ss*beta_f*beta_h1*beta_s1*mu_d + Sf*Sh2*Ss*beta_f*beta_h1*beta_s1*c2*gamma1 + Sf*Sh3*Ss*beta_f*beta_h1*beta_s1*c3*gamma1 + Sf*Sh4*Ss*beta_f*beta_h1*beta_s1*c4*gamma1 + Sf*Sh2*Ss*beta_f*beta_h1*beta_s1*c2*mu_c + Sf*Sh2*Ss*beta_f*beta_h1*beta_s1*c2*mu_d + Sf*Sh3*Ss*beta_f*beta_h1*beta_s1*c3*mu_c + Sf*Sh3*Ss*beta_f*beta_h1*beta_s1*c3*mu_d + Sf*Sh4*Ss*beta_f*beta_h1*beta_s1*c4*mu_c + Sf*Sh4*Ss*beta_f*beta_h1*beta_s1*c4*mu_d)/(gamma1^2*mu_f*mu_s + gamma1^2*mu_k*mu_s + mu_d^2*mu_f*mu_s + mu_d^2*mu_k*mu_s + gamma1*mu_c*mu_f*mu_s + 2*gamma1*mu_d*mu_f*mu_s + gamma1*mu_c*mu_k*mu_s + gamma1*mu_f*mu_h*mu_s + 2*gamma1*mu_d*mu_k*mu_s + gamma1*mu_h*mu_k*mu_s + mu_c*mu_d*mu_f*mu_s + mu_c*mu_f*mu_h*mu_s + mu_c*mu_d*mu_k*mu_s + mu_d*mu_f*mu_h*mu_s + mu_c*mu_h*mu_k*mu_s + mu_d*mu_h*mu_k*mu_s))^(1/3)
 
