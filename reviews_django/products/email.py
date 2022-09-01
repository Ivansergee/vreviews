from djoser.email import UsernameChangedConfirmationEmail, PasswordChangedConfirmationEmail


class UsernameChangedConfirmation(UsernameChangedConfirmationEmail):
    template_name = 'email/login-change.html'

    def get_context_data(self):
        context = super().get_context_data()
        return context


class PasswordChangedConfirmation(PasswordChangedConfirmationEmail):
    template_name = 'email/password-change.html'

    def get_context_data(self):
        context = super().get_context_data()
        return context