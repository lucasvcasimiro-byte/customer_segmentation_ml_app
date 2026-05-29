import pandas as pd
import numpy as np

from utils import *


customer_info = load_data('customer_info.csv')
customer_basket = load_data('customer_basket.csv')

num_cols = customer_info.select_dtypes(include=[np.number]).drop('customer_id', axis=1).columns.tolist()
cat_cols = customer_info.select_dtypes(include=[object])

# das visualizacoes, todas as colunas lifetime_ tem tail para direita, porque os preco mais normal é mais perto
# do zero do que do máximo, por isso aplico log transformation antes do scaling


