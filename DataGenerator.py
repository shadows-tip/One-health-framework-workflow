import numpy as np
from ModelPackage import Model
from joblib import Parallel, delayed
from Utils import lhs_sampling, get_data_column, save


def timeline_generator(intervene_measure, intervene_values):
    Ih = []
    for i, intervene_value in enumerate(intervene_values):
        model = Model(t=150, ratio=0.34)
        model.set_param(intervene_meas=intervene_measure, intervene_time=100, intervene_param=intervene_value)
        res = model.get_result(label=['Ih1', 'Ih2', 'Ih3', 'Ih4'])
        Ih.append(np.sum(res[:, 96 * 365:149 * 365], axis=0))
    Ih = np.array(Ih).T
    out = np.concatenate((np.full((len(Ih), 1), intervene_measure), np.arange(0, len(Ih)).reshape(len(Ih), 1), Ih),
                         axis=1)
    return out


def parallel_module(t, intervene_time, item, adaptive_training=False):
    scene_name, scene, intervene_meas = item
    if adaptive_training:
        dataset = {'adaptive_train_set': 100000}
    else:
        dataset = {'train_set': 6400, 'test_set': 1600}

    #  data before vaccination(99*365)、the first year(100*365)、the third year(102*365)、the fifth year(104*365)
    given_times = [(intervene_time - 1 + i) * 365 for i in [0, 1, 3, 5]]
    for dataset_key, dataset_value in dataset.items():
        print("{:s}, intervene_measure{:d}, {:s} Solving start....".format(scene_name, intervene_meas, dataset_key))
        lhs_param = lhs_sampling(n=dataset_value, param_range=[[0, 1]])
        res = np.zeros((len(lhs_param), len(given_times)))
        for i in range(len(lhs_param)):
            if i % 100 == 0 and i != 0:
                print("Combination[{:d}]-[{:d}] Solve completed".format(i - 100, i))
            param = get_param(lhs_param[i].item(), intervene_meas)
            model = Model(t, scene)
            model.set_param(intervene_meas, intervene_time, param)
            res[i] = np.sum(model.get_result(label=['Ih1', 'Ih2', 'Ih3', 'Ih4'], given_times=given_times), axis=0)
            # print(param, res[i])
        out = np.concatenate((lhs_param, res), axis=1)
        save(out, './DataFolder/DatasetFile2/' + scene_name + '/meas' + str(
            intervene_meas) + '_' + scene_name + '_' + dataset_key + '.csv',
             columns=['Coverage', 'Ih(before)', 'Ih(1th)', 'Ih(3th)', 'Ih(5th)'])


def get_param(coverage, measures):
    efficacy = {'1': [coverage, 0.99], '2': [coverage, 0.92], '3': [coverage, 0.5408], '4': [coverage, 1]}
    param = []
    for i in str(measures):
        param.extend(efficacy[i])
    return param


if __name__ == '__main__':
    '''
     1.fish vaccination: alpha; 2.chemotherapy: gamma2; 3.IEC: theta; 4.sanitation toilets: delta
    '''
    intervene_list = [[[0.6, 0.95], [0.85, 0.97], [1, 0.99]], [[0.3, 0.3], [0.5, 0.7], [0.8, 0.92]], [[0.3, 0.2], [0.5, 0.4], [0.9, 0.5408]], [[0.3, 0.5], [0.6, 0.8], [0.97, 1]]]
    intervene_measures = [1, 2, 3, 4]
    # intervene_list = [[[0.3, 0.3], [0.5, 0.7], [0.8, 0.92]],
    #                   [[0.6, 0.95, 0.3, 0.3], [0.85, 0.97, 0.5, 0.7], [1, 0.99, 0.8, 0.92]],
    #                   [[0.3, 0.3, 0.3, 0.2], [0.5, 0.7, 0.5, 0.4], [0.8, 0.92, 0.9, 0.5408]],
    #                   [[0.3, 0.3, 0.3, 0.5], [0.5, 0.7, 0.6, 0.8], [0.8, 0.92, 0.97, 1]]]
    # intervene_measures = [2, 12, 23, 24]
    OUT = []
    for m, measure in enumerate(intervene_measures):
        timeline_Out = timeline_generator(measure, intervene_list[m])
        OUT.extend(timeline_Out)
    save(OUT, './DataFolder/ResultFile/timeline_data_single_241027.csv', ['Interventions', 'day', 'min_Ih', 'med_Ih', 'max_Ih'])  # 单一干预措施
    print("timeline_data is saved!!")
    # save(OUT, './DataFolder/ResultFile/timeline_data_co.csv',
    #      ['Interventions', 'day', 'min_Ih', 'med_Ih', 'max_Ih'])  # combined
    # print("timeline_data_co is saved!!")

    Scenes = {'Scene1': 0.1, 'Scene2': 0.2, 'Scene3': 0.34, 'Scene4': 0.4, 'Scene5': 0.6, 'Scene6': 0.8}
    T = 120
    Intervene_time = 100
    Measures = [1, 2, 3, 4, 12, 13, 14, 23, 24, 34, 123, 124, 134, 234, 1234]  #  [1, 2, 3, 4, 12, 13, 14, 23, 24, 34, 123, 124, 134, 234, 1234]  # 干预措施
    Parallel_tuple = [(Scene_key, Scene, Measure) for Scene_key, Scene in Scenes.items() for Measure in Measures]
    Task = [delayed(parallel_module)(T, Intervene_time, parallel_item) for parallel_item in Parallel_tuple]
    Worker = Parallel(n_jobs=-1, backend='multiprocessing')
    Worker(Task)
