# -*- coding: UTF-8 -*-
import randomforestclassifier

klasyfikator = randomforestclassifier.RandomForestClassifier(2)
kl = klasyfikator.fit("nowe.txt", "nowekl.txt")
