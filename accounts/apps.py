from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    def ready(self):
        print('I am in side the ready ')
        import accounts.signal