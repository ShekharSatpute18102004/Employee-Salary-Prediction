### Employee Salary Predictor 💼💸
An interactive web application built with Streamlit that predicts realistic employee salaries based on candidate details using a machine learning model. The app also provides career growth projections, profile match insights, and personalized career advice.

Live Demo: https://employee-salary-prediction2.streamlit.app/


## 🛠️ Features

- 📊Predict monthly salary based on education, experience, job title, location, age, and gender.
- 📈 Visualize 10-year salary growth projections with adjustable growth rate.
- 📌Compare candidate profile against ideal job profiles using radar charts.
- 💡Receive tailored career advice and motivational quotes.
- 🎨 User-friendly interface with animations and responsive layout.

## 📁 File Structure
```
Employee-Salary-Predictor/
│
├── app.py                    # Main Streamlit app
├── rf_model_compressed.pkl   # Pre-trained ML model
├── requirements.txt          # Required packages
└── README.md                 # Project documentation
```

## Installation
1. Clone the repository:
```
git clone https://github.com/yourusername/ai-salary-predictor.git
cd Employee-Salary-Predictor
```
2. Create and activate a virtual environment:
```
python -m venv venv
venv\Scripts\activate
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Run the app:
```
streamlit run app.py
```
## 📈 Sample Input Fields
```
Education Level: High School, Bachelor's, Master's, PhD
Years of Experience: 0–30
Age: 18–65
Gender: Male/Female
Job Title: Clerk, Data Scientist, HR Manager, etc.
Location: Urban/Rural
```

## 🧠 How It Works
- Fill in all candidate details in the form.
- Click Predict to see the estimated salary and insights.
- Adjust the expected annual salary growth rate to see projections.
- Explore career tips and motivational quotes for inspiration.


## 📜 License    
This project is licensed under the [MIT License](LICENSE).


