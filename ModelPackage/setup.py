def get_initial_data(ratio):
    # Human
    tNh = 5.81e4  # total population（Fusha Town in 2012）
    tnh = 1200
    Nh = [802, 215, 123, 60]  # never/seldom/often/frequent
    ph = [121, 126, 98, 59]  # never/seldom/often/frequent
    Ih_rate = [0.2995, 0.3119, 0.2426, 0.1460]
    Sh = []  # never/seldom/often/frequent
    Ih = []  # never/seldom/often/frequent
    for i in range(len(Ih_rate)):
        Sh.append(((Nh[i] - ph[i]) / (Nh[i] * tnh)) * tNh)
        Ih.append(Ih_rate[i] * tNh * ratio)
    # print("--->", Sh, Ih, sum(Sh + Ih), sum(Ih)/sum(Sh + Ih))

    # freshwater snails
    mu_s = 1 / 365
    las = mu_s * (15000 * 667 * 174 / 1279)
    Ss = (1 - 0.019) * las / mu_s
    Is = 0.019 * las / mu_s

    # freshwater fish
    Nf = 186
    iIf = 39
    mu_f = 1 / (1.58 * 365)
    laf = mu_f * 150000 * 0.8 * 100
    Sf = (Nf - iIf) / Nf * laf / mu_f
    If = iIf / Nf * laf / mu_f

    # 猫
    Nc = 11000
    Ic = 11000 * 0.3359
    Sc = Nc - Ic

    initial_values = [Sh, Ih, Sc, Ic, Ss, Is, Sf, If]
    # print(initial_values)
    return initial_values


def get_fixed_param(Sh, Ih):
    lambda_h = []
    mu_h = 1.49e-5  # natural birth and death rate of human
    mu_d = 2.10e-7  # death rate infected by C.s

    for i in range(len(Sh)):
        lambda_h.append(mu_h * Sh[i] + (mu_h + mu_d) * Ih[i])

    c = [1, 3.8859416445623345, 5.2831564986737405, 6.520557029177719]
    beta_h = [5.814167018197654e-12, c[1] * 5.814167018197654e-12, c[2] * 5.814167018197654e-12,
              c[3] * 5.814167018197654e-12]

    lambda_s = 32132
    mu_s = 1 / 365
    beta_s1 = 4.618711547548286e-09
    beta_s2 = beta_s1 * 3

    lambda_f = 3406008
    mu_f = 1 / (1.58 * 365)
    beta_f = 1.8737590827590448e-08

    lambda_c = 1.507543671232877
    mu_c = 0.05 / 365
    beta_c = 7.128695790124483e-08

    gamma1 = 0.137 / 365
    b = 0.962/365  # recovery rate of infected humans through chemotherapy
    mu_k = 0.2821
    fixed_param = [lambda_h, beta_h, mu_h, lambda_c, beta_c, mu_c, lambda_s, beta_s1, beta_s2, mu_s, lambda_f, beta_f, mu_f, mu_d,
                   gamma1, mu_k, c, b]
    return fixed_param
