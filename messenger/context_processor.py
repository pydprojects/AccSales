from .utils import memoize


def unread_messages(request):
    """Memoize remembers return value of a function call, under the key made from it's arguments. For each arguments
    combination it's called at most one time. In our example, we're using argument-less lambda functions,
    so it's called either 0 or 1 time (on first usage).
    It's calculated when it appear for first time inside templates"""
    user = request.user
    unread_messages_count = memoize(lambda: user.dialog_set.unread(user=user).count())
    return {'unread_messages_count': unread_messages_count}
