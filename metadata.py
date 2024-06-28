class Data:
    def __init__(self, path: str):
        self.data_path = path

        self.ADRESS = None
        self.FLAT_NR = None
        self.NAME = None
        self.EMAIL = None
        self.PHONE_NR = None

        self.__readData(path)

    def __readData(self, file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()

            if len(lines) != 6:
                raise Exception("IncorrectDataFormatException")

            try:
                self.ADRESS = lines[0].split(":", 1)[1].strip()
                self.FLAT_NR = lines[1].split(":", 1)[1].strip()
                self.NAME = lines[2].split(":", 1)[1].strip()
                self.EMAIL = lines[3].split(":", 1)[1].strip()
                self.PHONE_NR = lines[4].split(":", 1)[1].strip()
                self.FINALIZATION_PERMIT = lines[5].split(":", 1)[1].strip()
            except:
                raise Exception("IncorrectDataFormatException")


