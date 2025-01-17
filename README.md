# Projeto J.A.R.V.I.S.

## Descrição

O J.A.R.V.I.S. é um assistente virtual inspirado no famoso assistente do Homem de Ferro. Desenvolvido em Python, ele realiza diversas funções, desde conversas simples até tarefas mais complexas, como buscas na web e previsão do tempo.\
JARVIS é um assistente virtual inteligente que combina **reconhecimento de voz**, **síntese de voz (Text-to-Speech)**, e **integrações avançadas com APIs** para oferecer uma experiência interativa e eficiente. Ele responde a comandos de voz e executa diversas ações no seu computador, além de responder a perguntas com precisão.

![Banner do Projeto](./Jarvis_banner.png)

## Funcionalidades

- **Apresentação inicial:** Ao iniciar, JARVIS se apresenta informando a data, hora e a temperatura atual na sua cidade.
- **Reação ao comando 'Jarvis':** Sempre que o nome JARVIS é pronunciado, ele reage com uma das sete respostas aleatórias, como:
  ```
  - "Como posso te ajudar?"
  - "Sim senhor Carlos?"
  - "Às suas ordens senhor?"
  - "Pois não senhor?"
  - "Estou aqui senhor?"
  - "O que posso fazer pelo senhor?"
  - "Pronto senhor?
  ```

### Recursos Técnicos
- **Reconhecimento de voz:** Converte sua fala em texto utilizando tecnologia de reconhecimento de fala.
- **Síntese de voz (Text-to-Speech):** Responde suas perguntas e executa comandos falando de forma natural.
- **Integração com Google API (Gemini):** Realiza buscas na web e fornece respostas detalhadas.
- **Previsão do tempo:** Obtém dados climáticos em tempo real com a API do OpenWeather.

### Comandos Suportados

#### Navegação e Ferramentas
- **Abrir Navegador:** Abre o navegador padrão com o comando de voz.
- **Abrir Calculadora:** Inicializa a calculadora do sistema.
- **Abrir Paint:** Abre o Paint.
- **Abrir Bloco de Notas:** Executa o Bloco de Notas.
- **Abrir Excel:** Inicia o Microsoft Excel.
- **Abrir Word:** Inicia o Microsoft Word.
- **Abrir CMD:** Abre o Prompt de Comando.
- **Abrir VS Code:** Inicia o Visual Studio Code.
- **Consertar Internet:** Executa o solucionador de problemas de rede para corrigir problemas de conexão.

#### Consultas
- **Que Horas São:** Informa a hora atual.
- **Que Dia é Hoje:** Diz a data atual.
- **Qual a Temperatura em [Cidade]:** Informa a temperatura atual da cidade solicitada utilizando a API do OpenWeather.

#### Funcionalidades Específicas
- **Pesquisar [Assunto]:** Faz uma pesquisa online e retorna a resposta. Caso o assunto não seja especificado, pergunta "Sobre o que deseja saber?"
- **Iniciar Modo Conversa:** Permite um diálogo contínuo com respostas e novas perguntas, utilizando a API do Gemini.
- **Reproduzir Música:** Abre o YouTube com a música solicitada.
- **Transcrever:** Pergunta "Qual mensagem você deseja salvar?" e salva a resposta em um arquivo de texto na área de trabalho.
- **Desligar Sistema:** Encerra o aplicativo com a mensagem "Desligando o sistema, até mais".

---

Com JARVIS, você tem um assistente flexível, eficiente e personalizável ao seu alcance.

## Tecnologias Utilizadas

- **Python**
- **tkinter:** Para a interface gráfica.
- **pyttsx3:** Para a síntese de voz.
- **speech_recognition:** Para o reconhecimento de voz.
- **Google API (Gemini):** Para buscas e respostas avançadas.
- **OpenWeather API:** Para previsão do tempo.


## Lista de todas as bibliotecas e dependências usadas no código:
- **os**
- **random**
- **time**
- **webbrowser**
- **threading.Thread**
- **datetime**
- **requests**
- **speech_recognition**
- **pyttsx3**
- **google.generativeai**
- **tkinter**

### Dependências adicionais:
- **OpenWeather API** (requisição externa).

## Como Utilizar

1. Clone o repositório:
    ```bash
    git clone https://github.com/Carlos-CGS/Projeto-JARVIS.git
    ```


## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests. Para mudanças maiores, por favor, abra uma discussão antes para que possamos alinhar as melhorias.

## Licença

Este projeto está licenciado sob a [MIT License]

## Contato

- **LinkedIn:** [Carlos Garcia - CGS](https://www.linkedin.com/in/carlos-cgs/)

  ## Projeto Funcionando
  Segue o link para uma postagem que fiz no meu LinkedIn com video deste aplicativo funcionando: https://www.linkedin.com/feed/update/urn:li:activity:7241385354061058048/
