import rules_light


# Should be secured in the view with
# self.request.session['appstore_environment']
rules_light.registry['formapp.record.create'] = True
rules_light.registry['formapp.record.list'] = True


def is_appstore_user(user, rule, record):
    return user in record.environment.users.all()
rules_light.registry['formapp.record.read'] = is_appstore_user
