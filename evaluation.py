import numpy as np


def evaluation(predictions, y_list):
    label_names = ['neg', 'pos', 'neut', 'mix']
    pred_labels = np.asarray([label_names.index(p) for p in predictions])
    true_labels = np.asarray([label_names.index(y) for y in y_list])
    # print('pred_labels.shape:', pred_labels.shape)
    # print('true_labels.shape:', true_labels.shape)
    # print('len(predictions):', len(predictions))
    # print('len(y_list):', len(y_list))
    # True Positive (TP): we predict a label of 1 (positive), and the true label is 1.
    TP = np.sum(np.logical_and(pred_labels == 1, true_labels == 1))
    # True Negative (TN): we predict a label of 0 (negative), and the true label is 0.
    TN = np.sum(np.logical_and(pred_labels == 0, true_labels == 0))
    # False Positive (FP): we predict a label of 1 (positive), but the true label is 0.
    FP = np.sum(np.logical_and(pred_labels == 1, true_labels == 0))
    # False Negative (FN): we predict a label of 0 (negative), but the true label is 1.
    FN = np.sum(np.logical_and(pred_labels == 0, true_labels == 1))
    print('TP: %i, FP: %i, TN: %i, FN: %i' % (TP, FP, TN, FN))
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    accuracy = (TP + TN) / (TP + TN + FP + FN)
    print('TP + TN + FP + FN = ', TP + TN + FP + FN)
    f_score = (2 * precision * recall) / (precision + recall)
    return accuracy, precision, recall, f_score


data = []
data_labels = []

positive_file = 'manual_annotation/manual_annotation_healthcare/healthcare_negative.txt'
negative_file = 'manual_annotation/manual_annotation_healthcare/healthcare_positive.txt'

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

positive_lexicon = open(positive_file, encoding='utf-8').read().splitlines()
negative_lexicon = open(negative_lexicon_file, encoding='utf-8').read().splitlines()


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

accuracy, precision, recall, f_score = evaluation(predictions, data_labels)
print('accuracy: {}'.format(precision))
print('precision: {}'.format(precision))
print('recall: {}'.format(recall))
print('f-score: {}'.format(f_score))
