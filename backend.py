from flask import Flask, render_template, request, jsonify
import os
import openai
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

# Function to generate AI-powered recipe
def generate_gino_recipe(nickname, personality, ingredients, cooking_style, spice_level):
    prompt = (
        f"Create a unique Nigerian recipe using {ingredients}, and it MUST include 'Gino Pepper Chicken' seasoning. "
        f"The cooking style should be {cooking_style}. "
        f"The dish should have a spice level of {spice_level}. "
        f"Name the dish after '{nickname}', incorporating their personality: '{personality}'. "
        f"Provide a fun and creative recipe name, a list of ingredients (ensuring 'Gino Pepper Chicken' seasoning is included), "
        f"and step-by-step cooking instructions that also mention using 'Gino Pepper Chicken' seasoning."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Nigerian chef specializing in traditional and innovative recipes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400
        )
        recipe_text = response['choices'][0]['message']['content']

        # Extracting recipe name (Assuming first line is the name)
        recipe_lines = recipe_text.split("\n")
        recipe_name = recipe_lines[0] if recipe_lines else "Special Recipe"

        return recipe_name, recipe_text
    except Exception as e:
        return "Error", f"Error generating recipe: {str(e)}"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate-recipe', methods=['POST'])
def generate_recipe():
    data = request.json
    recipe_name, recipe = generate_gino_recipe(
        data['nickname'],
        data['personality'],
        data['ingredients'],
        data['cooking_style'],
        data['spice_level']
    )
    return jsonify({'recipe_name': recipe_name, 'recipe': recipe})

@app.route('/random-recipe', methods=['GET'])
def random_recipe():
    sample_recipes = [
        "Jollof Rice with Grilled Chicken and Gino Pepper Chicken Seasoning",
        "Egusi Soup with Pounded Yam and Gino Pepper Chicken Seasoning",
        "Suya Spiced Beef Wrap with Gino Pepper Chicken Seasoning",
        "Pepper Soup with Fresh Fish and Gino Pepper Chicken Seasoning"
    ]
    return jsonify({'recipe_name': "Chef's Special", 'recipe': sample_recipes[os.urandom(1)[0] % len(sample_recipes)]})

if __name__ == '__main__':
    app.run(debug=True)
