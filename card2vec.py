# -*- coding: utf-8 -*-
import json
import MeCab
from gensim.models import doc2vec


mecab = MeCab.Tagger("-Owakati")

# カード名とカードテキストの入力データ作成
names = ""
texts = ""
with open("hs_card_list.json", "r") as file:
    hs_card_dict = json.load(file)
    for card in hs_card_dict:
        names += card["name"] + "\n"
        mecab_result = mecab.parse(card["card_text"])
        if mecab_result is False:
            texts += "\n"
        else:
            texts += mecab_result

# カードテキスト読み込み
card_text = doc2vec.TaggedLineDocument(texts)
