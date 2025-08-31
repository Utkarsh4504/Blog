import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

def train_and_save_model():
    """
    This function demonstrates a full, simplified workflow for training
    a vulnerability prediction model and saving it to a file.
    """
    print("Starting the AI model training process...")

    # --- Step 1: Create a Sample Dataset ---
    # In the real world, you would get this from vulnerability databases
    # (like CVE details) or by running scans on known vulnerable systems.
    data = {
        'service_info': [
            'apache httpd 2.4.29', 'apache httpd 2.4.51', 'openssh 7.6p1',
            'openssh 8.2p1', 'vsftpd 2.3.4', 'vsftpd 3.0.3',
            'proftpd 1.3.5', 'proftpd 1.3.6', 'nginx 1.14.0', 'nginx 1.21.0'
        ],
        'is_vulnerable': [
            1, 0, 1, 0, 1, 0, 1, 0, 1, 0  # 1 for vulnerable, 0 for not
        ]
    }
    df = pd.DataFrame(data)
    print("\n[Step 1] Sample dataset created:")
    print(df)

    # --- Step 2: Define Features (X) and Target (y) ---
    X = df['service_info']
    y = df['is_vulnerable']

    # Split data for training and testing (good practice)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- Step 3: Create a Machine Learning Pipeline ---
    # A pipeline chains together the steps:
    # 1. TfidfVectorizer: Converts text data into numerical vectors (Feature Engineering).
    # 2. LogisticRegression: The algorithm that learns to classify the data (The "Model").
    pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer()),
        ('classifier', LogisticRegression())
    ])
    print("\n[Step 2] Machine learning pipeline created.")

    # --- Step 4: Train the Model ---
    print("\n[Step 3] Training the model on the data...")
    pipeline.fit(X_train, y_train)
    print("Training complete.")

    # --- Step 5: Evaluate the Model (Optional but Recommended) ---
    accuracy = pipeline.score(X_test, y_test)
    print(f"\n[Step 4] Model accuracy on test data: {accuracy * 100:.2f}%")

    # --- Step 6: Save the Trained Model ---
    model_filename = 'vulnerability_scanner.pkl'
    print(f"\n[Step 5] Saving the trained model to '{model_filename}'...")
    joblib.dump(pipeline, model_filename)
    print("Model saved successfully!")

    return model_filename

if __name__ == '__main__':
    # Run the training process
    trained_model_file = train_and_save_model()

    # --- How to use the saved model ---
    print(f"\n--- Example of loading and using the model ---")
    # Load the model from the file
    loaded_model = joblib.load(trained_model_file)

    # New data to predict
    new_services = ['apache httpd 2.4.29', 'nginx 1.21.4']
    print(f"Predicting vulnerabilities for: {new_services}")

    # Make predictions
    predictions = loaded_model.predict(new_services)

    for service, prediction in zip(new_services, predictions):
        status = "Vulnerable" if prediction == 1 else "Not Vulnerable"
        print(f" - '{service}': {status}")
