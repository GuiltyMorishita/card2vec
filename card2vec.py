# -*- coding: utf-8 -*-
import json
import MeCab
from gensim.models import doc2vec
import os
import random


def load_json(target_game_name):
    # カード名とカードテキストの入力データ作成
    names = []
    text = ""
    texts = []

    # Mecabの出力を分かち書きに指定
    mecab = MeCab.Tagger("-Owakati")

    json_path = target_game_name + "/" + target_game_name + ".json"
    # カードのテキストを形態素解析し、分かち書きしたものを改行区切りで一つのstringにする
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

    with open(target_game_name + ".txt", "w") as file:
        file.write(text)

    return names, texts


def generate_doc2vec_model(target_game_name):
    print("Training Start")
    # カードテキスト読み込み
    card_text = doc2vec.TaggedLineDocument(target_game_name + ".txt")
    # 学習
    model = doc2vec.Doc2Vec(card_text, size=300, window=8, min_count=1,
                            workers=4, iter=400, dbow_words=1, negative=5)

    # モデルの保存
    model.save(target_game_name + ".model")
    print("Training Finish")
    return model


if __name__ == '__main__':
    TARGET_GAME_NAME = "hearth_stone"
    names, texts = load_json(TARGET_GAME_NAME)

    if os.path.isfile(TARGET_GAME_NAME + ".model") is True:
        model = doc2vec.Doc2Vec.load(TARGET_GAME_NAME + ".model")
    else:
        model = generate_doc2vec_model(TARGET_GAME_NAME)

    # 類似カードを求めたいカード名
    TARGET_CARD_NAME = "ロード・ジャラクサス"
    # TARGET_CARD_NAME = names[random.randint(0, len(names))]
    card_index = names.index(TARGET_CARD_NAME)

    # 類似カードと類似度のタプル（類似度上位10件）のリストを受け取る
    similar_docs = model.docvecs.most_similar(card_index)
    print(names[card_index])
    print(texts[card_index])
    print("--------------------is similar to--------------------\n")
    for similar_doc in similar_docs:
        print(names[similar_doc[0]] + " " + str(similar_doc[1]))
        print(texts[similar_doc[0]], "\n")
