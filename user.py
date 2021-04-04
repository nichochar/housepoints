class User:
    def __init__(self, username, is_authenticated=False):
        self.username = username
        self.is_authenticated = is_authenticated
        self.is_active = True  # we don't do email validation

    def is_authenticated(self):
        return self.is_authenticated

    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return not self.is_authenticated

    def get_id(self):
        return self.username
