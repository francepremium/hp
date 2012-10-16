from django.contrib import auth, messages
from django.shortcuts import redirect

from account.views import SignupView as PinaxSignupView
from account.views import LoginView as PinaxLoginView
from account.views import ConfirmEmailView as PinaxConfirmEmailView

from forms import SignupForm, LoginForm


class ConfirmEmailView(PinaxConfirmEmailView):
    def post(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm()
        user = confirmation.email_address.user
        user.is_active = True
        user.save()

        user.backend = "django.contrib.auth.backends.ModelBackend"
        auth.login(self.request, user)
        redirect_url = user.hpprofile.next_url

        if not redirect_url:
            redirect_url = self.get_redirect_url()
        if not redirect_url:
            ctx = self.get_context_data()
            return self.render_to_response(ctx)
        if self.messages.get("email_confirmed"):
            messages.add_message(
                self.request,
                self.messages["email_confirmed"]["level"],
                self.messages["email_confirmed"]["text"] % {
                    "email": confirmation.email_address.email
                }
            )
        return redirect(redirect_url)


class LoginView(PinaxLoginView):
    form_class = LoginForm


class SignupView(PinaxSignupView):
    form_class = SignupForm

    def generate_username(self, form):
        return form.cleaned_data['email']
