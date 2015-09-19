#!/usr/bin/python
# -*- coding: utf-8 -*-

# TeXマージくん
# Copyright (c) 2015 daiz.

# 以下のことしかできません。
# * 実行時引数に与えられたTeXファイル内に「%%%% hoge」という記述を見つけ次第、
#   実行ディレクトリ/articles/ 内の hoge.tex の内容をまるごと置換します。
#   置換完了後のファイルは hoge_o.tex という名前で生成されます。
# * 置換ファイルが見つからない場合はそこで終了します。（レポートは生成されません。）
#
# つまり、例えば、このように実行します:
# $ cd reports/Lesson8/
# $ python texmerge.py main

import sys
import os
import os.path
import re
import codecs

# エラーメッセージ
msg1 = "引数の数が違います."
msg2 = "メインファイルがありません."
msg3 = "`articles/`がありません."
msg4 = "記事が見つかりません: "
msg5 = "出力ファイルを更新しました."

# 実行ディレクトリ
cwd = os.getcwd()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        # main.tex を取得する
        main_name = sys.argv[1];
        main_path = "{}/{}.{}".format(cwd, main_name, 'tex')

        if os.path.exists(main_path) == False:
            print(msg2)
            exit()

        articlesdir_path = "{}/articles".format(cwd)
        if os.path.exists(articlesdir_path) == False:
            print(msg3)
            exit()

        # main.tex を一行ずつ読んでいく
        res = []  # 最終的に出力する内容
        main = codecs.open(main_path, 'r', 'utf_8')
        for line in main:
            line = line.strip();
            m = re.search('^\%\%\%\% *', line)
            if m != None:
                article_file = line.split(' ')[1]

                # 置換ファイルを読み取る
                article_file_path = "{}/articles/{}.{}".format(cwd, article_file.strip(), 'tex')
                if os.path.exists(article_file_path) == False:
                    print("{}{}".format(msg4, article_file_path.strip()))
                    main.close()
                    exit()
                article = codecs.open(article_file_path, 'r', 'utf_8')
                line = article.read()
                article.close()

            res.append(line)
        main.close()

        # 最終結果をファイルに出力する
        output_name = "{}.tex".format(main_name + '_o')
        output_path = "{}/{}".format(cwd, output_name)
        output = codecs.open(output_path, 'w', 'utf_8')
        for line in res:
            output.write(line)
        output.close()
        print(msg5)
    else:
        print(msg1)
        exit()
