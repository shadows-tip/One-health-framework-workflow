import numpy as np
import pandas as pd
from scipy.integrate import odeint, solve_ivp
import matplotlib.pyplot as plt
from .setup import get_initial_data, get_fixed_param

class Model:
    def __init__(self, t, ratio):

        self.t = t
        # self.level = level
        Sh, Ih, Sc, Ic, Ss, Is, Sf, If = get_initial_data(ratio)  # get initial values from setup
        self.Sh = Sh
        self.Ih = Ih
        self.INI = [Sh[0], Ih[0], Sh[1], Ih[1], Sh[2], Ih[2], Sh[3], Ih[3], Sc, Ic, Ss, Is, Sf, If]
        self.param = None
        self.intervene_time = None
        self.intervene_meas = None
        self.RES = None

    def set_param(self, intervene_meas: int = None, intervene_time=None, intervene_param=None):
        '''

        :param intervene_meas: intervention measures, int
        :param intervene_time: intervention time, unit:year
        :param intervene_param: intervention values, correspond to intervene_meas
        '''

        if intervene_time is not None and intervene_meas is not None:
            self.intervene_time = intervene_time - 1
            self.intervene_meas = str(intervene_meas)
        intervene_param = self.assign_param(intervene_param)
        self.param = (get_fixed_param(self.Sh, self.Ih), intervene_param, self.intervene_time, self.intervene_meas)

    def assign_param(self, intervene_param):
        '''
        1.fish vaccination: alpha; 2.chemotherapy: gamma2; 3.IEC: theta; 4.sanitation toilets: delta
        gamma2 = - np.log(1 - Cm * S * Ag(Cm) * h) / Tg
        '''
        alpha, gamma2, theta, delta = 0, 0, 0, 0
        S = 0.636  # diagnostic sensitivity
        Tg = 1  # gap of chemotherapy
        if intervene_param is not None:
            if len(intervene_param) == 2 * len(self.intervene_meas):
                intervene_param = list(map(lambda x, y: [x, y], intervene_param[::2], intervene_param[1::2]))
            for i in range(len(self.intervene_meas)):
                if self.intervene_meas[i] == '1':
                    alpha = np.prod(intervene_param[i])
                elif self.intervene_meas[i] == '2':
                    gamma2 = - np.log(1 - np.prod(intervene_param[i]) * S * intervene_param[i][0]) / Tg
                elif self.intervene_meas[i] == '3':
                    theta = np.prod(intervene_param[i])
                elif self.intervene_meas[i] == '4':
                    delta = np.prod(intervene_param[i])
        # print([alpha, gamma2, theta, delta])
        return [alpha, gamma2, theta, delta]

    @staticmethod
    def ode_func(t, x, *param):

        fixed_param, intervene_param, intervene_time, intervene_meas = param
        '''
        1.fish vaccination: alpha; 2.chemotherapy: gamma2; 3.IEC: theta; 4.sanitation toilets: delta
        '''
        lambda_h, beta_h, mu_h, lambda_c, beta_c, mu_c, lambda_s, beta_s1, beta_s2, mu_s, lambda_f, beta_f, mu_f, mu_d, gamma1, mu_k, c, b = fixed_param
        alpha, gamma2, theta, delta = 0, 0, 0, 0
        if intervene_meas is not None:
            if len(str(intervene_meas)) > 1:
                if int(t / 365) >= intervene_time:  # intervene_time <= int(t / 365) <= intervene_time + 2 // int(t / 365) >= intervene_time
                    if 30 < t % 365 <= 90:
                        alpha, gamma2, theta, delta = intervene_param
                    else:
                        alpha, theta, delta = intervene_param[0], intervene_param[2], intervene_param[3]
                # elif int(t / 365) > intervene_time + 2:
                #     alpha, theta, delta = intervene_param[0], intervene_param[2], intervene_param[3]
                else:
                    alpha, gamma2, theta, delta = 0, 0, 0, 0
            elif len(str(intervene_meas)) == 1:
                if int(t / 365) >= intervene_time:  # int(t / 365) >= intervene_time
                    if 30 < t % 365 <= 90:
                        alpha, gamma2, theta, delta = intervene_param
                    else:
                        alpha, theta, delta = intervene_param[0], intervene_param[2], intervene_param[3]
                else:
                    alpha, gamma2, theta, delta = 0, 0, 0, 0


        # print(alpha, gamma2, theta, delta)

        # initial values, the order is same as self.INI
        Sh1, Ih1, Sh2, Ih2, Sh3, Ih3, Sh4, Ih4, Sc, Ic, Ss, Is, Sf, If = x

        dSh1 = lambda_h[0] - (1 - theta) * beta_h[0] * Sh1 * If - mu_h * Sh1 + (gamma1 * (1 - gamma2) + b * gamma2) * Ih1
        dIh1 = (1 - theta) * beta_h[0] * Sh1 * If - mu_h * Ih1 - mu_d * Ih1 - (gamma1 * (1 - gamma2) + b * gamma2) * Ih1

        dSh2 = lambda_h[1] - (1 - theta) * beta_h[1] * Sh2 * If - mu_h * Sh2 + (gamma1 * (1 - gamma2) + b * gamma2) * Ih2
        dIh2 = (1 - theta) * beta_h[1] * Sh2 * If - mu_h * Ih2 - mu_d * Ih2 - (gamma1 * (1 - gamma2) + b * gamma2) * Ih2

        dSh3 = lambda_h[2] - (1 - theta) * beta_h[2] * Sh3 * If - mu_h * Sh3 + (gamma1 * (1 - gamma2) + b * gamma2) * Ih3
        dIh3 = (1 - theta) * beta_h[2] * Sh3 * If - mu_h * Ih3 - mu_d * Ih3 - (gamma1 * (1 - gamma2) + b * gamma2) * Ih3

        dSh4 = lambda_h[3] - (1 - theta) * beta_h[3] * Sh4 * If - mu_h * Sh4 + (gamma1 * (1 - gamma2) + b * gamma2) * Ih4
        dIh4 = (1 - theta) * beta_h[3] * Sh4 * If - mu_h * Ih4 - mu_d * Ih4 - (gamma1 * (1 - gamma2) + b * gamma2) * Ih4

        dSc = lambda_c - beta_c * Sc * If - mu_c * Sc + gamma1 * Ic
        dIc = beta_c * Sc * If - (mu_c + mu_d) * Ic - gamma1 * Ic

        dSs = lambda_s - (1 - delta) * beta_s1 * Ss * sum([Ih1, Ih2, Ih3, Ih4]) - beta_s2 * Ss * Ic - mu_s * Ss
        dIs = (1 - delta) * beta_s1 * Ss * sum([Ih1, Ih2, Ih3, Ih4]) + beta_s2 * Ss * Ic - mu_s * Is
        dSf = lambda_f - (1 - alpha) * beta_f * Sf * Is - mu_f * Sf - mu_k * Sf
        dIf = (1 - alpha) * beta_f * Sf * Is - mu_f * If - mu_k * If

        return [dSh1, dIh1, dSh2, dIh2, dSh3, dIh3, dSh4, dIh4, dSc, dIc, dSs, dIs, dSf, dIf]

    def ode_solver(self):
        t = self.t * 365
        t_eval = [i for i in range(t)]
        self.RES = solve_ivp(fun=self.ode_func, t_span=[0, t], y0=self.INI, t_eval=t_eval, args=self.param)
        # return self.RES

    def redirect_index(self, out_label):
        index_dict = pd.Series(
            {'Sh1': 0, 'Ih1': 1, 'Sh2': 2, 'Ih2': 3, 'Sh3': 4, 'Ih3': 5, 'Sh4': 6, 'Ih4': 7, 'Sc': 8, 'Ic': 9, 'Ss': 10,
             'Is': 11, 'Sf': 12, 'If': 13})
        # index_dict = pd.Series({'Sh': 0, 'Ih': 1, 'Ss': 2, 'Is': 3, 'Sf': 4, 'If': 5})
        out = self.RES.y[index_dict[out_label].to_list(), :]
        return out

    def turn_count_mode(self, res):
        if res.ndim == 1:
            res = res.reshape(1, -1)
        # print(res.shape)
        res = list(map(lambda x: np.sum(x, axis=1).tolist(), np.hsplit(res, self.t)))
        return np.array(res).T

    def get_result(self, label=None, given_times=None, plot=False):
        self.ode_solver()  # resolve
        # get result according to label
        if label is None:
            label = ['Sh1', 'Ih1', 'Sh2', 'Ih2', 'Sh3', 'Ih3', 'Sh4', 'Ih4', 'Sc', 'Ic', 'Ss', 'Is', 'Sf', 'If']
        out = self.redirect_index(label)
        if given_times is not None:
            out = np.squeeze(out[:, given_times])
        if plot:
            self.plot(out, label)
        return out

    def plot(self, out, out_label):
        plt.figure(figsize=(8, 4), dpi=200)
        if out.ndim == 1:
            out = out.reshape(1, -1)
        period = 'day' if out.shape[1] == self.t * 365 else 'year'
        for i in range(len(out_label)):
            plt.plot(out[i], label=out_label[i])
            for j, num in enumerate(out[i]):
                print("-{:s}room, {:d}{:s}, number of rooms:{:d}".format(out_label[i], j + 1, period, int(num)))
        plt.title('SimulationModel', fontsize=10)
        # plt.grid(linestyle='--', alpha=0.3)
        plt.legend(fontsize=8)
        plt.xlabel('Time(years)' if out.shape[1] == self.t else 'Time(days)', fontsize=9)
        plt.ylabel('Number', fontsize=9)
        plt.show()
