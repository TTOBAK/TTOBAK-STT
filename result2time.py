import sys
import json

def parse_text(src, dst):
    input_file = open(src, 'r')

    l = input_file.readlines()
    seq = l[1].split(' ')[1:]
    seq_arr = []
    for idx, el in enumerate(seq):
        if el != 'SIL' and el != '' and el != '\n':
            times = (idx+3+len(seq_arr))*20//3
            minutes = times // 60000
            secs = (times % 60000) // 1000
            milis = times % 1000
            seq_arr.append({'{0:02}:{1:02}.{2}'.format(minutes, secs, milis): el.split('_')[0]})

    input_file.close()

    output_file = open(dst, 'w')
    json.dump(seq_arr, output_file)
    output_file.close()

if __name__ == '__main__':
    print(sys.argv[1], sys.argv[2])
    parse_text(sys.argv[1], sys.argv[2])
    # src = '/home/marble/PycharmProjects/ali/1595071594619/temp.txt'
    # dst = '/home/marble/PycharmProjects/ali/1595071594619/result.txt'
    # parse_text(src, dst)
