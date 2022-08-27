from flask import Flask, request, jsonify
import pickle
import torch

with open('src/bert_tokenizer.pkl', 'rb') as file:
    tokenizer = pickle.load(file)

with open('src/bert_model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('src/logit_model.pkl', 'rb') as file:
    logit = pickle.load(file)


app = Flask('__name__')

@app.route('/predict', methods = ['POST'])
def predict():

    # input
    input_text = request.form.get('input_text')

    # preprocess text
    text = input_text.lower()

    # tokenize text
    tokens = tokenizer.encode_plus(text, max_length = 26, truncation = True, padding = True, return_tensors='pt')

    # create BERT embeddings
    with torch.no_grad():
        output = model(**tokens)
    embeddings = output.last_hidden_state[:,0,:].numpy()

    # apply logit
    pred_prob = float(logit.predict_proba(embeddings)[:,1][0])
    pred_class = int(pred_prob > 0.5)

    return jsonify({'input_text' : input_text,
                    'spam probability' : pred_prob,
                    'spam class' : pred_class})

if __name__ == '__main__':
	app.run(debug = True, use_reloader = False, host = '0.0.0.0', port = 9696)