from .script import answer_question
from tqdm import tqdm
from bisect import bisect_left
import difflib

def get_overlap(s1, s2):
    s = difflib.SequenceMatcher(None, s1, s2)
    pos_a, pos_b, size = s.find_longest_match(0, len(s1), 0, len(s2)) 
    return s1[pos_a:pos_a+size]

def get_closest(occurences, content, k=25):
    """
    Get the indices of words where all keywords occur most closely together
    Takes one keyword, and performs binary search for each index of that keyword for other keywords.
    Absolute distance is added, result is sorted and top `K` are extracted

    Args:
        occurences (list): list of list of occurences of each keyword
        content (str): text corpus
        k (int, optional): Number of closest instances to get. Defaults to 25.

    Returns: list of tuples of the form (score, index)
    """
    result = []
    o = occurences[0] #get first
    for idx in o:
        res = 0
        for i in range(1, len(occurences)): #other than first
            oo = occurences[i]
            where = bisect_left(oo, idx)
            #try both, after and before the binary searched index (if exists)
            try:
                res += min(abs(oo[min(len(oo)-1, where+1)]-idx), abs(oo[min(len(oo)-1, where)]-idx))
            except:
                print("Something went wrong here")
        result.append((res, idx))
    
    #if res < best:
    #   best = res
    #  best_where = (idx)

    result = sorted(result)
    final = []
    
    for score, i in tqdm(result):
        f = False
        for ii in final:
            if abs(i-ii) <= 200:
                f = True
                break
        if not f:
            final.append(i)

    paragraphs = []

    for idx in final:
        paragraphs.append(get_para(content, idx))

    print("DONE HERE")
    return paragraphs[:k] 

def get_all_occurences(s, word):
    """
    Find all occurences of a keyword progressively, until it isn't present anymore

    Args:
        s (str): Text corpus
        word (str): Keyword

    Returns:
        list: of indices where keyword is found
    """
    res = [0]
    print("Searching for " + word)
    while True:
        try:
            idx = s.index(word, res[-1])
            res.append(idx+1)
        #print("found at ", idx)
        except ValueError:
            break
    return res[1:]

def get_para(s, idx):
    #250 words before and 250 after
    before = ' '.join(s[max(0, idx-200):idx])
    after = ' '.join(s[idx:min(len(s), idx+200)])
    return before +  after

# def get_para(s, idx):
#     #250 words before and 250 after
#     before = s[max(0, idx-2000):idx]
#     after = s[idx:min(len(s), idx+2000)]
#     return before + after

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