from copyreg import pickle
from distutils.command.config import config
# import sqlalchemy
import hydra
from matplotlib.cbook import Grouper
from omegaconf import DictConfig
from hydra.utils import get_original_cwd, to_absolute_path
import pandas as pd 
import pickle as pkl 
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules, apriori, fpgrowth
import os.path
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from demand_forecast.db import get_engine

@hydra.main(config_path="config", config_name="learner_all_config")
def main(cfg: DictConfig) -> None:

    
    engine = get_engine(**cfg.db, pool_pre_ping=True)
    print('connecting',{cfg.db})

class Training():
    def trainer(result:pd.DataFrame,
    input_months:int,
    store_id: int,
    output_dir: str) -> None:
        result["ym"] = result["day"].apply(lambda row : row.strftime("%Y%m"))
        store=result[result['customer']==store_id]
        store=store[['customer','product','ym']]

        if input_months == 3:
            input_3months = str(int(max(result["ym"]))-int(2))
            splited_months=store[store["ym"] >= input_3months]
            
        elif input_months == 6:
            input_6months = str(int(max(result["ym"]))-int(5))
            splited_months=store[store["ym"] >= input_6months]
            
        else:
            print('input only 3 or 6')
                

        quantile_75=(splited_months['product'].value_counts()).quantile(q=0.75)
        quantile_proprecessed=splited_months[splited_months['product'].map(splited_months['product'].value_counts())>quantile_75]
        product_preprecessed=quantile_proprecessed.groupby('ym').agg(list)
    
        dataset=[]
        for c,p in product_preprecessed.iterrows():
            dataset.append(p['product'])
            
        te = TransactionEncoder()
        te_ary = te.fit(dataset).transform(dataset)
        single_dataset = pd.DataFrame(te_ary, columns=te.columns_)    
        
        frequent_itemsets = apriori(single_dataset, min_support = 0.1, max_len = 2, use_colnames=True)
            
        trained_model = association_rules(frequent_itemsets).sort_values(by=['lift'],ascending=False)

        print(f"trained_model : {trained_model}")
        
        train_file_path = f'{output_dir}/{store_id}_model.bin'

        with open(train_file_path,'wb') as file:
            pkl.dump(trained_model, file)


class Singleton(Training):
    has_inst = False
    def __new__(cls, *args, **kwargs):
        if cls.has_inst:
            raise ValueError('cannot create more objects')
        cls.has_inst = True
        print(f"super()2 : {super()}")
        return super().__new__(cls)
    
p1=Singleton()
print(p1)

class test1():
    def __init__(self):
        print("test1 init")

class test2(test1):
    def __init__(self):
        print("test2 init")
        print(f"super : {super()}")
        super().__init__()

p=test2()
print(p)

# p2=Singleton()
# print(p2)

# class Person:
#     def __new__(cls, firstname, lastname) :
#         obj= super().__new__(cls)
#         obj.firstname=firstname
#         obj.lastname=lastname
        
#         obj.fullname=f'{firstname}{lastname}'
#         return obj
    
# p=Person('joohyun','yoon')
# print(p.fullname)
# print(p.__dict__)

# _singleton = None

# class Example:
#     def __new__(cls):
#         global _singleton

#         if _singleton is None:
#             _singleton = super(Example, cls).__new__(cls)

#         return _singleton

# a = Example()
# b = Example()
# print(type(a))
# print(type(Example))