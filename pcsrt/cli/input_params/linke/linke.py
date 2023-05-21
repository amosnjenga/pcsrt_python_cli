class Linke:
    def __init__(self, *args):
        if len(args) == 1:
            value = args[0]
            self.monthly_data = [value]*12
        elif len(args) == 12:
            self.monthly_data = list(args)
        else:
            raise ValueError("Invalid number of arguments for Linke")

    @classmethod
    def from_array(cls, data):
        if len(data) != 12:
            raise ValueError("Invalid number of arguments for Linke")
        return cls(*data)

    def get_val(self, month):
        try:
            return self.monthly_data[month - 1]
        except IndexError:
            raise ValueError("Invalid month for Linke")
