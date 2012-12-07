import rules_light


# Should be secured in the view with
# self.request.session['appstore_environment']
rules_light.registry['formapp.record.create'] = True
rules_light.registry['formapp.record.list'] = True
