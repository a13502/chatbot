from flask import Flask, render_template, request
import openai

# Configure OpenAI API
openai.api_key = 'OPENAI_API_KEY'
completion_model = 'gpt-3.5-turbo'

# Dropdown options for health conditions and severity levels
health_conditions = ['headache', 'cough', 'fever']
severity_levels = ['Low', 'Medium', 'High']

# Initialize Flask app
app = Flask('health_bot', template_folder='Template')

# Define the home route
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get selected options from the form
        condition = request.form['condition']
        severity = request.form['severity']

        # Generate chat response using ChatGPT API
        response = generate_chat_response(condition, severity)

        return render_template('index.html', conditions=health_conditions, severities=severity_levels, response=response)
    else:
        return render_template('index.html', conditions=health_conditions, severities=severity_levels)

# Generate chat response using ChatGPT API
def generate_chat_response(condition, severity):
    # Define system and user messages for conversation
    system_message = {'role': 'system', 'content': 'You are a helpful assistant.'}
    user_message = {'role': 'user', 'content': f"Condition: {condition}\nSeverity: {severity}"}

    # Generate response using ChatGPT API
    response = openai.ChatCompletion.create(
        model=completion_model,
        messages=[system_message, user_message],
        max_tokens=1000,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()


# Run the Flask app
if 'health_bot' == '__main__':
    app.run()
