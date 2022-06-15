import warnings
warnings.filterwarnings(action='ignore')

from mlxtend.frequent_patterns import association_rules, apriori, fpgrowth

from mlxtend.preprocessing import TransactionEncoder
from sklearn.preprocessing import LabelEncoder
import sklearn
from sklearn.decomposition import TruncatedSVD
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns
import platform
import re
from glob import glob
from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus']= False

if platform.system() == 'Darwin':
    plt.style.use('seaborn-darkgrid')
    rc('font', family = 'AppleGothic')

