import numpy as np

from pycm import ConfusionMatrix

data = []
data_labels = []

negative_file = 'manual_annotation/manual_annotation_talak_c/talak_c_negative.txt'
positive_file = 'manual_annotation/manual_annotation_talak_c/talak_c_positive.txt'

print('read data ...')
# read positive data
with open(positive_file, encoding='utf-8') as f:
    for i in f:
        data.append(i)
        data_labels.append('pos')

# read negative data
with open(negative_file, encoding='utf-8') as f:
    for i in f:
        data.append(i)
        data_labels.append('neg')

print('data size', len(data_labels))
print('# of positive', data_labels.count('pos'))
print('# of negative', data_labels.count('neg'))

# load lexicons

positive_lexicon_file = 'positive_lexicon.txt'
negative_lexicon_file = 'negative_lexicon.txt'

positive_lexicon = open(positive_lexicon_file, encoding='utf-8').read().splitlines()
negative_lexicon = open(negative_lexicon_file, encoding='utf-8').read().splitlines()

print(positive_lexicon)
print(negative_lexicon)


def classify_tweet(text):
    pos_count = 0
    neg_count = 0
    for word in text.split():
        if word in positive_lexicon:
            pos_count += 1
        elif word in negative_lexicon:
            neg_count += 1
    if pos_count > neg_count:
        return 'pos'
    elif neg_count > pos_count:
        return 'neg'
    elif pos_count == neg_count == 0:
        return 'neut'
    else:
        return 'mix'


predictions = []
for tweet in data:
    predictions.append(classify_tweet(tweet))

for l, p in zip(data_labels, predictions):
    print(l, p)

label_names = ['neg', 'pos', 'neut', 'mix']
pred_labels = np.asarray([label_names.index(p) for p in predictions])
true_labels = np.asarray([label_names.index(y) for y in data_labels])
cm = ConfusionMatrix(actual_vector=true_labels, predict_vector=pred_labels)  # Create CM From Data
print(cm.classes)
print(cm)
print('----------- summary results -----------------')
print('ACC(Accuracy)', cm.class_stat.get('ACC'))
print('F1 score', cm.class_stat.get('F1'))
print('Accuracy AVG', sum(cm.class_stat.get('ACC').values()) / len(cm.class_stat.get('ACC')))
print('F1 AVG', sum(cm.class_stat.get('F1').values()) / len(cm.class_stat.get('F1')))
print('Recall', cm.class_stat.get('TPR')[1])
print('----------------------------------------------')