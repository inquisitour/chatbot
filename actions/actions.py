# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import pandas as pd
import random
import json
import requests
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionButtons(Action):

    def name(self) -> Text:
        return "action_show_categories"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('**** Track1 *****')
        track = tracker.latest_message['entities']
        print(track)
        print('*********')
        main_buttons = []
        f = open('./data/games.json')
        json_file = json.load(f)
        all_cat = []
        for i in json_file['data']['categories'][0]['subCategories']:
            all_cat.append(i)
        items = [x['subCategoryName'] for x in all_cat]

        for i, b in enumerate(items):
            payload = "/show_carousels{\"entity\": \"" + str(i) + "\"}"
            print(payload)
            main_buttons.append({"title": b, "payload": payload})  
            print(main_buttons)

        dispatcher.utter_message(text='Great! We have multiple options. Please select one option from the list: ',
                                 buttons=main_buttons)
        return []


class ActionCarousels(Action):

    def name(self) -> Text:
        return "action_show_carousels"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('**** Track2 *****')
        track = tracker.latest_message['entities']
        print(track)
        print('*********')
        
        f = open('./data/games.json')
        json_dict = json.load(f)

        output = []
        for key, val in json_dict.items():
            if key == 'data':
                for key2, val2 in val.items():
                    if key2 == 'categories':
                        temp = val2[0]['subCategories']
                        for i in range(len(temp)):
                            _title = temp[i]['title']
                            _content3 = temp[i]['content3']
                            for j in _content3:
                                _subtitle = j['title']
                                _image_url = j['previewImageUrl']
                                _url = j['gameurl']
                                output.append({
                                    'title': _title,
                                    'subtitle': _subtitle,
                                    'image_url': _image_url,
                                    'url': _url
                                })
        #print(output)
        
        carousel_list = []
        for i in range(len(output)):
            empty_dict = {}
            buttons = [{"title": "Play", "url": "", "type": "web_url"},
                       {"title": "Back", "type": "web_url", "type": "postback", "payload": "/show_categories"}]
            empty_dict['title'] = output[i]['title']
            empty_dict['subtitle'] = output[i]['subtitle']
            empty_dict['image_url'] = output[i]['image_url']
            empty_dict['buttons'] = buttons
            empty_dict['buttons'][0]['url'] = output[i]['url']
            carousel_list.append(empty_dict)
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": carousel_list
            }}
        
        dispatcher.utter_message(attachment=message)
        return []
