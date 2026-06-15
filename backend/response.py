from dotenv import load_dotenv
import google.generativeai as genai
import os
import json

load_dotenv()

def explain_prediction(probability, input_data, feature_importance=None):
    """
    Generate an explanation for the churn prediction using Google Gemini.
    
    Args:
        probability (float): The predicted probability of customer churn (0-1)
        input_data (dict): Dictionary containing customer input features
        feature_importance (dict, optional): Feature importance from the model
    
    Returns:
        str: AI-generated explanation of the churn prediction
    """
    
    # Format feature importance for the prompt if available
    importance_text = ""
    if feature_importance:
        importance_text = "Feature Importance (Ordered by Impact on Churn Probability):\n"
        for feature, importance in feature_importance.items():
            if isinstance(importance, dict) and 'importance' in importance:
                importance_text += f"- {feature}: {importance['importance']:.3f}\n"
            else:
                importance_text += f"- {feature}: {importance:.3f}\n"
    
    # Create different explanations based on probability threshold
    if probability < 0.3:
        risk_level = "Low Risk"
        churn_explanation = f"""
Customer has a low probability of churning ({probability:.1%}). 

This indicates that they are likely satisfied with our telecom services. Here are some reasons why they are staying:

Customer seems satisfied with current service offerings
Their usage patterns indicate strong engagement with our services
Contract terms and pricing appear to meet their needs
Customer demographic profile suggests loyalty

While churn risk is low, we should continue to engage them by:
Offering loyalty rewards or exclusive benefits to reinforce their commitment
Personalized service recommendations based on their usage patterns
Proactive customer support to ensure continued satisfaction

Our goal is to maintain this positive relationship and further solidify their trust in our company.
"""
    elif probability < 0.6:
        risk_level = "Medium Risk"
        churn_explanation = f"""
Customer has a moderate probability of churning ({probability:.1%}).

This indicates some potential dissatisfaction or competitive vulnerability:

Some engagement metrics show warning signs
Customer may be comparing our services with competitors
Certain aspects of their service experience could be improved
Usage patterns suggest possible service gaps

Recommended actions to reduce churn risk:
Targeted service upgrades or special promotions
Proactive outreach to address potential pain points
Service review to identify improvement opportunities
Loyalty incentives to strengthen relationship

Addressing these concerns promptly can help retain this customer.
"""
    else:
        risk_level = "High Risk"
        churn_explanation = f"""
Customer has a high probability of churning ({probability:.1%}).

Here are key factors contributing to their churn risk:
Service dissatisfaction indicators are present
Contract terms may not be competitive
Usage and engagement metrics show concerning patterns
Customer profile matches high-churn segments

Immediate retention actions required:
Personalized retention offer with significant value proposition
Direct customer outreach to address specific concerns
Service plan review and optimization
Premium support services to demonstrate commitment to customer satisfaction

Urgent intervention is needed to prevent losing this customer.
"""

    # Input data formatting for the prompt
    formatted_input = json.dumps(input_data, indent=2)

    prompt = f"""
You are an expert telecommunications analyst specializing in customer retention. 
Your task is to interpret a machine learning prediction for customer churn and provide an accurate, data-driven analysis.

Customer Profile:  
{formatted_input}

Churn Probability: {probability:.1%}  
Risk Level: {risk_level}

{importance_text}

{churn_explanation}

Based on the above information, provide a concise, professional explanation of:
1. Why this customer is likely to churn or stay
2. The specific factors in their profile that most influence this prediction
3. Targeted recommendations to retain this customer

Make the explanation data-driven, referencing specific values from their profile when relevant.
Ensure the response is clear, professional, and actionable for our retention team.
"""

    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating explanation: {str(e)}"


def generate_retention_plan(probability, input_data, explanation):
    """
    Generate a personalized retention plan using Google Gemini.
    
    Args:
        probability (float): The predicted probability of customer churn (0-1)
        input_data (dict): Dictionary containing customer input features
        explanation (str): The explanation generated for the prediction
    
    Returns:
        str: AI-generated retention plan
    """
    
    formatted_input = json.dumps(input_data, indent=2)
    
    # Create a retention approach based on probability
    if probability < 0.4:
        approach = "loyalty enhancement"
    elif probability < 0.7:
        approach = "proactive engagement"
    else:
        approach = "urgent intervention"

    prompt = f"""
You are a customer retention specialist at a telecommunications company. 
Your task is to create a detailed, actionable retention plan for a customer who has a {probability:.1%} probability of churning.

Customer Profile:  
{formatted_input}

Analysis of Churn Risk:  
{explanation}  

Create a comprehensive retention plan with the following sections:

1. (Brief overview of the customer situation and churn risk)
2. KEY RISK FACTORS (Identify the specific factors driving potential churn)
3. RETENTION STRATEGY (Detailed approach for {approach})
4. ACTION ITEMS (Specific, actionable steps)
5. SUCCESS METRICS (How to measure if retention efforts are working)

Make the plan specific to this customer's situation, referencing their service usage, contract details, and other relevant data points.
The plan should be practical, detailed, and immediately implementable by our retention team.
"""
    
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating retention plan: {str(e)}"


def generate_customer_email(probability, input_data, customer_name="Valued Customer"):
    """
    Generate a personalized customer email based on churn prediction using Google Gemini.
    
    Args:
        probability (float): The predicted probability of customer churn (0-1)
        input_data (dict): Dictionary containing customer input features
        customer_name (str): The customer's name for personalization
    
    Returns:
        str: AI-generated email to the customer
    """
    
    formatted_input = json.dumps(input_data, indent=2)
    
    # Determine email approach based on churn probability
    if probability < 0.4:
        email_type = "appreciation and value-add"
        subject_suggestion = "Thank You for Your Loyalty - Special Offer Inside"
    elif probability < 0.7:
        email_type = "service enhancement"
        subject_suggestion = "Enhancing Your Experience with Us - Exclusive Offer"
    else:
        email_type = "win-back"
        subject_suggestion = "We Value Your Business - Important Service Updates"

    prompt = f"""
You are a customer relations specialist at a telecommunications company.

Customer Profile:  
{formatted_input}

Churn Probability: {probability:.1%}

Write a personalized email to {customer_name} with the purpose of retention through {email_type}.

Requirements:
1. Professional but warm tone
2. Personalized offers based on their profile 
3. Clear value proposition
4. Specific call to action
5. Subject line suggestion: "{subject_suggestion}" (you can improve this)

DO NOT mention:
- Churn prediction
- Risk assessment
- That this is automated
- Any internal analysis we've done

The email should appear as a thoughtful, personal outreach from our customer service team.
Sign the email from "Customer Success Team, churnIT"
"""
    
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating email: {str(e)}"