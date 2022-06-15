import pandas as pd

class DataConnector:
    
    def __init__(self):
        print('Connecting')
    
    def df_preprocess(df_list):
        df_raw = pd.concat(df_list)
        df_raw.fillna("", inplace=True)
        df_raw.rename(columns={"일자":"day","매출처":"customer","코드":"code","수량":"quantity", "단가":"price", "합계":"total", "금액":"sum", "세액":"tax", "비고":"etc"}, inplace=True)
        df_raw = df_raw[df_raw["etc"].str.contains("취소")==False]
        df_raw = df_raw[df_raw["etc"].str.contains("반품")==False]
        df_raw = df_raw[df_raw["quantity"]!=0]
        df_raw = df_raw.drop(df_raw[df_raw["day"]=="소계"].index)
        df_raw = df_raw.drop(df_raw[df_raw["day"]=="합계"].index)
        df = df_raw.copy()
        df.drop(columns=["No","규격","단위","total","tax","etc"], inplace=True)
        
        return df
