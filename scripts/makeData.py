import sys
import os

def convert(transcript, d, lm):
    if not os.path.exists(d):
    	os.makedirs(d)
    basename = os.path.basename(d)
    text = '{}/text'.format(d)
    trans = '{}/{}.trans.txt'.format(d, basename)
    prons = '{}/{}.prons.txt'.format(d, basename)

    f = open(text, 'w')
    f.write(transcript)
    f.close()

    os.system('./updateSegmentation.sh {} {}'.format(d, lm))
    os.system('python3 genPhoneSeq.py {} {}'.format(trans, prons))
    print('Convert: {} completed'.format(basename))
        

if __name__ == '__main__':
    if len(sys.argv) == 4:
        d = sys.argv[3]
    else:
        print('Wrong Argument Given')
        print('Correct: python3 updateData.py <transcript> <language-model> <target-directory>')
        print('** <target-directory> is optional **')
        sys.exit()
    transcript = sys.argv[1]
    lm = sys.argv[2]
    convert(transcript, d, lm)
