import os
import json
from config import chat_to_shift


def extract_data(filename='data'):
    if os.path.exists(f'{filename}.json'):
        with open(f'{filename}.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return dict()


class Cases:
    data: dict = {}
    shift_data: dict = {}

    def __init__(self):
        self.data = extract_data()

    def is_in_dict(self, link: str, chat_id: int):
        return chat_to_shift[chat_id] in self.data and link in self.data[chat_to_shift[chat_id]].keys()

    def add_data(self, input_data, chat_id: int):
        if chat_to_shift[chat_id] in self.data.keys() and input_data[0] in self.data[chat_to_shift[chat_id]].keys():
            return f"{input_data[0]} {self.data[chat_to_shift[chat_id]][input_data[0]]}"
        if chat_to_shift[chat_id] not in self.data:
            self.data[chat_to_shift[chat_id]] = dict()
        self.data[chat_to_shift[chat_id]][input_data[0]] = [input_data[1], input_data[2]]
        return f"Добавлен новый кейс:\n{input_data[0]} {input_data[1]}"

    def remove_data(self, case_link: str, chat_id: int):
        if chat_to_shift[chat_id] in self.data.keys() and case_link in self.data[chat_to_shift[chat_id]].keys():
            del self.data[chat_to_shift[chat_id]][case_link]
            return f"{case_link} - кейс успешно удалён!"
        return f"{case_link} - кейс не найден!"

    def change_data(self, new_data, chat_id: int):
        if chat_to_shift[chat_id] in self.data.keys() and new_data[0] not in self.data[chat_to_shift[chat_id]].keys():
            return f"{new_data[0]} - кейс не найден!"
        if not new_data[2]:
            self.data[chat_to_shift[chat_id]][new_data[0]][0] = new_data[1]
        else:
            self.data[chat_to_shift[chat_id]][new_data[0]] = [new_data[1], new_data[2]]
        return f"{new_data[0]} - категория для кейса успешно обновлена на \"{new_data[1]}\"."

    def fetch_data(self, chat_id: int) -> dict:
        if chat_to_shift[chat_id] not in self.data.keys():
            return dict()
        final_data = dict()
        for key in self.data[chat_to_shift[chat_id]].keys():
            if self.data[chat_to_shift[chat_id]][key][0] not in final_data:
                final_data[self.data[chat_to_shift[chat_id]][key][0]] = list()
            final_data[self.data[chat_to_shift[chat_id]][key][0]].append(f"{key} {self.data[chat_to_shift[chat_id]][key][1]}")
        return final_data

    def fetch_data_final(self, chat_id: int) -> dict:
        if chat_to_shift[chat_id] not in self.data.keys():
            return dict()
        final_data = dict()
        for key in self.data[chat_to_shift[chat_id]].keys():
            if self.data[chat_to_shift[chat_id]][key][0] not in final_data:
                final_data[self.data[chat_to_shift[chat_id]][key][0]] = list()
            final_data[self.data[chat_to_shift[chat_id]][key][0]].append(key)
        return final_data

    def clean_data(self, chat_id: int):
        if chat_to_shift[chat_id] not in self.data.keys():
            return "Список пуст!"
        del self.data[chat_to_shift[chat_id]]
        return "Cписок успешно очищен!"

    def save_data(self, filename='data'):
        with open(f'{filename}.json', 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)


data = Cases()
