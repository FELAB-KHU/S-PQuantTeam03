#%%
# 1. ETF 수익률 가져오기
# 2. 국면별 날짜 데이터 불러오기
# 3. 국면별 날짜들의 ETF별 총 수익률 계산하기

import pandas as pd

etf_month = pd.read_csv('etf_month(regime).csv')
etf_month['Date'] = pd.to_datetime(etf_month['Date'])
etf_month = etf_month.set_index('Date')
etf_month = etf_month.drop(['regime'], axis = 1)
etf_month.index = etf_month.index.strftime('%Y-%m')

# 국면별 날짜(월) 데이터 불러오기
recovery = pd.read_csv('recovery_df.csv')
expansion = pd.read_csv('expansion_df.csv')
slowdown = pd.read_csv('slowdown_df.csv')
contraction = pd.read_csv('contraction_df.csv')
# 전체 기간 데이터 (Buy&Hold)
buy_hold = pd.concat([recovery, expansion, slowdown, contraction])

def regime_data(etf_month, regime_df):
   # 'Date' 열을 datetime 객체로 변환
    regime_df['Date'] = pd.to_datetime(regime_df['Date'])
    # etf_month 데이터프레임의 인덱스를 datetime 객체로 변환
    etf_month.index = pd.to_datetime(etf_month.index)
    # 공통 날짜를 기준으로 데이터 병합
    merged_data = pd.merge(regime_df[['Date']], etf_month, left_on='Date', right_on=etf_month.index, how='inner')
    # 날짜 형식을 'YYYY-MM'으로 변경
    merged_data['Date'] = merged_data['Date'].dt.strftime('%Y-%m')
    return merged_data

# 수정된 함수 사용
etf_BH = regime_data(etf_month, buy_hold)
etf_recovery = regime_data(etf_month, recovery)
etf_expansion = regime_data(etf_month, expansion)
etf_slowdown = regime_data(etf_month, slowdown)
etf_contraction = regime_data(etf_month, contraction)

def calculate_total_returns(*dfs):
    # 총 수익률을 저장할 딕셔너리 초기화
    total_returns = {}
    columns = ['Recovery', 'Expansion', 'Slowdown', 'Contraction', 'Buy and Hold']
    etf_name = ['Equity', 'Corporate', 'Treasury']

    # 각 데이터프레임에 대해 총 수익률 계산
    for df, column in zip(dfs, columns):
        regime_returns = {}
        for etf in df.columns[1:]:  # 첫 번째 열(Date)을 제외하고 계산
            total_return = ((1 + df[etf].mean()) ** 12 - 1) * 100 # percent 단위로 표현함
            regime_returns[etf] = total_return
        total_returns[column] = regime_returns 

    # 결과를 데이터프레임으로 변환
    total_return_df = pd.DataFrame(total_returns)
    # ETF 이름을 카테고리 이름으로 변경
    total_return_df.index = etf_name
    return total_return_df

# 모든 국면별 데이터프레임에 대해 함수 적용
final_returns = calculate_total_returns(etf_recovery, etf_expansion, etf_slowdown, etf_contraction, etf_BH)
final_returns = final_returns.round(2).apply(lambda x: x.map(lambda y: f'{y}%'))

# 결과 확인
print(final_returns)

# final_returns 데이터프레임을 CSV 파일로 저장
final_returns.to_csv('Panel_B.csv', index=True)