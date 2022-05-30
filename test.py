
from tokenize import Token
from turtle import update
import fitbit
from ast import literal_eval

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
print(steps_dic_list)
print(calories_dic_list)