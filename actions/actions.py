# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import datetime as dt
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import AllSlotsReset

from gtts import gTTS
import sys
from subprocess import call
from pydub import AudioSegment

def criar_audio(mensagem):
    saida = '/tmp/audios/mensagem.mp3'

    tts = gTTS(mensagem, lang='pt-br')
    tts.save(saida)

    sound = AudioSegment.from_mp3("/tmp/audios/mensagem.mp3")
    sound.export("/tmp/audios/mensagem.wav", format="wav")

    # print('OLIVIA: ', mensagem)
    call(['aplay', '-D', 'plughw:1,0', '/tmp/audios/mensagem.wav'])     # LINUX

class ActionDesativarMonitoramento(Action):

    def name(self) -> Text:
        return "action_desativar_monitoramento_sites"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #flag = True
        #if flag:
        #    dispatcher.utter_message(text="Teste")
        #    return []

        #telegram_username = tracker.latest_message["metadata"]["from"]["username"] #user that sent the message
        #telegram_chat_type = tracker.latest_message["metadata"]["chat"]["type"]
        
        #is_group = False
        #if telegram_chat_type == 'group':
        #    is_group = True

        monitor_sites_change_properties_file="/home/brleite/projetos/monitor-site-change/scripts/config.properties"
        property_enabled_false="enabled=false\n"

        f = open(monitor_sites_change_properties_file, "w")
        f.write(property_enabled_false)
        f.close()

        #if is_group:
        #    dispatcher.utter_message(text="Monitoramento de sites desabilitado! (GRUPO)")
        #else:
        #    dispatcher.utter_message(text="Monitoramento de sites desabilitado! (INDIVIDUAL)")
        
        dispatcher.utter_message(text="Monitoramento de sites desabilitado!")

        return []

class ActionAtivarMonitoramento(Action):

    def name(self) -> Text:
        return "action_ativar_monitoramento_sites"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        monitor_sites_change_properties_file="/home/brleite/projetos/monitor-site-change/scripts/config.properties"
        property_enabled_false="enabled=true\n"

        f = open(monitor_sites_change_properties_file, "w")
        f.write(property_enabled_false)
        f.close()
        
        dispatcher.utter_message(text="Monitoramento de sites habilitado!")

        return []

class ActionFalarOlivia(Action):
    def name(self) -> Text:
        return "action_falar_olivia"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.sender_id

        if (username == "161484917" or username == "1307765181" or username == "1001307765181"):
                 
          message = tracker.latest_message.get('text')
        
          criar_audio(mensagem=message)

          retorno = "Mensagem enviada."
          
          dispatcher.utter_message(text=retorno)
        else:
          retorno = "Desculpe-me! Você não está autorizado a essa funcionalidade."

          dispatcher.utter_message(text=retorno)
    
class ActionInformarHorario(Action):

    def name(self) -> Text:
        return "action_informar_horario"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"{dt.datetime.now()}")

        return []

class ActionInformarNome(Action):

    def name(self) -> Text:
        return "action_informar_nome"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        nome = tracker.get_slot("nome")
        if not nome:
            dispatcher.utter_message(text="Eu não sei o seu nome.")
        else:
            dispatcher.utter_message(text=f"O seu nome é {nome}!")
        return []

class ActionInformarTime(Action):

    def name(self) -> Text:
        return "action_informar_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        time = tracker.get_slot("time")
        if not time:
            dispatcher.utter_message(text="Eu não sei o seu time.")
        else:
            dispatcher.utter_message(text=f"O seu time é {time}!")
        return []

class ActionReseSlotsAssistente(Action):

    def name(self):
        return "action_reset_slots_assistente"

    def run(self, dispatcher, tracker, domain):
        # return [AllSlotsReset()]
        return [SlotSet("frase_assistente", None)]
