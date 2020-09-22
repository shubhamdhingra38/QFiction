# QFiction
Project uses BERT fine tuned on Stanford Question Answering Dataset (SQuAD) and then again fine tuned (language model) on corpus containing different fiction books concatenated into one large text file.
For question query, pipeline is basically:

`Extract keywords from question` -> `Search book for keywords closest to each other` -> `Run BERT QnA task on extracted abstracts` -> `Select the one with highest confidence`

Right now, it takes ~25-30 seconds to get an answer. Since for BERT the maximum sequence length after tokenization is 512, if an answer is not found centered around the searched keywords falling within this length, it is possible to get a random answer/[CLS] token which means an answer could not be found. 


<a href="https://colab.research.google.com/drive/12guTis2B1Xu8plxZGzgwe10AU24xHmde?usp=sharing">Jupyter notebook</a> for pretraining on Colab (use GPU).

Books used for the project in `.txt` format can be found in this repository. Merge all corpus into a single file, then train.

## Screenshots

## Technology Stack
* Django
* jQuery
* HTML/CSS/BootStrap4

I have used <a href="https://github.com/huggingface/transformers/">huggingface/transformers</a> for using BERT in python and pre-trained model on SQuAD can be downloaded here <a href="https://huggingface.co/mrm8488/bert-medium-finetuned-squadv2">bert-medium-finetuned-squadv2</a>.

