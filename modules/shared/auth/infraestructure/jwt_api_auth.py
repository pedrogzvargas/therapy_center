from modules.shared.auth.domain import ApiAuth


class JwtApiAuth(ApiAuth):
    def allowed(self):
        pass

    def get_user(self):
        pass
