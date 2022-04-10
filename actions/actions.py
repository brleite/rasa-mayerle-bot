# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

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
        
        criar_audio(mensagem="Oi pessoal!")

        dispatcher.utter_message(text="Mensagem enviada.")
    



