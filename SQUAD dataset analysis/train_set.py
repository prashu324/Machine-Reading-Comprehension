import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = json.load(open('train-v1.1.json'))
data = pd.Series(data)
para = data['data']
count = 0 # Question count
flag = 0
unknown = 0
unknown_qlength = 0
unknown_anslength = 0
dictionary = []
titles = []
context_count = 0
context_length = 0
word_count = 0
stats = pd.Series({'what':0,'who':0,'when':0,'why':0,'how':0,'where':0,'which':0})
q_length = pd.Series({'what':0,'who':0,'when':0,'why':0,'how':0,'where':0,'which':0})
ans_length = pd.Series({'what':0,'who':0,'when':0,'why':0,'how':0,'where':0,'which':0})
for s in para:
    titles.append(s['title'])
    title_words = s['title'].split()
    word_count += len(title_words)
    for word in title_words:
        word = word.lower()
        if word not in dictionary:
            dictionary.append(word)
    para2 = s['paragraphs']
    for str in para2:
        context_count += 1
        context = str['context'].lower()
        context_words = context.split()
        word_count += len(context_words)
        context_length += len(context_words)
        for word in context_words:
            if word not in dictionary:
                dictionary.append(word)
        para1 = str['qas']
        for string in para1:
            cur_ques = string['question']
            cur_ans = string['answers'][0]['text']
            words = cur_ques.split()
            ans_words = cur_ans.split()
            flag = 0
            word_count = word_count + len(cur_ques) + len(cur_ans)
            for i in range(0,len(ans_words)):
                ans_words[i] = ans_words[i].lower()
                if ans_words[i] not in dictionary:
                    dictionary.append(ans_words[i])
            for i in range(0,len(words)):
                words[i] = words[i].lower()
                for key in stats.index:
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
                
# Adding other type questions to question types
stats['other'] = unknown
q_length['other'] = unknown_qlength
ans_length['other'] = unknown_anslength

print("Training set Analysis:")
for key in stats.index:
    print(key,stats[key],round(q_length[key]/stats[key],2),round(ans_length[key]/stats[key],2))

print("Total Question count : ",count)
print("Total word count : ",word_count)
print("Total context count : ",context_count)
print("Total titles count : ",len(titles))
print("Avg. Context length : ",round(context_length / context_count))
print("Avg Question length : ",round(np.sum(q_length)/count,2))
print("Avg Answer length : ",round(np.sum(ans_length)/count,2))
print("Avg questions per context : ",round(count / context_count,2))

# Freqpuencies bar graph
plt.figure(figsize=(8,5))
plt.bar(stats.index,[stats[key] for key in stats.index],width = 0.5, color = 'red',label = 'Frequency of questions')
plt.xlabel('Question type')
plt.ylabel('Frequency')
plt.title('Question type frequencies')
plt.legend(loc = 'upper right', bbox_to_anchor=(1, 0, 0.5, 1))
plt.show()

# Question type distribution Pie chart
fig,ax = plt.subplots(figsize=(8,5))
ax.pie(stats,labels = stats.index, startangle = 90, shadow = True)
ax.legend(title = 'Question types', loc = 'center right', bbox_to_anchor=(1, 0, 0.5, 1))
ax.set_title('Question type Distribution', loc = 'center')
plt.show()

# Avg quesiton and answer lengths bar graph
index = np.arange(len(stats))
fig,ax = plt.subplots(figsize=(8,5))
rects1 = ax.bar(index,[q_length[key]/stats[key] for key in stats.index],color = 'red', label = 'Avg Question length',width = 0.35)
rects2 = ax.bar(index + 0.35,[ans_length[key]/stats[key] for key in stats.index],color = 'blue', label = 'Avg Answer length', width = 0.35)
ax.set_ylim(0,12)
ax.set_xlabel('Question type ')
ax.set_ylabel('Avg. length')
ax.set_title('Avg. Question and Answer lengths')
ax.set_xticks(index + 0.35/2)
ax.set_xticklabels(stats.index)
ax.legend(bbox_to_anchor=(1, 0, 0.5, 1), loc = 'upper right')
plt.show()