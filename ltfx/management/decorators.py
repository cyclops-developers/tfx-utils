from click.decorators import *
from click.decorators import command as click_command


def command(*args, **kwargs):
    def wrapper(func):
        @pass_context
        def new_func(ctx, *args, **kwargs):
            return ctx.invoke(func, ctx, *args, **kwargs)
        return click_command(*args, **kwargs)(update_wrapper(new_func, func))
    return wrapper
