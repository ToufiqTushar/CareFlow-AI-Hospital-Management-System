# 🏥 CareFlow AI - Intelligent Hospital Management System

<div align="center">
  <h1>🤖 CareFlow AI</h1>
  <p><strong>An AI-Powered Hospital Management System with Multiple Intelligent Algorithms</strong></p>
  
  <p>
    <img src="https://img.shields.io/badge/Python-3.9-blue?style=flat-square&logo=python&logoColor=white" alt="Python Version"/>
    <img src="https://img.shields.io/badge/Flask-2.3.3-red?style=flat-square&logo=flask&logoColor=white" alt="Flask"/>
    <img src="https://img.shields.io/badge/AI-5%20Algorithms-brightgreen?style=flat-square" alt="AI Algorithms"/>
    <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="License: MIT"/>
    <img src="https://img.shields.io/badge/Status-Academic%20Project-blue?style=flat-square" alt="Status"/>
  </p>
  
  <p>
    <a href="#features">Features</a> •
    <a href="#ai-algorithms">AI Algorithms</a> •
    <a href="#getting-started">Getting Started</a> •
    <a href="#project-structure">Structure</a> •
    <a href="#demo">Demo</a> •
    <a href="#future-improvements">Roadmap</a>
  </p>
</div>

<hr>

<h2>📌 Overview</h2>

<p><strong>CareFlow AI</strong> is a comprehensive hospital management system that leverages <strong>five different artificial intelligence algorithms</strong> to optimize patient care, resource allocation, and operational efficiency. From intelligent triage to optimal route planning and staff assignment, this system demonstrates how AI can transform healthcare delivery.</p>

<p>The system takes patient vitals as input, processes them through multiple AI algorithms, and provides real-time decisions including priority level, bed allocation, optimal hospital route, staff assignment, and predictive analytics.</p>

<hr>

<h2>✨ Features</h2>

<table>
  <tr>
    <td width="33%">
      <h3>🔹 AI-Powered Triage</h3>
      <ul>
        <li>Expert system with 25+ medical rules</li>
        <li>Priority levels: RED, YELLOW, GREEN, BLUE</li>
        <li>Real-time priority scoring</li>
        <li>Medical recommendation engine</li>
      </ul>
    </td>
    <td width="33%">
      <h3>🔸 Intelligent Bed Allocation</h3>
      <ul>
        <li>Constraint satisfaction algorithm</li>
        <li>Priority-based allocation (RED→ICU first)</li>
        <li>Real-time bed availability tracking</li>
        <li>Multi-ward management (ICU, General Ward)</li>
      </ul>
    </td>
    <td width="33%">
      <h3>🔹 Optimal Route Planning</h3>
      <ul>
        <li>A* search algorithm implementation</li>
        <li>Heuristic-based pathfinding</li>
        <li>Shortest path from ER to destination</li>
        <li>Distance optimization</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>
      <h3>🔸 Genetic Staff Assignment</h3>
      <ul>
        <li>Evolutionary optimization algorithm</li>
        <li>50 generations of evolution</li>
        <li>Selection, crossover, mutation operators</li>
        <li>Skill-based doctor matching</li>
      </ul>
    </td>
    <td>
      <h3>🔹 Predictive Analytics</h3>
      <ul>
        <li>Disease prediction from symptoms</li>
        <li>Outcome forecasting</li>
        <li>Recovery timeline estimation</li>
        <li>Risk factor identification</li>
      </ul>
    </td>
    <td>
      <h3>🔸 Interactive Dashboard</h3>
      <ul>
        <li>Real-time decision visualization</li>
        <li>Bed status monitoring</li>
        <li>Doctor availability tracking</li>
        <li>Print reports functionality</li>
      </ul>
    </td>
  </tr>
</table>

<hr>

<h2>🧠 AI Algorithms</h2>

<p>CareFlow AI implements <strong>five distinct AI algorithms</strong>, each solving a different aspect of hospital management:</p>

<table>
  <tr>
    <th width="20%">Algorithm</th>
    <th width="30%">Type</th>
    <th width="50%">Implementation</th>
  </tr>
  <tr>
    <td><strong>Expert System</strong></td>
    <td>Rule-Based AI</td>
    <td>25+ medical rules in <code>triage.py</code> for priority scoring based on vitals and symptoms</td>
  </tr>
  <tr>
    <td><strong>A* Search</strong></td>
    <td>Informed Search</td>
    <td>Optimal pathfinding in hospital graph using <code>f(n) = g(n) + h(n)</code> heuristic</td>
  </tr>
  <tr>
    <td><strong>Genetic Algorithm</strong></td>
    <td>Evolutionary Computing</td>
    <td>Staff assignment optimization with population size 20, 50 generations, tournament selection</td>
  </tr>
  <tr>
    <td><strong>Constraint Satisfaction</strong></td>
    <td>CSP</td>
    <td>Bed allocation with priority constraints (RED→ICU, YELLOW→Ward, etc.)</td>
  </tr>
  <tr>
    <td><strong>Pattern Matching</strong></td>
    <td>Knowledge-Based</td>
    <td>Disease prediction from symptom patterns using JSON knowledge base</td>
  </tr>
</table>

<hr>

<h2>📂 Project Structure</h2>

<pre>
careflow-ai/
│
├── 📁 algorithms/                          # AI Algorithm Implementations
│   ├── 📄 triage.py                        # Expert System (Rule-based AI)
│   ├── 📄 bed_allocation.py                 # Constraint Satisfaction
│   ├── 📄 route_finder.py                   # A* Search Algorithm
│   ├── 📄 staff_ga.py                       # Genetic Algorithm
│   └── 📄 dummy_predictor.py                 # Pattern Matching Prediction
│
├── 📁 data/                                 # Knowledge Base
│   └── 📄 dummy_data.json                   # Disease patterns & historical data
│
├── 📁 templates/                            # Web Interface
│   ├── 📄 index.html                        # Patient entry form
│   └── 📄 dashboard.html                     # AI decision display
│
├── 📁 static/                               # Styling
│   └── 📄 style.css                          # CSS styling
│
├── 📄 app.py                                 # Main Flask application
├── 📄 requirements.txt                       # Dependencies
├── 📄 .gitignore                              # Git ignore file
├── 📄 Procfile                                # Deployment configuration
├── 📄 runtime.txt                             # Python version
└── 📄 README.md                               # This file
</pre>

<hr>

<h2>🚀 Getting Started</h2>

<h3>Prerequisites</h3>
<ul>
  <li>Python 3.8 or higher</li>
  <li>pip package manager</li>
  <li>Basic understanding of AI concepts</li>
</ul>

<h3>Installation & Running</h3>

<ol>
  <li><strong>Clone the repository:</strong>
    <pre><code>git clone https://github.com/ToufiqTushar/careflow-ai.git</code></pre>
  </li>
  <li><strong>Navigate to project directory:</strong>
    <pre><code>cd careflow-ai</code></pre>
  </li>
  <li><strong>Create virtual environment (recommended):</strong>
    <pre><code>python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate</code></pre>
  </li>
  <li><strong>Install dependencies:</strong>
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li><strong>Run the application:</strong>
    <pre><code>python app.py</code></pre>
  </li>
  <li><strong>Open browser:</strong>
    <pre><code>http://localhost:5000</code></pre>
  </li>
</ol>

<hr>

<h2>📊 Sample Run</h2>

<pre>
🚀 Patient Entry:
-----------------
Age: 65
SPO2: 88%
Pulse: 120 bpm
BP: 150/95
Symptoms: chest pain, difficulty breathing

🤖 AI Processing...
-------------------
Step 1: Expert System Triage
  Score: 85/100
  Priority: 🔴 RED (Immediate treatment required)

Step 2: Bed Allocation (CSP)
  Allocated: ICU Bed #2

Step 3: Route Planning (A*)
  Optimal Path: ER → ICU
  Distance: 5 units

Step 4: Staff Assignment (Genetic Algorithm)
  Assigned: Dr. A (ICU Specialist)
  Generations: 50
  Fitness: 95%

Step 5: Disease Prediction (Pattern Matching)
  Predicted: Cardiac Issue
  Confidence: 85%
  Recovery Timeline: 5-7 days

✅ Patient processed successfully!
</pre>

<hr>

<h2>🧪 Test Cases</h2>

<table>
  <tr>
    <th>Patient Type</th>
    <th>Input</th>
    <th>Expected Output</th>
  </tr>
  <tr>
    <td><strong>Critical</strong></td>
    <td>Age 75, SPO2 85, Pulse 150, BP 180/120, "chest pain"</td>
    <td>RED Priority, ICU Bed</td>
  </tr>
  <tr>
    <td><strong>Moderate</strong></td>
    <td>Age 45, SPO2 92, Pulse 110, BP 140/90, "fever headache"</td>
    <td>YELLOW Priority, Ward Bed</td>
  </tr>
  <tr>
    <td><strong>Mild</strong></td>
    <td>Age 25, SPO2 98, Pulse 80, BP 120/80, "mild pain"</td>
    <td>GREEN Priority, Ward Bed</td>
  </tr>
</table>

<hr>

<h2>💡 Future Improvements</h2>

<ul>
  <li>✅ <strong>Expert System</strong> — Implemented with 25+ medical rules</li>
  <li>✅ <strong>A* Search</strong> — Implemented with heuristic optimization</li>
  <li>✅ <strong>Genetic Algorithm</strong> — Implemented with 50 generations</li>
  <li>✅ <strong>Constraint Satisfaction</strong> — Implemented for bed allocation</li>
  <li>✅ <strong>Pattern Matching</strong> — Implemented for disease prediction</li>
  <li>🔲 <strong>Machine Learning Integration</strong> — Train on real patient data</li>
  <li>🔲 <strong>Reinforcement Learning</strong> — Dynamic resource optimization</li>
  <li>🔲 <strong>NLP for Symptoms</strong> — Natural language processing for symptom analysis</li>
  <li>🔲 <strong>Multi-Hospital Support</strong> — Scale to multiple facilities</li>
  <li>🔲 <strong>Mobile App</strong> — React Native frontend</li>
  <li>🔲 <strong>Real-time Analytics</strong> — Live dashboards with charts</li>
  <li>🔲 <strong>Patient History Database</strong> — Store and analyze historical cases</li>
</ul>

<hr>

<h2>📖 Educational Value</h2>

<p>This project is ideal for:</p>
<ul>
  <li><strong>AI Courses</strong> — Demonstrates 5 different AI algorithm types</li>
  <li><strong>Healthcare Informatics</strong> — Real-world application of AI in medicine</li>
  <li><strong>Algorithm Design</strong> — From-scratch implementations of classic algorithms</li>
  <li><strong>Web Development</strong> — Flask integration with AI backend</li>
  <li><strong>Final Year Projects</strong> — Comprehensive system with multiple components</li>
</ul>

<hr>

<h2>📝 License</h2>

<div align="center">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"/>
  <p>This project is licensed under the MIT License - see the <a href="LICENSE">LICENSE</a> file for details.</p>
  <p>Free for academic and learning use.</p>
</div>

<hr>

<div align="center">
  <h2>👨‍💻 Author</h2>
  
  <h3>Taufiq Zahan Tushar</h3>
  <p>
    🎓 Computer Science & Engineering Undergraduate<br>
    Green University of Bangladesh
  </p>
  
  <p>
    <a href="mailto:toufiqtushar99@gmail.com">
      <img src="https://img.shields.io/badge/Email-toufiqtushar99%40gmail.com-D14836?style=flat-square&logo=gmail&logoColor=white" alt="Email"/>
    </a>
    <a href="https://linkedin.com/in/taufiq-zahan-tushar">
      <img src="https://img.shields.io/badge/LinkedIn-Toufiq%20Zahan%20Tushar-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"/>
    </a>
    <a href="https://github.com/ToufiqTushar">
      <img src="https://img.shields.io/badge/GitHub-@ToufiqTushar-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"/>
    </a>
  </p>
  
  <h3>📊 AI Lab Project - 7th Semester</h3>
  <p>
    <strong>Course:</strong> Artificial Intelligence Lab<br>
    <strong>University:</strong> Green University of Bangladesh
  </p>
  
  <p>
    ⭐ If you found this project helpful, consider giving it a star!<br>
    📬 Feel free to reach out for questions, suggestions, or collaborations.
  </p>
</div>

<hr>

<div align="center">
  <h3>🤖 CareFlow AI - Where Intelligence Meets Healthcare 🏥</h3>
  <p><i>Five AI algorithms working together to save lives, one patient at a time.</i></p>
  
  <p>
    <img src="https://img.shields.io/badge/Made%20with-Python-blue?style=flat-square&logo=python" alt="Made with Python"/>
    <img src="https://img.shields.io/badge/Powered%20by-Flask-red?style=flat-square&logo=flask" alt="Powered by Flask"/>
    <img src="https://img.shields.io/badge/AI-Expert%20System%20%7C%20A*%20%7C%20GA%20%7C%20CSP%20%7C%20ML-brightgreen?style=flat-square" alt="AI Algorithms"/>
  </p>
</div>
