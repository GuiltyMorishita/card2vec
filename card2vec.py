# -*- coding: utf-8 -*-
import json
import MeCab
from gensim.models import doc2vec


mecab = MeCab.Tagger("-Owakati")

# カード名とカードテキストの入力データ作成
names = []
text = ""
texts = []
with open("hs_card_list.json", "r") as file:
    hs_card_dict = json.load(file)
    for card in hs_card_dict:
        names.append(card["name"])
        mecab_result = mecab.parse(card["card_text"])
        if mecab_result is False:
            text += "\n"
            texts.append("")
        else:
            text += mecab_result
            texts.append(card["card_text"])

# with open("card_text.txt", "w") as file:
#     file.write(text)

# カードテキスト読み込み
card_text = doc2vec.TaggedLineDocument("card_text.txt")
model = doc2vec.Doc2Vec(card_text, size=100, window=8, min_count=2, workers=4)

model.save("hs.model")
model.save_word2vec_format("hs.w2vmodel")

# # ここから単語同士の類似度
# word = u'武器'  # 類似単語を求めたい単語
# print(word + ' is similar to...')
# # 類似単語と類似度のタプル（類似度上位10件）のリストを受け取る
# for similarity in model.most_similar(positive=word):
#     # タプルのままIPythonに出力するとリテラル表示されないのでこの書き方
#     print(similarity[0], similarity[1])

# 類似カードを求めたいカード名
target_card_name = u"土蜘蛛"
card_index = names.index(target_card_name)

# 類似カードと類似度のタプル（類似度上位10件）のリストを受け取る
similar_docs = model.docvecs.most_similar(card_index)
print(names[card_index] + ":" + texts[card_index] + " is similar to...\n")
for similar_doc in similar_docs:
    print(names[similar_doc[0]], texts[similar_doc[0]], "\n")
