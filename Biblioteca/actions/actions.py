import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionBuscarLivro(Action):

    def name(self) -> str:
        return "action_buscar_livro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
       
        titulo_livro = next(tracker.get_latest_entity_values("titulo_livro"), None)
        
        if titulo_livro:
           
            url = f"https://openlibrary.org/search.json?title={titulo_livro}"
            response = requests.get(url)
            data = response.json()

            if data['num_found'] > 0:
                livro = data['docs'][0]
                dispatcher.utter_message(text=f"Encontrei o livro: {livro['title']} por {livro.get('author_name', 'Desconhecido')}.")
            else:
                dispatcher.utter_message(text="Desculpe, não encontrei nenhum livro com esse título.")
        else:
            dispatcher.utter_message(text="Você não especificou um título de livro. Tente novamente.")
        
        return []
