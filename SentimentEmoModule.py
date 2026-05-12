from  transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
from scipy.special import softmax
import numpy as np

class SentimentDetection:
    def __init__(self):
        sentiment_model_name=f"cardiffnlp/twitter-roberta-base-sentiment-latest"
        self.tokenizer=AutoTokenizer.from_pretrained(sentiment_model_name)
        self.config=AutoConfig.from_pretrained(sentiment_model_name)
        self.sentiment_model=AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)
        
    def detect_sentiment(self,response) -> dict:
        sentiment_scores={}
        encoded_resp=self.tokenizer(response,return_tensors="pt")
        outputs=self.sentiment_model(**encoded_resp)
        scores=outputs[0][0].detach().numpy()
        scores=softmax(scores)
        ranks=np.argsort(scores)[::-1]
        
        for i in range(scores.shape[0]):
            label=self.config.id2label[ranks[i]]
            score=scores[ranks[i]]
            
            sentiment_scores[label]=score
        return sentiment_scores
    
class EmotionDectection:
    def __init__(self):
        emo_model_name=f"SamLowe/roberta-base-go_emotions"
        self.tokenizer=AutoTokenizer.from_pretrained(emo_model_name)
        self.config=AutoConfig.from_pretrained(emo_model_name)
        self.emo_model=AutoModelForSequenceClassification.from_pretrained(emo_model_name)
        self.k=3 #hardcoding for now, can change later
        
    def detect_emotion(self,response) -> dict:
        emotional_scores={}
        encoded_resp = self.tokenizer(response, return_tensors="pt")
        outputs = self.emo_model(**encoded_resp)
        scores = outputs[0][0].detach().numpy()
        scores = softmax(scores)
        ranks = np.argsort(scores)[::-1]
        
        for i in range(self.k):
            label = self.config.id2label[ranks[i]]
            score = scores[ranks[i]]
            emotional_scores[label] = score
        return emotional_scores
        
        
    