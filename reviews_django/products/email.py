from djoser.email import UsernameChangedConfirmationEmail


class UsernameChangedConfirmation(UsernameChangedConfirmationEmail):
    template_name = 'email/test.html'

    def get_context_data(self):
        context = super().get_context_data()
        return context