from flask import Flask, render_template, request, jsonify
from algorithms.triage import calculate_priority
from algorithms.bed_allocation import allocate_bed, get_bed_status
from algorithms.route_finder import a_star
from algorithms.staff_ga import genetic_algorithm

import json

app = Flask(__name__)

try:
    from algorithms.disease_predictor import AIDiseasePredictor
    ai_predictor = AIDiseasePredictor()
    print("✅ ML Disease Predictor loaded successfully!")
except Exception as e:
    print(f"⚠️  Could not load ML predictor: {e}")
    print("⚠️  Falling back to dummy predictor")
    from algorithms.dummy_predictor import DummyPredictor
    ai_predictor = DummyPredictor()


HOSPITAL_GRAPH = {
    "ER": [("ICU", 5), ("Ward", 8), ("Lab", 10)],
    "ICU": [("ER", 5), ("Lab", 4), ("Ward", 6)],
    "Ward": [("ER", 8), ("ICU", 6), ("Lab", 2)],
    "Lab": [("ER", 10), ("ICU", 4), ("Ward", 2)]
}

BEDS = {
    "ICU": [False, True, False],  
    "Ward": [False, False, False, False]  
}

DOCTORS = [
    {"name": "Dr. Smith", "skill": "ICU", "available": True},
    {"name": "Dr. Johnson", "skill": "Ward", "available": True},
    {"name": "Dr. Williams", "skill": "General", "available": True},
    {"name": "Dr. Brown", "skill": "ICU", "available": True},
    {"name": "Dr. Davis", "skill": "Ward", "available": True}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    try:
        patient = {
            "age": int(request.form["age"]),
            "spo2": int(request.form["spo2"]),
            "pulse": int(request.form["pulse"]),
            "bp": request.form["bp"],
            "symptoms": request.form["symptoms"]
        }
        
        print(f"📋 Processing patient: {patient}")
        
        priority = calculate_priority(patient)
        print(f"🚨 Priority: {priority['level']} (Score: {priority['score']})")
        
        bed_result = allocate_bed(priority["level"], BEDS.copy())
        
        if not bed_result:
            return render_template("error.html", 
                                 message="No beds available. Please wait.")
        
        bed_ward, bed_index = bed_result
        print(f"🛏️ Bed allocated: {bed_ward}, Bed #{bed_index + 1}")
        
        BEDS[bed_ward][bed_index] = True
        
        route, cost = a_star(HOSPITAL_GRAPH, "ER", bed_ward)
        
        if not route:
            return render_template("error.html", 
                                 message="Route not found.")
        
        print(f"🗺️ Route: {' → '.join(route)} (Cost: {cost})")
        
        patients_for_ga = [{
            "priority": priority["level"],
            "ward": bed_ward,
            "bed": bed_index
        }]
        
        available_doctors = [doc for doc in DOCTORS if doc["available"]]
        
        if not available_doctors:
            return render_template("error.html", 
                                 message="No doctors available.")
        
        staff_assignment = genetic_algorithm(available_doctors, patients_for_ga)
        
        assigned_doctor = staff_assignment[0]
        for doc in DOCTORS:
            if doc["name"] == assigned_doctor["name"]:
                doc["available"] = False
                break
        
        print(f"👨‍⚕️ Doctor assigned: {assigned_doctor['name']} ({assigned_doctor['skill']})")
        
        print("🤖 Generating AI insights...")
        ai_insights = ai_predictor.generate_ai_insights(
            patient=patient,
            priority=priority["level"],
            ward=bed_ward
        )
        
        current_bed_status = get_bed_status(BEDS)
        
        return render_template(
            "dashboard.html",
            patient=patient,
            priority=priority,
            bed=bed_result,
            route=route,
            cost=cost,
            staff=assigned_doctor,
            bed_status=current_bed_status,
            ai_insights=ai_insights
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return render_template("error.html", 
                             message=f"An error occurred: {str(e)}")

@app.route("/reset")
def reset():
    """Reset system state (for testing)"""
    global BEDS, DOCTORS
    BEDS = {
        "ICU": [False, True, False],
        "Ward": [False, False, False, False]
    }
    
    for doc in DOCTORS:
        doc["available"] = True
    
    return "System reset successfully! <a href='/'>Go back</a>"

@app.route("/bed-status")
def bed_status():
    """API endpoint for bed status"""
    return jsonify(get_bed_status(BEDS))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="Page not found"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html', message="Internal server error"), 500

if __name__ == "__main__":
    print("\n🏥 CareFlow AI Hospital Management System")
    print("=" * 50)
    print("Server starting on http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    app.run(debug=True, port=5000)