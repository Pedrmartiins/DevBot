import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionBuscarPorTitulo(Action):
    def name(self) -> Text:
        return "action_buscar_por_titulo"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:

        titulo = next(tracker.get_latest_entity_values("titulo"), None)
        if not titulo:
            dispatcher.utter_message(text="Qual é o título do livro que você procura?")
            return []
        
        url = f"https://openlibrary.org/search.json?title={titulo}"
        response = requests.get(url)
        data = response.json()

        if data["numFound"] > 0:
            livros = data["docs"][:3]
            mensagens = [f"- {livro.get('title')} por {', '.join(livro.get('author_name', []))}" for livro in livros]
            dispatcher.utter_message(text="Aqui estão alguns resultados:\n" + "\n".join(mensagens))
        else:
            dispatcher.utter_message(text="Desculpe, não encontrei nenhum livro com esse título.")
            return []
        

class ActionBuscarPorAutor(Action):
    def name(self) -> Text:
        return "action_buscar_por_autor"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:

        autor = next(tracker.get_latest_entity_values("autor"), None)
        if not autor:
            dispatcher.utter_message(text="Qual é o autor do livro que você procura?")
            return []
        
        url = f"https://openlibrary.org/search.json?author={autor}"
        response = requests.get(url)
        data = response.json()

        if data["numFound"] > 0:
            livros = data["docs"][:3]
            mensagens = [f"- {livro.get('title')} ({livro.get('first_publish_year', 'Ano desconhecido')})" for livro in livros]
            dispatcher.utter_message(text="Aqui estão alguns livros do autor:\n" + "\n".join(mensagens))
        else:
            dispatcher.utter_message(text="Desculpe, não encontrei livros deste autor.")
            return []


class ActionBuscarPorAssunto(Action):
    def name(self) -> Text:
        return "action_buscar_por_assunto"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:

        assunto = next(tracker.get_latest_entity_values("assunto"), None)
        if not assunto:
            dispatcher.utter_message(text="Qual é o assunto ou tema do livro que você procura?")
            return []
        
        url = f"https://openlibrary.org/search.json?subject={assunto}"
        response = requests.get(url)
        data = response.json()

        if data["numFound"] > 0:
            livros = data["docs"][:3]
            mensagens = [f"- {livro.get('title')} por {', '.join(livro.get('author_name', []))}" for livro in livros]
            dispatcher.utter_message(text="Aqui estão alguns livros sobre o assunto:\n" + "\n".join(mensagens))
        else:
            dispatcher.utter_message(text="Desculpe, não encontrei livros sobre esse assunto.")
            return []
