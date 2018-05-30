# coding:utf-8

import itchat
from matplotlib import pyplot as plt
import jieba
import codecs
from wordcloud import WordCloud, ImageColorGenerator
from scipy.misc import imread
from os import path
import re


def get_sex(friends):
    male = 0
    female = 0
    other = 0
    dict_sex = dict()
    for i in friends[1:]:
        dict_sex = i['Sex']
        if dict_sex == 1:
            male += 1
        elif dict_sex == 2:
            female += 1
        else:
            other += 1
    total = len(friends[1:])
    print u'男同学人数:', male
    print u'女同学人数:', female
    print u'未设置性别人数:', other
    print u'总人数:', total
    a1 = (float(male) / total * 100)
    a2 = (float(female) / total * 100)
    a3 = (float(other) / total * 100)
    print u'男同学: %.2f%%' % a1
    print u'女同学: %.2f%%' % a2
    print u'未设置性别: %.2f%%' % a3
    plt.rc('font', family=['Microsoft YaHei'])
    dict_sex = {u'男同学': male, u'女同学': female, u'未设置性别': other}
    for i in dict_sex.keys():
        plt.bar(i, dict_sex[i])
    plt.legend()
    plt.xlabel(u'性别')
    plt.ylabel(u'人数')
    plt.title(u'微信朋友概览')
    plt.show()


def get_word(friends):
    for i in friends:
        signature = i['Signature']
        siglist = []
        signature = signature.strip().replace("span", "").replace("class", "").replace("emoji", "").replace('\"', '')
        rep = re.compile("1f\d+\w*|[<>/=]")
        signature = rep.sub("", signature)
        siglist.append(signature)
        text = "".join(siglist)
        # text = text.replace('\"','')
        with codecs.open('text.txt', 'a', encoding='utf-8') as f:
            wordlist = jieba.cut(text, cut_all=True)
            word_space_split = " ".join(wordlist)
            f.write(word_space_split)
    siglist = []
    signature = signature.strip().replace('\"', '').replace("span", "").replace("class", "").replace("emoji", "")
    rep = re.compile("1f\d+\w*|[<>/=]")
    signature = rep.sub("", signature)
    siglist.append(signature)
    text = "".join(siglist)
    # text = text.replace('\"','')
    with codecs.open('text.txt', 'a', encoding='utf-8') as f:
        wordlist = jieba.cut(text, cut_all=True)
        word_space_split = " ".join(wordlist)
        f.write(word_space_split)
    d = path.dirname(__file__)
    back_coloring_path = "111.jpeg"
    text = codecs.open(u'text.txt', encoding='utf-8').read()
    back_coloring = imread(path.join(d, back_coloring_path))
    my_wordcloud = WordCloud(font_path="/Users/Carl/Downloads/pc6-DroidSansFallback/DroidSansFallback.ttf",
                             background_color="white",
                             max_words=2000,
                             mask=back_coloring,
                             max_font_size=60,
                             random_state=42,
                             width=1000, height=860, margin=2,
                             )

    my_wordcloud.generate(text)
    image_colors = ImageColorGenerator(back_coloring)
    plt.figure()
    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()


def main():
    itchat.auto_login()
    friends = itchat.get_friends(update=True)[0:]
    get_sex(friends)
    get_word(friends)


if __name__ == '__main__':
    main()
