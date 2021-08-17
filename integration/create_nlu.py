from urllib.request import urlopen
import ssl
import json
import re
import unicodedata

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# dataTrain1 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_001.json", context=ctx).read().decode()
# dataTrain2 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_002.json", context=ctx).read().decode()
# dataTrain3 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_003.json", context=ctx).read().decode()
# dataTrain4 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_004.json", context=ctx).read().decode()
# dataTrain5 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_005.json", context=ctx).read().decode()
# dataTrain6 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_006.json", context=ctx).read().decode()
# dataTrain7 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_007.json", context=ctx).read().decode()
# dataTrain8 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_008.json", context=ctx).read().decode()
# dataTrain9 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_009.json", context=ctx).read().decode()
# dataTrain10 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_010.json", context=ctx).read().decode()
# dataTrain11 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_011.json", context=ctx).read().decode()
# dataTrain12 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_012.json", context=ctx).read().decode()
# dataTrain13 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_013.json", context=ctx).read().decode()
# dataTrain14 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_014.json", context=ctx).read().decode()
# dataTrain15 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_015.json", context=ctx).read().decode()
# dataTrain16 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_016.json", context=ctx).read().decode()
# dataTrain17 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_017.json", context=ctx).read().decode()

dataTest1 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/test/dialogues_001.json", context=ctx).read().decode()
# dataTest2 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/test/dialogues_002.json", context=ctx).read().decode()

# myJsonTrain1 = json.loads(dataTrain1)
# myJsonTrain2 = json.loads(dataTrain2)
# myJsonTrain3 = json.loads(dataTrain3)
# myJsonTrain4 = json.loads(dataTrain4)
# myJsonTrain5 = json.loads(dataTrain5)
# myJsonTrain6 = json.loads(dataTrain6)
# myJsonTrain7 = json.loads(dataTrain7)
# myJsonTrain8 = json.loads(dataTrain8)
# myJsonTrain9 = json.loads(dataTrain9)
# myJsonTrain10 = json.loads(dataTrain10)
# myJsonTrain11 = json.loads(dataTrain11)
# myJsonTrain12 = json.loads(dataTrain12)
# myJsonTrain13 = json.loads(dataTrain13)
# myJsonTrain14 = json.loads(dataTrain14)
# myJsonTrain15 = json.loads(dataTrain15)
# myJsonTrain16 = json.loads(dataTrain16)
# myJsonTrain17 = json.loads(dataTrain17)

myJsonTest1 = json.loads(dataTest1)
# myJsonTest2 = json.loads(dataTest2)

def _is_punctuation(char):
  """Checks whether `chars` is a punctuation character."""
  cp = ord(char)
  # We treat all non-letter/number ASCII as punctuation.
  # Characters such as "^", "$", and "`" are not in the Unicode
  # Punctuation class but we treat them as punctuation anyways, for
  # consistency.
  if ((cp >= 33 and cp <= 47) or (cp >= 58 and cp <= 64) or
      (cp >= 91 and cp <= 96) or (cp >= 123 and cp <= 126)):
    return True
  cat = unicodedata.category(char)
  if cat.startswith("P"):
    return True
  return False

possibleIntents = ["find_res_pricerange_area_food", "find_res_pricerange_area", "find_res_pricerange_food", 
"find_res_area_food", "find_res_area", "find_res_pricerange", "find_res_food", "find_res",
"book_res_ booktime_bookday_bookpeople_name", "book_res_booktime_bookday_bookpeople_name", "book_res_booktime_bookday_bookpeople",
"book_res_booktime_bookday_name", "book_res_booktime_bookpeople_name", "book_res_bookday_bookpeople_name", "book_res_booktime_bookday",
"book_res_booktime_bookpeople", "book_res_bookday_bookpeople", "book_res_booktime_name", "book_res_bookday_name", "book_res_bookpeople_name",
"book_res_name", "book_res_bookpeople", "book_res_bookday", "book_res_booktime", "book_res"]

def filter(data):
  result = []

  for i, obj in enumerate(data):
      turns = obj.get("turns", None)
      for turn in turns:
          if turn:
              utterance = turn.get("utterance", None)
              speaker = turn.get("speaker", None)
              if utterance and speaker and speaker == "USER":
                  frames = turn.get("frames", None)
                  if frames:
                      dic = dict()
                      res = [[], []]
                      for frame in frames: 
                          state = frame.get("state", None)
                          service = frame.get("service", None)
                          if state : active_intent = state.get("active_intent", None)
                          if service and service == "restaurant" and state and active_intent and (active_intent == "book_restaurant" or active_intent == "find_restaurant"):
                              slot_values = state.get("slot_values", None)
                              if slot_values and len(slot_values) != 0:
                                  for key, value in slot_values.items():
                                      for elem in value:
                                        dic[elem] = key


                      if len(dic) > 0:
                        # se a frase só tem other...
                        onlyOther = True

                        noPontuationText = ""
                        for letter in utterance.strip():
                            if not _is_punctuation(letter) : 
                                noPontuationText += letter

                        gotItems = []
                        for word, slot_values in dic.items():
                            if word in noPontuationText:
                                for match in re.finditer(re.escape(word), noPontuationText):
                                    noPontuationText = noPontuationText[:match.start()] + '[' + noPontuationText[match.start():match.end()] + ']' + f'({slot_values})' + noPontuationText[match.end():]
                                    break

                                gotItems.append(word)

                        for key in gotItems:
                            if key != "O" : onlyOther = False
                            dic.pop(key)
                          
                        if not onlyOther : result.append(noPontuationText)

  return result

print(filter(myJsonTest1)[0:50])