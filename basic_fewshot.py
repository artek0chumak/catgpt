import json
import re
import yaml

import gradio as gr
import numpy as np

from openai import OpenAI


with open("config.yaml", encoding="utf-8") as config_file:
    config = yaml.safe_load(config_file)

messages = []
embeds = []
with open("embedded.jsonl") as embedding_file:
    for line in embedding_file:
        row = json.loads(line)
        messages.append(row["message"])
        embeds.append(np.array(row["embedding"], dtype=np.float16))

messages = np.array(messages)
embeds = np.array(embeds, dtype=np.float16)


def find_few_shots(query, password, api_key="", k=5, model=config["openai_api_model_embedder"]):
    if password == config["password"]:
        api_key = config["openai_api_key"]
    if api_key == "":
        raise ValueError("Неправильный API Key")
    client = OpenAI(
        api_key=api_key,
        max_retries=10,
    )
    query = query.replace("\n", " ")
    query_embed = np.array(client.embeddings.create(input = [query], model=model).data[0].embedding)
    dist = ((embeds - query_embed)** 2).sum(axis=0)
    idx = np.argsort(dist)[:k]
    examples = messages[idx]
    examples = "\n\n".join(examples)
    prompt = (
        f"Напиши сообщение в чат, используя сообщения ниже как примеры как надо писать:\n{examples}\n"
        f"Я хочу написать следующее сообщение: {query}. Перепиши его, чтобы он соответствовал стилю. Не пиши никнэйм или контакт для связи."
    )
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=config["openai_api_model_generator"],
    )
    message = completion.choices[0].message.content
    message = re.sub("@\w+", '', message)
    return message.strip()


desc = """# CatGPT
Специальный помощник для написания сообщений в чаты животных.
Берет твое описание по-простому, и добавляет в него идеальное количество эпитетов и эмодзи, чтобы люди помогли вам!

Используйте либо пароль, либо OpenAI API Key. Пароль спрашиваете у нужных людей.
"""


with gr.Blocks() as demo:
    gr.Markdown(desc)
    query = gr.Textbox(label="Напиши сообщение по-простому", autofocus=True)
    with gr.Row():
        password = gr.Textbox(label="Пароль для дефолтного ключа", type="password")
        api_key = gr.Textbox(label="Ключ от OpenAI(если нет пароля)", type="password")
    message_btn = gr.Button("Получить идеальное сообщение")
    message = gr.Textbox(label="Сообщения для чата", interactive=False)
    
    message_btn.click(fn=find_few_shots, inputs=[query, password, api_key], outputs=message,)


demo.launch()
