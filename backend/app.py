# app.py
from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import numpy as np
import seaborn as sns
import pickle
import matplotlib.pyplot as plt
import io
import base64
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from imblearn.combine import SMOTEENN
from response import explain_prediction, generate_retention_plan, generate_customer_email
import warnings
warnings.filterwarnings("ignore")

from flask_cors import CORS


app = Flask(__name__)
CORS(app) # 🟢 Enables cross-origin communication with your React frontend

# 🔒 In-memory credential store (Simulating a database table user account allocation)
USER_DATABASE = {}

# ==========================================
#             AUTHENTICATION APIS
# ==========================================

@app.route('/api/register', methods=['POST'])
def api_register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required."}), 400
            
        if email in USER_DATABASE:
            return jsonify({"success": False, "message": "Account already exists with this email."}), 400
            
        # Store user profile dictionary
        USER_DATABASE[email] = {"password": password}
        return jsonify({"success": True, "message": "Registration successful! Proceed to Login."}), 201
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required."}), 400
            
        # Validation checks against the local memory structure
        user = USER_DATABASE.get(email)
        if user and user['password'] == password:
            return jsonify({
                "success": True, 
                "message": "Login successful",
                "user": {"email": email}
            }), 200
        else:
            return jsonify({"success": False, "message": "Incorrect email or password."}), 401
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500



# Set plot style
plt.style.use('default')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['axes.grid'] = True

def create_plot():
    """Helper function to create plot"""
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url

def evaluate_model_performance(model, x_test, y_test, x_train=None, y_train=None, model_name="Model"):
    """Evaluate model performance and return metrics and plots"""
    prediction = model.predict(x_test)
    
    metrics = {
        'model_name': model_name,
        'validation_accuracy': accuracy_score(y_test, prediction),
        'precision': precision_score(y_test, prediction),
        'recall': recall_score(y_test, prediction),
        'f1': f1_score(y_test, prediction),
        'classification_report': classification_report(y_test, prediction)
    }
    
    if x_train is not None and y_train is not None:
        metrics['training_accuracy'] = model.score(x_train, y_train)
    
    # Create confusion matrix plot
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, prediction)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['No Churn', 'Churn'],
                yticklabels=['No Churn', 'Churn'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title(f'Confusion Matrix - {model_name}')
    metrics['confusion_matrix_plot'] = create_plot()
    
    # Feature importance plot
    if hasattr(model, 'feature_importances_'):
        feature_importance = pd.DataFrame({
            'feature': x_test.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x='importance', y='feature', data=feature_importance)
        plt.title(f'Feature Importance - {model_name}')
        metrics['feature_importance_plot'] = create_plot()
        metrics['feature_importance'] = feature_importance.to_dict()
    
    return prediction, metrics

def load_and_process_data():
    """Load and process the dataset"""
    df = pd.read_csv("dataset.csv")
    df.drop('customerID', axis=1, inplace=True)
    
    # Convert TotalCharges to numeric, handling any spaces
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'].str.strip(), errors='coerce')
    df['TotalCharges'].fillna(df['TotalCharges'].mean(), inplace=True)
    
    # Convert categorical values to standard format
    df['SeniorCitizen'] = df['SeniorCitizen'].astype(int)
    
    return df


@app.route('/')
def index():
    """Render the homepage dashboard with initial stats"""
    try:
        # Load and process data to get initial stats
        df = load_and_process_data()
        
        # Calculate initial statistics
        stats = {
            'total_customers': len(df),
            'churn_rate': len(df[df["Churn"] == "Yes"]) / len(df) * 100,
            'avg_monthly_charges': df['MonthlyCharges'].mean(),
            'avg_tenure': df['tenure'].mean(),
            'most_common_contract': df['Contract'].mode()[0]
        }
        
        # Get latest model results if available
        latest_model_results = None
        try:
            with open('trained_model.pkl', 'rb') as file:
                model_data = pickle.load(file)
                if 'metrics' in model_data:
                    latest_model_results = model_data['metrics']
        except Exception as e:
            print(f"Error loading model data: {e}")
        
        # Image paths (relative to static/ directory)
        churn_distribution_image = 'visualizations/02_churn_distribution.png'
        feature_importance_image = 'visualizations/03_feature_importance_scores.png'
        correlation_heatmap_image = 'visualizations/01_correlation_heatmap.png'

        return render_template('index.html', 
                             stats=stats,
                             latest_model_results=latest_model_results,
                             churn_distribution_image=churn_distribution_image,
                             feature_importance_image=feature_importance_image,
                             correlation_heatmap_image=correlation_heatmap_image)
    
    except Exception as e:
        # Provide default values if data loading fails
        default_stats = {
            'total_customers': 0,
            'churn_rate': 0,
            'avg_monthly_charges': 0,
            'avg_tenure': 0,
            'most_common_contract': 'N/A'
        }
        print(f"Error processing data: {e}")
        return render_template('index.html', 
                             stats=default_stats,
                             error=str(e),
                             churn_distribution_image=None,
                             feature_importance_image=None,
                             correlation_heatmap_image=None)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # Define fields outside the POST block since we need them for both GET and POST
    categorical_fields = [
        'gender', 'Partner', 'Dependents', 'PhoneService', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
        'PaperlessBilling', 'PaymentMethod'
    ]
    numeric_fields = ['tenure', 'MonthlyCharges', 'TotalCharges']

    # Handle GET request
    if request.method == 'GET':
        try:
            with open('trained_model.pkl', 'rb') as file:
                model_data = pickle.load(file)
            return render_template('predict.html', 
                                 features=model_data['feature_names'],
                                 prediction=None,
                                 probability=None)
        except Exception as e:
            return render_template('predict.html',
                                 error=f"Error loading model: {str(e)}",
                                 prediction=None,
                                 probability=None)

    # Handle POST request
    elif request.method == 'POST':
        form_data = {}
        try:
            # Load model data
            with open('trained_model.pkl', 'rb') as file:
                model_data = pickle.load(file)
            
            # Process PhoneService first to handle conditional fields
            phone_service = request.form.get('PhoneService')
            if not phone_service:
                raise ValueError("Missing required field: PhoneService")
            form_data['PhoneService'] = phone_service
            
            # Process InternetService next to handle conditional fields
            internet_service = request.form.get('InternetService')
            if not internet_service:
                raise ValueError("Missing required field: InternetService")
            form_data['InternetService'] = internet_service
            
            # Process other categorical fields with conditional validation
            for field in categorical_fields:
                # Skip fields we've already processed
                if field in ['PhoneService', 'InternetService']:
                    continue
                
                # Skip MultipleLines if PhoneService is No
                if field == 'MultipleLines' and form_data['PhoneService'] == 'No':
                    form_data[field] = 'No phone service'
                    continue
                
                # Skip internet-dependent services if InternetService is No
                if field in ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies'] and form_data['InternetService'] == 'No':
                    form_data[field] = 'No internet service'
                    continue
                
                value = request.form.get(field)
                if not value:
                    raise ValueError(f"Missing required field: {field}")
                form_data[field] = value
            
            # Process numeric fields with validation
            for field in numeric_fields:
                value = request.form.get(field)
                try:
                    if not value:
                        raise ValueError(f"Missing required field: {field}")
                    form_data[field] = float(value)
                    if form_data[field] < 0:
                        raise ValueError(f"{field} cannot be negative")
                except ValueError as e:
                    raise ValueError(f"Invalid value for {field}: {str(e)}")
            
            # Handle SeniorCitizen with validation
            senior_citizen = request.form.get('SeniorCitizen')
            if senior_citizen not in ['0', '1']:
                raise ValueError("Invalid value for SeniorCitizen")
            form_data['SeniorCitizen'] = 1 if senior_citizen == '1' else 0
            
            # Encode categorical variables
            encoder = model_data['encoder']
            input_encoded = []
            
            # Create input array with validation
            for feature in model_data['feature_names']:
                value = form_data.get(feature)
                if feature in categorical_fields:
                    try:
                        value = encoder.transform([value])[0]
                    except Exception:
                        # Log the unknown category
                        app.logger.warning(f"Unknown category '{value}' for feature '{feature}'")
                        value = 0
                input_encoded.append(value)
            
            # Make prediction
            prediction = model_data['model'].predict([input_encoded])[0]
            probability = model_data['model'].predict_proba([input_encoded])[0][1]
            
            # Inside your predict route after making the prediction
            explanation = explain_prediction(probability, form_data, model_data.get('feature_importance'))
            retention_plan = generate_retention_plan(probability, form_data, explanation)
            customer_email = generate_customer_email(probability, form_data)

            # Then include these in your template rendering
            return render_template('predict.html',
                                features=model_data.get('feature_names', []),
                                prediction=prediction,
                                probability=probability,
                                form_data=form_data,
                                explanation=explanation,
                                retention_plan=retention_plan,
                                customer_email=customer_email)
                                 
        except ValueError as e:
            # Handle validation errors
            return render_template('predict.html',
                                 features=model_data.get('feature_names', []),
                                 error=str(e),
                                 prediction=None,
                                 probability=None,
                                 form_data=form_data)
        except Exception as e:
            # Handle unexpected errors
            app.logger.error(f"Prediction error: {str(e)}")
            return render_template('predict.html',
                                 features=model_data.get('feature_names', []),
                                 error="An unexpected error occurred during prediction.",
                                 prediction=None,
                                 probability=None,
                                 form_data=form_data)
    # GET request - show empty form
    try:
        with open('trained_model.pkl', 'rb') as file:
            model_data = pickle.load(file)
        return render_template('predict.html', features=model_data['feature_names'], probability=None)
    except Exception as e:
        return render_template('predict.html', 
                             error="Model not found. Please train the model first.",
                             probability=None)



@app.route('/analyze', methods=['GET'])
def analyze():
    """Perform data analysis"""
    df = load_and_process_data()
    
    # Generate EDA plots
    plots = {}
    
    # Senior Citizens distribution
    plt.figure(figsize=(10, 5))
    plt.pie(df["SeniorCitizen"].value_counts(), autopct="%.1f%%", labels=["No", "Yes"])
    plt.title("Distribution of Senior Citizens")
    plots['senior_citizens'] = create_plot()
    
    # Churn distribution
    plt.figure(figsize=(10, 5))
    sns.countplot(data=df, x="Churn")
    plt.title("Distribution of Churn")
    plots['churn_distribution'] = create_plot()
    
    # Contract Type Distribution
    plt.figure(figsize=(10, 5))
    sns.countplot(data=df, x="Contract", hue="Churn")
    plt.title("Churn by Contract Type")
    plt.xticks(rotation=45)
    plots['contract_distribution'] = create_plot()
    
    # Monthly Charges Distribution
    plt.figure(figsize=(10, 5))
    sns.boxplot(data=df, x="Churn", y="MonthlyCharges")
    plt.title("Monthly Charges by Churn Status")
    plots['monthly_charges'] = create_plot()
    
    # Calculate statistics
    stats = {
        'total_customers': len(df),
        'churn_rate': len(df[df["Churn"]=="Yes"]) / len(df) * 100,
        'senior_citizen_rate': len(df[df["SeniorCitizen"]==1]) / len(df) * 100,
        'avg_monthly_charges': df['MonthlyCharges'].mean(),
        'avg_tenure': df['tenure'].mean(),
        'most_common_contract': df['Contract'].mode()[0]
    }
    
    return render_template('analysis.html', plots=plots, stats=stats)


@app.route('/train', methods=['GET', 'POST'])
def train_models():
    """Train and evaluate models"""
    try:
        # Load and process data
        df = load_and_process_data()

        # Encode categorical variables
        encoder = LabelEncoder()
        for feature in df.select_dtypes(include='object').columns:
            df[feature] = encoder.fit_transform(df[feature])

        # Feature selection
        X = df.drop("Churn", axis=1)
        y = df["Churn"]

        select_feature = SelectKBest(score_func=f_classif, k=10)
        select_feature.fit(X, y)
        selected_features = X.columns[select_feature.get_support()]
        X = X[selected_features]

        # Balance dataset
        smote = SMOTEENN(random_state=42)
        X_balanced, y_balanced = smote.fit_resample(X, y)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_balanced, y_balanced, test_size=0.2, random_state=42
        )

        # Train models and get results
        results = []
        models = {
            "Random Forest": RandomForestClassifier(random_state=42),
            "Gradient Boosting": GradientBoostingClassifier(random_state=42)
        }
        model_accuracies = {}

        for model_name, model in models.items():
            model.fit(X_train, y_train)
            predictions, metrics = evaluate_model_performance(
                model, X_test, y_test, X_train, y_train, model_name
            )
            results.append(metrics)
            model_accuracies[model_name] = metrics['validation_accuracy']

        # Select best model
        best_model_name = max(model_accuracies, key=model_accuracies.get)
        best_model = models[best_model_name]

        # Save model data
        model_data = {
            'model': best_model,
            'feature_names': selected_features.tolist(),
            'encoder': encoder,
            'features_info': {col: list(df[col].unique()) for col in df.columns if col != 'Churn'}
        }

        with open('trained_model.pkl', 'wb') as file:
            pickle.dump(model_data, file)

        # Generate overall visualizations
        plots = {}

        # Model Accuracies Comparison
        plt.figure(figsize=(10, 5))
        sns.barplot(x=list(model_accuracies.keys()), y=list(model_accuracies.values()))
        plt.ylabel('Accuracy')
        plt.title('Model Accuracies Comparison')
        plots['model_accuracies_plot'] = create_plot()

        # ROC Curve
        plt.figure(figsize=(10, 5))
        for model_name, model in models.items():
            from sklearn.metrics import roc_curve, auc
            y_probs = model.predict_proba(X_test)[:, 1]
            fpr, tpr, _ = roc_curve(y_test, y_probs)
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, label=f"{model_name} (AUC = {roc_auc:.2f})")

        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curves')
        plt.legend()
        plots['roc_curves_plot'] = create_plot()

        # Precision-Recall Curve
        plt.figure(figsize=(10, 5))
        for model_name, model in models.items():
            from sklearn.metrics import precision_recall_curve
            y_probs = model.predict_proba(X_test)[:, 1]
            precision, recall, _ = precision_recall_curve(y_test, y_probs)
            plt.plot(recall, precision, label=model_name)

        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curves')
        plt.legend()
        plots['precision_recall_curves_plot'] = create_plot()

        return render_template('results.html', results=results, **plots)

    except Exception as e:
        return jsonify({'error': True, 'message': str(e)}), 400

app = app 

if __name__ == '__main__':
    app.run(debug=True)