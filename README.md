# CatGPT

Специальный помощник для написания сообщений в чаты животных.
Берет твое описание по-простому, и добавляет в него идеальное количество эпитетов и эмодзи, чтобы люди помогли вам!

## Скрипты

Тут несколько скриптов для получения данных:

- [basic_scrapper.py](basic_scrapper.py) -- Скрипт для получения сообщений
- [basic_embedder.py](basic_embedder.py) -- Скрипт для получения эмбеддингов
- [basic_fewshot.py](basic_fewshot.py) -- Скрипт для запуска генератора

Если надо просто запустить оболочку, надо запустить последний скрипт этой командой:

```bash
pip install -r requirements.txt
python basic_fewshot.py
```

## Конфиг файл

Для контроля файлов, используется данные из `config.yaml`. Его формат:

```yaml
tg_api_id: 
tg_api_hash: 
tg_chats: 
  - tbilisi_animals
openai_api_key: 
openai_api_model_embedder: text-embedding-3-large
openai_api_model_generator: gpt-4-turbo-preview
password:
```

`tp_api_*` можно получить [тут](https://my.telegram.org/). Для ключа OpenAI надо идти в [сюда](https://platform.openai.com). Пароль пишите посложнее.