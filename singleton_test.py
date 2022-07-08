from copyreg import pickle
from distutils.command.config import config
import sqlalchemy
import hydra
from omegaconf import DictConfig
from hydra.utils import get_original_cwd, to_absolute_path
import pandas as pd 
import pickle as pkl 
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules, apriori, fpgrowth
import os.path
import os
import sys
from db import get_engine
from utils import get_logger
import warnings
from tqdm import tqdm

warnings.filterwarnings(action="ignore")
logger = get_logger("learner_proxy")

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def get_vendor_data(engine: sqlalchemy.engine.Engine, vendor_id) -> pd.DataFrame:
    product_get_query = f'SELECT trans_date, product_code AS product FROM transaction_list where vendor_code = {vendor_id};'
    result=pd.read_sql(product_get_query, engine)
    
    return result

@hydra.main(config_path="config", config_name="learner_all_config")
def main(cfg: DictConfig) -> None:
    logger.info(cfg.db)
    # logger.info(cfg.learn_product_list)

    # learn_product_list = cfg.learn_product_list
    
    engine = get_engine(**cfg.db, pool_pre_ping=True)
    if not engine:
        logger.error(f"cannot create engine with config:{cfg}")
        return -1
    print('connecting',{cfg.db})

    vendor_get_query=f'SELECT DISTINCT vendor_code FROM transaction_list;'
    vendor=pd.read_sql(vendor_get_query, engine)
    del vendor_get_query
    
    for index, row in tqdm(vendor.iterrows()):
        # print(row['vendor_code'])
        vendor_code=row['vendor_code']
        vendor_data=get_vendor_data(engine, vendor_code)
        print(vendor_data)
        preprocess(vendor_data, vendor_code, 3, cfg.output_dir)

def preprocess(vendor_data, vendor_code, input_months:int, output_dir: str)->None:

    vendor_data["ym"] = vendor_data["trans_date"].apply(lambda row : row.strftime("%Y%m"))
    # print(vendor_data)   
    
    if input_months == 3:
            input_3months = str(int(max(vendor_data["ym"]))-int(2))
            splited_months=vendor_data[vendor_data["ym"] >= input_3months]
        
    elif input_months == 6:
        input_6months = str(int(max(vendor_data["ym"]))-int(5))
        splited_months=vendor_data[vendor_data["ym"] >= input_6months]
        
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
    
    train_file_path = f'{output_dir}/{vendor_code}_model.bin'

    with open(train_file_path,'wb') as file:
        pkl.dump(trained_model, file)        

if __name__ == "__main__":
    main()