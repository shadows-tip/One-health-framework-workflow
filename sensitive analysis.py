import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import spearmanr
from scipy.stats.qmc import LatinHypercube


# function of calculate R0
def compute_R0(lambda_h, beta_f, lambda_f, lambda_s, beta_c, beta_s2, lambda_c, mu_c, mu_f, mu_s, gamma1, gamma_c, mu_h,
               beta_h1, beta_s1, c):
    R0 = ((beta_f * lambda_f * lambda_s * beta_c * beta_s2 * lambda_c / (
                mu_c * mu_f ** 2 * mu_s ** 2 * (gamma_c + mu_c))) +
          (beta_f * lambda_f * lambda_s * beta_h1 * beta_s1 * (
                  c[0] * lambda_h[0] + c[1] * lambda_h[1] + c[2] * lambda_h[2] + c[3] * lambda_h[3]
          ) / (mu_h * mu_f ** 2 * mu_s ** 2 * (gamma1 + mu_h)))) ** (1 / 3)
    return R0


# 全局敏感性分析函数
def global_sensitivity_analysis(compute_R0, param_ranges, num_samples, lambda_h, c, mu_f, mu_s):
    # LHS
    sampler = LatinHypercube(len(param_ranges))
    sample = sampler.random(num_samples)
    params_samples = []
    for i, (low, high) in enumerate(param_ranges):
        scaled_samples = low + (high - low) * sample[:, i]
        params_samples.append(scaled_samples)

    params_samples = np.array(params_samples).T  # shape: (num_samples, num_params)

    # calculate R0
    R0_values = []
    for i in range(num_samples):
        params = params_samples[i]
        beta_f, lambda_f, lambda_s, beta_c, beta_s1, beta_s2, lambda_c, mu_c, gamma1, mu_h, gamma_c, beta_h1 = params[
                                                                                                            :-len(
                                                                                                                lambda_h)]
        lambda_h = params[-len(lambda_h):]

        # fixed mu_f and mu_s
        R0 = compute_R0(lambda_h, beta_f, lambda_f, lambda_s, beta_c, beta_s2, lambda_c, mu_c, mu_f, mu_s, gamma1,
                        mu_h, gamma_c, beta_h1, beta_s1, c)
        R0_values.append(R0)

    R0_values = np.array(R0_values)

    # calculate mean and standard error of R0
    R0_mean = np.mean(R0_values)
    R0_std = np.std(R0_values)

    return params_samples, R0_values, R0_mean, R0_std


# Local sensitivity analysis function
def local_sensitivity_analysis(compute_R0, params_values, lambda_h, c):
    # define symbolic variables
    beta_f, lambda_f, lambda_s, beta_c, beta_s2, lambda_c, mu_c, mu_f, mu_s, gamma1, gamma_c, mu_h, beta_h1, beta_s1 = sp.symbols(
        'beta_f lambda_f lambda_s beta_c beta_s2 lambda_c mu_c mu_f mu_s gamma1 gamma_c mu_h beta_h1 beta_s1')
    lambda_h_syms = sp.symbols('lambda_h0 lambda_h1 lambda_h2 lambda_h3')
    c_syms = sp.symbols('c0 c1 c2 c3')

    # calculate R0
    R0_sym = ((beta_f * lambda_f * lambda_s * beta_c * beta_s2 * lambda_c / (
                mu_c * mu_f ** 2 * mu_s ** 2 * (gamma_c + mu_c))) +
              (beta_f * lambda_f * lambda_s * beta_h1 * beta_s1 * (
                      c_syms[0] * lambda_h_syms[0] + c_syms[1] * lambda_h_syms[1] + c_syms[2] * lambda_h_syms[2] +
                      c_syms[3] * lambda_h_syms[3]
              ) / (mu_h * mu_f ** 2 * mu_s ** 2 * (gamma1 + mu_h)))) ** (1 / 3)

    # labels
    all_params = [beta_f, lambda_f, lambda_s, beta_c, beta_s2, lambda_c, mu_c, mu_f, mu_s, gamma1, gamma_c, mu_h, beta_h1,
                  beta_s1, *lambda_h_syms]

    # calculate derivative of each parameter for R0
    dydx = [sp.diff(R0_sym, param) for param in all_params]

    # optim values
    param_vals = [params_values['beta_f'], params_values['lambda_f'], params_values['lambda_s'],
                  params_values['beta_c'],
                  params_values['beta_s2'], params_values['lambda_c'], params_values['mu_c'], params_values['mu_f'],
                  params_values['mu_s'], params_values['gamma1'], params_values['gamma_c'], params_values['mu_h'],
                  params_values['beta_h1'], params_values['beta_s1']] + lambda_h

    # calculate R0
    dydx_eval = [float(dydxi.subs(dict(zip(all_params, param_vals))).evalf()) for dydxi in dydx]
    R0_eval = compute_R0(lambda_h, **params_values, c=c)

    # Local sensitivity index
    indx = np.array(dydx_eval) * param_vals / R0_eval

    return indx, dydx_eval


# PRCC 计算函数
def calculate_prcc(params_df, selected_params):
    prcc_values = []
    for param in selected_params:
        correlation, _ = spearmanr(params_df[param], params_df['R0'])
        prcc_values.append(correlation)

    return np.array(prcc_values)


# PRCC
def plot_prcc(prcc_values, selected_params, param_symbols):
    plt.figure(figsize=(12, 6))
    plt.barh(selected_params, prcc_values, color='skyblue')
    plt.axvline(0, color='gray', linestyle='--')
    plt.yticks(range(len(selected_params)), [param_symbols[param] for param in selected_params])

    #plt.title('Partial rank correlation coefficients of R0', fontsize=18)
    plt.xlabel('PRCC', fontsize=20)
    plt.ylabel('Parameters', fontsize=20)
    plt.xlim(-1, 1)
    plt.grid(axis='x')
    plt.show()


# range of parameters
param_ranges = [
                   (1e-10, 1e-5),  # beta_f
                   (1e6, 1e7),  # lambda_f
                   (1e2, 1e5),  # lambda_s
                   (1e-10, 1e-6),  # beta_c
                   (1e-10, 1e-8),  # beta_s1
                   (1e-12, 1e-8),  # beta_s2
                   (1e-3, 1),  # lambda_c
                   (1e-10, 1e-2),  # mu_c
                   (1e-10, 1e-2),  # gamma1
                   (1e-10, 1e-2),  # gamma_c
                   (1e-7, 1e-5),  # mu_h
                   (1e-15, 1e-10),  # beta_h1
               ] + [(1e-3, 1e0)] * 4  # lambda_h

# example
params_values = {
    'beta_f': 1.8737590827590448e-08,
    'lambda_f': 3406008,
    'lambda_s': 32132,
    'mu_f': 1 / (1.58 * 365),
    'mu_s': 1 / 365,
    'beta_c': 7.128695790124483e-08,
    'beta_s1': 4.618711547548286e-09,
    'beta_s2': 4.618711547548286e-09 * 3,
    'lambda_c': 1.507543671232877,
    'mu_c': 0.05 / 365,
    'gamma1': 0.137 / 365,
    'gamma_c': 0.137 / 365,
    'mu_h': 1.49e-5,
    'beta_h1': 5.814167018197654e-12,
}
lambda_h = [0.1, 0.2, 0.3, 0.4]
c = [1, 3.8859416445623345, 5.2831564986737405, 6.520557029177719]

# global
num_samples = 5000
mu_f = params_values['mu_f']
mu_s = params_values['mu_s']
params_samples, R0_values, R0_mean, R0_std = global_sensitivity_analysis(compute_R0, param_ranges, num_samples,
                                                                         lambda_h, c, mu_f, mu_s)

# DataFrame
params_names = ['beta_f', 'lambda_f', 'lambda_s', 'beta_c', 'beta_s1', 'beta_s2',
                'lambda_c', 'mu_c', 'gamma1', 'gamma_c', 'mu_h', 'beta_h1'] + [f'lambda_h{i + 1}' for i in
                                                                            range(len(lambda_h))]
params_df = pd.DataFrame(params_samples, columns=params_names)
params_df['R0'] = R0_values

# calculate PRCC
selected_params = ['beta_f', 'lambda_f', 'lambda_s', 'beta_c', 'beta_s1', 'beta_s2',
                   'lambda_c', 'mu_c', 'gamma1', 'gamma_c', 'mu_h', 'beta_h1'] + [f'lambda_h{i + 1}' for i in range(4)]
prcc_values = calculate_prcc(params_df, selected_params)

# parameters label
param_symbols = {
    'beta_f': r'$\beta_f$',
    'lambda_f': r'$\lambda_f$',
    'lambda_s': r'$\lambda_s$',
    'beta_c': r'$\beta_c$',
    'beta_s1': r'$\beta_{s1}$',
    'beta_s2': r'$\beta_{s2}$',
    'lambda_c': r'$\lambda_c$',
    'mu_c': r'$\mu_c$',
    'gamma1': r'$\gamma_1$',
    'gamma_c': r'$\gamma_c$',
    'mu_h': r'$\mu_h$',
    'beta_h1': r'$\beta_{h,1}$',
    'lambda_h1': r'$\lambda_{h,1}$',
    'lambda_h2': r'$\lambda_{h,2}$',
    'lambda_h3': r'$\lambda_{h,3}$',
    'lambda_h4': r'$\lambda_{h,4}$',
}

# PRCC plot
plot_prcc(prcc_values, selected_params, param_symbols)

# Local sensitivity analysis
indx, dydx_eval = local_sensitivity_analysis(compute_R0, params_values, lambda_h, c)
print("Local sensitivity index:", indx)
