# A novel framework to accelerate the elimination of neglected tropical diseases

### Description
The objective of this study is to propose a novel, One Health-driven framework to guide and accelerate the elimination of NTDs.

### Environmental Dependencies
This project requires Python 3.9 or newer. Here are the main dependencies:  

numpy==1.22.0  
pyDOE2==1.3.0  
scipy==1.7.3  
joblib==1.3.1  
plotnine==0.10.1

### Usage
Executing the following code on the terminal will automatically call the propagation dynamics model to generate a dataset. During this process, a folder will be automatically created and the dataset will be automatically saved to the corresponding folder.  
```
python DataGenerator.py
 ```
After the above code execution is completed, the dataset required for machine learning will be generated. The following code will be executed at the terminal to train the machine learning model using the generated dataset. The training process is automated until the end of execution, and the trained model (. pkl file) and corresponding training results will be automatically saved to the corresponding folder. 
```
python GPTrain.py
```
Executing the following code will automatically load the machine learning model to complete parameter optimization, and similarly, the optimization results will be automatically saved to the corresponding folder.
```
python Optimization.py
```
This concludes the entire workflow. Execute two files to evaluate the machine learning model and plot the results generated throughout the workflow.
```
python MachineLearning.py
python Plot.py
```
### Quick Start
We recommend using the pycharm compiler to edit our files. We have packaged the propagation dynamics into a package so that users can quickly use the model to simulate and predict diseases according to their intervention needs. The following provides an example of how to use it, and the example code is in the test.py file.
```python
from ModelPackage import Model

# Call propagation dynamics model for testing
model = Model(T=80, Nd=40000)
model.set_param(intervene_time=50, intervene_meas=1, intervene_param=[0.6])
res = model.get_result(label=['Ih'], plot=True)
```
### Acknowledgments
Thank you to all the contributors who have improved this project in various ways!
