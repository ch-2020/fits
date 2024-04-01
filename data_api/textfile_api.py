import os

class TextFileApi:
    def __init__(self, file_path: str) -> None:
        self.file_path = ""
        self.file_exist = False
        self.lines = []

        if os.path.isfile(file_path):
            self.file_exist = True
            self.file_path = file_path
            self.content = open(self.file_path).read()
        else:
            print("Error while reading file!")

    def get_recc_incomes(self) -> list:
        return self._extract_data("Income")

    def get_recc_expense(self) -> list:
        return self._extract_data("Expense")

    def _extract_data(self, contenttype) -> list:
        if self.file_exist:
            blocks = self.content.split("\n\n")
            for b in blocks:
                lines = b.split("\n")
                if lines[0] == contenttype:
                    res = []
                    for l in lines[1:]:
                        type = l.split(" ")[0]
                        value = l.split(" ")[-1]
                        name = " ".join(l.split(" ")[1:-1])
                        res.append((type, name, value))
                    return res
        return []

    def __str__(self) -> str:
        return f"\nfile: {self.file_path}\nexists: {self.file_exist}\ncontents: \n{self.content}"
    