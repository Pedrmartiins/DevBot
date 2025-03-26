import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionInformaClima(Action):
    def name (self) -> Text:
        """Define o nome da action. esse nome deve ser o mesmo registrado no domain.yml"""
        return "action_informa_clima"
   
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        """Este metodo e chamado quando a action e executada. Ele: 
        -obtem a cidade da mensagem do usuario
        - consulta a api de clima
        - envia a resposta ao usuario
        """
        
        
        city = tracker.latest_message['text']
        weather_data = self.get_weather(city)

        print(f"City: {city}")
        print(f"Weather Data: {weather_data}")

        if weather_data:
            response = f"O clima na cidade de {city} esta em: {weather_data ['current'] ['temp_c'] } ℃."
        else:
            response = f"Me desculpe, mas nao consegui obter a situacao do clima da sua cidade de {city}."


        dispatcher.utter_message(text=response)
        return []

@staticmethod
def get_weather(city: str) -> Dict[Text, Any] :

    api_key = "4a26e120ac9e4a529f3235018252503"
    base_url = "http://api. weatherapi.com/v1/current. json"
    params = {
        "q": city,
        "agi": "no",
        "key": api_key

    }

    try:

        print(f"API Request URL: (base_url] ? {params} ")
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        api_response = response. json()
        print(f"API Response: {api_response}")
        return api_response
    except requests. exceptions. RequestException as e:

        print(f"API Request Error: {e}")
        return None