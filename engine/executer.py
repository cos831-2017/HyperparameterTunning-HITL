from keras.optimizers import SGD, Adam
from pyspark import SparkContext, SQLContext
from spark_sklearn import GridSearchCV
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from copy import deepcopy

def init_spark():
    spark_context = SparkContext.getOrCreate()
    spark_context.setLogLevel('OFF')

    return spark_context

def build_custom_model(optimizer='adam',
                       init_mode='normal',
                       batch_size=1,
                       epochs=1,
                       learn_rate=0.001,
                       momentum=0.001,
                       activation='relu',
                       n_neurons_per_layer=[12,8]):
    model = Sequential()
    
    # Add an input layer
    nNeurons = deepcopy(n_neurons_per_layer)
    model.add(Dense(nNeurons.pop(0), kernel_initializer=init_mode, input_dim=8, activation=activation))

    # Add hidden layers
    for n in nNeurons:
        model.add(Dense(n, kernel_initializer=init_mode, activation=activation))

    model.add(Dense(1, kernel_initializer=init_mode, activation='sigmoid'))

    # optimizer = SGD(lr=learn_rate, momentum=momentum)

    model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    return model

def train_model(X, y, param_grid, spark_context):
    model = KerasClassifier(build_fn=build_custom_model, verbose=0)
    grid = GridSearchCV(estimator=model, param_grid=param_grid, sc=spark_context)
    grid_result = grid.fit(X, y)
    return grid_result
