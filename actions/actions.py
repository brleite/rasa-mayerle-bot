# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import datetime as dt
from typing import Any, Text, Dict, List
from os.path import exists

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

ARQUIVO_AUDIO_GRAVADO_MICROFONE = '/tmp/audios/audio_mic.mp3'
ARQUIVO_AUDIO_GRAVADO_OLIVIA_MP3 = '/tmp/audios/mensagem.mp3'
ARQUIVO_AUDIO_GRAVADO_OLIVIA = '/tmp/audios/mensagem.wav'

DEBUG_MODE = False 

def clean_value(value):
    return "".join([c for c in value if c.isalpha()])

def tocar_audio(arquivo):
    call(['aplay', '-D', 'plughw:1,0', arquivo])

def criar_audio(mensagem):
    tts = gTTS(mensagem, lang='pt-br')
    tts.save(ARQUIVO_AUDIO_GRAVADO_OLIVIA_MP3)

    sound = AudioSegment.from_mp3(ARQUIVO_AUDIO_GRAVADO_OLIVIA_MP3)
    sound.export(ARQUIVO_AUDIO_GRAVADO_OLIVIA, format="wav")

    # print('OLIVIA: ', mensagem)
    # call(['aplay', '-D', 'plughw:1,0', '/tmp/audios/mensagem.wav'])     # LINUX
    tocar_audio(arquivo=ARQUIVO_AUDIO_GRAVADO_OLIVIA)


def gravar_audio_microfone(duracao, arquivo_saida):
    call(['arecord', '-f', 'S32_LE', '-r', '44100', '-D', 'plughw:CARD=PCH,DEV=0', arquivo_saida, '-d', str(duracao)])

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

        if (DEBUG_MODE == True or username == "161484917" or username == "1307765181" or username == "1001307765181"):
                 
          #  message = tracker.latest_message.get('text')
          message = tracker.get_slot("frase_assistente")
        
          criar_audio(mensagem=message)

          retorno = "Mensagem enviada."
          
          dispatcher.utter_message(text=retorno)
        else:
          retorno = "Desculpe-me! Voc?? n??o est?? autorizado(a) a essa funcionalidade."

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
            dispatcher.utter_message(text="Eu n??o sei o seu nome.")
        else:
            dispatcher.utter_message(text=f"O seu nome ?? {nome}!")
        return []

class ActionInformarTime(Action):

    def name(self) -> Text:
        return "action_informar_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        time = tracker.get_slot("time")
        if not time:
            dispatcher.utter_message(text="Eu n??o sei o seu time.")
        else:
            dispatcher.utter_message(text=f"O seu time ?? {time}!")
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
            dispatcher.utter_message(text="Talvez voc?? tenha digitado errado")
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
            max_duracao = 20
            
            if (duracao > max_duracao):
                dispatcher.utter_message(text="Voc?? informou um valor superior a " + max_duracao + ".")
                return {"duracao": None}
                
            return {"duracao": slot_value}
        except:
            dispatcher.utter_message(text="Voc?? informou um valor inv??lido. Digite um n??mero menor ou igual a " + str(max_duracao) + ".")
            return {"duracao": None}            

class ActionGravarAudio(Action):

    def name(self):
        return "action_gravar_audio_microfone"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       
        channel = tracker.get_latest_input_channel()

        username = tracker.sender_id

        if (DEBUG_MODE == True or username == "161484917" or username == "1307765181" or username == "1001307765181"):
                 
            duracaoStr = tracker.get_slot("duracao")
            duracao = int(duracaoStr)
            max_duracao = 20

            if (duracao <= max_duracao):
                gravar_audio_microfone(duracao=duracao, arquivo_saida=ARQUIVO_AUDIO_GRAVADO_MICROFONE)
                
                dispatcher.utter_message(text='??udio gravado com sucesso.')
        
                #if (channel == "telegram"):
                    # TODO: Enviar ??udio pelo telegram
                    #dispatcher.utter_message(text="Canal n??o suportado para essa funcionalidade.")
                    #return
 
            else:
                dispatcher.utter_message(text='N??o foi poss??vel realizar a grava????o. A dura????o especificada ?? muito longa.')
                
        else:
          retorno = "Desculpe-me! Voc?? n??o est?? autorizado(a) a essa funcionalidade."

          dispatcher.utter_message(text=retorno)

class ActionResetSlotsGravarAudioMicrofone(Action):

    def name(self):
        return "action_reset_slots_gravar_audio_microfone"

    def run(self, dispatcher, tracker, domain):
        # return [AllSlotsReset()]
        return [SlotSet("duracao", None)]

class ActionTocarAudio(Action):

    def name(self):
        return "action_tocar_audio_gravado_microfone"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        channel = tracker.get_latest_input_channel()

        username = tracker.sender_id
        #print(username)

        if (DEBUG_MODE == True or username == "161484917" or username == "1307765181" or username == "1001307765181"):

            if (exists(ARQUIVO_AUDIO_GRAVADO_MICROFONE)):
                dispatcher.utter_message(text='Ok. O ??udio est?? sendo reproduzido.')
                
                tocar_audio(arquivo=ARQUIVO_AUDIO_GRAVADO_MICROFONE)

                dispatcher.utter_message(text='??udio reproduzido com sucesso.')
            else:
                dispatcher.utter_message(text='N??o foi encontrado nenhum arquivo gravado pelo microfone.')

        else:
            retorno = "Desculpe-me! Voc?? n??o est?? autorizado(a) a essa funcionalidade."

            dispatcher.utter_message(text=retorno)
