# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
import random

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset
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

        options = [x for x in filter(lambda x: x["food"] == food and x["area"] in area and x["pricerange"] == pricerange, restaurants)]

        # add variety to result
        random.shuffle(options)
        # limit result options
        options = options[:min(4, len(options))]

        return options


class ActionFindRestaurants(Action):


    def name(self) -> Text:
        return "action_find_restaurants"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # getting stored slot values
        food = tracker.get_slot("restaurant_food")
        area = tracker.get_slot("restaurant_area")
        pricerange = tracker.get_slot("restaurant_pricerange")

        # informing user of the collected slots and search in progress
        utter_looking_4_res = f'Searching for {food} restaurants in the {area} with a {pricerange} price...' 
        dispatcher.utter_message(text=utter_looking_4_res)
        
        # select restaurants
        restaurant_api = RestaurantAPI()
        res = restaurant_api.filter_res(tracker)

        return [SlotSet("restaurant_list", res)]


class ActionShowOptions(Action):


    def name(self):
        return "action_show_options"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # get restaurant list in the slot
        res = tracker.get_slot("restaurant_list")
    
        resIntro = "here's what I found:\n"
        for x in res:
            if (x.get("introduction")):
                resIntro += x["name"].upper() + ": " +x["introduction"]+ "\n"
            else:
                resIntro += x["name"].upper() + "\n"
        
        buttons = [{"title": x["name"], "payload": '/affirm{"restaurant_name":"' + x["name"] + '"}'} for x in res] + [{"title": "No option, bye!", "payload": "/goodbye"}]
        dispatcher.utter_message(text=resIntro, buttons=buttons)

        return []


class ActionResetFindResSlots(Action):


    def name(self):
        return "action_reset_find_res_slots"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        return [SlotSet("restaurant_food", None),SlotSet("restaurant_area", None),SlotSet("restaurant_pricerange", None), SlotSet("restaurant_list", None)]

    
class ActionResetBookResSlots(Action):


    def name(self):
        return "action_reset_book_res_slots"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        return [SlotSet("restaurant_name", None),SlotSet("restaurant_bookpeople", None),SlotSet("restaurant_bookday", None), SlotSet("restaurant_booktime", None)]


class ActionResetAllSlots(Action):


    def name(self):
        return "action_reset_all_slots"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        return [AllSlotsReset()]