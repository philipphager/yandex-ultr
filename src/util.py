class LabelEncoder:
    def __init__(self):
        self.value2id = {}
        self.max_id = 0

    def __call__(self, value):
        if value not in self.value2id:
            self.value2id[value] = self.max_id
            self.max_id += 1

        return self.value2id[value]

    def __len__(self):
        return len(self.value2id)
