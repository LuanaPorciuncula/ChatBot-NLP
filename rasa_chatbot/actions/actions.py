# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
import random

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import json

with open("dataset/restaurant_db.json", "r") as read_file:
    restaurants = json.load(read_file)


class RestaurantAPI:
    def filter_res(self, tracker: Tracker):
        food = tracker.get_slot("restaurant_food")

        area = tracker.get_slot("restaurant_area")
        all_zones = ["centre", "north", "south", "east", "west"]
        area = all_zones if area not in all_zones else [area]

        pricerange = tracker.get_slot("restaurant_pricerange")

        print(food, area, pricerange)
        options = [x for x in filter(lambda x: x["food"] == food and x["area"] in area and x["pricerange"] == pricerange, restaurants)]

        random.shuffle(options)
        options[:min(3, len(options))]

        return options


class ActionFindRestaurants(Action):
    def name(self) -> Text:
        return "action_find_restaurants"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        food = tracker.get_slot("restaurant_food")
        area = tracker.get_slot("restaurant_area")
        pricerange = tracker.get_slot("restaurant_pricerange")
        utter_looking_4_res = f'Searching for {food} restaurants in the {area} with a {pricerange} price...' 
        
        dispatcher.utter_message(text=utter_looking_4_res)
        restaurant_api = RestaurantAPI()
        res = restaurant_api.filter_res(tracker)
        return [SlotSet("restaurant_list", res)]

class ActionShowOptions(Action):
    def name(self):
        return "action_show_options"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        res = tracker.get_slot("restaurant_list")

        buttons = [{"title": x["name"], "payload": '/affirm{"restaurant_name":"' + x["name"] + '"}'} for x in res] + [{"title": "No option", "payload": "/goodbye"}]
        dispatcher.utter_message(text="here's what I found:", buttons=buttons)

        return []