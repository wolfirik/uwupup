owners = [
    158750488563679232      # not AlexFlipnote
]

version = "v1.2.3"
invite = "https://discord.gg/DpxkY3x"


def is_owner(ctx):
    return ctx.author.id in owners
