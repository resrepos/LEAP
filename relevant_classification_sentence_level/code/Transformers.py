#!/usr/bin/env python
# coding: utf-8

import openpyxl
import xlrd
import simpletransformers
import pandas as pd
import logging
import torch
import sklearn
import math
import json
import dataframe_image as dfi
from simpletransformers.classification import ClassificationModel, ClassificationArgs
import sys
import argparse
#import resource, sys
#resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(100000)
print(sys.getrecursionlimit())

print('importing complete')
logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

def latex(path):
    
    with open(path) as f:
        data = json.load(f)

    diction = {'Model_Name': [], 'MCC': [], 'eval_loss':[], 'accuracy':[],
               'weighted_avg_f1-score':[], 'weighted_avg_precision': [], 'weighted_avg_recall': [],
               'macro_avg_f1-score':[], 'macro_avg_precision': [], 'macro_avg_recall': []}
    
    
    for d in data.items():
        #diction[d[0][d[0].index('/')+1:]]=
        diction['Model_Name'].append(d[0][d[0].index('/')+1:])
        mcc = float("{:.2f}".format(d[1]["mcc"]))
        diction['MCC'].append(mcc)
        eval_loss = float("{:.2f}".format(d[1]["eval_loss"]))
        diction['eval_loss'].append(eval_loss)
        diction['accuracy'].append(d[1]["classification_report"][d[1]["classification_report"].index('accuracy')+35:d[1]["classification_report"].index('accuracy')+39])

        diction['macro_avg_precision'].append(d[1]["classification_report"][d[1]["classification_report"].index('macro avg')+16:d[1]["classification_report"].index('macro avg')+20])
        diction['macro_avg_recall'].append(d[1]["classification_report"][d[1]["classification_report"].index('macro avg')+26:d[1]["classification_report"].index('macro avg')+30])
        diction['macro_avg_f1-score'].append(d[1]["classification_report"][d[1]["classification_report"].index('macro avg')+36:d[1]["classification_report"].index('macro avg')+40])

        diction['weighted_avg_precision'].append(d[1]["classification_report"][d[1]["classification_report"].index('weighted avg')+19:d[1]["classification_report"].index('weighted avg')+23])
        diction['weighted_avg_recall'].append(d[1]["classification_report"][d[1]["classification_report"].index('weighted avg')+29:d[1]["classification_report"].index('weighted avg')+33])
        diction['weighted_avg_f1-score'].append(d[1]["classification_report"][d[1]["classification_report"].index('weighted avg')+39:d[1]["classification_report"].index('weighted avg')+43])

    df = pd.DataFrame.from_dict(diction)

    #print(df.to_latex(index=False))
    latex= path.replace(".json", "_latex.txt")
    latex_file = open(latex, 'w')
    print(df.to_latex(index=False), file = latex_file)
    latex_file.close()
    png = path.replace(".json", ".png")
    df = df.sort_values(by=['MCC', 'weighted_avg_f1-score'], ascending=False)
    dfi.export(df,png)



# list of Pretrained Models
PretrainedModels = {'roberta': ['roberta-base', 'roberta-large', 'distilroberta-base'],'bert': ['bert-base-uncased', 'bert-base-cased', 'bert-large-uncased', 'bert-large-cased', 'bert-large-uncased-whole-word-masking', 'bert-large-cased-whole-word-masking'], 'xlnet': ['xlnet-base-cased', 'xlnet-large-cased'], 'albert': ['albert-base-v2', 'albert-large-v2', 'albert-xlarge-v2', 'albert-xxlarge-v2']}

# Preparing train data
train_df = pd.read_json('./data/training_data.json', lines=True)

# Preparing validation data
eval_df = pd.read_json('./data/validation_data.json', lines=True)

# Preparing test data
testing_data = pd.read_json('./data/testing_data.json', lines=True)
test_df = testing_data.drop("label")
test_df = test_dff['text'].tolist()
print('test_df', len(test_df))

parser = argparse.ArgumentParser()
parser.add_argument("--epoch", help="number of epoch",
                    type=int)
parser.add_argument("--seed", help="number of seed",
                    type=int)
parser.add_argument("--directory", help="results directory",
                    type=str)
args = parser.parse_args()
print("epoch", args.epoch, "seed", args.seed, "directory", args.directory)


# Optional model configuration
print('model configuration')
model_args = ClassificationArgs()
model_args.manual_seed = args.seed
model_args.overwrite_output_dir = True
model_args.num_train_epochs = args.epoch
model_args.evaluate_during_training = True
SAVE_EVERY_N_EPOCHS = 3
steps_per_epoch = math.floor(len(train_df) / SAVE_EVERY_N_EPOCHS)
if(len(train_df) % SAVE_EVERY_N_EPOCHS > 0):
    steps_per_epoch +=1
model_args.save_steps = steps_per_epoch * SAVE_EVERY_N_EPOCHS
model_args.save_model_every_epoch = True
model_args.n_gpu = 4
model_args.use_early_stopping = True

#model_args.eval_batch_size = 2
#model_args.train_batch_size= 2


cuda_available = torch.cuda.is_available()
print('cuda_available:', cuda_available)
parent_output_dir=args.directory
labels = 2 # number of classes in the classification problem
results = {} # dictionary of the models result

# Create a ClassificationModel
for Model_type, Model_ids in PretrainedModels.items():
    #print(type(Model_ids))
    Model_type_output_dir = parent_output_dir + str(Model_type).replace(' ','') + '/'
    #print(Model_type_output_dir)
    for Model_id in Model_ids:
        print(Model_type, Model_id)
        output_dir = Model_type_output_dir+str(Model_id).replace(' ','')
        print(output_dir)
        model_args.output_dir = output_dir

        model_args.best_model_dir = output_dir+'/best_model'
        model = ClassificationModel(str(Model_type), str(Model_id), num_labels=labels,args=model_args,use_cuda=cuda_available)
        
        # Train the model
        print('start Train the model')
        model.train_model(train_df, eval_df=eval_df, output_dir = output_dir, classification_report = sklearn.metrics.classification_report)
        print('end Train the model')
        print('Evaluate the model')
        # Evaluate the model
        result, model_outputs, wrong_predictions = model.eval_model(eval_df, output_dir = output_dir, classification_report = sklearn.metrics.classification_report)
        print(Model_type, '/', Model_id)
        print('result', result)
        results[str(Model_type)+'/'+str(Model_id)] = result

        print('model_outputs', len(model_outputs), model_outputs)
        print('wrong_predictions', len(wrong_predictions), wrong_predictions)
        
        # Make predictions with the model
        predictions, raw_outputs = model.predict(test_df)
        print('predictions', predictions)
        print('raw_outputs', raw_outputs)

print(results)
resultsDF = pd.DataFrame.from_dict(results)


path = './relevant_classification_sentence_level.json'
with open('./relevant_classification_sentence_level.txt', 'w') as f:
    print(results, file=f)
resultsDF.to_json(path, orient='columns')
latex(path)

