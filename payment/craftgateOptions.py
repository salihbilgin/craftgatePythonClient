# PROD
CRAFTGATE_BASE_URL = 'https://api.craftgate.io'
CRAFTGATE_API_KEY = 'API_KEY'
CRAFTGATE_SECRET_KEY = 'SECRET_KEY'
CRAFTGATE_RANDOM_STRING = "RANDOM_STRING-xyEwd"
CRAFTGATE_3DSECURE_CALLBACK_KEY = "32 Karakter"
# İşlem için gerekli 32 Haneli key değerine Panel üzerinde bulunan Yönetim -> Üye İşyeri Ayarları arayüzündeki
# "Üye İşyeri 3DSecure Callback Key" alanından ulaşabilirsiniz.

# TESTING
TESTCRAFTGATE_BASE_URL = 'https://sandbox-api.craftgate.io'
TESTCRAFTGATE_API_KEY = 'API_KEY'
TESTCRAFTGATE_SECRET_KEY = 'SECRET_KEY'
TESTCRAFTGATE_RANDOM_STRING = "RANDOM_STRING-xyEwd"
TESTCRAFTGATE_3DSECURE_CALLBACK_KEY = "32 Karakter"

class CraftgateOptionsProd():
    def __init__(self):
        self.api_key = CRAFTGATE_API_KEY
        self.secret_key = CRAFTGATE_SECRET_KEY
        self.base_url = CRAFTGATE_BASE_URL
        self.random_string = CRAFTGATE_RANDOM_STRING
        self.language = None

    def get_api_key(self):
        return self.api_key

    def get_secret_key(self):
        return self.secret_key

    def get_base_url(self):
        return self.base_url

    def get_random_string(self):
        return self.random_string

    def get_language(self):
        return self.language

    def to_dict(self):
        return {'api_key': self.api_key, 'secret_key': self.secret_key, 'base_url': self.base_url,
                'language': self.language, }


class CraftgateOptionsTest():
    def __init__(self):
        self.api_key = TESTCRAFTGATE_API_KEY
        self.secret_key = TESTCRAFTGATE_SECRET_KEY
        self.base_url = TESTCRAFTGATE_BASE_URL
        self.random_string = TESTCRAFTGATE_RANDOM_STRING
        self.language = None

    def get_api_key(self):
        return self.api_key

    def get_secret_key(self):
        return self.secret_key

    def get_base_url(self):
        return self.base_url

    def get_random_string(self):
        return self.random_string

    def get_language(self):
        return self.language

    def to_dict(self):
        return {'api_key': self.api_key, 'secret_key': self.secret_key, 'base_url': self.base_url,
                'language': self.language, }
