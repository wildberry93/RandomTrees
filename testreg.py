# -*- coding: UTF-8 -*-
import randomforestregressor

klasyfikator = randomforestregressor.RandomForestRegressor(2)
kl = klasyfikator.fit("forestfires_log.csv", "forestkl.csv")
