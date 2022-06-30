from distutils.command.config import config
# import sqlalchemy
import hydra
from omegaconf import DictConfig
from hydra.utils import get_original_cwd, to_absolute_path
from item_recommend.db import get_engine
import pandas as pd 
import pickle as pkl 
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules, apriori, fpgrowth


@hydra.main(config_path="config", config_name="learner_all_config")
def main(cfg: DictConfig) -> None:

    
    engine = get_engine(**cfg.db, pool_pre_ping=True)
    print('connecting',{cfg.db})
    
    ## for all store 
    ## 1. get data 
    ## 2. train model 
    ## 3. save trained model 
    
    
    ## make one single trainner module  --> Trainer 
    ## 1. get data( via argument) 
    ## 2. train model 
    ## 3. save tained model 
    
    ## for all store --> Trainner wrapper
    ## generate data (getter data and pre process )
    ## call single trainnner model (data)
    
    product_get_query = 'select trans_date as day, vendor_code as customer, product_code as product from transaction_list;'
    result=pd.read_sql(product_get_query, engine)
    # print(result)
    
    return_data  = trainer_3months(result, 2313)
    print(return_data)
    
    
    
def trainer_3months(result:pd.DataFrame, 
                    store_id: int,
                    output_dir: str="./item_recommend") -> None:
    
    result["ym"] = result["day"].apply(lambda row : row.strftime("%Y%m"))
    gunsan=result[result['customer']==store_id]
    gunsan=gunsan[['customer','product','ym']]
    
    grouped_ym=gunsan.groupby('ym').agg(list)
    
    months=str(int(max(result["ym"]))-int(2))
    gunsan_3months = gunsan[gunsan["ym"] >= months]
   
   
   
    quantile_75=(gunsan_3months['product'].value_counts()).quantile(q=0.75)
    
    gunsan_proprecessed=gunsan_3months[gunsan_3months['product'].map(gunsan_3months['product'].value_counts())>quantile_75]
    gunsan_product=gunsan_proprecessed.groupby('ym').agg(list)
    
    
    
    dataset=[]
    for c,p in gunsan_product.iterrows():
        dataset.append(p['product'])
        
    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)
    gunsan_dataset = pd.DataFrame(te_ary, columns=te.columns_)    
    
    frequent_itemsets = apriori(gunsan_dataset, min_support = 0.1, max_len = None, use_colnames=True)
        
    trained_model = association_rules(frequent_itemsets)
    
    return trained_model

    train_file_path = f'{output_dir}/{store_id}_model.bin'
    
    # with open(train_file_path,'wb') as file :
    #     pkl.dump(file, trained_model)
        
    # return train_file_path
        



if __name__ == "__main__":
    main()