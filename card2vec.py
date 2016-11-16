# -*- coding: utf-8 -*-
import json
import MeCab
from gensim.models import doc2vec


mecab = MeCab.Tagger("-Owakati")

target_game_name = "yugioh"

# カード名とカードテキストの入力データ作成
names = []
text = ""
texts = []

json_path = target_game_name + "/" + target_game_name + ".json"
with open(json_path, "r") as file:
    card_dict = json.load(file)
    for card in card_dict:
        if card["name"] not in names:
            names.append(card["name"])
            mecab_result = mecab.parse(card["text"])
            if mecab_result is False:
                text += "\n"
                texts.append("")
            else:
                text += mecab_result
                texts.append(card["text"])

    print(len(texts))

with open(target_game_name + ".txt", "w") as file:
    file.write(text)

# カードテキスト読み込み
card_text = doc2vec.TaggedLineDocument(target_game_name + ".txt")
model = doc2vec.Doc2Vec(card_text, size=100, window=8, min_count=2, workers=4)

model.save(target_game_name + ".model")
model.save_word2vec_format(target_game_name + ".w2vmodel")

# 類似カードを求めたいカード名
target_card_name = u"エフェクト・ヴェーラー"
card_index = names.index(target_card_name)

# 類似カードと類似度のタプル（類似度上位10件）のリストを受け取る
similar_docs = model.docvecs.most_similar(card_index)
print(names[card_index] + ":" + texts[card_index] + " is similar to...\n")
for similar_doc in similar_docs:
    print(names[similar_doc[0]], texts[similar_doc[0]], "\n")
