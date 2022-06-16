import pandas as pd 

class DataConnector:
    
    def __init__(self, files):
        
        """
        Importing the dataset.
        Define the data type for preprocessing easily later.
        Put all the data into the dataframe.
        """
        
        print('Connecting')        
        self.df = pd.DataFrame()
        
        for file in files:
            df_raw = pd.read_excel(file,dtype={'일자':str,'매출처':str,'코드':str,'수량': float,'합계': float})
            self.df=pd.concat([self.df, df_raw])
            
    
    def df_preprocess(self):
        
        """
        Preprocess the dataset to available for any algorythm.
        """
        
        df_raw = self.df
        df_raw.fillna("", inplace=True)
        df_raw = df_raw[df_raw["비고"].str.contains("취소")==False]
        df_raw = df_raw[df_raw["비고"].str.contains("반품")==False]
        df_raw.drop(columns=["No","품목명","규격","원산지","단위","단가","금액","세액","비고"], inplace=True)
        df_raw.rename(columns={"일자":"day","매출처":"customer","코드":"product","수량":"quantity", "합계":"aggregate"}, inplace=True)

        df_raw = df_raw[df_raw["quantity"]!=0]
        df_raw = df_raw.drop(df_raw[df_raw["day"]=="소계"].index)
        df_raw = df_raw.drop(df_raw[df_raw["day"]=="합계"].index)
        
        df_raw["day"] = pd.to_datetime(df_raw["day"])
        df_raw["ym"] = df_raw["day"].apply(lambda row : row.strftime("%Y%m"))
        
        df = df_raw.copy()
        
        return df
    