import requests, json
from datetime import datetime
from flask import Flask, jsonify

def get_page():
    url = f'https://www.compass-group.fi/menuapi/week-menus?costCenter=3026&date={datetime.today().strftime('%Y-%m-%d')}&language=fi'
    page = requests.get(url)
    return json.loads(page.content)

def get_macros(id: int):
    page = requests.get(f"https://www.compass-group.fi/menuapi/recipes/{id}?language=fi")
    recipe = json.loads(page.content)
    if not "status" in recipe.keys():
        data = {}

        macro_list = []
        for macro in recipe["nutritionalValues"]:
                macro_list.append(macro)

        data["diets"] = recipe["diets"]
        data["ingredients"] = recipe["ingredientsCleaned"]
        data["macros"] = macro_list
        return data


def extract_data(page: dict):
    menus = page["menus"]
    extracted = {}
    for menu in menus:
        day = menu["dayOfWeek"]
        extracted[day] = []
        for package in menu["menuPackages"]:
            meals = []
            for meal in package["meals"]:
                meals.append((meal["name"], get_macros(meal["recipeId"])))

            extracted[day].append({package["name"]: meals})
    return extracted

def do_all():
    page = get_page()
    return extract_data(page)



      
            

# Flask App
    
app = Flask(__name__)

@app.route('/')
def index():
    response = jsonify(do_all())
    response.headers.add('Access-Control-Allow-Origin', '*') 
    return response