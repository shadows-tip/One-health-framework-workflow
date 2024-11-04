import scipy.optimize as optimize

# 定义变量
nf = 186
pf = 39
nh1 = 802
ph1 = 121
nh2 = 215
ph2 = 126
nh3 = 123
ph3 = 98
nh4 = 60
ph4 = 59
nh = 1200
ph = 404
imuh = 315 / 58059 / 365
imus = 1 / 365
tN = 5.81 * 1e4  # Population in Fusha Town in 2012, treat as total population
tn = 1200
ip1 = nh1 / nh
ip2 = nh2 / nh
ip3 = nh3 / nh
ip4 = nh4 / nh
OR = 6.12
inci_cca = 1.5 / 100000 / 365
imuh_bs = inci_cca * (OR - 1)
alim = 0.001
blim = 0.037  # no snail data at the location, use a prevalence from [0.1%,3.7%]
ilah1 = imuh * tN * ip1 + imuh_bs * tN * ip1 * (ph1 / nh1)
ilah2 = imuh * tN * ip2 + imuh_bs * tN * ip2 * (ph2 / nh2)
ilah3 = imuh * tN * ip3 + imuh_bs * tN * ip3 * (ph3 / nh3)
ilah4 = imuh * tN * ip4 + imuh_bs * tN * ip4 * (ph4 / nh4)
ic2 = 8
ic3 = 22
ic4 = 332
ilas = imus * (15000 * 667 * 174 / 1279)
imuf = 1 / (1.5 * 365)
ilaf = imuf * 15000 * 0.8 * 100
igam1 = 0.14 / 365

print(ilaf)

# calculate β
def equations(vars):
    ah1, ah2, ah3, ah4, as_, af, ac = vars
    Sh1 = (nh1 - ph1) / tn * tN
    Sh2 = (nh2 - ph2) / tn * tN
    Sh3 = (nh3 - ph3) / tn * tN
    Sh4 = (nh4 - ph4) / tn * tN
    Ih1 = 121
    Ih2 = 126
    Ih3 = 98
    Ih4 = 59
    mus = imus
    muh = imuh
    muf = imuf
    muh_bs = imuh_bs
    gam1 = igam1
    las = ilas
    laf = ilaf
    Sf = (nf - pf) / nf * ilaf / muf
    If = pf / nf * ilaf / muf
    Ss = (1 - 0.019) * las / mus
    Is = 0.019 * las / mus

    Nc = 11000
    Ic = 11000 * 0.3359
    Sc = Nc - Ic
    muc = 0.05 / 365

    # beta_h1, beta_h2, beta_h3, beta_h4, beta_s, beta_f, beta_c: ah1, ah2, ah3, ah4, as_, af, ac
    f1 = ah1 * Sh1 * If - muh * Ih1 - muh_bs * Ih1 - gam1 * Ih1
    f2 = ah2 * Sh2 * If - muh * Ih2 - muh_bs * Ih2 - gam1 * Ih2
    f3 = ah3 * Sh3 * If - muh * Ih3 - muh_bs * Ih3 - gam1 * Ih3
    f4 = ah4 * Sh4 * If - muh * Ih4 - muh_bs * Ih4 - gam1 * Ih4
    f5 = as_ * Ss * (Ih1 + Ih2 + Ih3 + Ih4) + 3 * as_ * Ss * Ic - mus * Is
    f6 = af * Sf * Is - muf * If
    f7 = ac * Sc * Ic - muc * Ic - muh_bs * Ic - gam1 * Ic
    return f1, f2, f3, f4, f5, f6, f7


result = optimize.fsolve(equations, (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1))
ah1, ah2, ah3, ah4, as_, af, ac = result
print("c2 =", 58.60/15.08)
print("c3 =", 79.67/15.08)
print("c4 =", 98.33/15.08)
# c2 = 3.8859416445623345
# c3 = 5.2831564986737405
# c4 = 6.520557029177719
print("ah1 = ", ah1)
print("ah2 = ", ah1 * 58.60/15.08)
print("ah3 = ", ah1 * 79.67/15.08)
print("ah4 = ", ah1 * 98.33/15.08)
print("as_ = ", as_)
print("af = ", af)
print("ac =", ac)

# ah1 = 5.814167018197654e-12
# ah2 = 2.2593513744455076e-11
# ah3 = 3.071715426656546e-11
# ah4 = 3.791160761932197e-11
# as_ =  4.618711547548286e-09
# af =  1.873759082759045e-08
# ac = 7.128695790124483e-08


# lambda
# muc = 0.05 / 365
# Nc = 11000
# Ic = 11000 * 0.3359
# Sc = Nc - Ic
# mus = imus
# muf = imuf
# las = ilas
# Sf = (nf - pf) / nf * ilaf / muf
# If = pf / nf * ilaf / muf
# Ss = (1 - 0.019) * las / mus
# Is = 0.019 * las / mus
#
# print("lah1 = ", imuh * (802 - 121)/tn * tN + (imuh + imuh_bs) * 121/tn * tN)
# print("lah2 = ", imuh * (215 - 126)/tn * tN + (imuh + imuh_bs) * 126/tn * tN)
# print("lah3 = ", imuh * (123 - 98)/tn * tN + (imuh + imuh_bs) * 98/tn * tN)
# print("lah4 = ", imuh * (60 - 59)/tn * tN + (imuh + imuh_bs) * 59/tn * tN)
# print("lac = ", muc * Sc + (muc + imuh_bs) * Ic)
# print("las = ", imus * (Ss + Is))
# print("laf = ", imuf * (Sf + If))