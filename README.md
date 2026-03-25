# Bot ColabZoonoses 🦟📊

Um bot do Telegram colaborativo para monitoramento de zoonoses, utilizando relatos e integração com a comunidade pelo Telegram.

## 🚀 Sobre o Projeto
O **ColabZoonoses** tem como objetivo facilitar a coleta de relatos de ocorrências de zoonoses, usando ferramentas de mensagens que estão no dia a dia da população.

O repositório contém duas versões do bot, ideais para propósitos distintos:
- `bot.py`: A versão completa, que armazena usuários e os relatos (como texto, data e hora) de maneira **persistente** em um banco de dados MongoDB.
- `bot_telegram.py`: Uma versão simplificada que apenas realiza um cadastro simulado mantendo os dados temporariamente na memória.

## 🛠 Tecnologias Utilizadas
- [Python 3](https://www.python.org/)
- [pyTelegramBotAPI (telebot)](https://github.com/eternnoir/pyTelegramBotAPI) - API assíncrona para interagir com o Telegram.
- [MongoDB](https://www.mongodb.com/) - Banco de Dados NoSQL para armazenamento constante local utilizando `pymongo`.

## ⚙️ Pré-requisitos
Antes de executar, você precisará de:
- **Python 3.x**
- **MongoDB** executando localmente na porta padrão (`27017`).
- Uma conta no Telegram e o **Token** gerado pelo [BotFather](https://t.me/BotFather) da plataforma.

## 🚀 Como Executar Localmente

**1. Clone o Repositório**
```bash
git clone https://github.com/Cairo-Carneiro/py_bot.git
cd py_bot
```

**2. Ative o Ambiente Virtual (Recomendado)**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

**3. Instale as Dependências**
```bash
pip install pyTelegramBotAPI pymongo
```

**4. Configure o Token do seu Bot**
Nos arquivos `bot.py` ou `bot_telegram.py`, atualize a variável `CHAVE_API` para o token fornecido pelo BotFather.

*(⚠️ **Dica de Segurança**: Evite subir tokens ou credenciais diretamente no código base (ex: Github). Considere o uso de bibliotecas como `python-dotenv` para lidar com variáveis de ambiente na produção.)*

**5. Rode o Bot Completo (Requer MongoDB rodando)**
```bash
python bot.py
```

## 📱 Comandos Disponíveis do Bot
- `/opcao1` - Inicia o fluxo de cadastro e solicita nome e telefone (com validação básica).
- `/relato` - (Apenas em `bot.py`) Permite registrar um relato descritivo sobre o problema.

## 🤝 Contribuição e Próximos Passos
Sugestões de features que podem melhorar este bot no futuro:
- [ ] Implementar integração com ferramentas de geolocalização e mapas.
- [ ] Variáveis de ambiente configuráveis (esconder `CHAVE_API`).
- [ ] Interface administrativa via web para vizualizar os relatos.

Sinta-se à vontade para realizar "fork" do repositório, criar novos "branches" e abrir "Pull Requests". Todo o engajamento é muito bem-vindo para apoiar a saúde pública de maneira colaborativa!

---
✨ Criado para facilitar o relato de problemas de saúde da comunidade diretamente pelo Telegram.
