class Data:
    data: dict = {}

    def add_data(self, data):
        if data[0] in self.data.keys():
            return f"{data[0]} {self.data[data[0]]}"
        self.data[data[0]] = [data[1], data[2]]
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
        self.data[new_data[0]] = tuple(new_data[1], new_data[2])
        print(self.data)
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
        return final_data

    def clean_data(self):
        self.data.clear()


data = Data()
