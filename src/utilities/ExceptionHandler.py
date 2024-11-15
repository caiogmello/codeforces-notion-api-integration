class ExceptionHandler(Exception):
    def __init__(self, message):
        self._map = self.err_mapping()
        self._message = f"\n\n\nRequest failed: {self.treat_error(message)}"
        super().__init__(self.treat_error(message))

    def __str__(self):
        return self._message
    
    def err_mapping(self):
        return {
            "API token is invalid": "The API token you provided is invalid.",
            "body failed validation": "The Page URL you provided is invalid.",
        }         

    def treat_error(self, message):
        if message.split('.')[0] in self._map:
            return self._map[message.split('.')[0]]
        
        if message[:6] == "handle":
            return "The Codeforces username you provided is invalid."
        
        return message