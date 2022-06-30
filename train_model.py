from glob import glob
import warnings
warnings.filterwarnings(action='ignore')

from datetime import datetime

from mlxtend.frequent_patterns import association_rules, apriori, fpgrowth
from mlxtend.preprocessing import TransactionEncoder

import sklearn
from sklearn.decomposition import TruncatedSVD

import pandas as pd 
import numpy as np

import os
import pickle as pkl

def df_preprocess(
    
    '일자':str,
                  '매출처':str,
                  '코드':str,
                  '수량': float,
                  '합계': float)













def learn_prophet(df_dataset: pd.DataFrame,
                  df_holiday: pd.DataFrame,
                  product_id: str,
                  output_dir: str="./ai_model" )->None:
    """
    Prophet 모델 학습
    :param df_dataset: 실 데이터셋 column : [ds,y]
    :param df_holiday: 휴일 데이터셋, column : [ds, holiday]
    :param product_id: 프로덕트 아이디
    :param output_dir: 파일이 저장될 경로
    :return: NONE
    """
    pbounds = {
        'wseas': (3, 21),
        'mseas': (3, 21),
        'yseas': (3, 21),
        's_prior': (0.1, 1),
        'h_prior': (0.1, 1),
        'c_prior': (0.1, 1),
    }


    def build_model(wseas: int, mseas: int, yseas: int, s_prior: float, h_prior: float, c_prior: float)->Prophet:
        """
        최적화를 위해서 모델 생성 부분
        :param wseas: 주 주기율 강도
        :param mseas: 월 주기성 강도
        :param yseas: 년 주기성 강도
        :param s_prior: 주 적용 강도
        :param h_prior: 휴일 적용 강도
        :param c_prior: 변이점 적용 강도
        :return:
        """
        m = Prophet(growth='linear',
                    holidays=df_holiday,
                    daily_seasonality=False,
                    weekly_seasonality=False,
                    yearly_seasonality=False,
                    seasonality_prior_scale=s_prior,
                    holidays_prior_scale=h_prior,
                    changepoint_prior_scale=c_prior)

        m = m.add_seasonality(
            name='weekly',
            period=7,
            fourier_order=wseas)

        m = m.add_seasonality(
            name='monthly',
            period=30.5,
            fourier_order=mseas)

        m = m.add_seasonality(
            name='yearly',
            period=365.25,
            fourier_order=yseas)
        return m

    def black_box_function(
            wseas: float,
            mseas: float,
            yseas: float,
            s_prior: float,
            h_prior: float,
            c_prior: float)->float:
        """
        최적화를 위한 최적화 함수
        :param wseas: 주 주기성 값
        :param mseas: 월 주기성 값
        :param yseas: 년 주기성 값
        :param s_prior: 주 적용 강도
        :param h_prior: 휴일 적용 강도
        :param c_prior: 변이점 적용 강도
        :return: 모델 학습 후 mape 값
        """
        wseas = int(wseas)
        mseas = int(mseas)
        yseas = int(yseas)
        model = build_model(wseas, mseas, yseas, s_prior, h_prior, c_prior)
        model.fit(df_dataset)

        horiz = int(df_dataset.shape[0]/3)
        while True:
            try:
                cv_results = cross_validation(model, horizon=f"{horiz} days")
                return 100.0 - np.average(performance_metrics(cv_results, metrics=["mape"])["mape"])
            except Exception as e:
                logger.error(e)
                horiz = horiz / 3.0
                if horiz < 10.0:
                    return 100
                #     raise Exception("Holiday bound error")

    optimizer = BayesianOptimization(
        f=black_box_function,
        pbounds=pbounds,
        verbose=2,
        random_state=1,
    )
    optimizer.maximize(
        init_points=10,
        n_iter=50,
        # What follows are GP regressor parameters
        alpha=1e-3,
        n_restarts_optimizer=5
    )

    print(optimizer.max)
    params = optimizer.max["params"]
    wseas = int(params["wseas"])
    mseas = int(params["mseas"])
    yseas = int(params["yseas"])
    s_prior = params["s_prior"]
    h_prior = params["h_prior"]
    c_prior = params["c_prior"]
    model = build_model(wseas, mseas, yseas, s_prior, h_prior, c_prior)
    model.fit(df_dataset)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    file_name = f"{output_dir}/{product_id}_model.bin"
    logger.info(f"training file : {os.path.join(os.getcwd(), file_name)}")

    with open(file_name, "wb") as f:
        pkl.dump(model, f)
    return optimizer.max


def main(args):
    import holidays
    logger.info("run learner with args")

    kr_holidays = holidays.KR()
    df_dataset = pd.read_pickle(args.input)
    df_holiday = pd.DataFrame(columns=["ds", "holiday"])
    df_holiday["ds"] = pd.date_range(np.min(df_dataset["ds"]), np.max(df_dataset["ds"]))
    df_holiday["holiday"] = df_holiday.ds.apply(lambda x: 'holiday' if x in kr_holidays else '')
    df_holiday = df_holiday[df_holiday["holiday"] == "holiday"]

    learn_prophet(df_dataset=df_dataset,
                  df_holiday=df_holiday,
                  product_id=args.product_id,
                  output_dir=args.output_dir)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="prophet learner")
    parser.add_argument("input", type=argparse.FileType('r'), required=True)
    parser.add_argument('output_dir', type=str, default="./ai_model", required=True)
    parser.add_argument('product_id', type=str, required=True)
    args = parser.parse_args()
    main(args)