import hashlib


class Md5file():

    def __init__(self, file_name):
        self.file_name = file_name
        self.md5 = None
        self.md5_incache = False
        self.md5_calculator = hashlib.md5()
        self._temp_file = None

    def __enter__(self):
        self._temp_file = open(self.file_name)
        return self._temp_file

    def __exit__(self, type, value, traceback):
        self._temp_file.close()

    def get_md5(self):
        if self.md5 is not None:
            return self.md5
        else:
            with open(self.file_name) as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    self.md5_calculator.update(chunk)
            self.md5 = self.md5_calculator.hexdigest()
            self.md5_incache = True
            return self.md5
