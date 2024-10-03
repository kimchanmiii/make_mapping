import pandas as pd
import os

# cv -> result 

types = ['dtag/m/on', 'dtag/m/tr/x']
files = os.listdir(os.getcwd())

for input_filename in files:
    if not input_filename.endswith('_cv.csv'):
        continue

    output_filename = input_filename[:-7] + '_result.xlsx'
    print('<' + output_filename + '>')

    cv_data = pd.read_csv(input_filename, header=None, low_memory=False)
    result_data = pd.read_excel('220926_1s_rawdata_10만개_양식_1.0.6_트립구분 5분_Rev05.xlsx', header=None)

    result_data.loc[0, 35] = cv_data.loc[1, cv_data.shape[1] - 1]
    cv_data = cv_data.drop(0, axis=0).drop(cv_data.shape[1] - 1, axis=1)



    trip_num = cv_data[18]


    trip_list = trip_num.tolist()
    trip_set = set(trip_list)
    t_len = len(trip_set)


    for i in range(cv_data.shape[1]):
        cv_data[i] = pd.to_numeric(cv_data[i], errors='coerce').fillna(cv_data[i])

    columns = {}
    for i in range(cv_data.shape[1]):
        columns[i] = 29 + i
    cv_data.rename(columns=columns, inplace=True)

    delete_index = []
    for i in range(1, cv_data.shape[0] + 1):
        if cv_data.loc[i, 29] not in types:
            delete_index.append(i)
    cv_data.drop(delete_index, inplace=True)
    cv_data = pd.concat([cv_data], ignore_index=True)

    print(str(cv_data.shape[0]) + '개 행의 개별 데이터 계산중...')
    cv_data.insert(0, 0, ['=IF(D' + str(row + 1) + '=1,SQRT(AR' + str(row + 1) + '*AR' + str(row + 1) + '+AS' + str(row + 1) + '*AS' + str(row + 1) + '+AT' + str(row + 1) + '*AT' + str(row + 1) + '),)' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(1, 1, ['=IF(D' + str(row + 1) + '=0,0,((AG' + str(row + 1) + '-AG' + str(row) + ')*86400))' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(2, 2, ['=(AG' + str(row + 1) + '-AG' + str(row) + ')*86400' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(3, 3, ['=IF(AD' + str(row + 1) + '="dtag/m/on",0,IF(AD' + str(row + 1) + '="dtag/m/tr/x",1,"-"))' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(4, 4, ['=IF(G' + str(row + 1) + '=2,0,IF(NOT(AN' + str(row + 1) + '=0),1,E' + str(row) + '))' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(5, 5, ['=IF(AND(E' + str(row) + '=0,E' + str(row + 1) + '=1),1,0)' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(6, 6, ['=IF(OR(H' + str(row + 1) + '<H' + str(row + 2) + ',,H' + str(row + 2) + '=""),1,IF(H' + str(row) + '<H' + str(row + 1) + ',2,0))' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(7, 7, ['=IF(C' + str(row + 1) + '>300,H' + str(row) + '+1,H' + str(row) + ')' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(8, 8, ['=IF(OR(G' + str(row + 1) + '=2,D' + str(row + 1) + '=0),0,B' + str(row + 1) + ')' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(9, 9, ['=IF(D' + str(row + 1) + '=0,0,IF(AND(OR(D' + str(row) + '=0,G' + str(row + 1) + '=2),D' + str(row + 1) + '=1),1,IF(OR(D' + str(row) + '=0,G' + str(row + 1) + '=2),0,(AM' + str(row + 1) + '-AM' + str(row) + ')*86400)))' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(10, 10, ['=IF(AND(G' + str(row + 1) + '=2,D' + str(row + 1) + '=1),60, IF(G' + str(row + 1) + '=2,0,K' + str(row) + '+I' + str(row + 1) + '))' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(11, 11, ['=IF(G' + str(row + 1) + '=1,K' + str(row + 1) + ',0)' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(12, 12, ['=IF(AND(G' + str(row + 1) + '=2,D' + str(row + 1) + '=1),1,IF(G' + str(row + 1) + '=2,0,IF(J' + str(row + 1) + '<=1,M' + str(row) + '+J' + str(row + 1) + ',M' + str(row) + '+1)))' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(13, 13, ['=IF(G' + str(row + 1) + '=1,M' + str(row + 1) + ',0)' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(14, 14, ['=IF(F' + str(row + 1) + '=1,0,IFERROR(IF(AND(D' + str(row) + '=1,D' + str(row + 1) + '=1,Q' + str(row) + '>1,Q' + str(row + 1) + '>1),ACOS(COS(RADIANS(90-Q' + str(row) + '))*COS(RADIANS(90-Q' + str(row + 1) + '))+SIN(RADIANS(90-Q' + str(row) + '))*SIN(RADIANS(90-Q' + str(row + 1) + '))*COS(RADIANS(R' + str(row) + '-R' + str(row + 1) + ')))*6371009,0),0))' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(15, 15, ['=IF(F' + str(row + 1) + '=0,0,IFERROR(IF(AND(Q' + str(row) + '>1,Q' + str(row + 1) + '>1),ACOS(COS(RADIANS(90-Q' + str(row) + '))*COS(RADIANS(90-Q' + str(row + 1) + '))+SIN(RADIANS(90-Q' + str(row) + '))*SIN(RADIANS(90-Q' + str(row + 1) + '))*COS(RADIANS(R' + str(row) + '-R' + str(row + 1) + ')))*6371009,0),0))' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(16, 16, ['=IF(AND($D' + str(row + 1) + '=1,NOT(AN' + str(row + 1) + '=0)),AN' + str(row + 1) + ',Q' + str(row) + ')' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(17, 17, ['=IF(AND($D' + str(row + 1) + '=1,NOT(AO' + str(row + 1) + '=0)),AO' + str(row + 1) + ',R' + str(row) + ')' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(18, 18, ['=IF(O' + str(row + 1) + '>AA$2,1,0)' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(19, 19, ['=IF(1000<=P' + str(row + 1) + ',1,0)' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(20, 20, ['=IF(AND(0<P' + str(row + 1) + ', P' + str(row + 1) + '<1000),1,0)' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(21, 21, ['=IF(AND(1000<=P' + str(row + 1) + ', P' + str(row + 1) + '<2000),1,0)' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(22, 22, ['=IF(AND(2000<=P' + str(row + 1) + ', P' + str(row + 1) + '<3000),1,0)' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(23, 23, ['=IF(AND(3000<=P' + str(row + 1) + ', P' + str(row + 1) + '<5000),1,0)' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(24, 24, ['=IF(AND(5000<=P' + str(row + 1) + ', P' + str(row + 1) + '<7000),1,0)' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(25, 25, ['=IF(AND(7000<=P' + str(row + 1) + ', P' + str(row + 1) + '<10000),1,0)' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(26, 26, ['=IF(10000<=P' + str(row + 1) + ',1,0)' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(27, 27, ['=IF(I' + str(row + 1) + '>AC$2,1,0)' for row in range(3, cv_data.shape[0] + 3)])
    cv_data.insert(28, 28, ['=IF(AND(D' + str(row + 1) + '=1,AN' + str(row + 1) + '=0),1,0)' for row in range(3, cv_data.shape[0] + 3)])

    cv_data48 = pd.DataFrame({48:['=IF(G' + str(row) + '=2,TEXT(AM' + str(row + 1) + ',"yyyy-mm-dd hh:mm:ss"),TEXT(AW' + str(row) + ', "yyyy-mm-dd hh:mm:ss"))' for row in range(3, cv_data.shape[0] + 3)]})
    cv_data49 = pd.DataFrame({49:['=IF(F' + str(row + 1) + '=1, VALUE(TEXT(AM' + str(row + 1) + '-AW' + str(row + 1) + ', "[s]")), -1)' for row in range(3, cv_data.shape[0] + 3)]})
    cv_data = pd.concat([cv_data, cv_data48, cv_data49], axis=1)

    result_data = pd.concat([result_data, cv_data], axis=0, ignore_index=True)

    result_data.loc[3, 1] = 0
    result_data.loc[3, 2] = 0
    result_data.loc[3, 6] = 2
    result_data.loc[3, 7] = 1
    result_data.loc[3, 15] = 0
    result_data.loc[3, 16] = 0
    result_data.loc[3, 17] = 0

    count = cv_data.shape[0]

    print('종합 데이터 계산중...')
    result_data.loc[1, 3] = '=MAX(H4:H' + str(3 + count) + ')' # 주행 횟수
    result_data.loc[1, 4] = '=SUM(F2:G2)' # 총 주행 거리
    result_data.loc[1, 5] = '=SUM(O4:O' + str(3 + count) + ')/1000' # 연산 거리
    result_data.loc[1, 6] = '=SUM(P4:P' + str(3 + count) + ')/1000' # 점프디스턴스 거리
    result_data.loc[1, 7] = '=O2/D2' # 점프디스턴스 비율
    result_data.loc[1, 8] = '=SUM(L4:L' + str(3 + count) + ')/3600' # 총 주행 시간
    result_data.loc[1, 9] = '=SUM(N4:N' + str(3 + count) + ')/3600' # 1초 데이터 총 수신 시간
    result_data.loc[1, 10] = '=1-(J2/I2)' # 소실율
    result_data.loc[1, 11] = '=COUNTIF(AC4:AC' + str(3 + count) + ',1)/3600' # GPS 0 시간
    result_data.loc[1, 12] = '=L2/J2' # GPS 0 비율
    result_data.loc[1, 13] = '=COUNTIF(S4:S' + str(3 + count) + ',1)' # 1000m 이상 discon. 수
    result_data.loc[1, 14] = '=COUNTIF(T4:T' + str(3 + count) + ',1)' # 1000m 이상 jump dist 수
    result_data.loc[1, 15] = '=COUNTIF(U4:U' + str(3 + count) + ',1)' # 0-1km jump dist 수
    result_data.loc[1, 16] = '=COUNTIF(V4:V' + str(3 + count) + ',1)' # 1-2km jump dist 수
    result_data.loc[1, 17] = '=COUNTIF(W4:W' + str(3 + count) + ',1)' # 2-3km jump dist 수
    result_data.loc[1, 18] = '=COUNTIF(X4:X' + str(3 + count) + ',1)' # 3-5km jump dist 수
    result_data.loc[1, 19] = '=COUNTIF(Y4:Y' + str(3 + count) + ',1)' # 5-7km jump dist 수
    result_data.loc[1, 20] = '=COUNTIF(Z4:Z' + str(3 + count) + ',1)' # 7-10km jump dist 수
    result_data.loc[1, 21] = '=COUNTIF(AA4:AA' + str(3 + count) + ',1)' # 10km 이상 jump dist 수
    result_data.loc[1, 22] = '=COUNTIF(AB4:AB' + str(3 + count) + ',1)' # 300초 이상 discon. 수
    result_data.loc[1, 23] = '=AVERAGEIFS(AP4:AP' + str(3 + count) + ',AP4:AP' + str(3 + count) + ',">0",AP4:AP' + str(3 + count) + ',"<100")' # 정확도 평균
    result_data.loc[1, 24] = '=SUMIF(T4:T' + str(3 + count) + ',"=1",P4:P' + str(3 + count) + ')' # 1km 이상 점프디스턴스 거리 합
    result_data.loc[1, 25] = '=O2/D2' # 1km 이상 점프디스턴스 거리 평균
    result_data.loc[1, 26] = 1000 # Disconnect Distance 기준
    result_data.loc[1, 27] = 1000 # Jump Distance 기준
    result_data.loc[1, 28] = 300 # Disconnect time 기준
    result_data.loc[1, 29] = '=MAX(A4:A' + str(3 + count) + ')' # gSum Max
    result_data.loc[1, 30] = '=COUNTIF(A4:A' + str(3 + count) + ',">4")' # gSum

    print('엑셀 파일 생성중...')
    result_data.to_excel(output_filename, header=False, index=False)

    print('생성 완료\n')

print('전체 파일 생성 완료')