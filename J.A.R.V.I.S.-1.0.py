
import os
import random
import webbrowser
import tkinter as tk
from threading import Thread
from datetime import datetime, timedelta
from collections import deque

import requests
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai

# ==== CONFIGURAÇÕES GERAIS ====

OPENWEATHER_KEY = "SUA_CHAVE_OPENWEATHER"
GEMINI_KEY = "SUA_CHAVE_GEMINI"
genai.configure(api_key=GEMINI_KEY)

PLAYLISTS = {
  "foco": "https://www.youtube.com/playlist?list=SUA_PLAYLIST_FOCO",
  "estudo": "https://www.youtube.com/playlist?list=SUA_PLAYLIST_ESTUDO",
  "treino": "https://www.youtube.com/playlist?list=SUA_PLAYLIST_TREINO",
}

ARQUIVO_NOTAS = "notas_jarvis.txt"
memoria = deque(maxlen=20)
modo_privado = False


# ==== FUNÇÕES DE MEMÓRIA E NOTAS ====

def registrar_memoria(entrada, resposta):
  global modo_privado
  if modo_privado:
      return
  item = {
      "hora": datetime.now().strftime("%H:%M"),
      "entrada": entrada,
      "resposta": resposta
  }
  memoria.append(item)


def resumo_memoria():
  if not memoria:
      return "Ainda não tenho registros recentes, senhor."
  linhas = []
  for m in memoria:
      linhas.append(f"[{m['hora']}] Você: {m['entrada']} | Eu: {m['resposta']}")
  return "Aqui está um resumo das nossas últimas interações:\n" + "\n".join(linhas)


def registrar_nota(texto):
  global modo_privado
  if modo_privado:
      return "Modo privado ativo, não vou registrar essa anotação, senhor."
  timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
  linha = f"[{timestamp}] {texto}\n"
  with open(ARQUIVO_NOTAS, "a", encoding="utf-8") as f:
      f.write(linha)
  return "Anotação registrada com sucesso, senhor."


def ativar_modo_privado():
  global modo_privado
  modo_privado = True
  return "Modo privado ativado. Não irei registrar histórico nem anotações."


def desativar_modo_privado():
  global modo_privado
  modo_privado = False
  return "Modo privado desativado. Voltarei a registrar suas interações."


# ==== SERVIÇOS EXTERNOS ====

def obter_temperatura(cidade):
  base_url = "http://api.openweathermap.org/data/2.5/weather?"
  complete_url = base_url + "appid=" + OPENWEATHER_KEY + "&q=" + cidade
  response = requests.get(complete_url)
  if response.status_code == 200:
      data = response.json()
      temp = round(data["main"]["temp"] - 273.15, 1)
      desc = data["weather"][0]["description"]
      return f"A temperatura em {cidade} é de {temp}°C com {desc}."
  else:
      return "Não consegui encontrar essa cidade, senhor."


def obter_previsao(cidade):
  url = f"http://api.openweathermap.org/data/2.5/forecast?appid={OPENWEATHER_KEY}&q={cidade}"
  response = requests.get(url)
  if response.status_code == 200:
      dados = response.json()
      amanha = (datetime.now() + timedelta(days=1)).date()
      previsao = [item for item in dados["list"] if datetime.fromtimestamp(item["dt"]).date() == amanha]
      if not previsao:
          return "Não encontrei dados de previsão para amanhã, senhor."
      temp = round(previsao[0]["main"]["temp"] - 273.15, 1)
      desc = previsao[0]["weather"][0]["description"]
      return f"A previsão para amanhã em {cidade} é de {desc}, com temperatura de {temp}°C."
  else:
      return "Não consegui obter a previsão, senhor."


def pesquisar_na_internet(pergunta):
  regras = """
  Responda como J.A.R.V.I.S., assistente do Tony Stark:
  - Seja direto e educado.
  - Use no máximo 25 palavras.
  - Mantenha tom profissional e leve.
  """
  model = genai.GenerativeModel("gemini-2.5-flash")
  chat = model.start_chat(history=[])
  resposta = chat.send_message(regras + pergunta)
  return resposta.text


def tocar_playlist(nome):
  nome = nome.lower().strip()
  if nome in PLAYLISTS:
      webbrowser.open(PLAYLISTS[nome])
      return f"Tocando a playlist de {nome}, senhor."
  return "Não encontrei essa playlist, senhor."


# ==== APLICAÇÃO TKINTER + LOOP DE VOZ ====

class JarvisApp:
  def __init__(self, root):
      self.root = root
      self.root.title("Jarvis - CodeVerse 2025")
      self.root.geometry("260x230")

      bg_color = "#0B3D2E"
      fg_color = "#E6F2EF"
      self.root.configure(bg=bg_color)

      self.label = tk.Label(
          root,
          text="Assistente de Voz - J.A.R.V.I.S.",
          bg=bg_color,
          fg=fg_color,
          font=("Helvetica", 9)
      )
      self.label.pack(pady=10)

      self.canvas = tk.Canvas(root, width=120, height=120, bg=bg_color, highlightthickness=0)
      self.circle = self.canvas.create_oval(35, 35, 85, 85, outline="#00FFFF", width=5)
      self.canvas.pack()

      self.btn_iniciar = tk.Button(
          root,
          text="Iniciar Assistente",
          command=self.iniciar_assistente,
          bg=fg_color,
          fg=bg_color,
          font=("Helvetica", 9)
      )
      self.btn_iniciar.pack(pady=5)

      self.running = False

  def mudar_cor_circulo(self, cor):
      self.canvas.itemconfig(self.circle, outline=cor)

  def iniciar_assistente(self):
      if not self.running:
          self.running = True
          thread = Thread(target=self.executar_assistente)
          thread.start()
          self.label.config(text="Assistente iniciado...")

  def executar_assistente(self):
      engine = pyttsx3.init()
      r = sr.Recognizer()

      def falar(texto):
          self.mudar_cor_circulo("#00FF00")
          engine.say(texto)
          engine.runAndWait()
          self.mudar_cor_circulo("#00FFFF")

      def ouvir():
          with sr.Microphone() as source:
              r.adjust_for_ambient_noise(source)
              audio = r.listen(source)
          try:
              comando = r.recognize_google(audio, language="pt-BR").lower()
              print("Você disse:", comando)
              return comando
          except:
              return ""

      # Saudação inicial (base #44 + clima do #46)
      saudacao = "Bom dia" if datetime.now().hour < 12 else "Boa tarde" if datetime.now().hour < 18 else "Boa noite"
      clima_sp = obter_temperatura("São Paulo")
      falar(f"{saudacao}, senhor Carlos. Hoje é {datetime.now().strftime('%d/%m/%Y')}, "
            f"são {datetime.now().strftime('%H:%M')}. {clima_sp} Me chamo Jarvis.")
      falar("Se precisar de mim, diga meu nome, senhor.")
      self.label.config(text="Diga: 'Jarvis' para ativar.")

      while self.running:
          frase = ouvir()
          if not frase:
              continue

          if "jarvis" in frase:
              respostas_ativacao = [
                  "Sim, senhor?",
                  "Às ordens.",
                  "Estou aqui.",
                  "Pronto para ajudar."
              ]
              resp_ativacao = random.choice(respostas_ativacao)
              falar(resp_ativacao)
              self.label.config(text="Aguardando comando...")

              comando = ouvir()
              if not comando:
                  falar("Não consegui entender o comando, senhor.")
                  continue

              resposta_texto = self.processar_comando(comando, falar, ouvir)
              if resposta_texto:
                  registrar_memoria(comando, resposta_texto)

  def processar_comando(self, comando, falar, ouvir):
      comando = comando.lower()
      resposta = ""

      # COMANDOS LOCAIS (#45)
      if "abrir navegador" in comando:
          os.system("start chrome.exe")
          resposta = "Abrindo o navegador."
      elif "abrir calculadora" in comando:
          os.system("start calc.exe")
          resposta = "Abrindo a calculadora."
      elif "abrir word" in comando:
          os.system("start winword.exe")
          resposta = "Abrindo o Word."
      elif "abrir excel" in comando:
          os.system("start excel.exe")
          resposta = "Abrindo o Excel."
      elif "abrir vs code" in comando or "abrir vscode" in comando:
          os.system("start code")
          resposta = "Abrindo o Visual Studio Code."

      # HORA / DATA
      elif "que horas são" in comando:
          hora = datetime.now().strftime("%H:%M")
          resposta = f"Agora são {hora}."
      elif "que dia é hoje" in comando:
          data = datetime.now().strftime("%d/%m/%Y")
          resposta = f"Hoje é {data}."

      # CLIMA / PREVISÃO (#46)
      elif "temperatura" in comando:
          falar("De qual cidade deseja saber, senhor?")
          cidade = ouvir()
          resposta = obter_temperatura(cidade) if cidade else "Não consegui ouvir o nome da cidade."
      elif "previsão" in comando:
          falar("Para qual cidade devo consultar a previsão, senhor?")
          cidade = ouvir()
          resposta = obter_previsao(cidade) if cidade else "Não consegui ouvir o nome da cidade."

      # PESQUISA COM IA (GEMINI) (#32, #46)
      elif "pesquisar" in comando or "perguntar" in comando:
          assunto = comando.replace("pesquisar", "").replace("perguntar", "").strip()
          if not assunto:
              falar("Sobre o que deseja saber, senhor?")
              assunto = ouvir()
          if assunto:
              falar("Um momento, pesquisando.")
              resposta = pesquisar_na_internet(assunto)
          else:
              resposta = "Não consegui entender o assunto da pesquisa."

      # PLAYLISTS (#41, #42)
      elif "playlist" in comando or "tocar música" in comando:
          falar("Qual playlist o senhor deseja? Foco, estudo ou treino?")
          nome_playlist = ouvir()
          resposta = tocar_playlist(nome_playlist) if nome_playlist else "Não entendi o nome da playlist."

      # NOTAS / TRANSCRIÇÃO (#40)
      elif "anotar" in comando or "registrar nota" in comando:
          falar("O que deseja anotar, senhor?")
          nota = ouvir()
          if nota:
              resposta = registrar_nota(nota)
          else:
              resposta = "Não consegui ouvir o conteúdo da anotação."

      # MEMÓRIA CONTEXTUAL (#39, #43)
      elif "o que falamos hoje" in comando or "histórico" in comando:
          resposta = resumo_memoria()

      # MODO PRIVADO
      elif "ativar modo privado" in comando:
          resposta = ativar_modo_privado()
      elif "desativar modo privado" in comando:
          resposta = desativar_modo_privado()

      # DESLIGAR
      elif "desligar" in comando or "encerrar" in comando:
          resposta = "Encerrando o sistema. Até mais, senhor."
          falar(resposta)
          self.running = False
          self.root.after(1000, self.root.destroy)
          return resposta

      else:
          resposta = "Desculpe, não entendi o comando, senhor."

      if resposta:
          falar(resposta)
      return resposta


if __name__ == "__main__":
  root = tk.Tk()
  app = JarvisApp(root)
  root.mainloop() 
