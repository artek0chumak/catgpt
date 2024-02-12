import yaml

import pandas as pd

from openai import OpenAI
from tqdm.auto import tqdm
from multiprocessing.pool import ThreadPool


def main():
    with open("config.yaml", encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)
    
    dataset = pd.read_json("scrapped_messages.jsonl", lines=True)
    print(dataset.shape)
    messages = []
    for row in dataset.iloc:
        if row["text"] is not None and len(row["text"]) > 0 and row["text"] not in messages:
            messages.append(row["text"])
            
    print(len(messages))
    
    client = OpenAI(
        api_key=config["openai_api_key"],
        timeout=5.0,
        max_retries=10,
    )
    def get_embedding(text, model=config["openai_api_model_embedder"]):
        text = text.replace("\n", " ")
        return client.embeddings.create(input = [text], model=model).data[0].embedding
    
    messages_embs = []
    with ThreadPool(16) as pool:
        for message_emb in tqdm(pool.imap(get_embedding, messages), total=len(messages)):
            messages_embs.append(message_emb)
        
    dataframe = [
        {"message": message, "embedding": embedding}
        for message, embedding in zip(messages, messages_embs)
    ]
    pd.DataFrame(dataframe).to_json("embedded.jsonl", lines=True, force_ascii=False, orient='records')


if __name__ == "__main__":
    main()
