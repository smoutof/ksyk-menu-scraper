# Imports
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

# Needed URLs
ksyk_url = 'https://ksyk.fi/'
github_repo_url = 'https://github.com/smoutof/ksyk-menu-scraper'

#API info
info = {"github-repo":github_repo_url, "scraped-from":ksyk_url}

# Get the menu
def getMenu():
    # Request page

    page = requests.get(ksyk_url)
    soup = BeautifulSoup(page.content, "html.parser") # Turn into soup object

    # Find the menu div element
    menu_div = soup.find("div", class_="et_pb_column et_pb_column_1_3 et_pb_column_13 et_pb_css_mix_blend_mode_passthrough et-last-child")


    # Day variables, find div element for day
    week = menu_div.find("li", class_="et_pb_tab_0 et_pb_tab_active")
    monday = menu_div.find("div", class_="et_pb_tab et_pb_tab_1 clearfix")
    tuesday= menu_div.find("div", class_="et_pb_tab et_pb_tab_2 clearfix")
    wednesday = menu_div.find("div", class_="et_pb_tab et_pb_tab_3 clearfix")
    thursday = menu_div.find("div", class_="et_pb_tab et_pb_tab_4 clearfix")
    friday = menu_div.find("div", class_="et_pb_tab et_pb_tab_5 clearfix")

    # Find all text for days food and make list
    def find_food(day):
        p = day.find_all("p")
        food_list = []

        for i in p:
            food_list.append( str(i.get_text(";")) )

        final_string = ';'.join(map(str, food_list))

        return final_string

    # Make dictionary object with days and foodlist
    def final_d():
        final = {}
        week_a = week.find("a")
        final["Week"] = week_a.text

        days = [monday, tuesday, wednesday, thursday, friday]
        days_str = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        for day in days:
            index = days.index(day)
            final[days_str[index]] = find_food(day)

        return final

    return final_d()

# Flask App:

app = Flask(__name__)

@app.route('/')
def index():
    response = jsonify({"API-data":info,"menu-data":getMenu()})
    response.headers.add('Access-Control-Allow-Origin', '*') 
    return response