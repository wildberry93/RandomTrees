# -*- coding: UTF-8 -*-
import randomforestregressor

klasyfikator = randomforestregressor.RandomForestRegressor(2)
kl = klasyfikator.fit("Data\forestfires_log.csv", "Data\forestkl.csv")
