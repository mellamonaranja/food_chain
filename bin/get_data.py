# from typing import Any, List
# from unittest import result

# import sqlalchemy
# import hydra
# from hydra.utils import get_original_cwd, to_absolute_path
# import multiprocessing as mp
# from multiprocessing import Pool

# import pandas as pd
# from omegaconf import DictConfig
# from tqdm import tqdm
# import sys
# import traceback
# import warnings
# import definitions
# from demand_forecast.db import get_engine
# from demand_forecast.learner import learn_prophet
# from demand_forecast.utils import get_logger
import PyMySQL


warnings.filterwarnings(action="ignore")
# logger = get_logger("learner_proxy")

num_cpu = int(mp.cpu_count() * .75)

import pandas as pd
import pymysql
engine = pymysql.connect(host='172.30.1.44',
                         port=3307,
                       user='abcfood',
                       password='illunex123!',
                       db='abc_food',
                       charset='utf8')
product_get_query = 'select trans_date as ds, vendor_code, product_code from transaction_list;'
result=pd.read_sql(product_get_query, engine)
print(result)

# def get_deal_data_with_product_id(engine: sqlalchemy.engine.Engine, product_id: str) -> pd.DataFrame:
#     product_get_query = \
#         f"select trans_date as ds, sum(buy_count) as y from transaction_list where product_code = {product_id} and cancel= 0 group by trans_date;"
        
    
    # product_get_query = \
    #     f"select trans_date as ds, vendor_code, product_code from transaction_list"
    
    # return pd.read_sql(product_get_query, engine)

# def get_deal_data(engine: sqlalchemy.engine.Engine)-> pd.DataFrame:
#     product_get_query = \
#         f"select trans_date as ds, vendor_code, product_code from transaction_list"
    
#     return pd.read_sql(product_get_query, engine)


# get_deal_data(engine=sqlalchemy.engine.Engine)

# def learn_prophet_wrapper(arg):
#     print(arg)
#     args, kwargs = arg
#     print(kwargs)
#     return learn_prophet(kwargs['df_dataset'], kwargs['df_holiday'], kwargs['product_id'], kwargs['output_dir'])



# @hydra.main(config_path="config", config_name="learner_all_config")
# def main(cfg: DictConfig) -> None:
#     logger.info(cfg.db)

#     engine = get_engine(**cfg.db, pool_pre_ping=True)

#     if not engine:
#         logger.error(f"cannot create engine with config:{cfg}")
#         return -1

#     # get holiday data
#     df_holiday = pd.read_sql("select holiday as ds, holiday_desc holiday from holiday", engine)

#     # 학습할 product 리스트 가져옴
#     df_product = pd.read_sql("select product_id as product from forecast_item_list", engine)
#     learn_list = df_product["product"].tolist()
#     del df_product

#     datasets = []

#     # learn_list = learn_list[0:20]
#     for product_id in tqdm(learn_list):
#         df_dataset = get_deal_data_with_product_id(engine, product_id)
#         if df_dataset.shape[0] < 150:
#             logger.info(f"{product_id} row data too small skip it")
#             continue

#         datasets.append({
#             "df_dataset": df_dataset,
#             "df_holiday": df_holiday,
#             "product_id": product_id,
#             "output_dir": to_absolute_path(cfg.model_path)
#         })
#     engine.dispose()

#     with Pool(processes=num_cpu) as pool:
#         future_parameters = [(pool.apply_async(learn_prophet, kwds=parameters), parameters) for parameters in datasets]
#         for future, parameters in future_parameters:
#             result = future.get()
#             print(parameters, "=>", result)





# if __name__ == "__main__":
#     main()


