# algorithms/dummy_predictor.py
import json
import random
from datetime import datetime, timedelta
import math

class DummyPredictor:
    def __init__(self):
        with open('project/data/dummy_data.json', 'r') as f:
            self.data = json.load(f)
    
    def predict_disease(self, patient):
        """Predict likely disease based on symptoms"""
        symptoms = patient["symptoms"].lower()
        patient_age = patient["age"]
        
        predictions = []
        
        for disease, pattern in self.data["disease_patterns"].items():
            score = 0
            
            # Symptom matching
            matched_symptoms = []
            for symptom in pattern["symptoms"]:
                if symptom in symptoms:
                    matched_symptoms.append(symptom)
                    score += 20
            
            # Age matching
            age_min, age_max = pattern["age_group"]
            if age_min <= patient_age <= age_max:
                score += 10
            else:
                score -= 5
            
            # Vital sign matching (simplified)
            spo2 = patient.get("spo2", 98)
            if "typical_spo2" in pattern:
                spo2_min, spo2_max = pattern["typical_spo2"]
                if spo2_min <= spo2 <= spo2_max:
                    score += 5
            
            if score > 0:
                probability = min(score / 100, 0.95)
                predictions.append({
                    "disease": disease,
                    "probability": round(probability, 2),
                    "matched_symptoms": matched_symptoms,
                    "recommended_ward": pattern["recommended_ward"],
                    "icu_probability": pattern["icu_probability"]
                })
        
        # Sort by probability
        predictions.sort(key=lambda x: x["probability"], reverse=True)
        
        return {
            "top_prediction": predictions[0] if predictions else None,
            "all_predictions": predictions,
            "confidence": "high" if predictions and predictions[0]["probability"] > 0.6 else "medium"
        }
    
    def predict_outcome(self, patient, priority, assigned_ward):
        """Predict patient outcomes"""
        # Simulate some "intelligent" predictions
        predictions = {
            "estimated_treatment_time": self._estimate_treatment_time(priority, assigned_ward),
            "mortality_risk": self._calculate_mortality_risk(priority, patient),
            "readmission_risk": self._calculate_readmission_risk(patient),
            "icu_transfer_probability": self._icu_transfer_probability(priority, assigned_ward),
            "recovery_timeline": self._generate_recovery_timeline(priority)
        }
        
        return predictions
    
    def _estimate_treatment_time(self, priority, ward):
        """Estimate treatment time based on historical data"""
        base_time = self.data["historical_outcomes"]["avg_treatment_times"][ward][priority]
        
        # Add some randomness
        variation = random.uniform(0.8, 1.2)
        estimated_minutes = int(base_time * variation)
        
        # Convert to hours:minutes
        hours = estimated_minutes // 60
        minutes = estimated_minutes % 60
        
        return {
            "minutes": estimated_minutes,
            "display": f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m",
            "confidence": random.choice(["high", "medium", "low"])
        }
    
    def _calculate_mortality_risk(self, priority, patient):
        """Calculate mortality risk"""
        base_risk = self.data["historical_outcomes"]["mortality_rates"][priority]
        
        # Adjust based on age
        age_factor = 1.0
        if patient["age"] > 70:
            age_factor = 2.0
        elif patient["age"] > 50:
            age_factor = 1.5
        elif patient["age"] < 10:
            age_factor = 1.2
        
        # Adjust based on SPO2
        spo2_factor = 1.0
        if patient["spo2"] < 90:
            spo2_factor = 1.8
        elif patient["spo2"] < 95:
            spo2_factor = 1.3
        
        final_risk = base_risk * age_factor * spo2_factor
        final_risk = min(final_risk, 0.5)  # Cap at 50%
        
        return {
            "percentage": round(final_risk * 100, 1),
            "level": "critical" if final_risk > 0.2 else "high" if final_risk > 0.1 else "medium",
            "factors": ["age", "spo2", "priority"]
        }
    
    def _calculate_readmission_risk(self, patient):
        """Calculate readmission risk"""
        # Check symptoms against disease patterns
        disease_pred = self.predict_disease(patient)
        if disease_pred["top_prediction"]:
            disease = disease_pred["top_prediction"]["disease"]
            base_rate = self.data["historical_outcomes"]["readmission_rates"].get(disease, 0.1)
        else:
            base_rate = 0.1
        
        # Adjust based on age
        if patient["age"] > 65:
            base_rate *= 1.5
        if "diabetes" in patient["symptoms"].lower():
            base_rate *= 1.3
        
        return round(base_rate * 100, 1)
    
    def _icu_transfer_probability(self, priority, current_ward):
        """Probability of needing ICU transfer"""
        if current_ward == "ICU":
            return {"percentage": 0, "reason": "Already in ICU"}
        
        base_prob = 0.15 if priority == "RED" else 0.05
        
        # Simulate some "intelligence"
        hour = datetime.now().hour
        if 2 <= hour <= 6:  # Night hours
            base_prob *= 0.7  # Lower at night
        
        return {
            "percentage": round(base_prob * 100, 1),
            "peak_hours": ["18:00-22:00"],
            "monitoring_recommendation": "frequent" if base_prob > 0.1 else "standard"
        }
    
    def _generate_recovery_timeline(self, priority):
        """Generate a recovery timeline"""
        timelines = {
            "RED": [
                {"day": 1, "milestone": "Stabilization", "probability": 0.85},
                {"day": 3, "milestone": "Critical Care", "probability": 0.70},
                {"day": 7, "milestone": "Improvement", "probability": 0.50},
                {"day": 14, "milestone": "Recovery", "probability": 0.25}
            ],
            "YELLOW": [
                {"day": 1, "milestone": "Initial Treatment", "probability": 0.95},
                {"day": 3, "milestone": "Symptom Relief", "probability": 0.80},
                {"day": 7, "milestone": "Significant Improvement", "probability": 0.65},
                {"day": 10, "milestone": "Near Recovery", "probability": 0.40}
            ],
            "GREEN": [
                {"day": 1, "milestone": "Assessment", "probability": 0.98},
                {"day": 2, "milestone": "Treatment", "probability": 0.90},
                {"day": 5, "milestone": "Recovery", "probability": 0.75}
            ],
            "BLUE": [
                {"day": 1, "milestone": "Observation", "probability": 0.99},
                {"day": 2, "milestone": "Discharge", "probability": 0.85}
            ]
        }
        
        return timelines.get(priority, [])
    
    def generate_ai_insights(self, patient, priority, ward):
        """Generate comprehensive AI insights"""
        disease_pred = self.predict_disease(patient)
        outcome_pred = self.predict_outcome(patient, priority, ward)
        
        insights = {
            "disease_prediction": disease_pred,
            "outcome_prediction": outcome_pred,
            "resource_recommendations": self._generate_resource_recommendations(priority, ward),
            "risk_factors": self._identify_risk_factors(patient),
            "ai_confidence": random.choice(["high", "medium"]),
            "timestamp": datetime.now().isoformat()
        }
        
        return insights
    
    def _generate_resource_recommendations(self, priority, ward):
        """Generate resource recommendations"""
        recommendations = []
        
        if priority == "RED" and ward == "ICU":
            recommendations.extend([
                "Continuous vital monitoring",
                "Prepare emergency medications",
                "Assign senior ICU specialist",
                "Alert surgical team if needed"
            ])
        elif priority == "YELLOW":
            recommendations.extend([
                "Hourly vital checks",
                "Regular pain assessment",
                "Prepare lab tests",
                "Family consultation"
            ])
        
        # Add ward-specific recommendations
        if ward == "ICU":
            recommendations.append("Prepare ventilator if SPO2 < 90")
        else:
            recommendations.append("Regular nurse rounds every 2 hours")
        
        return recommendations
    
    def _identify_risk_factors(self, patient):
        """Identify risk factors"""
        risk_factors = []
        
        if patient["age"] > 65:
            risk_factors.append({"factor": "Age > 65", "severity": "high"})
        
        if patient["spo2"] < 92:
            risk_factors.append({"factor": "Low oxygen saturation", "severity": "critical"})
        
        # Parse blood pressure
        try:
            systolic, diastolic = map(int, patient["bp"].split("/"))
            if systolic > 160:
                risk_factors.append({"factor": "High systolic BP", "severity": "medium"})
        except:
            pass
        
        # Check symptoms
        critical_symptoms = ["chest pain", "difficulty breathing", "unconscious"]
        for symptom in critical_symptoms:
            if symptom in patient["symptoms"].lower():
                risk_factors.append({"factor": f"Symptom: {symptom}", "severity": "critical"})
        
        return risk_factors