# -*- coding: utf-8 -*-
"""
Inventario TI - leitor de hardware do aparelho + envio para planilha Google.
Reconstruido a partir do APK original (inventarioti-0.1).
O usuario escolhe seu nome na lista, o app le o hardware e envia para o
Google Sheets (via Apps Script Web App).
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.utils import platform
import threading
import ssl
import urllib.request
import urllib.parse

# URL do Web App do Google Apps Script (recebe os dados e grava na planilha).
SHEETS_URL = 'https://script.google.com/macros/s/AKfycby5xMw4GLrKl9o_JFxoRfM88crWh74kdZ_VTcFnbTJd_SmVrOcvszjFJdorjc1jF_cL5A/exec'

USUARIOS = [
    'Selecione o usuario...',
    'Alana Da Silva Martins',
    'Aline Luiza Da Silva',
    'Amanda Vieira',
    'Ana Paula Jacobsen',
    'Andreia Silva',
    'Anita Carvalho',
    'Bruna Cardoso',
    'Carlos Eduardo',
    'Claudio Claudio José Pontello Junior',
    'Dayane Pereira',
    'Edilson Magalhães',
    'Elizangela Warmin',
    'Emerson Moreira',
    'Felipe Duarte',
    'Felipe Raphael',
    'Fiscal NF',
    'Flavio Puntell',
    'Franciele Rocha Da Silveira',
    'Gabriel Ferreira',
    'Geovana Pereira',
    'Hailton Filho',
    'Hiago Cavalheiro',
    'John Maciel',
    'Karine Marlene',
    'Ketlyn Cordeiro',
    'Luciano Santos',
    'Luma Caroline',
    'Maicol Correa',
    'Maiko Chamorro',
    'Marcella Brião Fachel',
    'Marcelo Teixeira',
    'Mareana Sipriano',
    'Maria Isabelle Leal Pereira',
    'Matheus Hoffmann',
    'Matheus Macedo',
    'Maureci Zimmermann',
    'Michele Scherer',
    'Nathalia Pereira',
    'Nicole De Jesus',
    'Nicolly Godoi',
    'Nora Freitas',
    'Operacional TLM',
    'Priscila Aparecida Da Fonseca',
    'Priscila Gonçalves',
    'Rafael Braguini',
    'Rafael Trindade',
    'Samuel Gattelli',
    'Samyra Sperb',
    'Shayenderson Oliveira',
    'Silvaneide Araujo Dos Santos',
    'Stefanie Lima',
    'Talita Modesto',
    'Thalita Lacerda',
    'Thiago Simoes',
    'Vanessa Bernardino',
    'Vanessa Ronque']


def coletar_dados():
    """Le os dados de hardware do aparelho Android."""
    dados = {'fabricante': '', 'modelo': '', 'serial': '', 'android': '', 'imei': ''}
    if platform == 'android':
        try:
            from jnius import autoclass
            Build = autoclass('android.os.Build')
            VERSION = autoclass('android.os.Build$VERSION')
            dados['fabricante'] = Build.MANUFACTURER or ''
            dados['modelo'] = Build.MODEL or ''
            dados['android'] = VERSION.RELEASE or ''
            # Serial: tenta getSerial(), depois SERIAL, depois ID
            try:
                dados['serial'] = Build.getSerial()
            except Exception:
                dados['serial'] = Build.SERIAL or Build.ID or ''
            # Identificador unico do dispositivo: ANDROID_ID
            try:
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                context = PythonActivity.mActivity
                Settings = autoclass('android.provider.Settings$Secure')
                dados['imei'] = Settings.getString(context.getContentResolver(), 'android_id') or ''
            except Exception:
                dados['imei'] = ''
        except Exception as e:
            dados['fabricante'] = 'Erro: %s' % e
    else:
        # Fora do Android (teste no PC) usa valores ficticios.
        dados = {'fabricante': 'Samsung', 'modelo': 'Galaxy A32',
                 'serial': 'TEST123', 'android': '13', 'imei': '123456789012345'}
    return dados


def enviar_sheets(payload):
    """Envia os dados para o Google Sheets via POST. Retorna a resposta do servidor."""
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        data = urllib.parse.urlencode(payload).encode()
        req = urllib.request.Request(SHEETS_URL, data=data)
        r = urllib.request.urlopen(req, timeout=10, context=ctx)
        return r.read().decode()
    except Exception as e:
        return 'Erro: %s' % e


class InventarioApp(App):
    def build(self):
        self.dados = coletar_dados()
        root = BoxLayout(orientation='vertical', padding=20, spacing=12)
        root.add_widget(Label(text='Identificador de Dispositivo', font_size='20sp',
                              bold=True, size_hint_y=None, height=50))
        info = ('Fabricante: %s\n'
                'Modelo:     %s\n'
                'Serial:     %s\n'
                'Android:    %s\n'
                'Android ID: %s') % (self.dados['fabricante'], self.dados['modelo'],
                                     self.dados['serial'], self.dados['android'],
                                     self.dados['imei'])
        root.add_widget(Label(text=info, font_size='13sp', halign='left', valign='top',
                              size_hint_y=None, height=140))
        root.add_widget(Label(text='Selecione seu nome:', font_size='14sp',
                              size_hint_y=None, height=30))
        self.spinner = Spinner(text=USUARIOS[0], values=USUARIOS, size_hint_y=None, height=44)
        root.add_widget(self.spinner)
        self.btn = Button(text='ENVIAR INVENTARIO', font_size='16sp', bold=True,
                          background_color=(0.16, 0.65, 0.27, 1), size_hint_y=None, height=56)
        self.btn.bind(on_press=self.enviar)
        root.add_widget(self.btn)
        self.status = Label(text='', font_size='13sp', size_hint_y=None, height=40)
        root.add_widget(self.status)
        return root

    def enviar(self, *args):
        if self.spinner.text == USUARIOS[0]:
            self.status.text = 'Selecione seu nome primeiro!'
            self.status.color = (1, 0.3, 0.3, 1)
            return
        self.btn.disabled = True
        self.status.text = 'Enviando...'
        self.status.color = (1, 1, 1, 1)
        payload = {
            'usuario': self.spinner.text,
            'fabricante': self.dados['fabricante'],
            'modelo': self.dados['modelo'],
            'serial': self.dados['serial'],
            'android': self.dados['android'],
            'imei': self.dados['imei'],
        }
        threading.Thread(target=self._bg, args=(payload,), daemon=True).start()

    def _bg(self, payload):
        resultado = enviar_sheets(payload)
        Clock.schedule_once(lambda dt: self._fim(resultado), 0)

    def _fim(self, resultado):
        self.btn.disabled = False
        if 'Erro' in resultado:
            self.status.text = 'Falha: %s' % resultado
            self.status.color = (1, 0.3, 0.3, 1)
            return
        self.status.text = 'Dados enviados com sucesso!'
        self.status.color = (0.16, 0.65, 0.27, 1)


if __name__ == '__main__':
    InventarioApp().run()
