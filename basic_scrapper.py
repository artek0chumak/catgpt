import datetime
import time
import json
import yaml

from telethon.sync import TelegramClient
from tqdm.auto import tqdm


def main():
    with open("config.yaml", encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)

    api_id = config["tg_api_id"]
    api_hash = config["tg_api_hash"]

    chats = config["tg_chats"]

    with open("scrapped_messages.jsonl", "w") as result_file:
        for chat in chats:
            with TelegramClient('test', api_id, api_hash) as client:
                for message in tqdm(client.iter_messages(chat, offset_date=datetime.date.today() - datetime.timedelta(days=365), reverse=True)):
                    data = { "group" : chat, "sender" : message.sender_id, "text" : message.text, "date" : message.date.isoformat()}
                    result_file.write(json.dumps(data, ensure_ascii=False) + "\n")
                    time.sleep(0.01)


if __name__ == "__main__":
    main()
