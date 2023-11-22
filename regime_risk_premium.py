# 국면별 Risk Premium의 수익률을 계산하는 코드

# Eq_1, Eq_2, Term_1, Term_2, Term_3, Credit_1, Credit_2, Credit_3 (risk premium 수익률 데이터들)
# recovery_df, expansion_df, slowdown_df, contraction_df (국면별 년도-월 데이터들)
# 위의 12개 csv 파일이 필요함

# 코드를 실행하면 eq_ret.csv, term_ret.csv, credit_ret.csv와 eq_std.csv, term_ret.csv, credit_ret.csv가 생성됨
#%%
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# Risk Premium 데이터 불러오기
eq1 = pd.read_csv('Eq_1.csv')
eq2 = pd.read_csv('Eq_2.csv')

term1 = pd.read_csv('Term_1.csv')
term2 = pd.read_csv('Term_2.csv')
term3 = pd.read_csv('Term_3.csv')

credit1 = pd.read_csv('Credit_1.csv')
credit2 = pd.read_csv('Credit_2.csv')
credit3 = pd.read_csv('Credit_3.csv')

# 국면별 날짜(월) 데이터 불러오기
recovery = pd.read_csv('recovery_df.csv')
expansion = pd.read_csv('expansion_df.csv')
slowdown = pd.read_csv('slowdown_df.csv')
contraction = pd.read_csv('contraction_df.csv')

#YYYY-MM 형식으로 바꾸기
recovery['Date'] = pd.to_datetime(recovery['Date']).dt.strftime('%Y-%m')
expansion['Date'] = pd.to_datetime(expansion['Date']).dt.strftime('%Y-%m')
slowdown['Date'] = pd.to_datetime(slowdown['Date']).dt.strftime('%Y-%m')
contraction['Date'] = pd.to_datetime(contraction['Date']).dt.strftime('%Y-%m')

# 전체 기간 데이터 (Buy&Hold)
buy_hold = pd.concat([recovery, expansion, slowdown, contraction])
# Accelerating & Decelerating 기간 데이터
accelerating = pd.concat([recovery, expansion])
decelerating = pd.concat([slowdown, contraction])


# DATE 열을 DatetimeIndex로 바꿔주는 함수
def convert_date(df):
    df['DATE'] = pd.to_datetime(df['DATE'])
    df.set_index('DATE', inplace=True)
    return df


# DATE열과 Return열로 구성된 df를 입력에 넣으면, 연율화된 수익률의 평균 수치와 표준편차를 계산해주는 함수
def annual_ret_std(df):
    annualized_returns = []
    annual_stds = []
    for year, group in df.groupby(df.index.year):
        # 연도별 평균 수익률 계산
        yearly_average_return = group['Return'].mean()
        # 연율화된 수익률 계산
        #annualized_ret = ((1 + yearly_average_return / 100) ** 12) - 1
        annualized_returns.append(yearly_average_return)
        annual_stds.append(group['Return'].std())

    # 연율화된 수익률들의 평균과 연간 표준편차의 평균 계산
    avg_annualized_return = np.mean(annualized_returns) * 100
    avg_std = np.std(annualized_returns) * 100  # annualized_returns를 numpy 배열로 변환하여 std() 사용

    # 결과를 소수점 둘째자리로 반올림
    avg_annualized_return = round(avg_annualized_return, 2)
    avg_std = round(avg_std, 2)

    return avg_annualized_return, avg_std


# risk premium data랑 국면 data를 입력하면, 국면에 해당하는 data만 반환하는 함수
def regime_data(return_df, regime_df):
    df = convert_date(return_df[return_df['DATE'].isin(regime_df['Date'])])
    
    # df = df.pct_change() + 1
    # df = df.rolling(window=12).apply(lambda x: x.prod(), raw=True) - 1
    # df = df.dropna()
    return df

####################################################################################

# Equity Risk Premium1
# Buy & Hold
eq1_BH = regime_data(eq1, buy_hold)
eq1_BH_ret, eq1_BH_std = annual_ret_std(eq1_BH)
# Recovery
eq1_recovery = regime_data(eq1, recovery)
eq1_rec_ret, eq1_rec_std = annual_ret_std(eq1_recovery)
# Expansion
eq1_expansion = regime_data(eq1, expansion)
eq1_exp_ret, eq1_exp_std = annual_ret_std(eq1_expansion)
# Slowdown
eq1_slowdown = regime_data(eq1, slowdown)
eq1_slow_ret, eq1_slow_std = annual_ret_std(eq1_slowdown)
# Contraction
eq1_contraction = regime_data(eq1, contraction)
eq1_con_ret, eq1_con_std = annual_ret_std(eq1_contraction)
# Accelerating
eq1_accelerating = regime_data(eq1, accelerating)
eq1_acc_ret, eq1_acc_std = annual_ret_std(eq1_accelerating)
# Decelerating
eq1_decelerating = regime_data(eq1, decelerating)
eq1_dec_ret, eq1_dec_std = annual_ret_std(eq1_decelerating)

# Equity Risk Premium2
# Buy & Hold
eq2_BH = regime_data(eq2, buy_hold)
eq2_BH_ret, eq2_BH_std = annual_ret_std(eq2_BH)
# Recovery
eq2_recovery = regime_data(eq2, recovery)
eq2_rec_ret, eq2_rec_std = annual_ret_std(eq2_recovery)
# Expansion
eq2_expansion = regime_data(eq2, expansion)
eq2_exp_ret, eq2_exp_std = annual_ret_std(eq2_expansion)
# Slowdown
eq2_slowdown = regime_data(eq2, slowdown)
eq2_slow_ret, eq2_slow_std = annual_ret_std(eq2_slowdown)
# Contraction
eq2_contraction = regime_data(eq2, contraction)
eq2_con_ret, eq2_con_std = annual_ret_std(eq2_contraction)
# Accelerating
eq2_accelerating = regime_data(eq2, accelerating)
eq2_acc_ret, eq2_acc_std = annual_ret_std(eq2_accelerating)
# Decelerating
eq2_decelerating = regime_data(eq2, decelerating)
eq2_dec_ret, eq2_dec_std = annual_ret_std(eq2_decelerating)

# Term Risk Premium1
# Buy & Hold
term1_BH = regime_data(term1, buy_hold)
term1_BH_ret, term1_BH_std = annual_ret_std(term1_BH)
# Recovery
term1_recovery = regime_data(term1, recovery)
term1_rec_ret, term1_rec_std = annual_ret_std(term1_recovery)
# Expansion
term1_expansion = regime_data(term1, expansion)
term1_exp_ret, term1_exp_std = annual_ret_std(term1_expansion)
# Slowdown
term1_slowdown = regime_data(term1, slowdown)
term1_slow_ret, term1_slow_std = annual_ret_std(term1_slowdown)
# Contraction
term1_contraction = regime_data(term1, contraction)
term1_con_ret, term1_con_std = annual_ret_std(term1_contraction)
# Accelerating
term1_accelerating = regime_data(term1, accelerating)
term1_acc_ret, term1_acc_std = annual_ret_std(term1_accelerating)
# Decelerating
term1_decelerating = regime_data(term1, decelerating)
term1_dec_ret, term1_dec_std = annual_ret_std(term1_decelerating)

# Term Risk Premium2
# Buy & Hold
term2_BH = regime_data(term2, buy_hold)
term2_BH_ret, term2_BH_std = annual_ret_std(term2_BH)
# Recovery
term2_recovery = regime_data(term2, recovery)
term2_rec_ret, term2_rec_std = annual_ret_std(term2_recovery)
# Expansion
term2_expansion = regime_data(term2, expansion)
term2_exp_ret, term2_exp_std = annual_ret_std(term2_expansion)
# Slowdown
term2_slowdown = regime_data(term2, slowdown)
term2_slow_ret, term2_slow_std = annual_ret_std(term2_slowdown)
# Contraction
term2_contraction = regime_data(term2, contraction)
term2_con_ret, term2_con_std = annual_ret_std(term2_contraction)
# Accelerating
term2_accelerating = regime_data(term2, accelerating)
term2_acc_ret, term2_acc_std = annual_ret_std(term2_accelerating)
# Decelerating
term2_decelerating = regime_data(term2, decelerating)
term2_dec_ret, term2_dec_std = annual_ret_std(term2_decelerating)

# Term Risk Premium3
# Buy & Hold
term3_BH = regime_data(term3, buy_hold)
term3_BH_ret, term3_BH_std = annual_ret_std(term3_BH)
# Recovery
term3_recovery = regime_data(term3, recovery)
term3_rec_ret, term3_rec_std = annual_ret_std(term3_recovery)
# Expansion
term3_expansion = regime_data(term3, expansion)
term3_exp_ret, term3_exp_std = annual_ret_std(term3_expansion)
# Slowdown
term3_slowdown = regime_data(term3, slowdown)
term3_slow_ret, term3_slow_std = annual_ret_std(term3_slowdown)
# Contraction
term3_contraction = regime_data(term3, contraction)
term3_con_ret, term3_con_std = annual_ret_std(term3_contraction)
# Accelerating
term3_accelerating = regime_data(term3, accelerating)
term3_acc_ret, term3_acc_std = annual_ret_std(term3_accelerating)
# Decelerating
term3_decelerating = regime_data(term3, decelerating)
term3_dec_ret, term3_dec_std = annual_ret_std(term3_decelerating)

# Credit Risk Premium1
# Buy & Hold
credit1_BH = regime_data(credit1, buy_hold)
credit1_BH_ret, credit1_BH_std = annual_ret_std(credit1_BH)
# Recovery
credit1_recovery = regime_data(credit1, recovery)
credit1_rec_ret, credit1_rec_std = annual_ret_std(credit1_recovery)
# Expansion
credit1_expansion = regime_data(credit1, expansion)
credit1_exp_ret, credit1_exp_std = annual_ret_std(credit1_expansion)
# Slowdown
credit1_slowdown = regime_data(credit1, slowdown)
credit1_slow_ret, credit1_slow_std = annual_ret_std(credit1_slowdown)
# Contraction
credit1_contraction = regime_data(credit1, contraction)
credit1_con_ret, credit1_con_std = annual_ret_std(credit1_contraction)
# Accelerating
credit1_accelerating = regime_data(credit1, accelerating)
credit1_acc_ret, credit1_acc_std = annual_ret_std(credit1_accelerating)
# Decelerating
credit1_decelerating = regime_data(credit1, decelerating)
credit1_dec_ret, credit1_dec_std = annual_ret_std(credit1_decelerating)

# Credit Risk Premium2
# Buy & Hold
credit2_BH = regime_data(credit2, buy_hold)
credit2_BH_ret, credit2_BH_std = annual_ret_std(credit2_BH)
# Recovery
credit2_recovery = regime_data(credit2, recovery)
credit2_rec_ret, credit2_rec_std = annual_ret_std(credit2_recovery)
# Expansion
credit2_expansion = regime_data(credit2, expansion)
credit2_exp_ret, credit2_exp_std = annual_ret_std(credit2_expansion)
# Slowdown
credit2_slowdown = regime_data(credit2, slowdown)
credit2_slow_ret, credit2_slow_std = annual_ret_std(credit2_slowdown)
# Contraction
credit2_contraction = regime_data(credit2, contraction)
credit2_con_ret, credit2_con_std = annual_ret_std(credit2_contraction)
# Accelerating
credit2_accelerating = regime_data(credit2, accelerating)
credit2_acc_ret, credit2_acc_std = annual_ret_std(credit2_accelerating)
# Decelerating
credit2_decelerating = regime_data(credit2, decelerating)
credit2_dec_ret, credit2_dec_std = annual_ret_std(credit2_decelerating)

# Credit Risk Premium3
# Buy & Hold
credit3_BH = regime_data(credit3, buy_hold)
credit3_BH_ret, credit3_BH_std = annual_ret_std(credit3_BH)
# Recovery
credit3_recovery = regime_data(credit3, recovery)
credit3_rec_ret, credit3_rec_std = annual_ret_std(credit3_recovery)
# Expansion
credit3_expansion = regime_data(credit2, expansion)
credit3_exp_ret, credit3_exp_std = annual_ret_std(credit3_expansion)
# Slowdown
credit3_slowdown = regime_data(credit3, slowdown)
credit3_slow_ret, credit3_slow_std = annual_ret_std(credit3_slowdown)
# Contraction
credit3_contraction = regime_data(credit3, contraction)
credit3_con_ret, credit3_con_std = annual_ret_std(credit3_contraction)
# Accelerating
credit3_accelerating = regime_data(credit3, accelerating)
credit3_acc_ret, credit3_acc_std = annual_ret_std(credit3_accelerating)
# Decelerating
credit3_decelerating = regime_data(credit3, decelerating)
credit3_dec_ret, credit3_dec_std = annual_ret_std(credit3_decelerating)

eq_ret_list = [eq1_BH_ret, eq1_rec_ret, eq1_exp_ret, eq1_slow_ret, eq1_con_ret, eq1_acc_ret, eq1_dec_ret]
term_ret_list = [term3_BH_ret, term3_rec_ret, term3_exp_ret, term3_slow_ret, term3_con_ret, term3_acc_ret, term3_dec_ret]
credit_ret_list = [credit3_BH_ret, credit3_rec_ret, credit3_exp_ret, credit3_slow_ret, credit3_con_ret, credit3_acc_ret, credit3_dec_ret]
eq_std_list = [eq1_BH_std, eq1_rec_std, eq1_exp_std, eq1_slow_std, eq1_con_std, eq1_acc_std, eq1_dec_std]
term_std_list = [term3_BH_std, term3_rec_std, term3_exp_std, term3_slow_std, term3_con_std, term3_acc_std, term3_dec_std]
credit_std_list = [credit3_BH_std, credit3_rec_std, credit3_exp_std, credit3_slow_std, credit3_con_std, credit3_acc_std, credit3_dec_std]
'''
eq_ret_list = [eq1_BH_ret, eq1_rec_ret, eq1_exp_ret, eq1_slow_ret, eq1_con_ret, eq1_acc_ret, eq1_dec_ret,
            eq2_BH_ret, eq2_rec_ret, eq2_exp_ret, eq2_slow_ret, eq2_con_ret, eq2_acc_ret, eq2_dec_ret]
term_ret_list = [term1_BH_ret, term1_rec_ret, term1_exp_ret, term1_slow_ret, term1_con_ret, term1_acc_ret, term1_dec_ret,
            term2_BH_ret, term2_rec_ret, term2_exp_ret, term2_slow_ret, term2_con_ret, term2_acc_ret, term2_dec_ret,
            term3_BH_ret, term3_rec_ret, term3_exp_ret, term3_slow_ret, term3_con_ret, term3_acc_ret, term3_dec_ret]
credit_ret_list = [credit1_BH_ret, credit1_rec_ret, credit1_exp_ret, credit1_slow_ret, credit1_con_ret, credit1_acc_ret, credit1_dec_ret,
            credit2_BH_ret, credit2_rec_ret, credit2_exp_ret, credit2_slow_ret, credit2_con_ret, credit2_acc_ret, credit2_dec_ret,
            credit3_BH_ret, credit3_rec_ret, credit3_exp_ret, credit3_slow_ret, credit3_con_ret, credit3_acc_ret, credit3_dec_ret]
eq_std_list = [eq1_BH_std, eq1_rec_std, eq1_exp_std, eq1_slow_std, eq1_con_std, eq1_acc_std, eq1_dec_std,
            eq2_BH_std, eq2_rec_std, eq2_exp_std, eq2_slow_std, eq2_con_std, eq2_acc_std, eq2_dec_std]
term_std_list = [term1_BH_std, term1_rec_std, term1_exp_std, term1_slow_std, term1_con_std, term1_acc_std, term1_dec_std,
            term2_BH_std, term2_rec_std, term2_exp_std, term2_slow_std, term2_con_std, term2_acc_std, term2_dec_std,
            term3_BH_std, term3_rec_std, term3_exp_std, term3_slow_std, term3_con_std, term3_acc_std, term3_dec_std]
credit_std_list = [credit1_BH_std, credit1_rec_std, credit1_exp_std, credit1_slow_std, credit1_con_std, credit1_acc_std, credit1_dec_std,
            credit2_BH_std, credit2_rec_std, credit2_exp_std, credit2_slow_std, credit2_con_std, credit2_acc_std, credit2_dec_std,
            credit3_BH_std, credit3_rec_std, credit3_exp_std, credit3_slow_std, credit3_con_std, credit3_acc_std, credit3_dec_std]
'''
#%%
print("                 B&H, Recovery, Exp, Slowdown, Cont, Accel, Decelerating")
print( "equity return : ", eq_ret_list)
print("term return : ", term_ret_list)
print("credit return ", credit_ret_list)

print("equity std : ", eq_std_list)
print("term std : ", term_std_list)
print("credit std : ", credit_std_list)

#%%
# 리스트를 7개씩 묶어서 2차원 리스트로 만들고 데이터프레임으로 만드는 함수
def item7csv(ret_list):
    num_per_row = 7
    matrix = [ret_list[i:i+num_per_row] for i in range(0, len(ret_list), num_per_row)]
    ret_df = pd.DataFrame(matrix)
    return ret_df

eq_ret_df = item7csv(eq_ret_list)
term_ret_df = item7csv(term_ret_list)
credit_ret_df = item7csv(credit_ret_list)
eq_std_df = item7csv(eq_std_list)
term_std_df = item7csv(term_std_list)
credit_std_df = item7csv(credit_std_list)

# 데이터프레임을 CSV 파일로 저장
eq_ret_df.to_csv('eq_ret.csv', index=False, header=False)
term_ret_df.to_csv('term_ret.csv', index=False, header=False)
credit_ret_df.to_csv('credit_ret.csv', index=False, header=False)
eq_std_df.to_csv('eq_std.csv', index=False, header=False)
term_std_df.to_csv('term_std.csv', index=False, header=False)
credit_std_df.to_csv('credit_std.csv', index=False, header=False)

# %%
