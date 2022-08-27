import pickle
import torch

with open('src/bert_tokenizer.pkl', 'rb') as file:
    tokenizer = pickle.load(file)

with open('src/bert_model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('src/logit_model.pkl', 'rb') as file:
    logit = pickle.load(file)

def predict(input_text:str, 
            bert_tokenizer = tokenizer, 
            bert_model = model, 
            logit_model = logit) -> dict:

    # preprocess text
    text = input_text.lower()

    # tokenize text
    tokens = bert_tokenizer.encode_plus(text, max_length = 26, truncation = True, padding = True, return_tensors='pt')

    # create BERT embeddings
    with torch.no_grad():
        output = bert_model(**tokens)
    embeddings = output.last_hidden_state[:,0,:].numpy()

    # apply logit
    pred_prob = float(logit_model.predict_proba(embeddings)[:,1][0])
    pred_class = int(pred_prob > 0.5)

    return {'input_text' : input_text,
            'spam probability' : pred_prob,
            'spam class' : pred_class}

if __name__ == '__main__':
    print(predict('Congrats, you won a brand new iPhone!'))