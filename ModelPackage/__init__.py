import os
from .SimulationModel import *

__all__ = ["Model"]

folder_path = "./DataFolder"
if not os.path.exists(folder_path):
    os.mkdir(folder_path)

data_path = "./DataFolder/DatasetFile"
if not os.path.exists(data_path):
    os.mkdir(data_path)
model_path = "./DataFolder/ModelFile"
if not os.path.exists(model_path):
    os.mkdir(model_path)
result_path = "./DataFolder/ResultFile"
if not os.path.exists(result_path):
    os.mkdir(result_path)
figure_path = "./DataFolder/FigureFile"
if not os.path.exists(figure_path):
    os.mkdir(figure_path)

scenes = ['Scene1', 'Scene2', 'Scene3', 'Scene4', 'Scene5', 'Scene6']
paths = [folder + "/" + scene for folder in [data_path, model_path, result_path] for scene in scenes]
for path in paths:
    if not os.path.exists(path):
        os.mkdir(path)

