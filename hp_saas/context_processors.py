from forms import SignupForm, LoginForm


def login_or_signup_forms(request):
    if request.user.is_authenticated():
        return {}

    return {
        'signup_form': SignupForm(),
        'login_form': LoginForm(),
    }
