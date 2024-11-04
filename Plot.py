import numpy as np
import time
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
from plotnine import *
import warnings
from Utils import save
from sklearn.metrics import r2_score
from ModelPackage import Model
from itertools import cycle

warnings.filterwarnings("ignore")


# GP plot
def plot_single_sample_curve(y_pre, y_true, y_std):
    i = np.random.randint(0, len(y_true))

    x = np.linspace(0, y_true.shape[1], y_true.shape[1])
    plt.plot(x, y_true[i, :], label="true values")
    plt.plot(x, y_pre[i, :], label="predict values", linestyle='--', color='orange')
    plt.fill_between(x, y_pre[i, :] - y_std[i, :] * 1.96, y_pre[i, :] + y_std[i, :] * 1.96,
                     label="95% confidence interval", interpolate=True, facecolor='blue', alpha=0.1)
    plt.title("sample[" + str(i) + "]-GPRResult")
    plt.xlabel("Times(year)")
    plt.ylabel("population")
    plt.legend()
    plt.show()


def plot_scatter(y_pre, y_true):
    for p in range(y_pre.shape[1]):
        plt.rcParams.update({'font.size': 11})
        fig, ax = plt.subplots()
        axis_line = np.linspace(*ax.get_xlim(), 2)
        ax.plot(axis_line, axis_line, transform=ax.transAxes, linestyle='--', linewidth=2, color='black',
                label="1:1 Line")
        plt.xlabel("True value", fontsize=12)
        plt.ylabel("Predicted value", fontsize=12)
        plt.scatter(y_true[:, p], y_pre[:, p], c='orange', s=100, alpha=0.3, marker='o', edgecolors='red')
        plt.show()


def plot_scatter_boxplot(true_data, pre_data, cv_score, time_score, meas):
    titles = ["One year follow-up", "Three year follow-up", "Five year follow-up"]
    position = [[0.252, .22, .055, .27], [0.58, .22, .055, .27], [0.908, .22, .055, .27]]
    config = {
        "font.family": "serif",
        "font.serif": ["Arial"],
        "font.size": 14,
        "axes.unicode_minus": False
    }
    matplotlib.rcParams.update(config)
    fig = plt.figure(figsize=(12, 5))
    for i in range(3):
        X, Y = true_data[:, i], pre_data[:, i]
        ax1 = fig.add_subplot(1, 3, i + 1)

        axis_line = np.linspace(*ax1.get_xlim(), 2)
        ax1.plot(axis_line, axis_line, transform=ax1.transAxes, linestyle='--', linewidth=1, color='black')
        ax1.scatter(X, Y, c="w", s=200, edgecolors='k')
        # plt.xlim(xmax=800)
        # plt.ylim(ymax=800)
        # plt.xticks(np.linspace(int(ax1.get_xlim()[0]) if ax1.get_xlim()[0] > 0 else 0, ax1.get_xlim()[1], 5))
        # plt.yticks(np.linspace(ax1.get_ylim()[0], ax1.get_ylim()[1], 5))

        # ax1.text(ax1.get_xlim()[0], ax1.get_ylim()[1], 'R²=' + str(round(time_score[i], 4)), fontsize=16, ha='left',
        #          va='top')

        if i == 0:
            plt.text(x=0, y=1800, s='R²=' + str(round(time_score[i], 4)), fontsize=16)
        elif i == 1:
            plt.text(x=0, y=1800, s='R²=' + str(round(time_score[i], 4)), fontsize=16)
        else:
            plt.text(x=0, y=1800, s='R²=' + str(round(time_score[i], 4)), fontsize=16)
        print(ax1.get_ylim())
        plt.xlabel("True value", fontdict={'family': "Arial", 'size': 16})
        plt.ylabel("Predicted value", fontdict={'family': "Arial", 'size': 16})
        plt.title(titles[i])

        sub_axes = plt.axes(position[i])
        sub_axes.boxplot(cv_score[:, i], widths=0.6, showcaps=False,
                         medianprops={'color': 'k'})  # whiskerprops={'linestyle': ""}
        sub_axes.scatter(x=[1], y=[time_score[i]], marker='D', c='k', edgecolors='k', s=50)
        # sub_axes.set(ylabel="r2")  # title="boxplot"
        # print(cv_score[0:5])
        # print(np.arange(round(np.min(cv_score[0:5]), 4), 0.9999, 0.0001))
        # plt.yticks(np.arange(round(np.min(cv_score[0:5]), 4), round(np.max(cv_score[0:5]), 4), 0.0001))
        sub_axes.xaxis.set_visible(False)
        sub_axes.yaxis.set_visible(False)
        plt.ylabel("R²")

        plt.setp(sub_axes)
    fig.suptitle('GP fit result(Measure' + meas + ' Scene1)', fontsize=20)
    fig.tight_layout()
    plt.savefig('./DataFolder/FigureFile2/GP-fit-adaptive-result(Meas' + meas + ' , Scene1).png', dpi=500)
    # plt.show()


def plot_gp_result():
    measures = [1, 2, 3, 4, 12, 13, 14, 23, 24, 34, 123, 124, 234, 1234]
    for meas in measures:
        m = str(meas)
        true_data = pd.read_csv("DataFolder/DatasetFile2/Scene1/meas" + m + "_Scene1_test_set.csv").values[:, 2:]
        pred_data = pd.read_csv("DataFolder/ResultFile2/Scene1/m" + m + "_GP_predict.csv").values[:, [1, 2, 3]]
        cv_score = pd.read_csv("DataFolder/ResultFile2/Scene1/m" + m + "_GP_cv_res.csv").values[:, 4:]
       plot_scatter_boxplot(true_data, pred_data, cv_score[0:5], cv_score[5].reshape(-1), m)


# time-line plot
def plot_timeline(plot_data):
    # plot_data = plot_data[plot_data['Interventions'] < 100]

    plot_data['Interventions'].replace(
        {1: 'Fish vaccination', 2: 'Chemotherapy', 3: 'IEC', 4: 'Sanitation toilets',
         12: 'Fish vaccination + Chemotherapy',
         13: 'Fish vaccination + IEC',
         14: 'Fish vaccination + Sanitation toilets',
         23: 'Chemotherapy + IEC',
         24: 'Chemotherapy + Sanitation toilets',
         123: 'Fish vaccination + Chemotherapy + IEC',
         124: 'Fish vaccination + Chemotherapy + Sanitation toilets',
         234: 'Chemotherapy + IEC + Sanitation toilets',
         1234: 'Fish vaccination + Chemotherapy + IEC + Sanitation toilets', None: '2'},
        inplace=True)
    human_df = plot_data[['Interventions', 'day', 'min_Ih', 'med_Ih', 'max_Ih']]

    print(human_df.head())
    human_plot = (
            ggplot(human_df, aes(x='day', y='med_Ih', ymin='min_Ih', ymax='max_Ih', fill='Interventions'))
            + geom_line()
            + geom_ribbon(alpha=0.5)
            + theme_bw()
            # + theme(panel_grid=element_blank())
            + theme_matplotlib()
            + labs(x="Months", y="Number of infected people", linetype='Interventions'))

    ggsave(plot=human_plot, filename='./DataFolder/FigureFile/human_timeline.png', dpi=500)
    print(human_plot)


# optimization plot
def plot_optim_figure(plot_data):
    # low_colors = ("#d0d1e6", "#c7e9b4", "#9ecae1")"#B6C5B2" "#e3e9db"  #FFF0F5  #AEB7C6 #92A3B3 #E5E6C4  #A2B8C6  #D3E2EF #AEB7C6
    # high_colors = ("#3792BF", "#6CC3B9", "#0D539C")"#7D8B72" "#b2bfa1"  #8B8386  #536C8A #1A4669 #D2D489  #3F7291  #8C6BB1  #536C8A
    low_colors = (
        "#558ebe", "#c7e9b4", "#3792bf", "#afa6d0", "#558ebe", "#c7e9b4", "#3792bf", "#9ecae1", "#c7e9b4", "#A88FC8")
    high_colors = (
        "#2e54a1", "#6cc3b9", "#3f7291", "#8c6bb1", "#2e54a1", "#6cc3b9", "#3f7291", "#3792bf", "#6cc3b9", "#907dac")
    intervene_titles = ["Fish vaccination", "Chemotherapy", "IEC", "Sanitation toilets"]
    combination_titles = ["Fish vaccination(Efficacy=0.8) + Chemotherapy",
                          "Fish vaccination(Efficacy=0.8) + IEC",
                          "Fish vaccination(Efficacy=0.8) + Sanitation toilets",
                          "Fish vaccination(Efficacy=0.8) + Chemotherapy(Coverage=0.8, Efficacy=0.92) + IEC",
                          "Fish vaccination(Efficacy=0.8) + Chemotherapy(Coverage=0.8, Efficacy=0.92) + Sanitation toilets",
                          "Fish vaccination(Efficacy=0.8) + Chemotherapy(Coverage=0.8, Efficacy=0.92) + IEC(Coverage=0.9, Efficacy=0.5408) + Sanitation toilets"]
    titles = intervene_titles + combination_titles
    years_titles = [", One year follow-up", ", Three year follow-up", ", Five year follow-up"]

    for i, measure in enumerate(pd.unique(plot_data.interv_measure)):
        for t, year in enumerate(pd.unique(plot_data.year)):

            def process_subtitle(x, *arg):
                item, meas = arg
                if str(x) == 'nan':
                    out = str(x)
                else:
                    if len(str(meas)) == 1:
                        out = titles[i] + '(Efficacy=' + str(x) + ")"
                    else:
                        temp = x.split('/')
                        out = intervene_titles[int(str(measure)[-1]) - 1] + "(Coverage=" + temp[-2] + ", Efficacy=" + \
                              temp[-1] + ")"

                return out

            df = plot_data[(plot_data.interv_measure == measure) & (data.year == year)]
            df.scene = df.scene.apply(lambda x: str(x) if str(x) == 'nan' else 'Scene' + str(int(x)))
            # df.efficacy = df.efficacy.apply(lambda x: str(x) if str(x) == 'nan' else 'Efficacy' + str(x))
            df.efficacy = df.efficacy.apply(process_subtitle, args=(i, measure))
            df['object_value'] = pd.Categorical(-df['object_value'])
            df['object_value'] = df['object_value'].apply(lambda x: int(-x))
            # single interventions：intervene_titles[i] + years_titles[t]；combined interventions：combination_titles[i] + years_titles[t]
            plt.gca().axes.xaxis.set_visible(False)

            args = (df, low_colors[i], high_colors[i], measure, year, titles[i] + years_titles[t])
            plot_tile(args)


def plot_optim_figure2(plot_data):
    # low_colors = ("#d0d1e6", "#c7e9b4", "#9ecae1")"#B6C5B2" "#e3e9db"  #FFF0F5  #AEB7C6 #92A3B3 #E5E6C4  #A2B8C6  #D3E2EF #AEB7C6
    # high_colors = ("#3792BF", "#6CC3B9", "#0D539C")"#7D8B72" "#b2bfa1"  #8B8386  #536C8A #1A4669 #D2D489  #3F7291  #8C6BB1  #536C8A
    low_colors = (
        "#2171B5", "#2171B5", "#2171B5", "#2171B5", "#F5F5F5", "#F5F5F5", "#F5F5F5", "#9E9AC8", "#9E9AC8", "#9E9AC8",
        "#78C679", "#78C679", "#78C679", "#78C679")
    high_colors = (
        "#0D539C", "#0D539C", "#0D539C", "#0D539C", "#01665E", "#01665E", "#01665E", "#3F007D", "#3F007D", "#3F007D",
        "#004529", "#004529", "#004529", "#004529")
    intervene_titles = ["Fish vaccination(Efficacy=0.8)", "Chemotherapy(Efficacy=0.92)", "IEC(Efficacy=0.5408)",
                        "Sanitation toilets(Efficacy=1)"]
    combination_titles = ["Fish vaccination(Efficacy=0.8) + Chemotherapy(Efficacy=0.92)",
                          "Fish vaccination(Efficacy=0.8) + IEC(Efficacy=0.5408)",
                          "Fish vaccination(Efficacy=0.8) + Sanitation toilets(Efficacy=1)",
                          "Chemotherapy(Efficacy=0.92) + IEC(Efficacy=0.5408)",
                          "Chemotherapy(Efficacy=0.92) + Sanitation toilets(Efficacy=1)",
                          "IEC(Efficacy=0.5408) + Sanitation toilets(Efficacy=1)",
                          "Fish vaccination(Efficacy=0.8) + Chemotherapy(Efficacy=0.92) + IEC(Efficacy=0.5408)",
                          "Fish vaccination(Efficacy=0.8) + Chemotherapy(Efficacy=0.92) + Sanitation toilets(Efficacy=1)",
                          "Chemotherapy(Efficacy=0.92) + IEC(Efficacy=0.5408) + Sanitation toilets(Efficacy=1)",
                          "Fish vaccination(Efficacy=0.8) + Chemotherapy(Efficacy=0.92) + \n IEC(Efficacy=0.5408) + Sanitation toilets(Efficacy=1)"]
    titles = combination_titles  # intervene_titles + combination_titles
    years_titles = ["One year's intervention", "Three years' intervention", "Five years' intervention"]
    interv_measure = [12, 13, 14, 23, 24, 34, 123, 124, 234, 1234]

    for i, measure in enumerate(interv_measure):
        def process_subtitle(x):
            out = ""
            if x == 1:
                out = years_titles[0]
            elif x == 3:
                out = years_titles[1]
            elif x == 5:
                out = years_titles[2]
            return out

        df = plot_data[(plot_data.interv_measure == measure)]
        df.scene = df.scene.apply(lambda x: str(x) if str(x) == 'nan' else 'Scene' + str(int(x)))
        df.year = df.year.apply(process_subtitle)
        print(df.head())
        df['object_value'] = pd.Categorical(-df['object_value'])
        df['object_value'] = df['object_value'].apply(lambda x: int(-x))
        # single interventions：intervene_titles[i] + years_titles[t]；combined interventions：combination_titles[i] + years_titles[t]
        plt.gca().axes.xaxis.set_visible(False)
        year = 0
        args = (df, low_colors[i], high_colors[i], measure, year, titles[i])
        plot_tile(args)


def plot_tile(args):
    df, low_color, high_color, measure, year, title = args
    opt_param_ranges = (0, 1)
    if df['min_coverage'].isnull().all():
        df['min_coverage'] = -1
    base_plot = (
            ggplot(df, aes(x='scene', y='object_value', fill='min_coverage'))
            + geom_tile()
            + theme_bw(base_size=11.5)
            + theme(panel_grid_major=element_blank(), panel_grid_minor=element_blank())
            + scale_fill_gradient2(low=low_color, mid="white", high=high_color, na_value="white",
                                   limits=opt_param_ranges, midpoint=-1)

            + facet_wrap('~year', scales='free_x', nrow=1)
            # + theme(subplots_adjust={'wspace': 0.02})  # 设置各分图的间距
            + labs(x="Transmission level", y="Target Health Goal", fill="Minimum Coverage", title=title)
            + guides(fill=guide_colourbar(title_position='left'))
            + theme(legend_text=element_text(va='bottom', ha='left'),
                    legend_title=element_text(angle=90, va='bottom', ha='right'))
            + theme(panel_background=element_rect(fill='white'))
            + theme(strip_background=element_rect(fill="white"))
    )
    if len(str(measure)) == 1:
        width = 18
    else:
        width = 12
    ggsave(plot=base_plot, filename='./DataFolder/FigureFile2/optim_m_' + str(measure) + '_t_' + str(int(year)) + '.png',
           dpi=500, width=width, height=4)


# y_pred = pd.read_csv("./DataFile/GP_predict.csv").values
# y_pred_std = pd.read_csv("./DataFile/GP_predict_std.csv").values
# plot_scatter(y_pred)

# plot_single_sample_curve(y_pred, y_pred_std)
# data = pd.read_csv("./DataFolder/ResultFile/Optimization_num_multi_eff_Res.csv")

# data = pd.read_csv("./DataFolder/ResultFile2/Optim1009.csv")
# plot_optim_figure2(data)

# plot_gp_result()  # GP


time_line_data = pd.read_csv("./DataFolder/ResultFile/timeline_data_com_241018.csv")
plot_timeline(time_line_data)

# time_line_data = time_line_data[time_line_data[:, 0] == 2]
# time_line_data[:, 0] = 0
# time_line_data_co = pd.read_csv("./DataFolder/ResultFile/timeline_data_co.csv").values
# time_line_data_merge = np.concatenate((time_line_data, time_line_data_co), axis=0)
# time_line_data_merge = pd.DataFrame(time_line_data_merge,
#                                     columns=['interv_measure', 'day', 'min_Ih', 'med_Ih', 'max_Ih'])
# time_line_data_merge.to_csv("./DataFolder/ResultFile/time_line_data_merge.csv", index=False)
#
# print(time_line_data_merge.shape)
# print(time_line_data_co.shape)

# time_line_data_merge = pd.read_csv("./DataFolder/ResultFile/time_line_data_merge.csv")
# plot_timeline(pd.DataFrame(time_line_data_merge))
