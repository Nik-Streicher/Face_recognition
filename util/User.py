class User:

    def __init__(self, name, embedding, access):
        self._name = name
        self._embedding = embedding
        self._access = access

    def get_name(self):
        return self._name

    def get_embedding(self):
        return self._embedding

    def get_access(self):
        return self._access



