import requests, json
from datetime import datetime
from flask import Flask, jsonify

def get_page():
    time = datetime.today().strftime('%Y-%m-%d')
    url = 'https://www.compass-group.fi/menuapi/week-menus?costCenter=3026&date='+str(time)+'&language=fi'
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
    # Needed URLs
    time = datetime.today().strftime('%Y-%m-%d')
    scrape_url = 'https://www.compass-group.fi/menuapi/week-menus?costCenter=3026&date='+str(time)+'&language=fi'
    github_repo_url = 'https://github.com/smoutof/ksyk-menu-scraper'

    #API info
    info = {"github-repo":github_repo_url, "menu-from":scrape_url, "macros-from": "https://www.compass-group.fi/menuapi/recipes/90?language=fi", "last-updated": time}
    page = get_page()
    to_return = {"Info": info,"Week": page["weekNumber"], "Menu": extract_data(page)}
    return to_return



previous = 0
data = {}

def now():
    return datetime.today().strftime('%d')

def last_response():
    global previous
    global data

    today = now() 

    if int(today) != previous:
        data = do_all()
        previous = int(today)
        
    return data
            

# Flask App
    
app = Flask(__name__)

@app.route('/')
def index():
    response = jsonify(last_response())
    response.headers.add('Access-Control-Allow-Origin', '*') 
    return response