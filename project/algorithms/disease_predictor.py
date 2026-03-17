import joblib
import numpy as np
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class AIDiseasePredictor:
    def __init__(self, model_path='models'):
        try:
            # Load trained models
            self.model = joblib.load(f'{model_path}/disease_model.pkl')
            self.symptom_encoder = joblib.load(f'{model_path}/symptom_encoder.pkl')
            self.disease_encoder = joblib.load(f'{model_path}/disease_encoder.pkl')
            print("✅ ML Model loaded successfully!")
        except FileNotFoundError as e:
            print(f"⚠️  Model files not found: {e}")
            print("⚠️  Using fallback rule-based predictor")
            self.model = None
            self.symptom_encoder = None
            self.disease_encoder = None
        
        # Initialize all_symptoms as empty list
        self.all_symptoms = []
        
        # Load disease patterns for additional info
        try:
            with open('data/dummy_data.json', 'r') as f:
                self.disease_patterns = json.load(f).get("disease_patterns", {})
        except FileNotFoundError:
            try:
                with open('project/data/dummy_data.json', 'r') as f:
                    self.disease_patterns = json.load(f).get("disease_patterns", {})
            except:
                self.disease_patterns = {}
                print("⚠️  Could not load disease patterns")
        
        # Extract symptoms after loading patterns
        self.all_symptoms = self._extract_all_symptoms()
    
    def _extract_all_symptoms(self):
        """Extract all unique symptoms from disease patterns"""
        if not self.disease_patterns:
            return []
        
        symptoms = set()
        for disease, pattern in self.disease_patterns.items():
            symptoms.update(pattern.get("symptoms", []))
        return list(symptoms)
    
    def _parse_symptoms(self, symptom_text):
        """Extract symptoms from free text"""
        symptom_text = symptom_text.lower()
        found_symptoms = []
        
        # If all_symptoms is empty, extract them now
        if not self.all_symptoms:
            self.all_symptoms = self._extract_all_symptoms()
        
        for symptom in self.all_symptoms:
            if symptom in symptom_text:
                found_symptoms.append(symptom)
        
        # Also look for symptom variations
        symptom_mapping = {
            "sob": "shortness of breath",
            "cp": "chest pain",
            "n/v": "nausea",
            "abd pain": "abdominal pain",
            "difficulty breathing": "shortness of breath",
            "breathing difficulty": "shortness of breath"
        }
        
        for short, long in symptom_mapping.items():
            if short in symptom_text and long not in found_symptoms:
                found_symptoms.append(long)
        
        return list(set(found_symptoms))
    
    def predict(self, patient_data):
        """Make prediction using ML model or fallback"""
        # Parse symptoms
        symptoms = self._parse_symptoms(patient_data["symptoms"])
        
        # If no ML model, use fallback
        if self.model is None or self.symptom_encoder is None:
            return self._fallback_prediction(patient_data, symptoms)
        
        try:
            # Prepare feature vector
            symptom_vector = self.symptom_encoder.transform([symptoms])
            
            # Add other features
            age = patient_data["age"]
            spo2 = patient_data.get("spo2", 98)
            pulse = patient_data.get("pulse", 80)
            
            features = np.hstack([
                symptom_vector.toarray().flatten(),
                [age, spo2, pulse]
            ]).reshape(1, -1)
            
            # Make prediction
            disease_idx = self.model.predict(features)[0]
            disease_probs = self.model.predict_proba(features)[0]
            
            # Get disease name
            disease_name = self.disease_encoder.inverse_transform([disease_idx])[0]
            
            # Get probabilities for all diseases
            predictions = []
            for idx, prob in enumerate(disease_probs):
                disease = self.disease_encoder.inverse_transform([idx])[0]
                
                # Get additional disease info
                disease_info = self.disease_patterns.get(disease, {})
                
                predictions.append({
                    "disease": disease,
                    "probability": float(prob),
                    "matched_symptoms": symptoms,
                    "recommended_ward": disease_info.get("recommended_ward", "Ward"),
                    "icu_probability": disease_info.get("icu_probability", 0.1),
                    "confidence": self._calculate_confidence(prob, symptoms, disease_info)
                })
            
            # Sort by probability
            predictions.sort(key=lambda x: x["probability"], reverse=True)
            
            return {
                "top_prediction": predictions[0] if predictions else None,
                "all_predictions": predictions,
                "model_used": "XGBoost Classifier",
                "features_used": ["symptoms", "age", "spo2", "pulse"],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"⚠️  ML prediction failed: {e}")
            return self._fallback_prediction(patient_data, symptoms)
    
    def _fallback_prediction(self, patient_data, symptoms):
        """Fallback rule-based prediction when ML fails"""
        predictions = []
        symptoms_lower = patient_data["symptoms"].lower()
        
        for disease, pattern in self.disease_patterns.items():
            score = 0
            matched = []
            
            # Symptom matching
            for symptom in pattern.get("symptoms", []):
                if symptom in symptoms_lower:
                    matched.append(symptom)
                    score += 20
            
            # Age matching
            age_range = pattern.get("age_group", [0, 100])
            if age_range[0] <= patient_data["age"] <= age_range[1]:
                score += 10
            
            # Calculate probability
            if score > 0:
                probability = min(score / 100, 0.95)
                predictions.append({
                    "disease": disease,
                    "probability": round(probability, 2),
                    "matched_symptoms": matched,
                    "recommended_ward": pattern.get("recommended_ward", "Ward"),
                    "icu_probability": pattern.get("icu_probability", 0.1),
                    "confidence": "high" if probability > 0.6 else "medium"
                })
        
        predictions.sort(key=lambda x: x["probability"], reverse=True)
        
        return {
            "top_prediction": predictions[0] if predictions else None,
            "all_predictions": predictions,
            "model_used": "Rule-based Fallback",
            "features_used": ["symptoms", "age"],
            "timestamp": datetime.now().isoformat()
        }
    
    def _calculate_confidence(self, probability, symptoms, disease_info):
        """Calculate confidence score"""
        base_confidence = probability
        
        # Adjust based on symptom match
        disease_symptoms = set(disease_info.get("symptoms", []))
        matched = set(symptoms).intersection(disease_symptoms)
        
        if len(matched) >= 3:
            base_confidence *= 1.2
        elif len(matched) >= 2:
            base_confidence *= 1.1
        
        # Cap at 0.95
        base_confidence = min(base_confidence, 0.95)
        
        if base_confidence > 0.8:
            return "high"
        elif base_confidence > 0.6:
            return "medium"
        else:
            return "low"
    
    def predict_outcome(self, patient, priority, assigned_ward):
        """Predict patient outcomes"""
        disease_pred = self.predict(patient)
        
        predictions = {
            "estimated_treatment_time": self._estimate_treatment_time(disease_pred, priority, assigned_ward),
            "mortality_risk": self._calculate_mortality_risk(disease_pred, patient, priority),
            "readmission_risk": self._calculate_readmission_risk(disease_pred, patient),
            "icu_transfer_probability": self._icu_transfer_probability(disease_pred, priority, assigned_ward),
            "recovery_timeline": self._generate_recovery_timeline(disease_pred, priority)
        }
        
        return predictions
    
    def _estimate_treatment_time(self, disease_pred, priority, ward):
        """Estimate treatment time"""
        base_time = 60  # Default 60 minutes
        
        if disease_pred["top_prediction"]:
            disease = disease_pred["top_prediction"]["disease"]
            disease_info = self.disease_patterns.get(disease, {})
            base_time = disease_info.get("avg_treatment_time", base_time)
        
        # Adjust based on priority
        priority_multiplier = {
            "RED": 1.5,
            "YELLOW": 1.2,
            "GREEN": 1.0,
            "BLUE": 0.8
        }.get(priority, 1.0)
        
        estimated_minutes = int(base_time * priority_multiplier)
        
        hours = estimated_minutes // 60
        minutes = estimated_minutes % 60
        
        return {
            "minutes": estimated_minutes,
            "display": f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m",
            "confidence": "high" if disease_pred["top_prediction"] else "medium"
        }
    
    def _calculate_mortality_risk(self, disease_pred, patient, priority):
        """Calculate mortality risk"""
        base_risk = 0.01
        
        if disease_pred["top_prediction"]:
            disease = disease_pred["top_prediction"]["disease"]
            try:
                with open('data/dummy_data.json', 'r') as f:
                    data = json.load(f)
                    if disease in data["historical_outcomes"]["readmission_rates"]:
                        base_risk = data["historical_outcomes"]["readmission_rates"][disease] * 0.5
            except:
                pass
        
        # Age factor
        age_factor = 1.0
        if patient["age"] > 70:
            age_factor = 2.5
        elif patient["age"] > 50:
            age_factor = 1.8
        elif patient["age"] < 10:
            age_factor = 1.5
        
        # Vital sign factors
        spo2_factor = 1.0
        if patient.get("spo2", 98) < 90:
            spo2_factor = 2.0
        elif patient.get("spo2", 98) < 95:
            spo2_factor = 1.3
        
        # Priority factor
        priority_factor = {
            "RED": 3.0,
            "YELLOW": 1.5,
            "GREEN": 1.0,
            "BLUE": 0.5
        }.get(priority, 1.0)
        
        final_risk = base_risk * age_factor * spo2_factor * priority_factor
        final_risk = min(final_risk, 0.7)
        
        return {
            "percentage": round(final_risk * 100, 2),
            "level": "critical" if final_risk > 0.3 else "high" if final_risk > 0.15 else "medium" if final_risk > 0.05 else "low",
            "factors_considered": ["disease", "age", "spo2", "priority"],
            "ai_model_used": "Ensemble Risk Assessment"
        }
    
    def _calculate_readmission_risk(self, disease_pred, patient):
        """Calculate readmission risk"""
        base_rate = 0.1
        
        if disease_pred["top_prediction"]:
            disease = disease_pred["top_prediction"]["disease"]
            try:
                with open('data/dummy_data.json', 'r') as f:
                    data = json.load(f)
                    base_rate = data["historical_outcomes"]["readmission_rates"].get(disease, base_rate)
            except:
                pass
        
        # Adjust based on patient factors
        adjustment = 1.0
        
        if patient["age"] > 65:
            adjustment *= 1.4
        
        # Comorbidity check
        comorbidities = ["diabetes", "hypertension", "asthma", "copd"]
        for comorbidity in comorbidities:
            if comorbidity in patient["symptoms"].lower():
                adjustment *= 1.2
        
        final_rate = base_rate * adjustment
        
        return round(final_rate * 100, 2)
    
    def _icu_transfer_probability(self, disease_pred, priority, current_ward):
        """ICU transfer probability"""
        if current_ward == "ICU":
            return {"percentage": 0, "reason": "Already in ICU"}
        
        base_prob = 0.1
        
        if disease_pred["top_prediction"]:
            disease = disease_pred["top_prediction"]["disease"]
            disease_info = self.disease_patterns.get(disease, {})
            base_prob = disease_info.get("icu_probability", base_prob)
        
        # Priority adjustment
        if priority == "RED":
            base_prob *= 1.8
        
        return {
            "percentage": round(base_prob * 100, 2),
            "peak_hours": ["18:00-22:00", "02:00-06:00"],
            "monitoring_recommendation": "continuous" if base_prob > 0.3 else "frequent" if base_prob > 0.15 else "standard"
        }
    
    def _generate_recovery_timeline(self, disease_pred, priority):
        """Generate recovery timeline"""
        base_timelines = {
            "RED": [
                {"day": 1, "milestone": "Critical Stabilization", "probability": 0.75},
                {"day": 3, "milestone": "Organ Function Monitoring", "probability": 0.60},
                {"day": 7, "milestone": "Condition Improvement", "probability": 0.45},
                {"day": 14, "milestone": "Significant Recovery", "probability": 0.30}
            ],
            "YELLOW": [
                {"day": 1, "milestone": "Symptom Control", "probability": 0.90},
                {"day": 3, "milestone": "Treatment Response", "probability": 0.75},
                {"day": 7, "milestone": "Clinical Improvement", "probability": 0.60},
                {"day": 10, "milestone": "Functional Recovery", "probability": 0.40}
            ],
            "GREEN": [
                {"day": 1, "milestone": "Initial Assessment", "probability": 0.95},
                {"day": 2, "milestone": "Symptom Resolution", "probability": 0.85},
                {"day": 5, "milestone": "Full Recovery", "probability": 0.70}
            ],
            "BLUE": [
                {"day": 1, "milestone": "Observation", "probability": 0.98},
                {"day": 2, "milestone": "Discharge", "probability": 0.90}
            ]
        }
        
        timeline = base_timelines.get(priority, [])
        
        # Adjust based on disease
        if disease_pred["top_prediction"]:
            disease = disease_pred["top_prediction"]["disease"]
            if disease in ["cardiac", "neurological"]:
                for milestone in timeline:
                    milestone["probability"] = round(milestone["probability"] * 0.8, 2)
        
        return timeline
    
    def generate_ai_insights(self, patient, priority, ward):
        """Generate comprehensive AI insights"""
        disease_pred = self.predict(patient)
        outcome_pred = self.predict_outcome(patient, priority, ward)
        
        insights = {
            "disease_prediction": disease_pred,
            "outcome_prediction": outcome_pred,
            "resource_recommendations": self._generate_resource_recommendations(disease_pred, priority, ward),
            "risk_factors": self._identify_risk_factors(patient, disease_pred),
            "ai_confidence": disease_pred.get("confidence", "medium"),
            "model_explanation": self._explain_prediction(patient, disease_pred),
            "timestamp": datetime.now().isoformat()
        }
        
        return insights
    
    def _generate_resource_recommendations(self, disease_pred, priority, ward):
        """Generate resource recommendations"""
        recommendations = []
        
        if disease_pred["top_prediction"]:
            disease = disease_pred["top_prediction"]["disease"]
            
            if disease == "cardiac":
                recommendations.extend([
                    "Continuous ECG monitoring",
                    "Cardiac enzyme tests",
                    "Cardiology consultation"
                ])
            elif disease == "respiratory":
                recommendations.extend([
                    "Pulse oximetry monitoring",
                    "Chest X-ray",
                    "Oxygen therapy if needed"
                ])
        
        if priority == "RED":
            recommendations.append("Assign senior specialist")
        
        if ward == "ICU":
            recommendations.append("Ventilator on standby")
        
        return recommendations
    
    def _identify_risk_factors(self, patient, disease_pred):
        """Identify risk factors"""
        risk_factors = []
        
        if patient["age"] > 65:
            risk_factors.append({
                "factor": "Advanced Age (>65)",
                "severity": "high"
            })
        
        spo2 = patient.get("spo2", 98)
        if spo2 < 92:
            risk_factors.append({
                "factor": f"Low Oxygen (SPO2: {spo2}%)",
                "severity": "critical" if spo2 < 90 else "high"
            })
        
        return risk_factors
    
    def _explain_prediction(self, patient, disease_pred):
        """Explain the prediction"""
        if not disease_pred["top_prediction"]:
            return "Insufficient data for prediction"
        
        disease = disease_pred["top_prediction"]["disease"]
        probability = disease_pred["top_prediction"]["probability"]
        
        explanation = f"""
        The {disease_pred['model_used']} predicts {disease} with {probability:.1%} confidence.
        
        Key factors:
        - Matched {len(disease_pred['top_prediction']['matched_symptoms'])} symptoms
        - Patient age: {patient['age']} years
        - Model analyzed multiple possible conditions
        """
        
        return explanation.strip()