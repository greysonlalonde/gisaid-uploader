class DataError(Exception):

    def __init__(self):
        self.error = 'missing or corrupt data. reference the upload examples.'

    def __str__(self):
        return self.error


class InputError(Exception):

    def __init__(self):
        self.error = 'invalid parameter.'

    def __str__(self):
        return self.error


class FileError(Exception):

    def __init__(self):
        self.error = 'improper file types.'

    def __str__(self):
        return self.error


class ConfigFileError(Exception):

    def __init__(self):
        self.error = "ConfigFileError: reference your config file."

    def __str__(self):
        return self.error
