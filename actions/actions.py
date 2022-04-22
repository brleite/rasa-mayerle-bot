# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import datetime as dt
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.types import DomainDict

from gtts import gTTS
import sys
from subprocess import call
from pydub import AudioSegment

import telegrambot as bot

def clean_value(value):
    return "".join([c for c in value if c.isalpha()])

def criar_audio(mensagem):
    saida = '/tmp/audios/mensagem.mp3'

    tts = gTTS(mensagem, lang='pt-br')
    tts.save(saida)

    sound = AudioSegment.from_mp3("/tmp/audios/mensagem.mp3")
    sound.export("/tmp/audios/mensagem.wav", format="wav")

    # print('OLIVIA: ', mensagem)
    call(['aplay', '-D', 'plughw:1,0', '/tmp/audios/mensagem.wav'])     # LINUX

def gravar_audio_microfone(duracao, arquivo_saida):
    call(['arecord', '-f', 'S32_LE', '-r', '44100', '-D', 'plughw:CARD=PCH,DEV=0', arquivo_saida, '-d', '5'])

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

        monitor_sites_change_properties_file="/home/brleite/projetos/monitor-site-changes/scripts/config.properties"
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

        monitor_sites_change_properties_file="/home/brleite/projetos/monitor-site-changes/scripts/config.properties"
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
                 
          #  message = tracker.latest_message.get('text')
          message = tracker.get_slot("frase_assistente")
        
          criar_audio(mensagem=message)

          retorno = "Mensagem enviada."
          
          dispatcher.utter_message(text=retorno)
        else:
          retorno = "Desculpe-me! Você não está autorizado(a) a essa funcionalidade."

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

class ActionResetSlotsAssistente(Action):

    def name(self):
        return "action_reset_slots_assistente"

    def run(self, dispatcher, tracker, domain):
        # return [AllSlotsReset()]
        return [SlotSet("frase_assistente", None)]

class ValidateFraseAssistenteForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_frase_assistente_form"

    def validate_frase_assistente(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `frase_assistente` value."""

        # If the name is super short, it might be wrong.
        value = clean_value(slot_value)
        if len(value) == 0:
            dispatcher.utter_message(text="Talvez você tenha digitado errado")
            return {"frase_assistente": None}
        return {"frase_assistente": slot_value}

class ValidateGravarAudioMicrofoneForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_gravar_audio_microfone_form"

    def validate_duracao(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `duracao` value."""

        try:
            duracao = int(slot_value)
            
            if duracao > 60:
                dispatcher.utter_message(text="Você informou um valor superior a 60.")
                return {"duracao": None}
                
            return {"duracao": slot_value}
        except:
            dispatcher.utter_message(text="Você informou um valor inválido. Digite somente números.")
            return {"duracao": None}            

class ActionGravarAudio(Action):

    def name(self):
        return "action_gravar_audio_microfone"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       
        channel = tracker.get_latest_input_channel()
        print(channel)

        if (channel != "telegram"):
            dispatcher.utter_message(text="Canal não suportado para essa funcionalidade.")
            return
 
        username = tracker.sender_id

        if (username == "161484917" or username == "1307765181" or username == "1001307765181"):
                 
            duracaoStr = tracker.get_slot("duracao_gravacao")
            duracao = int(duracaoStr)

            if (duracao <= 60):
                gravar_audio_microfone(duracao, '/tmp/audios/audio_mic.mp3')
                
                dispatcher.utter_message(text='Áudio gravado com sucesso.')
            else:
                dispatcher.utter_message(text='Não foi possível realizar a gravação. A duração especificada é muito longa.')
                
        else:
          retorno = "Desculpe-me! Você não está autorizado(a) a essa funcionalidade."

          dispatcher.utter_message(text=retorno)

class ActionResetSlotsGravarAudioMicrofone(Action):

    def name(self):
        return "action_reset_slots_gravar_audio_microfone"

    def run(self, dispatcher, tracker, domain):
        # return [AllSlotsReset()]
        return [SlotSet("duracao", None)]

