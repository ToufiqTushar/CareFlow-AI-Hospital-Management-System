
def calculate_priority(patient):
    score = 0
    
    spo2 = patient.get("spo2", 100)
    pulse = patient.get("pulse", 80)
    bp = patient.get("bp", "120/80")
    age = patient.get("age", 30)
    symptoms = patient.get("symptoms", "").lower()
    
    if spo2 < 85:
        score += 50
    elif spo2 < 90:
        score += 40
    elif spo2 < 95:
        score += 20
    elif spo2 < 98:
        score += 5
    
    if pulse > 140 or pulse < 50:
        score += 40
    elif pulse > 120 or pulse < 60:
        score += 20
    elif pulse > 100 or pulse < 70:
        score += 10
    
    try:
        systolic, diastolic = map(int, bp.split("/"))
        if systolic > 180 or diastolic > 120:
            score += 40  
        elif systolic > 160 or diastolic > 100:
            score += 20
        elif systolic < 90 or diastolic < 60:
            score += 30  
        elif systolic < 100:
            score += 15
    except:
        score += 10
    
    if age >= 70:
        score += 15
    elif age >= 60:
        score += 10
    elif age >= 50:
        score += 5
    elif age < 1:
        score += 20  
    
    critical_symptoms = ["chest pain", "difficulty breathing", "stroke", 
                        "severe bleeding", "unconscious", "seizure"]
    moderate_symptoms = ["fever", "vomiting", "dizziness", "pain"]
    
    for symptom in critical_symptoms:
        if symptom in symptoms:
            score += 40
    
    for symptom in moderate_symptoms:
        if symptom in symptoms:
            score += 15
    
    if "pregnant" in symptoms and score < 50:
        score += 25  
    
    if score >= 70:
        level = "RED"
        color = "red"
    elif score >= 40:
        level = "YELLOW"
        color = "orange"
    elif score >= 20:
        level = "GREEN"
        color = "green"
    else:
        level = "BLUE" 
        color = "blue"
    
    return {
        "score": min(score, 100),  
        "level": level,
        "color": color,
        "recommendation": get_recommendation(level)
    }

def get_recommendation(level):
    recommendations = {
        "RED": "Immediate treatment required. Critical condition.",
        "YELLOW": "Urgent treatment needed within 30 minutes.",
        "GREEN": "Treatment needed within 1-2 hours.",
        "BLUE": "Non-urgent. Can wait or consider outpatient care."
    }
    return recommendations.get(level, "Evaluation needed.")