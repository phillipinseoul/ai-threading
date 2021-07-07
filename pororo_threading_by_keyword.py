# -*- coding: utf-8 -*-
"""PORORO_Threading_by_Keyword.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1knEXB8laLdSLtg4GWmpGguMsyWNsr30g
"""

# https://github.com/lovit/KR-WordRank
# !pip install krwordrank
# !pip install pororo

from pororo import Pororo
from krwordrank.word import KRWordRank
import operator
import json
import os

from google.colab import drive
drive.mount('/content/drive')

os.chdir('/content/drive/MyDrive/korean-summary/data')
# os.listdir()

text_list = []
for f in os.listdir():
  with open(f) as json_file:
    json_data = json.load(json_file)
    sentences = json_data["sentences"]
    full_text = '. '.join(sentences)
    text_list.append(full_text)

# Default threads
# threadList = []
fit_in_threadlist = Pororo(task="zero-topic", lang="ko")

from krwordrank.word import KRWordRank, summarize_with_keywords
wordrank_extractor = KRWordRank(min_count=3, max_length=15)

def setDefaultThread():
  threadList = []
  while True:
    thread = input("Default thread를 입력해주세요 (건너뛰기: Enter): ")
    if thread == "":
      break
    else:
      threadList.append(thread)
  
  try:
    if len(threadList) == 0:
      raise ValueError
    return threadList
  except ValueError:
    print("Default thread를 1개 이상 입력해야 합니다.")

def getKeyword(text):
  keywordList = []
  sentences = text.split('. ')    # Parse into sentences
  try:
    keywords = summarize_with_keywords(sentences, min_count=3, max_length=10)
    for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:5]:
      keywordList.append(word)
    return keywordList
  except AttributeError:
    print("Attribute Error 발생")

def threadByKeyword(text):
  # Check if the text belongs in an existing thread
  try:
    th = fit_in_threadlist(text, threadList)
    thMax = max(th, key=lambda key: th[key])
  except ValueError:
    print("길이가 512자를 초과합니다.")
    return

  if th[thMax] > 60:                      # if thMax > 60, belongs in original thread
    print("기존 Thread [%s]에 포함됩니다." % thMax)
  else:                                   # else if thMax < 60, add a new thread
    keywordList = getKeyword(text)
    reply = input("새로운 Thread [" + keywordList[0] + "]을(를) 추가하시겠습니까? (y/n): ")     # keywordList[0]: Main keyword

    try:
      if reply == "y":
        threadList.append(keywordList[0])
        print("새로운 Thread [%s]가 추가되었습니다." % keywordList[0])
      elif reply == "n":
        # new_thread = input("새로운 Thread를 직접 입력해주세요.\n(추천 키워드: %s, %s, %s, %s): " % (keywordList[1], keywordList[2], keywordList[3], keywordList[4]))
        other_keywords = ', '.join(keywordList[1:])
        new_thread = input("새로운 Thread를 직접 입력해주세요. (추천 키워드: %s): " % other_keywords)
        threadList.append(new_thread)
        print("새로운 Thread [%s]이(가) 추가되었습니다." % new_thread)
      else:
        raise ValueError
    except ValueError:
      print("잘못된 입력입니다.")

threadList = setDefaultThread()
print("\nDefault thread list: ", end="")
print(threadList)
print()

stopwords = {}
i = 1
for text in text_list:
  print("Text%d: " % i + text[:50] + "...")
  threadByKeyword(text)
  print()
  i += 1

print(threadList)