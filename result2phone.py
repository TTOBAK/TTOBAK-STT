import sys

def parse_text(src, dst):
    input_file = open(src, 'r')

    l = input_file.readlines()
    seq = l[1].split(' ')
    inter_seq = [el for el in seq if el != '' and el != 'SIL' and el != '\n'][1:]
    final_seq = [el.split('_')[0] for el in inter_seq]

    input_file.close()

    output_file = open(dst, 'w')
    output_file.write(' '.join(final_seq)+'\n')
    output_file.close()

if __name__ == '__main__':
    print(sys.argv[1], sys.argv[2])
    parse_text(sys.argv[1], sys.argv[2])
    # src = '/home/marble/PycharmProjects/ali/1595071594619/temp.txt'
    # dst = '/home/marble/PycharmProjects/ali/1595071594619/result.txt'
    # parse_text(src, dst)