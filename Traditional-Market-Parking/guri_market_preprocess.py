# python 3.9.12
# 작성 : 2023.01.16 유태준
# 1차 수정 : 2023.01.18
# 1차 수정내용 : 요금 계산결과 -500원인 오류, 방문비율계산활용 컬럼생성 구조 및 순서 변경, 요금_전통시장이용 컬럼생성 순서 변경 등 오류 3건 수정
# 전통시장 주차장 이용현황 분석
#   - 주차장 이용자 중 전통시장 방문자 수
#   - 주차장 이용 시 혼잡 시간대 도출
#   - 을 위한 데이터 전처리 작업을 진행하는 코드
# 2차 수정 : 2023.01.31
# 2차 수정내용 : 1시간, 1분 단위로 분할해 작성되어있는 전처리 과정을 10분단위로 통합·수정
# 3차 수정 : 2023.12.19
# 2차 수정내용 : Client 익명화

print("[전통시장 주차장 데이터 전처리]")

### 0. 라이브러리 불러오기 ###
print("<<< 0 >>> 라이브러리 호출                           ")
import os
import pandas as pd
from datetime import timedelta, datetime



### 1. 경로 설정 ###
print("<<< 1 >>> 경로 설정                             ")
#base_directory = os.getcwd() # Jupyter 환경 실행
base_directory = os.path.dirname(os.path.realpath(__file__)) # Python 환경 실행
# 원본 데이터 저장경로 지정
data_directory = os.path.join(base_directory,'data')
# 출력 데이터 저장경로 지정
output_directory = os.path.join(base_directory,'output')
# 원본 데이터 저장경로의 파일명을 리스트로 가져옴
data_name_list = os.listdir(data_directory)



### 2. 데이터 불러오기, 전처리, 오류처리 ###
print("<<< 2 >>> 데이터 전처리                            ")
i = 1 # Counter
# 폴더 내 파일명 리스트로 반복문 실행
for n in data_name_list:


    ### 2 - 1. 불러오기 ###
    # 진행상태 확인
    print("\r - {}/{}번째 데이터 처리하는 중 . . .".format(i,len(data_name_list)), end="")
    # data 폴더 내 데이터를 df1~n 으로 변수지정해 데이터프레임으로 불러옴
    globals()['df{}'.format(i)] = pd.read_excel(os.path.join(data_directory,n))
    # df.columns = list(df.loc[39]) >> 정확한 컬럼명 할당 (39번 행)
    globals()['df{}'.format(i)].columns = list(globals()['df{}'.format(i)].loc[39])


    ### 2 - 2. 데이터 정제 ###
    # 불필요 데이터 제거 (40번 Row 까지)
    globals()['df{}'.format(i)] = globals()['df{}'.format(i)][40:]
    # 인덱스 리셋, 순번 컬럼 제거
    globals()['df{}'.format(i)] = globals()['df{}'.format(i)].reset_index(drop=True).drop((globals()['df{}'.format(i)].columns[0]),axis=1)


    ### 2 - 3. 오류처리 ###
    time_in_list = []
    time_out_list = []
    counter = 0
        # 오류처리 (연도 불일치 오류, 1-2분기 데이터 초반 입차연도 오류)
    for time_in_str, time_out_str in zip(globals()['df{}'.format(i)]['입차시각'],globals()['df{}'.format(i)]['출차시각']):
        # 왜 Datetime으로 바뀐건지 모르겠음 근데 형식 바꿔주면 일단 되긴 됨 -> Python 타입과 Pandas 타입의 차이 때문임
        time_in_str = str(time_in_str)
        time_out_str = str(time_out_str)
        # STR을 List로 변경
        time_in_strlist = list(time_in_str)
        time_out_strlist = list(time_out_str)
        # 오류처리 (파일명에 표시된 연도값으로 변경, 기존 오류값은 전부 2022)
        time_in_strlist[0:4] = data_name_list[i-1][0:4]
        time_out_strlist[0:4] = data_name_list[i-1][0:4]
        # 오류처리 (10~12월달인데 앞에서부터 1000번째 데이터 안쪽인 경우 - 전체 코드에 검색 적용시 너무 오래걸림)
        if counter < 1000:
            counter = counter + 1
            # 이게 더 느릴지, 아니면 대소비교하는게 더 느릴지? 한번 물어봐야 알것 같음
            # 들어온 날짜의 월 앞자리가 1인경우 (10, 11, 12월)
            if time_in_strlist[5] == '1':
                # 연도값을 -1 해서 적용
                time_in_strlist[0:4] = str(int(data_name_list[i-1][0:4]) - 1)
        else:
            counter = counter + 1
        # List를 다시 STR으로 변경해 List에 적재
        time_in_list.append("".join(time_in_strlist))
        time_out_list.append("".join(time_out_strlist))
        # 처리 결과 데이터프레임에 적용
    globals()['df{}'.format(i)]['입차시각'] = time_in_list
    globals()['df{}'.format(i)]['출차시각'] = time_out_list
    

    ### 2 - 4. 컬럼 타입 변경 ###
    globals()['df{}'.format(i)]['입차시각'] = globals()['df{}'.format(i)]['입차시각'].apply(pd.to_datetime)
    globals()['df{}'.format(i)]['출차시각'] = globals()['df{}'.format(i)]['출차시각'].apply(pd.to_datetime)

    i = i + 1 # Counter
    
data_count_int = i - 1



### 3. 데이터 병합 ###
print("\r<<< 3 >>> 데이터 병합                       ")
print("\r - {}~{}번째 데이터 합치는 중 . . .                    ",end="")
for i in range(1,data_count_int+1):
    # index = 1 ~ data 폴더 내 파일 개수
    # index 맨 앞의 값일 경우 : temp_df 에 넣어두고 다음 반복문으로 넘어가 2트부터 합침
    if i == 1:
        df = globals()['df{}'.format(i)]
        continue

    df = pd.concat([df, globals()['df{}'.format(i)]])
# Index 초기화
df = df.reset_index(drop=True)



### 4. 특성공학 ###
print("\r<<< 4 >>> 특성공학                       ")


# 4 - 1. 실제 주차장 이용시간 계산
# 기존 이용시간은 할인이 적용된 값이라 별도 계산이 필요함
print("[4 - 1] 실제 주차장 이용시간 계산                           ")
df['이용시간'] = df['출차시각'] - df['입차시각']
# 시각화 편의를 위해 정수형태 이용시간 만듬 (분단위)
df['이용시간_정수'] = df['이용시간']/timedelta(minutes=1)
df['이용시간_정수'] = df['이용시간_정수'].astype(int)


# 4 - 2. 이용시간_무료, 유료 계산, 요금 계산
print("[4 - 2] 유료 / 무료 이용시간 및 요금 계산                    ")
### 요금계산 함수선언 ###
def calculate_billing(usage_td, continuous = 0):
# 사용시간(timedelta)을 받아 요금(int)을 계산해주는 함수
# 전날에 이어서 계산하는경우 Continuous = 1 로 정보전달
    bill = 0
    
    # 전날에 이어서 계산하는경우 1시간 1000원 미반영
    if continuous == 1:
        bill += round((-(-(usage_td.total_seconds())//600)) * 300)
        return bill  # 나머지 계산 없이 바로 빠져나감

    # 5분 이하 이용시(회차시) 요금 0원, 1시간 기본요금 1000원
    if usage_td <= timedelta(minutes=5):
        pass
    else:
        bill = 1000

    # 1시간 이상 사용시 10분당(600초) 300원
    if usage_td > timedelta(hours=1):
        bill += round(((-(-(usage_td.total_seconds())//600))-6) * 300)
    return bill

bill_list = []
bill_dc_list = []
temp_list = []
df_len = len(df)
for i in range(len(df)):
    print("\r - 데이터 처리하는 중 . . . {}%               ".format(round((i+1)/df_len*100)), end="")
    pay_starting_datetime = datetime.strptime("".join(list(str(df['입차시각'][i]))[:10]) + " 09:00:00", "%Y-%m-%d %H:%M:%S")
    if (df['입차시각'][i] < pay_starting_datetime):
        no_check_time = pay_starting_datetime - df['입차시각'][i]
        # [1차 수정] 조건문 추가됨
        # 오류 : 입차시각과 출차시각이 동일날짜, 0900시 이전인 경우 계산되는 무료 이용시간에 출차시각이 반영되지 않음.
        # 해결 : 출차시각도 0900시 이전이면, 전부 무료 이용시간이라고 가정, 이용시간의 값을 전부 무료이용시간에 가져옴.
        if (df['출차시각'][i] <= pay_starting_datetime):
            no_check_time = df['이용시간'][i]
    else:
        no_check_time = pd.to_timedelta(0)
    
    #주차시와 출차시 일자가 달라졌는지 확인
    car_in_date = datetime.strptime("".join(list(str(df['입차시각'][i]))[:10]), "%Y-%m-%d") # 어차피 같은지만 확인하면 되기 때문에 굳이 TimeStamp 형변환 불필요
    car_out_date = datetime.strptime("".join(list(str(df['출차시각'][i]))[:10]), "%Y-%m-%d") # 한줄 알았으나 알고보니 아니었고
    parking_date_diff = car_out_date - car_in_date
    if(car_in_date == car_out_date):
        ## 같은날 출차
        temp_list.append(no_check_time)
        
    else:
        ## 과금시간 이후 출차
        car_out_0000 = datetime.strptime("".join(list(str(df['출차시각'][i]))[:10]) + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        ## 출차일 09시
        car_out_0900 = datetime.strptime("".join(list(str(df['출차시각'][i]))[:10]) + " 09:00:00", "%Y-%m-%d %H:%M:%S")
        # 출차일 09시보다 늦게 뺐으면
        if df['출차시각'][i] > car_out_0900:
            no_check_time = no_check_time + timedelta(hours=9) * parking_date_diff.days
            
            temp_list.append(no_check_time)
        # 출차일 09시보다 일찍 뻈으면
        else:
        # 이전에 계산한 값(과금시간 전 이용시간) 과 합쳐서 비과금 이용시간을 구함
            no_check_time = no_check_time + (df['출차시각'][i] - car_out_0000) + timedelta(hours=9) * (parking_date_diff.days - 1)
        # 리스트에 계산값 추가
            temp_list.append(no_check_time)

    ### 요금계산 ###
    # 요금 = 요금계산함수적용 ( 이용시간 - 무료 이용시간 )
    bill = calculate_billing(df['이용시간'][i] - no_check_time)
    
    # 계산총액이 하루에 16,000원 이상이면 16,000원 까지만 계산
    if bill > 16000:
        # 하루 안에 나갔으면
        if parking_date_diff.days == 0:
            bill = 16000
        # 이틀 이상 주차했으면
        else:
            # 주차일로 For문 돌림
            for d in range(parking_date_diff.days):
                if d == 0:
                    # 첫째날 주차 시간
                    parking_time_first_day = datetime.strptime("".join(list(str(df['입차시각'][i]))[:10]) + " 00:00:00", "%Y-%m-%d %H:%M:%S") + timedelta(days=1) - df['입차시각'][i]
                    bill = calculate_billing(parking_time_first_day)
                    
                elif d == parking_date_diff.days:
                    # 마지막날 주차 시간
                    parking_time_last_day = df['출차시각'][i] - datetime.strptime("".join(list(str(df['출차시각'][i]))[:10]) + " 00:00:00", "%Y-%m-%d %H:%M:%S")
                    bill = calculate_billing(parking_time_last_day, continuous=1) # continuous 파라미터 전달으로 첫 10분부터 300원 요금 적용
                else:
                    # 중간 주차 시간 (하루종일 주차함)
                    bill += 16000

    # 리스트에 추가
    bill_list.append(bill)
    # [1차 수정] 조건문 추가
    # 0일때 1000 빼고 2나눠서 요금계산이 -500되는 오류 해결
    if bill == 0:
        bill_dc_list.append(0)
    else:
        bill_dc_list.append((bill - 1000) / 2)

df['이용시간_무료'] = temp_list
df['이용시간_유료'] = df['이용시간'] - df['이용시간_무료']
df['이용시간_요금'] = bill_list
df['요금_전통시장이용'] = bill_dc_list


# 4 - 3. 전통시장 이용 비율을 계산하기 위한 할인유형별 데이터 분류
print("\r[4 - 3] 전통시장 이용 비율을 계산하기 위한 할인유형별 데이터 분류             ")
# non_use 할인 값을 받아서 이용 비율 계산시 활용할 값과 활용하지 않을 값으로 나눔
market_visit_ratio_non_use = ['저공해차량', '장애3시간+장애인', '경차', '인식오류', 0.5, '전기차2시간+저공해차량', '전기차2시간+50%',
        '장애3시간+국가유공자', '장애3시간', '관공서언론', '장애3시간+50%', '전기차2시간', '국가유공자', '1시간', '장애인',
        '요일제', '장애3시간+요일제', '장애3시간+저공해차량', '장애3시간+관공서언론', '장애3시간+인식오류', '전기차2시간+장애인','1시간+국가유공자']
temp_list = []
for i in range(df_len):
    if df['할인'][i] in market_visit_ratio_non_use:
        temp_list.append(0)
    elif df['이용시간_요금'][i]==0:
        temp_list.append(0)
    else:
        temp_list.append(1)

df['방문비율계산활용'] = temp_list
# 컬럼을 추가로 생성, 분류 활용여부를 먼저 나타냄(0, 1)
print("\r - 전체 데이터 중 분류(시장방문여부) 활용 데이터 비율 :",round(df['방문비율계산활용'].value_counts()[1]/df['방문비율계산활용'].count()*100,2),"%")


# 4 - 4. 청구요금에 따른 전통시장 이용여부 분류
print("[4 - 4] 청구요금에 따른 전통시장 이용여부 분류            ")
# 세 값을 받아서 두번째 값과 세번째 값 중 무슨 값이 첫째 값에 가까운지를 비교해 0 또는 1을 반환
def closest_value(val1, val2, val3):
    diff1 = abs(val1 - val2)
    diff2 = abs(val1 - val3)
    if diff1 < diff2:
        return 0
    elif diff2 < diff1:
        return 1
    else:
        return 2

temp_list = []
for i in range(df_len):
    print("\r - 데이터 처리하는 중 . . . {}%              ".format(round((i+1)/df_len*100)), end="")
    # [1차 수정] 조건문 추가
    # 이용시간_요금 값이 0원이면 (5분 미만 주차 혹은 새벽시간만 주차) 방문여부 판단불가
    if df['이용시간_요금'][i] == 0:
        temp_list.append(2)
    elif df['요금'][i] == df['요금_전통시장이용'][i]:
        temp_list.append(1)
    elif df['요금'][i] == df['이용시간_요금'][i]:
        temp_list.append(0)
    elif df['방문비율계산활용'][i] == 0:
        temp_list.append(2)
    else:
        # 만든함수 closest_value 사용, 실제 요금과 계산 요금 중 가까운곳으로 분류
        # 실제 시간과 미묘하게 다른 case 있어서 추가됨 (30분으로 요금 계산됬는데 31분 주차된 값 등..)
        temp_list.append(closest_value(df['요금'][i],df['이용시간_요금'][i],df['요금_전통시장이용'][i]))

df['전통시장_이용여부'] = temp_list
# 전체 이용고객 중 전통시장 이용비율
print("\r - 주차장 이용고객 중 전통시장 이용비율:",round(df[df['방문비율계산활용']==1]['전통시장_이용여부'].value_counts()[1] / len(df[df['방문비율계산활용']==1]) * 100,2),"%")


### 5. 시계열 데이터 변환
# 5 - 3. 10분단위 시계열 데이터 변환
print("\r<<< 5 >>> 시계열 데이터 변환              ")
print("\r[5 - 1] 10분단위 데이터 변환                ")
time_start = datetime.strptime("".join(list(str(df['출차시각'][0]))[:10]) + " 00:00:00", "%Y-%m-%d %H:%M:%S")
time_end = datetime.strptime("".join(list(str(df['출차시각'][df_len-1]))[:10]) + " 23:59:00", "%Y-%m-%d %H:%M:%S")
total_10min = round((time_end-time_start).total_seconds() / 600) # 10분 단위로 절사
# 시간별 주차된 차량 계산
car_status_park_ed_list = []
# 시장이용여부 반영
car_market_notuse_count = [] # value = 0
car_market_use_count = [] # value = 1
car_market_bruh = [] # value = 2
# 입.출차 혼잡도 계산
car_status_park_in_list = []
car_status_park_out_list = []
# 요일, 시 추가 (분류 편의성)
yoil = ["월",'화','수','목','금','토','일']
yoil_list = []
time_list = []
hour_list = []

time = time_start
for i in range(total_10min + 1):
    print("\r데이터 처리하는 중 . . . {}             ".format(time.date()), end="")
    time_list.append(time)
    # 시간별 주차된 차량 계산
    car_status_park_ed_list.append(len(df[(df['입차시각']<=time+timedelta(minutes=10)) & (df['출차시각']>=time)]))
    # 시장이용여부 반영
    try:
        car_market_notuse_count.append(df[(df['입차시각']<=time+timedelta(minutes=10)) & (df['출차시각']>=time)]['전통시장_이용여부'].value_counts().sort_index()[0])
    except:
        car_market_notuse_count.append(0)
    try:
        car_market_use_count.append(df[(df['입차시각']<=time+timedelta(minutes=10)) & (df['출차시각']>=time)]['전통시장_이용여부'].value_counts().sort_index()[1])
    except:
        car_market_use_count.append(0)
    try:
        car_market_bruh.append(df[(df['입차시각']<=time+timedelta(minutes=10)) & (df['출차시각']>=time)]['전통시장_이용여부'].value_counts().sort_index()[2])
    except:
        car_market_bruh.append(0)
    # 입.출차 혼잡도 계산
    car_status_park_in_list.append(len(df[(df['입차시각'] >= time) & (df['입차시각'] <= time+timedelta(minutes=10))]))
    car_status_park_out_list.append(len(df[(df['출차시각'] >= time) & (df['출차시각'] <= time+timedelta(minutes=10))]))
    # 요일, 시 컬럼 추가 (분류 편의성 위함)
    hour_list.append(time.hour)
    yoil_list.append(yoil[time.weekday()])
    
    time += timedelta(minutes=10)
time_df_hour = pd.DataFrame({"주차중":car_status_park_ed_list,
                        "주차_전통시장 불용":car_market_notuse_count,
                        "주차_전통시장 활용":car_market_use_count,
                        "주차_전통시장 모름":car_market_bruh,
                        "입차중":car_status_park_in_list,
                        "출차중":car_status_park_out_list,
                        "요일":yoil_list,
                        "시간":hour_list},
                        index = time_list)




"""
### 5. 시계열 데이터 변환 ###
# 5 - 1. 시간단위 시계열 데이터 변환
print("\r<<< 5 >>> 시계열 데이터 변환              ")
print("\r[5 - 1] 시간단위 데이터 변환                ")
time_start = datetime.strptime("".join(list(str(df['출차시각'][0]))[:10]) + " 00:00:00", "%Y-%m-%d %H:%M:%S")
time_end = datetime.strptime("".join(list(str(df['출차시각'][df_len-1]))[:10]) + " 23:59:00", "%Y-%m-%d %H:%M:%S")
total_hours = round((time_end-time_start).total_seconds() / 3600)
# 시간별 주차된 차량 계산
car_status_park_ed_list = []
# 시장이용여부 반영
car_market_notuse_count = [] # value = 0
car_market_use_count = [] # value = 1
car_market_bruh = [] # value = 2
# 입.출차 혼잡도 계산
car_status_park_in_list = []
car_status_park_out_list = []
# 요일, 시 추가 (분류 편의성)
yoil = ["월",'화','수','목','금','토','일']
yoil_list = []
time_list = []
hour_list = []

time = time_start
for i in range(total_hours + 1):
    print("\r데이터 처리하는 중 . . . {}             ".format(time.date()), end="")
    time_list.append(time)
    # 시간별 주차된 차량 계산
    car_status_park_ed_list.append(len(df[(df['입차시각']<=time+timedelta(hours=1)) & (df['출차시각']>=time)]))
    # 시장이용여부 반영
    try:
        car_market_notuse_count.append(df[(df['입차시각']<=time+timedelta(hours=1)) & (df['출차시각']>=time)]['전통시장_이용여부'].value_counts().sort_index()[0])
    except:
        car_market_notuse_count.append(0)
    try:
        car_market_use_count.append(df[(df['입차시각']<=time+timedelta(hours=1)) & (df['출차시각']>=time)]['전통시장_이용여부'].value_counts().sort_index()[1])
    except:
        car_market_use_count.append(0)
    try:
        car_market_bruh.append(df[(df['입차시각']<=time+timedelta(hours=1)) & (df['출차시각']>=time)]['전통시장_이용여부'].value_counts().sort_index()[2])
    except:
        car_market_bruh.append(0)
    # 입.출차 혼잡도 계산
    car_status_park_in_list.append(len(df[(df['입차시각'] >= time) & (df['입차시각'] <= time+timedelta(hours=1))]))
    car_status_park_out_list.append(len(df[(df['출차시각'] >= time) & (df['출차시각'] <= time+timedelta(hours=1))]))
    # 요일, 시 컬럼 추가 (분류 편의성 위함)
    hour_list.append(time.hour)
    yoil_list.append(yoil[time.weekday()])
    
    time += timedelta(hours=1)
time_df_hour = pd.DataFrame({"주차중":car_status_park_ed_list,
                        "주차_전통시장 불용":car_market_notuse_count,
                        "주차_전통시장 활용":car_market_use_count,
                        "주차_전통시장 모름":car_market_bruh,
                        "입차중":car_status_park_in_list,
                        "출차중":car_status_park_out_list,
                        "요일":yoil_list,
                        "시간":hour_list},
                        index = time_list)

#[분단위 데이터 - 보통 계산시간 10~ 15시간 정도 걸려서 일단 주석처리 해 둠]
# 5 - 2. 분단위 시계열 데이터 변환
print("\r[5 - 2] 분단위 데이터 변환                ")
time_start = datetime.strptime("".join(list(str(df['출차시각'][0]))[:10]) + " 00:00:00", "%Y-%m-%d %H:%M:%S")
time_end = datetime.strptime("".join(list(str(df['출차시각'][df_len-1]))[:10]) + " 23:59:00", "%Y-%m-%d %H:%M:%S")
total_minute = round((time_end-time_start).total_seconds() / 60)
# 시간별 주차된 차량 계산
car_status_park_ed_list = []
# 시장이용여부 반영
car_market_notuse_count = [] # value = 0
car_market_use_count = [] # value = 1
car_market_bruh = [] # value = 2
# 입.출차 혼잡도 계산
car_status_park_in_list = []
car_status_park_out_list = []
# 요일, 시 추가 (분류 편의성)
yoil = ["월",'화','수','목','금','토','일']
yoil_list = []
time_list = []
hour_list = []

time = time_start
for i in range(total_minute + 1):
    print("\r데이터 처리하는 중 . . . {} ".format(time), end="")
    time_list.append(time)
    # 시간별 주차된 차량 계산
    car_status_park_ed_list.append(len(df[(df['입차시각']<=time) & (df['출차시각']>=time)]))
    # 시장이용여부 반영
    try:
        car_market_notuse_count.append(df[(df['입차시각']<=time) & (df['출차시각']>=time)]['전통시장_이용여부'].value_counts().sort_index()[0])
    except:
        car_market_notuse_count.append(0)
    try:
        car_market_use_count.append(df[(df['입차시각']<=time) & (df['출차시각']>=time)]['전통시장_이용여부'].value_counts().sort_index()[1])
    except:
        car_market_use_count.append(0)
    try:
        car_market_bruh.append(df[(df['입차시각']<=time) & (df['출차시각']>=time)]['전통시장_이용여부'].value_counts().sort_index()[2])
    except:
        car_market_bruh.append(0)
    # 입.출차 혼잡도 계산
    car_status_park_in_list.append(len(df[(df['입차시각'] + timedelta(minutes=5) >= time) & (df['입차시각'] - timedelta(minutes=5) <= time)]))
    car_status_park_out_list.append(len(df[(df['출차시각'] + timedelta(minutes=5) >= time) & (df['출차시각'] - timedelta(minutes=5) <= time)]))
    # 요일, 시 컬럼 추가 (분류 편의성 위함)
    hour_list.append(time.hour)
    yoil_list.append(yoil[time.weekday()])

    time += timedelta(minutes=1)
print("\r - 데이터 처리 완료.                             ")
print(" - 데이터 적용하는 중 . . .      ", end = "")
time_df_minute = pd.DataFrame({"주차중":car_status_park_ed_list,
                        "주차_전통시장 불용":car_market_notuse_count,
                        "주차_전통시장 활용":car_market_use_count,
                        "주차_전통시장 모름":car_market_bruh,
                        "입차중":car_status_park_in_list,
                        "출차중":car_status_park_out_list,
                        "요일":yoil_list,
                        "시":hour_list},
                        index = time_list)
print("\r데이터 적용 완료.                    ")
"""

### 6. 처리결과 저장 ###
print("\r<<< 6 >>> 처리결과 저장              ")

print("\r - 저장 중 . . .            ", end="")
df.to_csv(os.path.join(output_directory,'1_original.csv'))
#time_df_hour.to_csv(os.path.join(output_directory,'2_time_hour.csv'))
#time_df_minute.to_csv(os.path.join(output_directory,"3_time_minute.csv")) # 시간 오래걸려서 일단 주석처리
print("\r[전통시장 주차장 데이터 전처리 완료]")


# 추가수정 필요사항
# 4시간 동안 20%정도, 총 소요시간 ; 20시간 예상됨