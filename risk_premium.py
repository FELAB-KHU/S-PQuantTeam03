# 해야할 일 Risk Premium을 계산하기
# 월별 premium을 구하기

# Equity Premium은 단순 수익률이 아니라, Total 수익률을 가지고 계산해야 함
# Credit Premium은 4가지 케이스에서 회사채에서 3M 국채를 빼는 것으로 단순 수익률을 계산함
# Term Premium은 duration 별 3가지 케이스에서 단순 수익률을 계산함


# Equity Premium
# S&P500 Total Return Index (SP500) - 10Y US Treasury Total Return (DGS10)
# S&P500 Total Return Index (SP500) - 10Y Corporate Bond Total Return (HQMCB10YR)

# Credit Premium
# High Yield (BAMLH0A0HYM2EY) - 3M T-bill (DGS3MO)
# Leverage Loan (BOGZ1FL623069503Q) - 3M T-bill (DGS3MO) -> 안 쓰기로 함
# EM US Dollar Index (DTWEXEMEGS) - 3M T-bill (DGS3MO)
# Investment Grade (WAAA) - 3M T-bill(DGS3MO)

# Term Premium
# 3Y US Treasury (DGS3)
# 7Y US Treasury (DGS7)
# 10Y US Treasury (DGS10)

#%%
from pandas_datareader import data as web
import datetime
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 원래 데이터가 percent이고, 데이터를 월별 수익률로 만들어주는 함수
def percent_M_data(ticker, start, end):
    data = web.DataReader(ticker, 'fred', start, end).dropna()
    # 각 월별 데이터를 1에 더하고 누적곱을 구함
    data = (1 + data / 100).resample('M').prod() - 1
    #data = data.resample('M').apply(lambda x: (1 + x/100).prod() - 1)
    data.index = data.index.strftime('%Y-%m')
    return data

# 원래 데이터가 index이고, 데이터를 월별 수익률로 만들어주는 함수
def index_M_data(ticker, start, end):
    data = web.DataReader(ticker, 'fred', start, end).dropna()
    # 월의 첫날과 마지막날의 값을 사용하여 수익률 계산
    data_monthly_start = data.resample('M').first()
    data_monthly_end = data.resample('M').last()
    data = (data_monthly_end - data_monthly_start) / data_monthly_start
    data.index = data.index.strftime('%Y-%m')
    return data


# 인덱스가 다른 데이터 간의 수익률을 빼는 연산 함수
def minus(df1, df2):
    common_index = df1.index.intersection(df2.index)
    df1_common = df1.loc[common_index].iloc[:, 0]  # 첫 번째 열만 선택
    df2_common = df2.loc[common_index].iloc[:, 0]  # 첫 번째 열만 선택
    result = pd.DataFrame(df1_common - df2_common)
    result.rename(columns={0: 'Return'}, inplace=True)
    return result

# 설정된 시작일과 종료일
start = datetime.datetime(1998, 1, 1)
end = datetime.datetime(2021, 12, 31)

# S&P 500 지수의 월별 데이터 가져오기
sp500_monthly_data = yf.download('^GSPC', start='1997-12-01', end='2021-12-31', interval='1mo')
sp500_adj_close = sp500_monthly_data['Adj Close']
sp500_returns = sp500_adj_close.pct_change().dropna()
SP500 = pd.DataFrame({'DATE': sp500_returns.index, 'S&P 500': sp500_returns.values})
SP500.set_index("DATE", inplace=True)
SP500.index = SP500.index.strftime("%Y-%m")

# 필요한 데이터를 FRED에서 가져오기
# Equity Premium에 필요한 데이터
#SP500 = index_M_data('SP500', start, end) # 2013-11부터 있음
US_10Y = percent_M_data('DGS10', start, end) # 1993-01도 있음
Corp_10Y = web.DataReader('HQMCB10YR', 'fred', start, end).dropna()
Corp_10Y.index = Corp_10Y.index.strftime('%Y-%m') # 1993-01도 있음

Eq_1 = minus(SP500, US_10Y)
Eq_2 = minus(SP500, Corp_10Y)

# Credit Premium에 필요한 데이터
HY = percent_M_data('BAMLH0A0HYM2EY', start, end) #1996-12부터 있음
EM = index_M_data('DTWEXEMEGS', start, end) #2006-01부터 있음
IG = percent_M_data('WAAA', start, end) # 1993-01도 있음
US_3M = percent_M_data('DGS3MO', start, end) # 1993-01도 있음

Credit_1 = minus(HY, US_3M)
Credit_2 = minus(EM, US_3M)
Credit_3 = minus(IG, US_3M)

# Term Premium에 필요한 데이터
US_3Y = percent_M_data('DGS3', start, end) # 1993-01도 있음
US_7Y = percent_M_data('DGS7', start, end) # 1993-01도 있음
US_10Y = percent_M_data('DGS10', start, end) # 1993-01도 있음

Term_1 = minus(US_3Y, US_3M)
Term_2 = minus(US_7Y, US_3M)
Term_3 = minus(US_10Y, US_3M)

# 열이름 수정
Term_1.rename(columns={'DGS3': 'Return'}, inplace=True)
Term_2.rename(columns={'DGS7': 'Return'}, inplace=True)
Term_3.rename(columns={'DGS10': 'Return'}, inplace=True)

# csv파일로 저장
Eq_1.to_csv('Eq_1.csv')
Eq_2.to_csv('Eq_2.csv')
Credit_1.to_csv('Credit_1.csv')
Credit_2.to_csv('Credit_2.csv')
Credit_3.to_csv('Credit_3.csv')
Term_1.to_csv('Term_1.csv')
Term_2.to_csv('Term_2.csv')
Term_3.to_csv('Term_3.csv')

