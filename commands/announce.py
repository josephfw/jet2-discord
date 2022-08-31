import interactions
from interactions.ext.wait_for import wait_for
from functions import get
import asyncio

class announce(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client
    
    @interactions.extension_command(
        name = 'announce',
        description = 'Announce a message to the entire server.',
        options = [
            interactions.Option(
                name = 'type',
                description = 'The type of announcement and the channel it will be sent in.',
                type = interactions.OptionType.STRING,
                required = True,
                choices = [
                    interactions.Choice(
                        name = 'Development',
                        value = 'Development'
                    ),
                    interactions.Choice(
                        name = 'Announcement',
                        value = 'Announcement'
                    )
                ]
            ),
            interactions.Option(
                name = 'title',
                description = 'The title of the announcement.',
                type = interactions.OptionType.STRING,
                required = True
            )
        ]
    )
    async def announce_command(self, ctx, type: str, title: str):
        channels = await ctx.guild.get_all_channels()
        roles = await ctx.guild.get_all_roles()

        executiveRole = interactions.search_iterable(roles, name='Executive')[0]
        directorRole = interactions.search_iterable(roles, name='Director')[0]

        announcementChannel = interactions.search_iterable(channels, name='announcements')[0]
        developmentChannel = interactions.search_iterable(channels, name='development')[0]

        if type == 'Development':
            await ctx.send('Not yet supported.')
        elif type == 'Announcement':
            if directorRole.id in ctx.author.roles or executiveRole.id in ctx.author.roles:
                await ctx.send(
                    embeds = [
                        interactions.Embed(
                            color = 0x2F3136,
                            fields = [
                                interactions.EmbedField(
                                    name = f'Enter announcement description',
                                    value = f'Send the announcement you would like to send in this channel, not including the title. You may use discord markdown.\n\nAlternatively, you may say `cancel` to cancel this action.'
                                )
                            ]
                        )
                    ],
                    ephemeral = False
                )

                async def check(msg):
                    if int(msg.author.id) == int(ctx.author.user.id):
                        return True
                    else:
                        return False

                try:
                    msg: message = await wait_for(self.client, 'on_message_create', check = check, timeout = 60)

                    if msg.content == 'cancel':
                        await ctx.send(
                            embeds = [
                                interactions.Embed(
                                    color = 0x2F3136,
                                    fields = [
                                        interactions.EmbedField(
                                            name = 'Action cancelled',
                                            value = f'Your announcement has been cancelled, nothing has been announced.'
                                        )
                                    ]
                                )
                            ]
                        )
                    else:
                        await announcementChannel.send(
                            embeds = [
                                interactions.Embed(
                                    color = 0x2F3136,
                                    fields = [
                                        interactions.EmbedField(
                                            name = title,
                                            value = msg.content
                                        )
                                    ]
                                )
                            ]
                        )

                        await ctx.send(
                            embeds = [
                                interactions.Embed(
                                    color = 0x2F3136,
                                    fields = [
                                        interactions.EmbedField(
                                            name = 'Action completed',
                                            value = f'Your announcement has been posted in <#{announcementChannel.id}>, you may now tag people as you wish.'
                                        )
                                    ]
                                )
                            ]
                        )
                except asyncio.TimeoutError:
                    await ctx.send('You took longer than 60 seconds to send a message, the action has now been cancelled.')
            else:
                await ctx.send(
                    embeds = [
                        interactions.Embed(
                        color = 0x2F3136,
                            fields = [
                                interactions.EmbedField(
                                    name = 'Action failed',
                                    value = f'You do not have the `{directorRole.name}` or `{executiveRole.name}` role.'
                                )
                            ]
                        )
                    ]
                )

def setup(client):
    announce(client)