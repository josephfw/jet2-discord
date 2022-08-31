import interactions

async def command(context):
    channels = await context.guild.get_all_channels()

    logChannel = interactions.search_iterable(channels, name='log-channel')[0]
    
    await logChannel.send(
        embeds = [
            interactions.Embed(
                color = 0x2F3136,
                author = interactions.EmbedAuthor(
                    name = context.author.user.username,
                    icon_url = context.author.user.avatar_url
                ),
                description = f'The `{context.data.name}` command has been executed in <#{context.channel.id}> by <@{context.author.id}>.'
            )
        ]
    )