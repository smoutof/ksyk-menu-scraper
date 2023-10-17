# Imports
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify
from random import randint

ksyk_url = 'https://ksyk.fi/'
github_repo_url = ''

# Get the menu
def getMenu():
    # Request page
    global ksyk_url, github_repo_url

    page = requests.get(ksyk_url)

    soup = BeautifulSoup(page.content, "html.parser") # Turn into soup object

    # Find the menu div element
    menu_div = soup.find("div", class_="et_pb_column et_pb_column_1_3 et_pb_column_13 et_pb_css_mix_blend_mode_passthrough et-last-child")


    # Day variables, find div element for day
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
            if i.text == '*':
                pass
            elif i.text.lower() == 'leipäpöytä':
                pass
            elif i.text.lower() == 'ruokajuoma':
                pass
            else:
                food_list.append(i.text)
        
        return food_list

    # Make dictionary object with days and foodlist
    def final_d():
        final = {}
        days = [monday, tuesday, wednesday, thursday, friday]
        days_str = ["monday", "tuesday", "wednesday", "thursday", "friday"]

        for day in days:
            index = days.index(day)
            final[days_str[index]] = find_food(day)

        return final

    return final_d()

# Flask App:
app = Flask(__name__)

@app.route('/')
def index():
    return jsonify(getMenu())

app.run()