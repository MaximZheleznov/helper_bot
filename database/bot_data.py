import os
import json


def extract_data(filename='data'):
    if os.path.exists(f'{filename}.json'):
        with open(f'{filename}.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return dict()


class Cases:
    data: dict = {}

    def __init__(self):
        self.data = extract_data()

    def is_in_dict(self, link: str):
        return link in self.data.keys()

    def add_data(self, input_data):
        if input_data[0] in self.data.keys():
            return f"{input_data[0]} {self.data[input_data[0]]}"
        self.data[input_data[0]] = [input_data[1], input_data[2]]
        print(self.data)
        return "Новый кейс добавлен!"

    def remove_data(self, case_link: str):
        if case_link in self.data.keys():
            del self.data[case_link]
            return "Кейс успешно удалён!"
        return "Такой кейс не найден!"

    def change_data(self, new_data):
        if new_data[0] not in self.data.keys():
            return "Такой кейс не найден!"
        if not new_data[2]:
            self.data[new_data[0]][0] = new_data[1]
            print(self.data)
        else:
            self.data[new_data[0]] = [new_data[1], new_data[2]]
        return "Категория успешно обновлена!"

    def fetch_data(self) -> dict:
        final_data = dict()
        for key in self.data.keys():
            if self.data[key][0] not in final_data:
                final_data[self.data[key][0]] = list()
            final_data[self.data[key][0]].append(f"{key} {self.data[key][1]}")
        return final_data

    def fetch_data_final(self) -> dict:
        final_data = dict()
        for key in self.data.keys():
            if self.data[key][0] not in final_data:
                final_data[self.data[key][0]] = list()
            final_data[self.data[key][0]].append(key)
        print(final_data)
        return final_data

    def clean_data(self):
        self.data.clear()
        return "Cписок успешно очищен!"

    def save_data(self, filename='data'):
        with open(f'{filename}.json', 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)


data = Cases()
