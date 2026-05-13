# Step 1: Import Required Libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib  # For saving and loading models

# Step 2: Load and Prepare the Data
# Load dataset (Titanic dataset as an example)
df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")

# Select relevant features
features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
df = df[features + ['Survived']].dropna()  # Drop rows with missing values

# Display the first few rows of the dataset
print("Data Sample:\n", df.head())

# Step 3: Define Preprocessing Steps
# Define numerical and categorical features
num_features = ['Age', 'SibSp', 'Parch', 'Fare']
cat_features = ['Pclass', 'Sex', 'Embarked']

# Define transformers for preprocessing
num_transformer = StandardScaler()  # Standardize numerical features
cat_transformer = OneHotEncoder(handle_unknown='ignore')  # One-hot encode categorical features

# Combine transformers into a single preprocessor
preprocessor = ColumnTransformer([
    ('num', num_transformer, num_features),
    ('cat', cat_transformer, cat_features)
])

# Step 4: Split Data into Training and Testing Sets
# Define target and features
X = df[features]
y = df['Survived']

# Split into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training set shape: {X_train.shape}")
print(f"Testing set shape: {X_test.shape}")

# Step 5: Build the Machine Learning Pipeline
# Define the pipeline (includes preprocessing + RandomForest classifier)
pipeline = Pipeline([
    ('preprocessor', preprocessor),  # Apply preprocessing steps
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))  # ML model (RandomForest)
])

# Step 6: Train the Model
# Train the model using the pipeline
pipeline.fit(X_train, y_train)
print("Model training complete!")

# Step 7: Evaluate the Model
# Make predictions on the test data
y_pred = pipeline.predict(X_test)

# Compute accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# Step 8: Save and Load the Model
# Save the trained pipeline (preprocessing + model)
joblib.dump(pipeline, 'ml_pipeline.pkl')

# Load the model back
loaded_pipeline = joblib.load('ml_pipeline.pkl')

# Predict using the loaded model
sample_data = pd.DataFrame([{'Pclass': 3, 'Sex': 'male', 'Age': 25, 'SibSp': 0, 'Parch': 0, 'Fare': 7.5, 'Embarked': 'S'}])
prediction = loaded_pipeline.predict(sample_data)

# Output prediction for a sample input
print(f"Prediction for Sample Data: {'Survived' if prediction[0] == 1 else 'Did not Survive'}")