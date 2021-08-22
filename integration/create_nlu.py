from urllib.request import urlopen
import ssl
import json
import re
import unicodedata
from itertools import groupby
from word2number import w2n

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

dataTrain1 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_001.json", context=ctx).read().decode()
dataTrain2 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_002.json", context=ctx).read().decode()
dataTrain3 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_003.json", context=ctx).read().decode()
dataTrain4 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_004.json", context=ctx).read().decode()
dataTrain5 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_005.json", context=ctx).read().decode()
dataTrain6 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_006.json", context=ctx).read().decode()
dataTrain7 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_007.json", context=ctx).read().decode()
dataTrain8 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_008.json", context=ctx).read().decode()
dataTrain9 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_009.json", context=ctx).read().decode()
dataTrain10 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_010.json", context=ctx).read().decode()
dataTrain11 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_011.json", context=ctx).read().decode()
dataTrain12 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_012.json", context=ctx).read().decode()
dataTrain13 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_013.json", context=ctx).read().decode()
dataTrain14 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_014.json", context=ctx).read().decode()
dataTrain15 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_015.json", context=ctx).read().decode()
dataTrain16 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_016.json", context=ctx).read().decode()
dataTrain17 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/train/dialogues_017.json", context=ctx).read().decode()

dataTest1 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/test/dialogues_001.json", context=ctx).read().decode()
dataTest2 = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.2/test/dialogues_002.json", context=ctx).read().decode()

myJsonTrain1 = json.loads(dataTrain1)
myJsonTrain2 = json.loads(dataTrain2)
myJsonTrain3 = json.loads(dataTrain3)
myJsonTrain4 = json.loads(dataTrain4)
myJsonTrain5 = json.loads(dataTrain5)
myJsonTrain6 = json.loads(dataTrain6)
myJsonTrain7 = json.loads(dataTrain7)
myJsonTrain8 = json.loads(dataTrain8)
myJsonTrain9 = json.loads(dataTrain9)
myJsonTrain10 = json.loads(dataTrain10)
myJsonTrain11 = json.loads(dataTrain11)
myJsonTrain12 = json.loads(dataTrain12)
myJsonTrain13 = json.loads(dataTrain13)
myJsonTrain14 = json.loads(dataTrain14)
myJsonTrain15 = json.loads(dataTrain15)
myJsonTrain16 = json.loads(dataTrain16)
myJsonTrain17 = json.loads(dataTrain17)

myJsonTest1 = json.loads(dataTest1)
myJsonTest2 = json.loads(dataTest2)

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

timepat = re.compile("\d{1,2}[:]\d{1,2}")
pricepat = re.compile("\d{1,3}[.]\d{1,2}")

fin = urlopen("https://raw.githubusercontent.com/budzianowski/multiwoz/master/utils/mapping.pair", context=ctx)
replacements = []
for line in fin.readlines():
    line = line.decode().replace('\n', '')
    tok_from, tok_to = line.replace('\n', '').split('\t')
    replacements.append((' ' + tok_from + ' ', ' ' + tok_to + ' '))


def insertSpace(token, text):
    sidx = 0
    while True:
        sidx = text.find(token, sidx)
        if sidx == -1:
            break
        if sidx + 1 < len(text) and re.match('[0-9]', text[sidx - 1]) and \
                re.match('[0-9]', text[sidx + 1]):
            sidx += 1
            continue
        if text[sidx - 1] != ' ':
            text = text[:sidx] + ' ' + text[sidx:]
            sidx += 1
        if sidx + len(token) < len(text) and text[sidx + len(token)] != ' ':
            text = text[:sidx + 1] + ' ' + text[sidx + 1:]
        sidx += 1
    return text


def normalize(text):
    # lower case every word
    text = text.lower()

    # replace white spaces in front and end
    text = re.sub(r'^\s*|\s*$', '', text)

    # hotel domain pfb30
    text = re.sub(r"b&b", "bed and breakfast", text)
    text = re.sub(r"b and b", "bed and breakfast", text)

    # normalize phone number
    ms = re.findall('\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4,5})', text)
    if ms:
        sidx = 0
        for m in ms:
            sidx = text.find(m[0], sidx)
            if text[sidx - 1] == '(':
                sidx -= 1
            eidx = text.find(m[-1], sidx) + len(m[-1])
            text = text.replace(text[sidx:eidx], ''.join(m))

    # normalize postcode
    ms = re.findall('([a-z]{1}[\. ]?[a-z]{1}[\. ]?\d{1,2}[, ]+\d{1}[\. ]?[a-z]{1}[\. ]?[a-z]{1}|[a-z]{2}\d{2}[a-z]{2})',
                    text)
    if ms:
        sidx = 0
        for m in ms:
            sidx = text.find(m, sidx)
            eidx = sidx + len(m)
            text = text[:sidx] + re.sub('[,\. ]', '', m) + text[eidx:]

    # weird unicode bug
    text = re.sub(u"(\u2018|\u2019)", "'", text)

    # replace time and and price
    times = re.findall(timepat, text)
    prices = re.findall(pricepat, text)
    text = re.sub(timepat, ' [value_time] ', text)
    text = re.sub(pricepat, ' [value_price] ', text)
    #text = re.sub(pricepat2, '[value_price]', text)

    # replace st.
    text = text.replace(';', ',')
    text = re.sub('$\/', '', text)
    text = text.replace('/', ' and ')

    # replace other special characters
    text = text.replace('-', ' ')
    text = re.sub('[\":\<>@\(\)]', '', text)

    # insert white space before and after tokens:
    for token in ['?', '.', ',', '!']:
        text = insertSpace(token, text)

    # insert white space for 's
    text = insertSpace('\'s', text)

    # replace it's, does't, you'd ... etc
    text = re.sub('^\'', '', text)
    text = re.sub('\'$', '', text)
    text = re.sub('\'\s', ' ', text)
    text = re.sub('\s\'', ' ', text)
    for fromx, tox in replacements:
        text = ' ' + text + ' '
        text = text.replace(fromx, tox)[1:-1]

    # remove multiple spaces
    text = re.sub(' +', ' ', text)

    # concatenate numbers
    tmp = text
    tokens = text.split()
    i = 1
    while i < len(tokens):
        if re.match(u'^\d+$', tokens[i]) and \
                re.match(u'\d+$', tokens[i - 1]):
            tokens[i - 1] += tokens[i]
            del tokens[i]
        else:
            i += 1
    text = ' '.join(tokens)

    for time in times:
      text = re.sub('\\[value_time\\]', time, text, 1)

    for price in prices:
      text = re.sub('\\[value_price\\]', price, text, 1)

    return text

def splitWithIndices(s, c=' '):
  p = 0
  for k, g in groupby(s, lambda x:x==c):
   q = p + sum(1 for i in g)
   if not k:
    yield p, q
   p = q

# possibleIntents = {"find_res_pricerange_area_food": [], "find_res_pricerange_area": [], "find_res_pricerange_food": [], 
# "find_res_area_food": [], "find_res_area": [], "find_res_pricerange": [], "find_res_food": [], "find_res":[],
# "book_res_booktime_bookday_bookpeople_name":[], "book_res_booktime_bookday_bookpeople":[], "book_res_booktime_bookday_name":[], 
# "book_res_booktime_bookpeople_name":[],"book_res_bookday_bookpeople_name":[],"book_res_booktime_bookday":[],"book_res_booktime_bookpeople":[],
# "book_res_bookday_bookpeople":[], "book_res_booktime_name":[], "book_res_bookday_name":[], "book_res_bookpeople_name":[],
# "book_res_name": [], "book_res_bookpeople": [], "book_res_bookday": [], "book_res_booktime": [], "book_res": []}

possibleIntents = {"find_res": [], "book_res": []}

# def getCurrIntent(slot_values, active_intent):
#   slot_values = slot_values.values()

#   if (active_intent == "find_restaurant"):
#     if "restaurant-area" in slot_values:
#       if "restaurant-food" in slot_values:
#         if "restaurant-pricerange" in slot_values : return "find_res_pricerange_area_food"
#         else : return "find_res_area_food"
#       elif "restaurant-pricerange" in slot_values : return "find_res_pricerange_area"
#       else : return "find_res_area"

#     elif "restaurant-food" in slot_values:
#       if "restaurant-pricerange" in slot_values : return "find_res_pricerange_food"
#       else : return "find_res_food"

#     elif "restaurant-pricerange" in slot_values: return "find_res_pricerange"

#     else : return "find_res"

#   else: # book
#     if "restaurant-booktime" in slot_values:
#       if "restaurant-bookday" in slot_values:
#         if "restaurant-bookpeople" in slot_values:
#           if "restaurant-name" in slot_values : return "book_res_booktime_bookday_bookpeople_name"
#           else : return "book_res_booktime_bookday_bookpeople"

#         elif "restaurant-name" in slot_values : return "book_res_booktime_bookday_name"
#         else : return "book_res_booktime_bookday"

#       elif "restaurant-bookpeople" in slot_values:
#         if "restaurant-name" in slot_values : return "book_res_booktime_bookpeople_name"
#         else : return "book_res_booktime_bookpeople"
      
#       elif "restaurant-name" in slot_values : return "book_res_booktime_name"
      
#       else : return "book_res_booktime"

#     elif "restaurant-bookday" in slot_values:
#       if "restaurant-bookpeople" in slot_values:
#         if "restaurant-name" in slot_values : return "book_res_bookday_bookpeople_name"
#         else : return "book_res_bookday_bookpeople"

#       elif "restaurant-name" in slot_values : return "book_res_bookday_name"

#       else : return "book_res_bookday"

#     elif "restaurant-bookpeople" in slot_values:
#       if "restaurant-name" in slot_values : return "book_res_bookpeople_name"
#       else : return "book_res_bookpeople"

#     elif "restaurant-name" in slot_values : return "book_res_name"

#     else : return "book_res"
        
_SIMILAR_WORDS = {
    'portuguese': ['portugese', 'portugeuese'],
    '01:30': ['1 thirty p  m'],
    '16:30': ['after 16:00'],
    'anatolia': ['anatoilia'],
    'allenbell': ['allenball'],
    'caribbean': ['carribbean'],
    'seafood': ['sea food'],
    'moroccan': ['morrocan'],
    'avalon': ['avaion'],
    'barbeque': ['bbq'],
    'american': ['americas'],
    'italian': ['pizza place'],
    'indian': ['taj tandoori'],
    'british': ['english'],
    'cambridge': ['cambride'],
    'fen ditton': ['fenditton'],
    'caffe': ['cafe'],
    'gonville': ['gonvile'],
    'shaddia': ['shaddai'],
    'center': ['centre'],
    'centre': ['center'],
    'japanese': ['japanise']
}

def filter(data):
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
                      the_active_intent = None
                      for frame in frames: 
                          state = frame.get("state", None)
                          service = frame.get("service", None)
                          if state : active_intent = state.get("active_intent", None)
                          if service and service == "restaurant" and state and active_intent and (active_intent == "book_restaurant" or active_intent == "find_restaurant"):
                              slot_values = state.get("slot_values", None)
                              if slot_values and len(slot_values) != 0:
                                  for key, value in slot_values.items():
                                      for elem in value:
                                        dic[elem] = key.replace('-', '_')

                                  the_active_intent = active_intent


                      if len(dic) > 0 and the_active_intent:
                        # se a frase só tem other...
                        onlyOther = True

                        # ver o tipo de frase que estamos lidando
                        currIntent = the_active_intent.replace("restaurant", "res")

                        # bad dataset
                        if "steakhouses" in dic.keys() and "steakhouse" in dic.keys() : dic.pop("steakhouses")
                        if "corsican" in dic.keys() and "corsica" in dic.keys() : dic.pop("corsican")
                        if "gastropubs" in dic.keys() and "gastropub" in dic.keys() : dic.pop("gastropubs")
                        if "carribbean" in dic.keys() and "caribbean" in dic.keys() : dic.pop("carribbean")
                        if "portugese" in dic.keys() and "portuguese" in dic.keys() : dic.pop("portugese")
                        if "sea food" in dic.keys() and "seafood" in dic.keys() : dic.pop("sea food")
                        if "american" in dic.keys() and "americas" in dic.keys() : dic.pop("americas")
                        if "moroccan" in dic.keys() and "morrocan" in dic.keys() : dic.pop("morrocan")
                        if "east" in dic.keys() and "eastern european" in dic.keys() : dic.pop("eastern european")
                        if "bbq" in dic.keys() and "barbeque" in dic.keys() : dic.pop("bbq")
                        if utterance == "Where is the Addenbrookes Hospital located?" : continue
                        if utterance == "I need a restaurant called the bedouin for the same group of people at 14:15 and I would need the reference number." : continue
                        if utterance == "Can you book me a table at nandos city centre for 21:00 and give me a ref number" : continue
                        if utterance == "Can you help me find a restaurant in the south that doesn't cost a lot of money. In fact, I need one that's quite inexpensive." : continue

                        # tirar pontuação
                        noPontuationText = ""
                        lastLetter = None
                        for letter in utterance.strip():
                            if not _is_punctuation(letter) or letter==':' or letter=='/': 
                                if letter != ' ' or lastLetter != ' ':
                                  noPontuationText += letter
                                  lastLetter = letter
                            elif lastLetter != ' ':
                                noPontuationText += ' '
                                lastLetter = ' '

                        # tentar achar labels na frase original (sem pontuação)
                        gotItems = []
                        for word, slot_values in dic.items():
                            if word in noPontuationText:
                                selectedMatch = None
                                for match in re.finditer(re.escape(word), noPontuationText):
                                    if (match.start() == 0 or noPontuationText[match.start()-1] == ' ') and (len(noPontuationText) == match.end() or noPontuationText[match.end()] == ' '):
                                        selectedMatch = (match.start(), match.end())
                                        break

                                if selectedMatch:
                                    noPontuationText = noPontuationText[:selectedMatch[0]] + '[' + noPontuationText[selectedMatch[0]:selectedMatch[1]] + ']' + '{"entity": "' + slot_values + '", "value": "' + word + '"}' + noPontuationText[selectedMatch[1]:]

                                    gotItems.append(word)

                            elif _SIMILAR_WORDS.get(word, None):
                                for _word in _SIMILAR_WORDS.get(word):
                                    if _word in noPontuationText:
                                        selectedMatch = None
                                        for match in re.finditer(re.escape(_word), noPontuationText):
                                            if (match.start() == 0 or noPontuationText[match.start()-1] == ' ') and (len(noPontuationText) == match.end() or noPontuationText[match.end()] == ' '):
                                                selectedMatch = (match.start(), match.end())
                                                break

                                        if selectedMatch:
                                            noPontuationText = noPontuationText[:selectedMatch[0]] + '[' + noPontuationText[selectedMatch[0]:selectedMatch[1]] + ']' + '{"entity": "' + slot_values + '", "value": "' + word + '"}' + noPontuationText[selectedMatch[1]:]

                                            gotItems.append(word)
                                            break


                        for key in gotItems:
                            if key != "O" : onlyOther = False
                            dic.pop(key)

                        # tentar achar labels na frase original (sem pontuação) com lower case
                        gotItems = []
                        for word, slot_values in dic.items():
                            if word in noPontuationText.lower():
                                selectedMatch = None
                                for match in re.finditer(re.escape(word), noPontuationText.lower()):
                                    if (match.start() == 0 or noPontuationText[match.start()-1] == ' ') and (len(noPontuationText) == match.end() or noPontuationText[match.end()] == ' '):
                                        selectedMatch = (match.start(), match.end())
                                        break

                                if selectedMatch:
                                    noPontuationText = noPontuationText[:selectedMatch[0]] + '[' + noPontuationText[selectedMatch[0]:selectedMatch[1]] + ']' + '{"entity": "' + slot_values + '", "value": "' + word + '"}' + noPontuationText[selectedMatch[1]:]

                                    gotItems.append(word)

                            elif _SIMILAR_WORDS.get(word, None):
                                for _word in _SIMILAR_WORDS.get(word):
                                    if _word in noPontuationText.lower():
                                        selectedMatch = None
                                        for match in re.finditer(re.escape(_word), noPontuationText.lower()):
                                            if (match.start() == 0 or noPontuationText[match.start()-1] == ' ') and (len(noPontuationText) == match.end() or noPontuationText[match.end()] == ' '):
                                                selectedMatch = (match.start(), match.end())
                                                break

                                        if selectedMatch:
                                            noPontuationText = noPontuationText[:selectedMatch[0]] + '[' + noPontuationText[selectedMatch[0]:selectedMatch[1]] + ']' + '{"entity": "' + slot_values + '", "value": "' + word + '"}' + noPontuationText[selectedMatch[1]:]

                                            gotItems.append(word)
                                            break

                        for key in gotItems:
                            if key != "O" : onlyOther = False
                            dic.pop(key)

                        # tentar achar labels na frase original (sem pontuação) com normalizacao de palavras
                        gotItems = []
                        wordsIndices = splitWithIndices(noPontuationText)
                        
                        for word, slot_values in dic.items():
                            for wStartIndex, wEndIndex in wordsIndices:
                                normalizedWord = normalize(noPontuationText[wStartIndex:wEndIndex])
                                similarWords = _SIMILAR_WORDS.get(word, None)
                                if word == normalizedWord:
                                    noPontuationText = noPontuationText[:wStartIndex] + '[' + noPontuationText[wStartIndex:wEndIndex] + ']' + '{"entity": "' + slot_values + '", "value": "' + word + '"}' + noPontuationText[wEndIndex:]
                                  
                                    gotItems.append(word)
                                    continue

                                if similarWords:
                                    for _word in similarWords:
                                        if _word == normalizedWord:
                                            noPontuationText = noPontuationText[:wStartIndex] + '[' + noPontuationText[wStartIndex:wEndIndex] + ']' + '{"entity": "' + slot_values + '", "value": "' + word + '"}' + noPontuationText[wEndIndex:]

                                            gotItems.append(word)
                                            break
                                
                                normalizedWord = None
                                try:
                                    normalizedWord = w2n.word_to_num(noPontuationText[wStartIndex:wEndIndex])
                                except: pass

                                if normalizedWord and word == normalizedWord:
                                    noPontuationText = noPontuationText[:wStartIndex] + '[' + noPontuationText[wStartIndex:wEndIndex] + ']' + '{"entity": "' + slot_values + '", "value": "' + word + '"}' + noPontuationText[wEndIndex:]
                                
                                    gotItems.append(word)
                                
                                elif similarWords and normalizedWord:
                                    for _word in similarWords:
                                        if _word == normalizedWord:
                                            noPontuationText = noPontuationText[:wStartIndex] + '[' + noPontuationText[wStartIndex:wEndIndex] + ']' + '{"entity": "' + slot_values + '", "value": "' + word + '"}' + noPontuationText[wEndIndex:]

                                            gotItems.append(word)
                                            break


                        for key in gotItems:
                            if key != "O" : onlyOther = False
                            dic.pop(key)

                        # tentar achar labels na frase original (sem pontuação)
                        gotItems = []
                        for word, slot_values in dic.items():
                            if word in noPontuationText:
                                selectedMatch = None
                                for match in re.finditer(re.escape(word), noPontuationText):
                                    if (match.start() == 0 or noPontuationText[match.start()-1] == ' ') and (len(noPontuationText) == match.end() or noPontuationText[match.end()] == ' '):
                                        selectedMatch = (match.start(), match.end())
                                        break

                                if selectedMatch is None:
                                    for match in re.finditer(re.escape(word), noPontuationText):
                                        selectedMatch = (match.start(), match.end())
                                        break

                                    for index, letter in enumerate(noPontuationText):
                                        if index < selectedMatch[1]: continue

                                        if letter == ' ' : 
                                          selectedMatch = (selectedMatch[0], index)
                                          break

                                noPontuationText = noPontuationText[:selectedMatch[0]] + '[' + noPontuationText[selectedMatch[0]:selectedMatch[1]] + ']' + '{"entity": "' + slot_values + '", "value": "' + word + '"}' + noPontuationText[selectedMatch[1]:]

                                gotItems.append(word)

                            elif _SIMILAR_WORDS.get(word, None):
                                for _word in _SIMILAR_WORDS.get(word):
                                    if _word in noPontuationText:
                                        selectedMatch = None
                                        for match in re.finditer(re.escape(_word), noPontuationText):
                                            if (match.start() == 0 or noPontuationText[match.start()-1] == ' ') and (len(noPontuationText) == match.end() or noPontuationText[match.end()] == ' '):
                                                selectedMatch = (match.start(), match.end())
                                                break

                                        if selectedMatch is None: 
                                            for match in re.finditer(re.escape(_word), noPontuationText):
                                                selectedMatch = (match.start(), match.end())
                                                break

                                            for index, letter in enumerate(noPontuationText):
                                                if index < selectedMatch[1]: continue

                                                if letter == ' ' : 
                                                    selectedMatch = (selectedMatch[0], index)
                                                    break

                                        noPontuationText = noPontuationText[:selectedMatch[0]] + '[' + noPontuationText[selectedMatch[0]:selectedMatch[1]] + ']' + '{"entity": "' + slot_values + '", "value": "' + word + '"}' + noPontuationText[selectedMatch[1]:]

                                        gotItems.append(word)
                                        break


                        for key in gotItems:
                            if key != "O" : onlyOther = False
                            dic.pop(key)

                        # tentar achar labels na frase original (sem pontuação) com lower case
                        gotItems = []
                        for word, slot_values in dic.items():
                            if word in noPontuationText.lower():
                                selectedMatch = None

                                for match in re.finditer(re.escape(word), noPontuationText.lower()):
                                    selectedMatch = (match.start(), match.end())
                                    break

                                for index, letter in enumerate(noPontuationText):
                                    if index < selectedMatch[1]: continue

                                    if letter == ' ' : 
                                        selectedMatch = (selectedMatch[0], index)
                                        break

                                noPontuationText = noPontuationText[:selectedMatch[0]] + '[' + noPontuationText[selectedMatch[0]:selectedMatch[1]] + ']' + '{"entity": "' + slot_values + '", "value": "' + word + '"}' + noPontuationText[selectedMatch[1]:]

                                gotItems.append(word)

                            elif _SIMILAR_WORDS.get(word, None):
                                for _word in _SIMILAR_WORDS.get(word):
                                    if _word in noPontuationText.lower():
                                        selectedMatch = None

                                        for match in re.finditer(re.escape(_word), noPontuationText.lower()):
                                            selectedMatch = (match.start(), match.end())
                                            break

                                        for index, letter in enumerate(noPontuationText):
                                            if index < selectedMatch[1]: continue

                                            if letter == ' ' : 
                                                selectedMatch = (selectedMatch[0], index)
                                                break

                                        noPontuationText = noPontuationText[:selectedMatch[0]] + '[' + noPontuationText[selectedMatch[0]:selectedMatch[1]] + ']' + '{"entity": "' + slot_values + '", "value": "' + word + '"}' + noPontuationText[selectedMatch[1]:]

                                        gotItems.append(word)
                                        break

                        for key in gotItems:
                            if key != "O" : onlyOther = False
                            dic.pop(key)

                        
                        # if the_active_intent == "book_restaurant" : print(noPontuationText)
                          
                        if not onlyOther and len(dic) == 0: possibleIntents[currIntent].append(noPontuationText.strip())

filter(myJsonTrain1)
filter(myJsonTrain2)
filter(myJsonTrain3)
filter(myJsonTrain4)
filter(myJsonTrain5)
filter(myJsonTrain6)
filter(myJsonTrain7)
filter(myJsonTrain8)
filter(myJsonTrain9)
filter(myJsonTrain10)
filter(myJsonTrain11)
filter(myJsonTrain12)
filter(myJsonTrain13)
filter(myJsonTrain14)
filter(myJsonTrain15)
filter(myJsonTrain16)
filter(myJsonTrain17)
filter(myJsonTest1)
filter(myJsonTest2)

f = open("nlu.yml", "w")
f.write("nlu:\n")
for pInt, lista in possibleIntents.items():
  f.write(f'- intent: {pInt}\n')
  f.write("  examples: |\n")
  f.writelines([f'    - {phrase}\n' for phrase in lista])
  f.write('\n')

f.close()