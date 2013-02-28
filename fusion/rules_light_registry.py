import rules_light


@rules_light.is_authenticated
def is_env_user(user, rule, obj):
    return user in obj.environment.users.all()
rules_light.registry['fusion.list.detail'] = is_env_user
