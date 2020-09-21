from script import answer_question
from tqdm import tqdm

def get_all_occurences(s, word):
    res = [0]
    while True:
        idx = s.find(word, res[-1])
        #print("found at ", idx)
        if idx == -1: break
        res.append(idx+1)
    return res[1:]

# def get_para(s, idx):
#     #250 words before and 250 after
#     # before = ' '.join(s[max(0, idx-200):idx])
#     # after = ' '.join(s[idx:min(len(s), idx+20)])
#     return before +  after
def get_para(s, idx):
    #250 words before and 250 after
    before = s[max(0, idx-2000):idx]
    after = s[idx:min(len(s), idx+2000)]
    return before + after

def get_all_para(c, o):
    result = []
    for i in o:
        result.append(get_para(c, i))
    return result

if __name__ == '__main__':
    question = 'Who was Dudley?'
    with open('./Q_Fiction/cleaned1.txt') as f:
        contents = f.read().lower()
    contents_spit = contents.split(' ')
    o = get_all_occurences(contents, 'dudley')
    p = get_all_para(contents, o)

    print('Found {} paragraphs...'.format(len(p)))
    print('\n')
    best_score = float('-inf')
    ans = 'No answer'
    # for para in p:
    for para in tqdm(p):
        answer, score = answer_question(question, para)
        # print(para)

        # print(answer, score)
        if answer != '[CLS]' and score > best_score:
            best_score = score
            ans = answer
        # print(answer)
        # print("SCORE: ", score)
        # print('\n')
        # print('*' * 10)
        # print('\n')
    print(ans)