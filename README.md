# QFiction
Project uses BERT fine tuned on Stanford Question Answering Dataset (SQuAD) and then again fine tuned (language model) on corpus containing different fiction books concatenated into one large text file.
For question query, pipeline is basically:

`Extract keywords from question` -> `Search book for keywords closest to each other` -> `Run BERT QnA task on extracted abstracts` -> `Select the one with highest confidence`

Right now, it takes ~25-30 seconds to get an answer. Since for BERT the maximum sequence length after tokenization is 512, if an answer is not found centered around the searched keywords falling within this length, it is possible to get a random answer/[CLS] token which means an answer could not be found. 

This project works decent with Harry Potter book, but for Lord Of The Rings and A Song Of Ice and Fire it doesn't. It might be because of simplicity of language in Harry Potter books and lot of complexity in the latter mentioned. 


<a href="https://colab.research.google.com/drive/12guTis2B1Xu8plxZGzgwe10AU24xHmde?usp=sharing">Jupyter notebook</a> for pretraining on Colab (use GPU).

Books used for the project in `.txt` format can be found in this repository. Merge all corpus into a single file, then train.

## Screenshots

<details><summary>Home</summary>
<p>
<img src="https://github.com/shubhamdhingra38/QFiction/blob/master/screenshots/Screenshot%202020-09-23%20at%207.06.40%20AM.png"></img>
<img src="https://github.com/shubhamdhingra38/QFiction/blob/master/screenshots/Screenshot%202020-09-23%20at%207.06.59%20AM.png"></img>
<img src="https://github.com/shubhamdhingra38/QFiction/blob/master/screenshots/Screenshot%202020-09-23%20at%207.07.21%20AM.png"></img>
</p>
</details>


<details><summary>Questions</summary>
<p>
<img src="https://github.com/shubhamdhingra38/QFiction/blob/master/screenshots/Screenshot%202020-09-23%20at%206.35.05%20AM.png"></img>
<img src="https://github.com/shubhamdhingra38/QFiction/blob/master/screenshots/Screenshot%202020-09-23%20at%206.35.34%20AM.png"></img>
<img src="https://github.com/shubhamdhingra38/QFiction/blob/master/screenshots/Screenshot%202020-09-23%20at%206.36.23%20AM.png"></img>
<img src="https://github.com/shubhamdhingra38/QFiction/blob/master/screenshots/Screenshot%202020-09-23%20at%206.38.15%20AM.png"></img>
<img src="https://github.com/shubhamdhingra38/QFiction/blob/master/screenshots/Screenshot%202020-09-23%20at%206.38.37%20AM.png"></img>
</p>
</details>

<details><summary>Epic Fails</summary>
<p>Wouldn't have disagreed if I asked this about the Starks</p>
<img src="https://github.com/shubhamdhingra38/QFiction/blob/master/screenshots/Screenshot%202020-09-23%20at%207.00.34%20AM.png"></img>
<p>What a plot twist!</p>
<img src="https://github.com/shubhamdhingra38/QFiction/blob/master/screenshots/Screenshot%202020-09-23%20at%207.01.11%20AM.png"></img>
<img src="https://github.com/shubhamdhingra38/QFiction/blob/master/screenshots/Screenshot%202020-09-23%20at%206.59.30%20AM.png"></img>
<p>Cunning indeed!</p>
<img src="https://github.com/shubhamdhingra38/QFiction/blob/master/screenshots/Screenshot%202020-09-23%20at%207.02.02%20AM.png"></img>
</p>
</details>

## Video
https://youtu.be/N6OQ2bsTO2c


## Technology Stack
* Django
* jQuery
* HTML/CSS/BootStrap4

I have used <a href="https://github.com/huggingface/transformers/">huggingface/transformers</a> for using BERT in python and pre-trained model on SQuAD can be downloaded here <a href="https://huggingface.co/mrm8488/bert-medium-finetuned-squadv2">bert-medium-finetuned-squadv2</a>.

For better results one can try BERT large which is ~1GB in size. Or even better, gain access to GPT-3 API if lucky.

