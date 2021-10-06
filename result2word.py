import sys

BASE_IDX = 0xAC00
MAPPING_TABLE = {
    'g': 'ㄱ', 'gg': 'ㄲ', 'kh': 'ㅋ', 'g2': 'ㄱ',
    'n': 'ㄴ', 'n2': 'ㄴ',
    'd': 'ㄷ', 'dd': 'ㄸ', 't': 'ㅌ', 'd2': 'ㄷ',
    'l': 'ㄹ', 'l2': 'ㄹ',
    'm': 'ㅁ', 'm2': 'ㅁ',
    'b': 'ㅂ', 'bb': 'ㅃ', 'p': 'ㅍ', 'b2': 'ㅂ',
    's': 'ㅅ', 'ss': 'ㅆ',
    'ng': 'ㅇ',
    'j': 'ㅈ', 'jj': 'ㅉ', 'ch': 'ㅊ',
    'h': 'ㅎ',
    'i': 'ㅣ', 'wi': 'ㅟ', 'eu': 'ㅡ', 'u': 'ㅜ',
    'e': 'ㅔ', 'oe': 'ㅚ', 'o': 'ㅗ',
    'ae': 'ㅐ', 'eo': 'ㅓ',
    'a': 'ㅏ',
    'ya': 'ㅑ', 'yae': 'ㅒ', 'yeo': 'ㅕ', 'ye': 'ㅖ',
    'wae': 'ㅙ', 'yo': 'ㅛ', 'wo': 'ㅝ', 'we': 'ㅞ',
    'yu': 'ㅠ', 'ui': 'ㅢ', 'wa': 'ㅘ'
}

CHOSUNG = (

   "ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ",

   "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ",

   "ㅌ", "ㅍ", "ㅎ")

JUNGSUNG = (

   "ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ",

   "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ",

   "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ")

JONGSUNG = (

   "", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ",

   "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ",

   "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ",

   "ㅋ", "ㅌ", "ㅍ", "ㅎ")

def parse_text(src, dst):
    input_file = open(src, 'r')

    l = input_file.readlines()
    seq = l[1].split(' ')

    phone_word_list = [[]]
    phone_word_idx = 0

    for i in range(1, len(seq)):
        if seq[i] == '' or seq[i] == '\n': continue
        elif seq[i] == 'SIL': # 띄어쓰기일 경우
            phone_word_idx+=1
            phone_word_list.append([])
        else: phone_word_list[phone_word_idx].append(seq[i].split('_')[0]) 
    input_file.close()

    word_list = []
    for word_idx in range(len(phone_word_list)):
        current_idx = 0
        word_list.append('')
        if len(phone_word_list[word_idx]) == 0: # 빈 array이면 넘어감
            continue

        while(True):
            if current_idx >= len(phone_word_list[word_idx]): break # 현재 인덱스가 array 크기 초과하면 넘어감

            el = phone_word_list[word_idx][current_idx]

            # 자음 없이 모음으로 시작하는 경우를 감지
            flag = False
            for mo in 'aeiouw':
                if mo in el:
                    flag = True
            
            if flag:
                cho = 'ㅇ'
            else:
                cho = MAPPING_TABLE[phone_word_list[word_idx][current_idx]]
                current_idx += 1

            # 다음 글자가 마지막이고 그 글자가 종성이거나, 다음 글자가 마지막이 아닌데 종성 초성이 연달아 나온다면 받침이 있는 경우
            if (current_idx + 2 == len(phone_word_list[word_idx]) \
                    and MAPPING_TABLE[phone_word_list[word_idx][current_idx+1]] in JONGSUNG) \
                or (current_idx + 2 < len(phone_word_list[word_idx]) \
                    and MAPPING_TABLE[phone_word_list[word_idx][current_idx+1]] in JONGSUNG \
                    and MAPPING_TABLE[phone_word_list[word_idx][current_idx+2]] in CHOSUNG):
                jung = MAPPING_TABLE[phone_word_list[word_idx][current_idx]]
                jong = MAPPING_TABLE[phone_word_list[word_idx][current_idx+1]]

                cho_idx = CHOSUNG.index(cho)
                jung_idx = JUNGSUNG.index(jung)
                jong_idx = JONGSUNG.index(jong)

                word_list[word_idx] += chr(0xAC00 + ((cho_idx*21)+jung_idx)*28+jong_idx)
                current_idx += 2
            else: # 받침이 없는 경우
                jung = MAPPING_TABLE[phone_word_list[word_idx][current_idx]]
                cho_idx = CHOSUNG.index(cho)
                jung_idx = JUNGSUNG.index(jung)

                word_list[word_idx] += chr(0xAC00 + ((cho_idx*21)+jung_idx)*28)
                current_idx += 1
    word_list = [el for el in word_list if el != '']
    
    # 파일로 저장
    f = open(dst, 'w')
    for word in word_list:
        f.write(word + ' ')
    f.close()

if __name__ == '__main__':
    print(sys.argv[1], sys.argv[2])
    parse_text(sys.argv[1], sys.argv[2])
    # src = '/home/marble/PycharmProjects/ali/1595071594619/temp.txt'
    # dst = '/home/marble/PycharmProjects/ali/1595071594619/result.txt'
    # parse_text(src, dst)
