import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from sklearn.metrics import roc_curve, auc, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from imblearn.combine import SMOTEENN
import warnings
warnings.filterwarnings("ignore")

# Create a directory to save the visualizations
os.makedirs('visualizations', exist_ok=True)

# Set plot style
plt.style.use('default')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['axes.grid'] = True

def save_plot(filename):
    """Save the current figure to the visualizations directory"""
    plt.savefig(f'visualizations/{filename}.png', format='png', bbox_inches='tight', dpi=300)
    plt.close()

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

def create_essential_visualizations(df):
    """Create only the essential visualizations"""
    # 1. Correlation Heatmap
    plt.figure(figsize=(14, 10))
    # Convert categorical to numeric for correlation
    df_corr = df.copy()
    for column in df_corr.select_dtypes(include=['object']).columns:
        df_corr[column] = LabelEncoder().fit_transform(df_corr[column])
    
    corr = df_corr.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", 
                linewidths=0.5, vmin=-1, vmax=1)
    plt.title("Correlation Matrix", fontsize=16, fontweight='bold')
    save_plot("01_correlation_heatmap")
    
    # 2. Churn distribution (important for understanding class imbalance)
    plt.figure(figsize=(10, 5))
    ax = sns.countplot(data=df, x="Churn", palette=['#66b3ff', '#ff9999'])
    plt.title("Distribution of Churn", fontsize=14, fontweight='bold')
    # Add count labels on top of bars
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontsize=12)
    save_plot("02_churn_distribution")

def prepare_data_for_modeling(df):
    """Prepare data for modeling"""
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
    X_selected = X[selected_features]
    
    # 3. Feature importance visualization - FIX: Ensure arrays are the same length
    plt.figure(figsize=(12, 6))
    features_list = list(selected_features)  # Convert to list to ensure consistent ordering
    scores_list = select_feature.scores_[select_feature.get_support()]
    
    # Create DataFrame with correct matching of features and scores
    feature_scores = pd.DataFrame({
        'Feature': features_list,
        'Score': scores_list
    }).sort_values('Score', ascending=False)
    
    sns.barplot(x='Score', y='Feature', data=feature_scores, palette='viridis')
    plt.title('Feature Importance Scores', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_plot("03_feature_importance_scores")

    # Balance dataset
    smote = SMOTEENN(random_state=42)
    X_balanced, y_balanced = smote.fit_resample(X_selected, y)
    
    # Class balance comparison
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    original_counts = pd.Series(y).value_counts()
    plt.pie(original_counts, labels=['No Churn', 'Churn'], autopct='%1.1f%%', colors=['#66b3ff', '#ff9999'])
    plt.title('Original Class Distribution', fontsize=12)
    
    plt.subplot(1, 2, 2)
    balanced_counts = pd.Series(y_balanced).value_counts()
    plt.pie(balanced_counts, labels=['No Churn', 'Churn'], autopct='%1.1f%%', colors=['#66b3ff', '#ff9999'])
    plt.title('Balanced Class Distribution (SMOTEENN)', fontsize=12)
    
    plt.tight_layout()
    save_plot("04_class_balance_comparison")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_balanced, y_balanced, test_size=0.2, random_state=42
    )
    
    return X_selected, y, X_train, X_test, y_train, y_test, selected_features

def train_and_visualize_models(X_train, X_test, y_train, y_test, selected_features):
    """Train models and create performance visualizations"""
    # Train models
    models = {
        "Random Forest": RandomForestClassifier(random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42)
    }
    
    results = {}
    model_predictions = {}
    model_probabilities = {}
    
    for model_name, model in models.items():
        # Train model
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        
        # Store results
        results[model_name] = {
            'train_score': model.score(X_train, y_train),
            'test_score': model.score(X_test, y_test)
        }
        model_predictions[model_name] = y_pred
        model_probabilities[model_name] = y_prob
        
        # 4. Confusion Matrix
        plt.figure(figsize=(8, 6))
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=['No Churn', 'Churn'],
                    yticklabels=['No Churn', 'Churn'])
        plt.xlabel('Predicted', fontsize=12)
        plt.ylabel('Actual', fontsize=12)
        plt.title(f'Confusion Matrix - {model_name}', fontsize=14, fontweight='bold')
        save_plot(f"05_confusion_matrix_{model_name.replace(' ', '_').lower()}")
        
        # 5. Feature Importance
        if hasattr(model, 'feature_importances_'):
            plt.figure(figsize=(12, 8))
            # Create DataFrame with model feature importances
            feature_importance = pd.DataFrame({
                'feature': selected_features,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            sns.barplot(x='importance', y='feature', data=feature_importance, palette='viridis')
            plt.title(f'Feature Importance - {model_name}', fontsize=14, fontweight='bold')
            plt.tight_layout()
            save_plot(f"06_feature_importance_{model_name.replace(' ', '_').lower()}")
    
    # 6. Model Comparison - Accuracy
    plt.figure(figsize=(10, 6))
    comparison_data = pd.DataFrame({
        'Model': list(results.keys()) * 2,
        'Accuracy': [results[model]['train_score'] for model in results] + [results[model]['test_score'] for model in results],
        'Dataset': ['Training'] * len(results) + ['Testing'] * len(results)
    })
    
    sns.barplot(x='Model', y='Accuracy', hue='Dataset', data=comparison_data, palette=['#66b3ff', '#ff9999'])
    plt.title('Model Accuracy Comparison', fontsize=14, fontweight='bold')
    plt.ylim(0.7, 1.0)  # Adjust as needed based on actual scores
    plt.legend(title='')
    save_plot("07_model_accuracy_comparison")
    
    # 7. ROC Curves
    plt.figure(figsize=(10, 8))
    for model_name, y_prob in model_probabilities.items():
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f"{model_name} (AUC = {roc_auc:.3f})")
    
    plt.plot([0, 1], [0, 1], 'k--', label='Random')
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('ROC Curves', fontsize=14, fontweight='bold')
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    save_plot("08_roc_curves")

def main():
    print("Loading and processing data...")
    df = load_and_process_data()
    
    print("Creating essential visualizations...")
    create_essential_visualizations(df)
    
    print("Preparing data for modeling...")
    X, y, X_train, X_test, y_train, y_test, selected_features = prepare_data_for_modeling(df)
    
    print("Training models and creating performance visualizations...")
    train_and_visualize_models(X_train, X_test, y_train, y_test, selected_features)
    
    print(f"All visualizations have been saved to the 'visualizations' directory.")

if __name__ == "__main__":
    main()