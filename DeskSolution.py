class DeskSolution:
    __lines = []

    def __init__(self, lines=[]):
        self.__lines = lines

    @property
    def lines(self):
        return self.__lines

    def print_desk(self, on_screen=False):
        res = ""
        for i in range(8):
            row = "++++++++"
            ind = self.lines[i]
            row = row[:ind] + "Q" + row[ind + 1:]
            if on_screen:
                print(row)
            res += row + "\n"
        return res