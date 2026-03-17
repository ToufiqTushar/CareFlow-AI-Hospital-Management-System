import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

class DiseaseModelTrainer:
    def __init__(self):
        self.model = None
        self.symptom_encoder = MultiLabelBinarizer()
        self.disease_encoder = LabelEncoder()
        
    def create_training_data(self):
        """Create or load training data"""
        json_paths = [
            'data/disease_symptoms.json',
            'project/data/disease_symptoms.json',
            'data/dummy_data.json',
            'project/data/dummy_data.json'
        ]
        
        for json_path in json_paths:
            try:
                with open(json_path, 'r') as f:
                    disease_patterns = json.load(f)
                    print(f"✅ Loaded data from: {json_path}")
                    break
            except FileNotFoundError:
                continue
        else:
            raise FileNotFoundError("Could not find disease patterns JSON file")
        
        # Generate synthetic training data
        data = []
        for disease, patterns in disease_patterns.items():
            for _ in range(100):  
                num_symptoms = np.random.randint(2, len(patterns['symptoms']) + 1)
                selected_symptoms = np.random.choice(
                    patterns['symptoms'], 
                    num_symptoms, 
                    replace=False
                ).tolist()
                
                if np.random.random() > 0.7:
                    all_symptoms = []
                    for d in disease_patterns.values():
                        all_symptoms.extend(d['symptoms'])
                    extra = np.random.choice(
                        [s for s in all_symptoms if s not in selected_symptoms],
                        min(2, len(all_symptoms) - len(selected_symptoms)),
                        replace=False
                    )
                    selected_symptoms.extend(extra)
                
                data.append({
                    'symptoms': selected_symptoms,
                    'disease': disease,
                    'age': np.random.randint(patterns['age_group'][0], patterns['age_group'][1]),
                    'spo2': np.random.randint(patterns['typical_spo2'][0], patterns['typical_spo2'][1]),
                    'pulse': np.random.randint(patterns['typical_pulse'][0], patterns['typical_pulse'][1])
                })
        
        return pd.DataFrame(data)
    
    def preprocess_data(self, df):
        """Prepare data for training"""
        X_symptoms = self.symptom_encoder.fit_transform(df['symptoms'])
        
        X_additional = df[['age', 'spo2', 'pulse']].values
        X = np.hstack([X_symptoms, X_additional])
        
        y = self.disease_encoder.fit_transform(df['disease'])
        
        return X, y
    
    def train(self, X, y):
        """Train the model"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.model = XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Model Accuracy: {accuracy:.2f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, 
                                   target_names=self.disease_encoder.classes_))
        
        return accuracy
    
    def save_model(self, path='models'):
        """Save trained model and encoders"""
        if not os.path.exists(path):
            os.makedirs(path)
        
        joblib.dump(self.model, f'{path}/disease_model.pkl')
        joblib.dump(self.symptom_encoder, f'{path}/symptom_encoder.pkl')
        joblib.dump(self.disease_encoder, f'{path}/disease_encoder.pkl')
        
        print(f"Models saved to {path}/")
    
    def load_model(self, path='models'):
        """Load trained model and encoders"""
        try:
            self.model = joblib.load(f'{path}/disease_model.pkl')
            self.symptom_encoder = joblib.load(f'{path}/symptom_encoder.pkl')
            self.disease_encoder = joblib.load(f'{path}/disease_encoder.pkl')
            print("Models loaded successfully!")
        except FileNotFoundError:
            print(f"⚠️ Models not found in {path}/. Training new model...")
            self.run_training()
    
    def run_training(self):
        """Complete training pipeline"""
        print("Creating training data...")
        df = self.create_training_data()
        
        print("Preprocessing data...")
        X, y = self.preprocess_data(df)
        
        print("Training model...")
        accuracy = self.train(X, y)
        
        print("Saving model...")
        self.save_model()
        
        return accuracy

if __name__ == "__main__":
    trainer = DiseaseModelTrainer()
    trainer.run_training()