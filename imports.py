import pandas as pd
import eli5
import numpy as np
from sklearn.linear_model import LinearRegression, Lasso
import re
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn import linear_model
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import AdaBoostRegressor
from scipy.stats import skew
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from pandas.core.common import flatten
from sklearn import linear_model
from sklearn.svm import SVR
from math import e
import ast
from collections import Counter
from scipy.stats import pearsonr

import math
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.options.mode.chained_assignment = None
