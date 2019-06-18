class writer_class():
    def __init__(self, data):
        self.data = data
        self.writer()
    
    def writer(self):
        f = open("./shared/numbers.txt", 'a')
        f.write(self.data+";\n")
        f.close()