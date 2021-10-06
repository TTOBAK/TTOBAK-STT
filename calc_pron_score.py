import sys
import math
import json

# 두 음운의 각 요소별로 Levenshtein 거리를 측정
def levenshtein_distance_each(x, y):
    if x[0] < 10.0 and y[0] < 10.0: # 둘 다 자음인 경우
        # 첫 번째 클래스의 차이 계산
        if x[0] == y[0]:
            diff1 = 0.0
        elif int(x[0]) == int(y[0]):
            diff1 = 0.3 ** 2
        else:
            diff1 = 1.0

        # 두 번째 클래스의 차이 계산
        if x[1] == y[1]:
            diff2 = 0.0
        else:
            diff2 = 1.0

        return math.sqrt((diff1 + diff2) / 2.0)
    elif x[0] >= 10.0 and y[0] >= 10.0: #  둘 다 모음인 경우
        # 첫 번째 클래스의 차이 계산
        if x[0] == y[0]:
            diff1 = 0.0
        elif int(x[0]) == int(y[0]):
            diff1 = (x[0] - y[0]) ** 2
        else:
            diff1 = 1.0

        # 두 번째 클래스의 차이 계산
        if x[1] == y[1]:
            diff2 = 0.0
        elif int(x[1]) == int(y[1]):
            diff2 = (x[1] - y[1]) ** 2
        else:
            diff2 = 1.0

        return math.sqrt((diff1 + diff2) / 2.0)
    else:
        return 1.0

# Levenshtein 거리 측정
def levenshtein_distance(phone1, phone2):
    table = {
        'g': (1.0, 4.0), 'gg': (1.3, 4.0), 'kh': (1.6, 4.0), 'g2': (1.0, 4.0),
        'n': (4.0, 2.0), 'n2': (4.0, 2.0),
        'd': (1.0, 2.0), 'dd': (1.3, 2.0), 't': (1.6, 2.0), 'd2': (1.0, 2.0),
        'l': (5.0, 2.0), 'l2': (5.0, 2.0),
        'm': (4.0, 1.0), 'm2': (4.0, 1.0),
        'b': (1.0, 1.0), 'bb': (1.3, 1.0), 'p': (1.9, 1.0), 'b2': (1.0, 1.0),
        's': (3.0, 2.0), 'ss': (3.3, 2.0),
        'ng': (4.0, 4.0),
        'j': (2.0, 3.0), 'jj': (2.3, 3.0), 'ch': (2.6, 3.0),
        'h': (3.0, 5.0),
        'i': (10.0, 10.0), 'wi': (10.0, 10.2), 'eu': (10.0, 10.5), 'u': (10.0, 10.9),
        'e': (10.3, 10.15), 'oe': (10.3, 10.37), 'o': (10.3, 10.8),
        'ae': (10.6, 10.3), 'eo': (10.6, 10.65),
        'a': (10.9, 10.5),
        'ya': (10.72, 10.4), 'yeo': (10.48, 10.52), 'yo': (10.24, 10.64), 'yu': (10.0, 10.72), 'yae': (10.48, 10.24), 'ye': (10.24, 10.12),
        'ui': (10.0, 10.1),
        'wa': (10.78, 10.56), 'wae': (10.54, 10.4), 'wo': (10.54, 10.68), 'we': (10.3, 10.28)
    }
    if phone1 not in table or phone2 not in table: # 없는 음운이라면 0을 리턴
        return 0.0
    v1 = table[phone1]
    v2 = table[phone2]

    return levenshtein_distance_each(v1, v2)

def get_distance(text1, text2):
    text1_len = len(text1)
    text2_len = len(text2)

    # 변두리의 값을 초기화
    cache = [[0] * (text2_len+1) for _ in range(text1_len+1)]
    for i in range(0, text1_len+1):
        cache[i][0] = i
    for j in range(0, text2_len+1):
        cache[0][j] = j

    # i, j에서의 최소 Levenshtein Distance 값을 구함
    for i in range(1, text1_len+1):
        for j in range(1, text2_len+1):
            cache[i][j] = min(cache[i][j-1]+1.0, cache[i-1][j]+1.0, cache[i-1][j-1]+levenshtein_distance(text1[i-1], text2[j-1])) 
    return cache[text1_len][text2_len]

# 각각의 엘리먼트 시간 값을 integer로 바꿔줌
def get_time(element):
    key = list(element.keys())[0]
    temp1 = key.split(':')
    temp2 = temp1[1].split('.')
 
    minutes = int(temp1[0])
    seconds = int(temp2[0])
    milis = int(temp2[1])
   
    return minutes * 60000 + seconds * 1000 + milis

# 앞 음운과 뒤 음운 사이 시간 차이에 따른 스코어 값 계산(0.15초 이상 차이나면 감점)
def get_time_score(element1, element2):
    time1 = get_time(element1)
    time2 = get_time(element2)

    if time2 - time1 >= 150:
        return -1.0
    else:
        return 0.0 

def calc_score(res, words, ans, trans, final):
    trans_file = open(trans, 'r')
    res_file = open(res, 'r')
    ans_file = open(ans, 'r')
    words_file = open(words, 'r')
    
    temp0 = trans_file.readlines()
    data = json.load(res_file)
    temp1 = ans_file.readlines()
    words_data = words_file.readline()    

    trans_file.close()
    res_file.close()
    ans_file.close()
    words_file.close()
    
    flag = False
    phone_score = 0.0
    speed_score = 0.0
    rhythm_score = 0.0

    if len(temp0) == 0: # transcript 파일이 비어있으면 점수는 0점
        trans_text = ''
        phone_score = 0.0
        speed_score = 0.0
        rhythm_score = 0.0
        flag = True
    else:
        trans_text = temp0[0].strip()

    if len(temp1) == 0: # answer 파일이 비어있으면 점수는 0점
        ans = []
        phone_score = 0.0
        speed_score = 0.0
        rhythm_score = 0.0
        flag = True
    else:
        ans = temp1[0].strip().split(' ')
    
    res = [list(el.values())[0] for el in data]
    if len(res) == 0: # result json 파일이 비어있으면 점수는 0점
        phone_score = 0.0
        speed_score = 0.0
        rhythm_score = 0.0
        flag = True

    if not flag: # 문제가 발생하지 않았다면
        avg_speed = get_time(data[-1]) / len(res) # 말하는 평균 속도 계산
        
        # 음운 사이의 간격이 평균 속도의 1.7 이상이면 '_' 추가
        ins_cand = []
        for idx in range(len(data)-1):
            if get_time(data[idx+1]) - get_time(data[idx]) > avg_speed * 1.7: 
                ins_cand.append(idx+len(ins_cand)+1)
        for el in ins_cand:
            res.insert(el, '_')

        res_no_underbar = [el for el in res if el != '_']
        ans_no_underbar = [el for el in ans if el != '_']

        # 정답 script와 학생 script 사이의 Levenshtein 거리 측정
        distance = get_distance(res_no_underbar, ans_no_underbar)
        total = max(len(res_no_underbar), len(ans_no_underbar))

        # 100점 만점으로 phone_score를 계산
        phone_score = 100.0 - (distance / total * 100.0)
        
        # -10 ~ 0점으로 speed 점수 계산(정답 스크립트의 띄어쓰기 개수에서 느리게 말한 개수를 빼준 값)
        for idx in range(len(data)-1):
            speed_score += get_time_score(data[idx], data[idx+1])
        speed_score = min(max(speed_score + ans.count('_'), -10), 0)

        underbar_count = abs(ans.count('_') - res.count('_'))
        rhythm_count_score = 5.0 - min(underbar_count*0.5, 10.0) # 띄어쓰기 개수가 맞으면 5점, 틀리면 틀린 개수마다 0.5점 감점(-5 ~ 5점)

        idx_underbar_res = [idx for idx, el in enumerate(res) if el == '_']
        idx_underbar_ans = [idx for idx, el in enumerate(ans) if el == '_']

        # 띄어쓰기 사이 최소 간격의 합을 측정해서 합친 후, 길이로 나눈 후 5를 곱해 줌(-5 ~ 5점)
        rhythm_dis = 0.0
        for res_idx, res_el in enumerate(idx_underbar_res):
            min_val = 987654321
            for ans_idx, ans_el in enumerate(idx_underbar_ans):
                min_val = min(min_val, abs(ans_idx - res_idx))
                if ans_idx >= res_idx: break
            rhythm_dis += min_val
        rhythm_dis_score = 5.0 - min(rhythm_dis * 5 / max(len(res), len(ans)), 10.0)

        rhythm_score = rhythm_count_score + rhythm_dis_score

    score = min(100.0, phone_score + speed_score + rhythm_score) # 100점 만점으로 계산해서 발음 점수 + 속도 점수 + 리듬 점수 합산
    ans_text = ' '.join(ans)
    res_text = ' '.join(res)

    print('Transcript : ', trans_text)
    print('Correct : ', ans_text)
    print('Student Transcript : ', words_data)
    print('Student : ', res_text)
    print('Score : ', score)
    print('Phone Score : ', phone_score)
    print('Speed Score : ', speed_score)
    print('Rhythm Score : ', rhythm_score)
    
    result = {'score': score, 'phone_score': phone_score, 'speed_score': speed_score, 'rhythm_score': rhythm_score, 'transcript': trans_text, 'correct': ans_text, 'student_trans': words_data, 'student': res_text}

    final_file = open(final, 'w')
    json.dump(result, final_file)
    final_file.close()

if __name__ == '__main__':
    print(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    calc_score(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    # res = '/home/marble/PycharmProjects/ali/1595071594619/result.txt'
    # ans = '/home/marble/PycharmProjects/data/00008024/00008024.prons.txt'
    # final = '/home/marble/PycharmProjects/result/00008024_104_1595070537522.txt'
    # calc_score(res, ans, final)
