import json
data = json.load(open('dev-v1.1.json'))
para = data['data']
count = 0 # Question count
flag = 0
unknown = 0 # Unknown question count
unknown_qlength = 0
unknown_anslength = 0
dictionary = []
stats = {'what':0,'who':0,'when':0,'why':0,'how':0,'whom':0,'whose':0,'where':0,'which':0}
q_length = {'what':0,'who':0,'when':0,'why':0,'how':0,'whom':0,'whose':0,'where':0,'which':0}
ans_length = {'what':0,'who':0,'when':0,'why':0,'how':0,'whom':0,'whose':0,'where':0,'which':0}
for s in para:
    para2 = s['paragraphs']
    for str in para2:
        para1 = str['qas']
        for string in para1:
            cur_ques = string['question']
            cur_ans = string['answers'][0]['text']
            words = cur_ques.split()
            ans_words = cur_ans.split()
            flag = 0
            for i in range(0,len(ans_words)):
                ans_words[i] = ans_words[i].lower()
                if ans_words[i] not in dictionary:
                    dictionary.append(ans_words[i])
            for i in range(0,len(words)):
                words[i] = words[i].lower()
                for key in stats:
                    if(key == words[i]):
                        stats[key] += 1
                        q_length[key] += len(words)
                        ans_length[key] += len(ans_words)
                        flag = 1
                if words[i] not in dictionary:
                    dictionary.append(words[i])
            count += 1
            
            if(flag == 0):
                unknown += 1
                unknown_qlength += len(words)
                unknown_anslength += len(ans_words)
print("Test set Analysis:")
print("Question count : ",count)
for key in stats:
    print(key,stats[key],q_length[key]/stats[key],ans_length[key]/stats[key])
print("Other question count : ",unknown)
print("Other question avg length : ",unknown_qlength/unknown)
print("Other answer avg length : ",unknown_anslength/unknown)
