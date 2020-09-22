from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .main import *
import json
from rake_nltk import Rake
from nltk.corpus import stopwords
import colorama

WARNING = colorama.Fore.YELLOW
INFO = colorama.Fore.BLUE
SUCCESS = colorama.Fore.GREEN
CLOSEST = 50

stopwords_eng = stopwords.words('english')

def foo(request):
    return render(request, 'main/index.html', context=None)

def bar(request, book_name):
    return render(request, 'main/{}-catalog.html'.format(book_name))

def foobar(request, book_name, id):
    return HttpResponse(book_name + " and " + str(id))


def ask_ques(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        question = data['question'].lower()

        print('\n{}Got question: {}'.format(INFO, question))

        rake = Rake(stopwords_eng)
        rake.extract_keywords_from_text(question)
        keywords = rake.get_ranked_phrases()

        sep_keywords = []
        for keyword in keywords:
            splitted_keywords = keyword.split(' ')
            for k in splitted_keywords:
                sep_keywords.append(k)

        print('\n{}Extracted keywords: {}'.format(INFO, sep_keywords))



        if len(sep_keywords) == 0:
            print('\n{}Could not find any keywords, using all words...'.format(WARNING))
            sep_keywords = question.split(' ')

        with open('./books/cleaned1.txt') as f:
            contents = f.read().lower()

        all_keyword_occurences = []
        for k in sep_keywords:
            print(k)
            keyword_occurence = get_all_occurences(contents.split(' '), k)
            all_keyword_occurences.append(keyword_occurence)
        

        paragraphs = get_closest(all_keyword_occurences, contents.split(' '), CLOSEST)

        # for para in paragraphs:
            # print('{}Got paragraph: {}'.format(INFO, para))
        # paragraphs = []
        # for occurence in closest_occurences:
        #     score, idx = occurence
        #     print('\n{}Got score: {}'.format(INFO, score))
        #     para = get_para(contents, idx)
        #     print('{}With paragraph: {}'.format(INFO, para))
        #     paragraphs.append(para)
    

        # contents_spit = contents.split(' ')

        # o = get_all_occurences(contents, 'headmaster')
        # p = get_all_para(contents, o)

        print('\n{}Found {} paragraphs...'.format(INFO, len(paragraphs)))
        print('\n')


        best_score = float('-inf')
        ans = 'Couldn\'t find an answer'

        for para in tqdm(paragraphs):
            answer, score = answer_question(question, para)
            if answer != '[CLS]' and score > best_score:
                best_score = score
                ans = answer
        
        print("\n{}Found answer : {}".format(SUCCESS, ans))
        if '[CLS]' in ans:
            ans = ' '.join(ans.split('[SEP]')[1:]).strip()
        ans = ans[0].upper() + ans[1:]
        # ans = ' '.join(sep_keywords)

        return JsonResponse({"ans": ans}, status=200)

    return render(request, 'main/question.html')