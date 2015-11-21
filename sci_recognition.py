from sklearn import svm
import os
import numpy as np
from PIL import Image



class Reco:

    img_size = (16, 16)
    training_data = []
    training_target = []

    def load_training_data(self,folder):
        files = os.listdir(folder)
        images = []
        for f in files:
            img = Image.open(folder + '/' + f)
            img = img.resize(self.img_size, Image.BILINEAR)
            images.append(np.array(img.getdata()).flatten())

        return images


    def load_all(self,folder, targetvalue):
        data = self.load_training_data(folder)
        for i in range(0, len(data)):
            self.training_target.append(targetvalue)
        self.training_data.extend(data)


    def __init__(self):
        self.load_all('training_data_high/background', -1)
        self.load_all('training_data_high/albastru', 0)
        self.load_all('training_data_high/rosu', 1)
        self.load_all('training_data_high/verde', 2)
        self.load_all('training_data_high/galben', 3)
        self.load_all('training_data_high/roz', 4)
        self.load_all('training_data_high/brown', 5)
        self.load_all('training_data_high/laser', 6)
        self.load_all('training_data_high/boom', 7)


        self.np_train_data = np.asarray(self.training_data)
        self.np_train_target = np.asarray(self.training_target)
        print self.np_train_data
        print self.np_train_target

        self.clf = svm.SVC(gamma=0.001, C=100.0, kernel='linear')

        img = Image.open('training_data_high/bad.png')
        img = img.resize(self.img_size, Image.BILINEAR)


    def predict(self,img):
        resized_image = img.resize(self.img_size,Image.BILINEAR)
        data = np.array(resized_image.getdata()).flatten()
        return int(self.clf.predict(data)[0])

    def train(self):
        self.clf.fit(self.np_train_data,self.np_train_target)