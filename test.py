# -*- coding: UTF-8 -*-
import randomforestclassifier

klasyfikator = randomforestclassifier.RandomForestClassifier(2)
kl = klasyfikator.fit("Data\nowe.txt", "Data\nowekl.txt")
