# -*- coding: utf-8 -*-
"""EyeDiseasesClassification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/mariana73154/OcularDiseasesClassification/blob/master/Src/EyeDiseasesClassification.ipynb

# Imports

* May be needed to install some modules in our python enviroment - here are some of the modules This project does need to run
"""

# uncomment the following lines if you need to install any of the modules described below
# %pip install --upgrade pip    # pip, model for package management
# %pip install tensorflow       # tensorflow, model knowed for deep learning
# %pip install seaborn          # seaborn, model for data visualization
# %pip install matplotlib       # matplotlib, model for data visualization
# %pip install opencv-python    # opencv-python, model for image processing

using_Colab = False

#if using_Colab:
  #!git clone https://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@github.com/mariana73154/OcularDiseasesClassification.git

import numpy as np                  # numpy, model for data manipulation  
import pandas as pd                 # pandas, model for data manipulation
import os, random                   # os, model for operating system
import matplotlib.pyplot as plt     # matplotlib, model for data visualization
import seaborn as sns               # seaborn, model for data visualization
import tensorflow as tf             # tensorflow, model knowed for deep learning
import keras                        # keras, model knowed for deep learning

# other keras imports
from keras.preprocessing import image   # image, model for image processing
from keras.models import Sequential     # Sequential, model for deep learning
# keras layers
from keras.layers import  Conv2D, MaxPool2D, Flatten, Dense, Dropout, BatchNormalization, Activation, GlobalAveragePooling2D, Input                               
from keras.preprocessing.image import ImageDataGenerator # ImageDataGenerator, model for image processing
from keras.applications import VGG16, InceptionResNetV2, ResNet50, Xception  # VGG16, InceptionResNetV2, RESNet model for deep learning    
from keras import regularizers                           # regularizers, model for deep learning
from keras.optimizers import Adam,RMSprop,SGD,Adamax     # Adam,RMSprop,SGD,Adamax, model for deep learning
from keras.models import Model                           # Model, model for deep learning
from keras import layers                                 # layers, model for deep learning
from keras.callbacks import ReduceLROnPlateau, EarlyStopping # ReduceLROnPlateau, EarlyStopping, model for deep learning
from keras.metrics import Precision, Recall, AUC, TruePositives, TrueNegatives, FalsePositives, FalseNegatives

"""# Problem and Data

Whit this notebook I pretend to use deep learning in order to classified diferent type of eye diseases. As of any deep learning model it needs data to train and lean from it. I´ve searched for data in sites such as the well knowed Kaggle and Google datasets. 
In this case the dataset I will use will be mainly the one from kaggle : https://www.kaggle.com/datasets/gunavenkatdoddi/eye-diseases-classification.

Dataset is stored in "Data" folder and is composed of:

* 1038 images of eyes with cataracts
* 1098 images of eyes with diabetic retinopathy
* 1007 images of eyed with glaucoma
* 1074 images of healthy eyes
"""

# count number of files in a directory
#def count_files(directory):
#    return len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])

EyeDiseases = dict()
DatasetPath = '/content/OcularDiseasesClassification/Data/dataset/' if using_Colab else './dataset/'

#for dir in os.listdir(DatasetPath):
#    print('Total number of images in the [', dir.upper() ,'] : ', count_files(DatasetPath + dir))
#    EyeDiseases.update({dir:count_files(DatasetPath + dir)} )

#print('Total number of images in the [ DATASET ] :', sum(EyeDiseases.values()))

"""The dataset has four equally distributed classes.
However, 4000 images may not be sufficient, so I will create synthetic images using data augmentation
"""

#Plot the number of images in each class using a pie chart
#plt.figure(figsize=(3,3))
#plt.pie(EyeDiseases.values(), labels=EyeDiseases.keys(), autopct='%1.1f%%', startangle=90)
#plt.title('Number of images in each class')
#plt.show()

"""# Model

## Get Data
"""

#Function to load images from the dataset folder
def get_data(path_folder):
    #Load the images from the folder "dataset" into train and test sets using ImageDataGenerator
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2,
        horizontal_flip=True,
        vertical_flip=True,
        rotation_range=20,
    )

    train_generator = train_datagen.flow_from_directory(
        path_folder,
        target_size=(512, 512),
        batch_size=32,
        class_mode='categorical',
        subset='training',
        seed=10
    )

    validation_generator = train_datagen.flow_from_directory(
        path_folder,
        target_size=(512, 512),
        batch_size=32,
        class_mode='categorical',
        subset='validation',
        seed=10
    )

    return train_generator, validation_generator

"""## Get Model"""

#Function to get model
#model_list = models list available
#model_name = model name to get
def get_model(model_list,model_name,weigths=None):

    model = model_list[model_name](weigths)

    #Summary of the model
    model.summary()

    # Compile the model
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy', Precision(), Recall(), AUC()],
    )
    return model

"""## Train Model"""

#Function to train model
#model = model to train
#train_generator = train data
#validation_generator = validation data
#epochs = number of epochs to train

def train_model(model,train_generator,validation_generator,epochs,model_name):
    #Hyperparameters
    #epochs=epochs

    #Callback
    callback = [
        tf.keras.callbacks.EarlyStopping(patience=3, monitor='val_accuracy'),
        tf.keras.callbacks.ModelCheckpoint(save_best_only=True, monitor='val_accuracy',filepath='Best_Model/'+ model_name +'.h5'),
    ]

    #Train the model
    history = model.fit(
        train_generator,
        validation_data=validation_generator,
        epochs=epochs,
        verbose=1,
        callbacks=callback,
    )

    return model, history

"""## Evaluate Model"""

#Function to evaluate model
#history = history of the model

def evaluate_model(history):

    #Plot the training and validation accuracy and loss at each epoch
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    #Plot training and validation metrics of the model
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.plot(history.history['recall'], label='Training Recall')
    plt.plot(history.history['val_recall'], label='Validation Recall')
    plt.plot(history.history['precision'], label='Training Precision')
    plt.plot(history.history['val_precision'], label='Validation Precision')
    plt.plot(history.history['auc'], label='Training AUC')
    plt.plot(history.history['val_auc'], label='Validation AUC')
    plt.title('Training and Validation Metrics')
    plt.xlabel('Epochs')
    plt.legend()

    return plt

"""## Save Model"""

#Function to save model
#model = model to save
#model_name = model name to save
#history = history of the model

def save_model(model,model_name,history):

    #Create a folder to save models if it does not exist
    if not os.path.exists('Saved_Models'):
        os.mkdir('Saved_Models')
    
    #Create a folder to save the model if it does not exist
    if not os.path.exists('Saved_Models/'+ model_name):
        os.mkdir('Saved_Models/'+ model_name)
    
    #Save the model
    model.save('Saved_Models/'+ model_name +'/'+ model_name +'.h5')

    #Save the evaluation of model
    plt = evaluate_model(history)
    plt.savefig('Saved_Models/'+ model_name +'/'+ model_name +'_evaluation.png')

    #Save the model architecture
    tf.keras.utils.plot_model(
        model,
        to_file='Saved_Models/'+ model_name +'/'+ model_name +'.png',
        show_shapes=True,
        show_layer_names=True,
    )

    #Save the model history into a csv 
    hist_df = pd.DataFrame(history.history)
    hist_csv_file = 'Saved_Models/'+ model_name +'/'+ model_name +'_history.csv'
    with open(hist_csv_file, mode='w') as f:
        hist_df.to_csv(f)


"""## Run Model"""

#Function to load Model
#model_list = models list available
#path_folder = path to load model
#model_name = model name to load
def Run_Model(model_list,path_folder,model_name, weights = None):
        #Get data
        train_generator, validation_generator = get_data(path_folder)
    
        #Get model
        model = get_model(model_list,model_name)
    
        #Train model
        model, history = train_model(model,train_generator,validation_generator,epochs=50,model_name=model_name)
    
        #Evaluate model
        evaluate_model(history)
    
        #Save model
        save_model(model,model_name,history)
    
        return model

"""## CNN """

#Function of architecture of CNN model
def CNN_model(weights=None):
    #Create a CNN model
    model = Sequential()

    #Input Layer
    Inputlayer = Input(shape=(512, 512, 3))

    # 1st Convolutional Layer
    x = Conv2D(filters=32, kernel_size=(3,3), activation='relu', padding='same')(Inputlayer)
    x = Conv2D(filters=32, kernel_size=(3,3), activation='relu', padding='same')(x)
    x = MaxPool2D(pool_size=(2,2))(x)

    # 2nd Convolutional Layer
    x = Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same')(x)
    x = Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same')(x)
    x = MaxPool2D(pool_size=(2,2))(x)

    # 3rd Convolutional Layer
    x = Conv2D(filters=128, kernel_size=(3,3), activation='relu', padding='same')(x)
    x = Conv2D(filters=128, kernel_size=(3,3), activation='relu', padding='same')(x)
    x = MaxPool2D(pool_size=(2,2))(x)

    # 4th Convolutional Layer
    x = Conv2D(filters=256, kernel_size=(3,3), activation='relu', padding='same')(x)
    x = Conv2D(filters=256, kernel_size=(3,3), activation='relu', padding='same')(x)
    x = MaxPool2D(pool_size=(2,2))(x)
    
    # Output Layer
    x = Flatten()(x)
    x = Dense(units=128, activation='relu')(x)
    x = Dropout(rate=0.2)(x)
    x = Dense(units=4, activation='softmax')(x)

    # Model
    model = Model(inputs=Inputlayer, outputs=x)
    return model

"""## VGG16"""

#Function of architecture of VGG16 model
def VGG16_model(weights=None):
    #Create a VGG16 model
    model = Sequential()

    #Input Layer
    Inputlayer = Input(shape=(512, 512, 3))
    
    # Importing VGG16 from keras API
    x=VGG16(include_top=False, weights=weights, input_shape=(512,512,3))(Inputlayer)

    # Output Layer
    x = Flatten()(x)
    x = Dense(units=128, activation='relu')(x)
    x = Dropout(rate=0.2)(x)
    x = Dense(units=4, activation='softmax')(x)

    # Model
    model = Model(inputs=Inputlayer, outputs=x)
    return model

"""## RESNet"""

#Function of architecture of RESNet model
def RESNet_model(weights=None):
    #Create a VGG16 model
    model = Sequential()

    #Input Layer
    Inputlayer = Input(shape=(512, 512, 3))

    # Importing RESNet from keras API without weights
    x=ResNet50(include_top=False, weights=weights, input_shape=(512,512,3))(Inputlayer)
    
    # Output Layer
    x = Flatten()(x)
    x = Dense(units=128, activation='relu')(x)
    x = Dropout(rate=0.2)(x)
    x = Dense(units=4, activation='softmax')(x)

    # Model
    model = Model(inputs=Inputlayer, outputs=x)
    return model

"""## Xception"""

#Function of architecture of Xception model
def Xception_model(weights=None):
    #Create a VGG16 model
    model = Sequential()

    #Input Layer
    Inputlayer = Input(shape=(512, 512, 3))

    # Importing Xception from keras API without weights
    x=Xception(include_top=False, weights=weights, input_shape=(512,512,3))(Inputlayer)
    
    # Output Layer
    x = Flatten()(x)
    x = Dense(units=128, activation='relu')(x)
    x = Dropout(rate=0.2)(x)
    x = Dense(units=4, activation='softmax')(x)

    # Model
    model = Model(inputs=Inputlayer, outputs=x)
    return model

"""## List Of Models"""

# List off available Models - defined above
model_list = { 
    "CNN_model":CNN_model , 
    "VGG16_model" : VGG16_model ,
    "RESNet_model" : RESNet_model ,
    "Xception_model" : Xception_model ,
}

"""## Run all models

### CNN
"""

Run_Model(model_list,DatasetPath,"CNN_model")

"""### VGG16"""

#Without weights
Run_Model(model_list,DatasetPath,"VGG16_model", weights = None)
#With weights
Run_Model(model_list,DatasetPath,"VGG16_model", weights = 'imagenet')

"""### RESNet"""

#Without weights
Run_Model(model_list,DatasetPath,"RESNet_model", weights = None)
#With weights
Run_Model(model_list,DatasetPath,"RESNet_model", weights = 'imagenet')

"""### Xception"""

#Without weights
Run_Model(model_list,DatasetPath,"Xception_model", weights = None)
#With weights
Run_Model(model_list,DatasetPath,"Xception_model", weights = 'imagenet')

"""## Save models in zip"""

# Save the models in a zip file -- use this in colab to download the models
#zip -r /content/saved_models.zip /content/saved_models