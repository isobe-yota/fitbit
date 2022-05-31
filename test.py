
from tokenize import Token
from turtle import update
import fitbit
from ast import literal_eval
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as mdates


def get_steps(base_date, detail_level, start_time, end_time):
    steps_data =client.intraday_time_series('activities/steps', base_date=base_date,
                                                    detail_level=detail_level, start_time=start_time, end_time=end_time)
    steps_dic_list = steps_data['activities-steps-intraday']['dataset']
    return steps_dic_list

def get_calories( base_date, detail_level, start_time, end_time):
    calories_data = client.intraday_time_series('activities/calories', base_date=base_date,
                                                    detail_level=detail_level, start_time=start_time, end_time=end_time)
    calories_dic_list = calories_data['activities-calories-intraday']['dataset']
    return calories_dic_list

# 心拍数を取得する関数
def get_heart_rate(date, detail_level):
    # heart rateを1[s]単位で取得してpandas DataFrameに変換する
    hr = client.intraday_time_series(resource='activities/heart',
                                     base_date=date,
                                     detail_level=detail_level)['activities-heart-intraday']['dataset']
    hr = pd.DataFrame.from_dict(hr)
    return hr

# tokenファイルを上書きする関数
def updateToken(token):
    f = open(TOKEN_FILE, 'w')
    f.write(str(token))
    f.close()
    return
 
# ユーザ情報の定義
CLIENT_ID =  '238KL8'
CLIENT_SECRET  = 'b614d0ecbf395548e64c42bbd7ef63d6'
TOKEN_FILE = "token.txt"
 
# ファイルからtoken情報を読み込む
tokens = open(TOKEN_FILE).read()
token_dict = literal_eval(tokens)
access_token = token_dict['access_token']
refresh_token = token_dict['refresh_token']
 
# .FitbitでClient情報を取得
# refresh_cbに関数を定義する事で期限切れのtokenファイルを自動更新する
client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET,
                       access_token = access_token,
                       refresh_token = refresh_token,
                       refresh_cb = updateToken)

# if __name__ == '__main__':
base_date = '2022-05-26'
detail_level = '15min'
start_time = '18:00'
end_time = '18:15'
steps_dic_list = get_steps(base_date, detail_level, start_time, end_time)
calories_dic_list = get_calories(base_date, detail_level, start_time, end_time)
hr = get_heart_rate(base_date, detail_level='1sec')
print(steps_dic_list)
print(calories_dic_list)
print(hr)


# フォントの種類とサイズを設定する。
plt.rcParams['font.size'] = 14
plt.rcParams['font.family'] = 'Times New Roman'

# 目盛を内側にする。
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
 
# グラフの上下左右に目盛線を付ける。
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.yaxis.set_ticks_position('both')
ax1.xaxis.set_ticks_position('both')
 
# 軸のラベルを設定する。
ax1.set_xlabel('Time [h]')
ax1.set_ylabel('Heart Rate [bpm]')
 
# スケールの設定をする。
ax1.xaxis.set_major_locator(mdates.HourLocator(byhour=range(0, 24, 6)))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
 
# データプロットの準備とともに、ラベルと線の太さ、凡例の設置を行う。
ax1.plot(pd.to_datetime(hr['time']), hr['value'], label=base_date, lw=1)
ax1.legend()
 
# レイアウト設定
fig.tight_layout()
 
# グラフを表示する。
plt.show()
plt.close()