import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import random

# Load dataset
df = pd.read_csv(r"c:\Users\pramay wankhade\OneDrive\Documents\B.Tech\Sem IV\DAV\Project\Dataset.csv")

# One-Hot Encode the Job_Role column
column_transformer = ColumnTransformer([
    ('one_hot', OneHotEncoder(handle_unknown='ignore'), ['Job_Role'])
], remainder='passthrough')

# Splitting features and target variable
X = df[['Job_Role', 'Years_of_Experience']]
y = df['Average_Salary']

# Transform categorical features
X = column_transformer.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")
print(f"R^2 Score: {r2:.2f}")

# Function to predict salary
def predict_salary(job_role, years_of_experience):
    # Convert input to DataFrame to match training format
    input_data = pd.DataFrame([[job_role, years_of_experience]], columns=['Job_Role', 'Years_of_Experience'])
    
    # Apply the same transformation used during training
    job_encoded = column_transformer.transform(input_data)
    
    # Predict salary
    predicted_salary = model.predict(job_encoded)[0]
    return predicted_salary

def get_salary_stats(job_role):
    # Returns min, avg, and max salary for a given job role.
    role_data = df[df['Job_Role'] == job_role]['Average_Salary']
    if not role_data.empty:
        return role_data.min(), role_data.mean(), role_data.max()
    return None, None, None


# Example usage
if __name__ == "__main__":
    job_role_input = input("Enter Job Role: ")
    years_experience_input = float(input("Enter Years of Experience: "))
    predicted_salary = predict_salary(job_role_input, years_experience_input)
    print(f"Predicted Salary for {job_role_input} with {years_experience_input} years experience: ₹{predicted_salary:,.2f}")
    # plot_actual_vs_predicted(job_role_input, years_experience_input)