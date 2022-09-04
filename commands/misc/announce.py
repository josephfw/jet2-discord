import interactions
from interactions.ext.wait_for import wait_for
from functions import get, log
import asyncio

class announce(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client
    
    @interactions.extension_command()
    async def announce(self, ctx):
        pass

    @announce.subcommand(
        options = [
            interactions.Option(
                name = 'title',
                description = 'The title of the description / first embed.',
                type = interactions.OptionType.STRING,
                required = True
            ),
            interactions.Option(
                name = 'description',
                description = 'The description of the description / first embed.',
                type = interactions.OptionType.STRING,
                required = True
            ),
            interactions.Option(
                name = 'attachment1',
                description = 'An image you would like to send.',
                type = interactions.OptionType.ATTACHMENT,
                required = True
            ),
            interactions.Option(
                name = 'attachment2',
                description = 'Another image you would like to send.',
                type = interactions.OptionType.ATTACHMENT,
                required = False
            ),
            interactions.Option(
                name = 'attachment3',
                description = 'Another image you would like to send.',
                type = interactions.OptionType.ATTACHMENT,
                required = False
            ),
            interactions.Option(
                name = 'attachment4',
                description = 'Another image you would like to send.',
                type = interactions.OptionType.ATTACHMENT,
                required = False
            ),
            interactions.Option(
                name = 'attachment5',
                description = 'Another image you would like to send.',
                type = interactions.OptionType.ATTACHMENT,
                required = False
            )
        ]
    )
    async def development(self, ctx, title, description, attachment1, attachment2 = None, attachment3 = None, attachment4 = None, attachment5 = None):
        '''Show off some development images in #development.'''

        channels = await ctx.guild.get_all_channels()
        roles = await ctx.guild.get_all_roles()

        executiveRole = interactions.search_iterable(roles, name='Executive')[0]
        developmentChannel = interactions.search_iterable(channels, name='development')[0]

        if executiveRole.id in ctx.author.roles:
            attachments = [attachment1, attachment2, attachment3, attachment4, attachment5]
            
            announcementEmbeds = [
                interactions.Embed(
                    color = 0x2F3136,
                    fields = [
                        interactions.EmbedField(
                            name = title,
                            value = description
                        )
                    ]
                )
            ]

            for attachment in attachments:
                if attachment == None:
                    continue
                elif attachment.content_type[0:5] == 'image':
                    announcementEmbeds.append(
                        interactions.Embed(
                            color = 0x2F3136,
                            image = interactions.EmbedImageStruct(
                                url = attachment.url
                            )
                        )
                    )

            await developmentChannel.send(embeds = announcementEmbeds)

            await ctx.send(
                embeds = [
                    interactions.Embed(
                        color = 0x2F3136,
                        fields = [
                            interactions.EmbedField(
                                name = 'Action completed',
                                value = f'Your images have been posted in <#{developmentChannel.id}>, you may now tag people as you wish.'
                            )
                        ]
                    )
                ]
            )

            await log.command(ctx)
        else:
            await ctx.send(
                embeds = [
                    interactions.Embed(
                        color = 0x2F3136,
                        fields = [
                            interactions.EmbedField(
                                name = 'Error',
                                value = 'You need the `Executive` role to run this command.'
                            )
                        ]
                    )
                ]
            )

    @announce.subcommand(
        options = [
            interactions.Option(
                name = 'title',
                description = 'The title of the announcement.',
                type = interactions.OptionType.STRING,
                required = True
            )
        ]
    )
    async def announcement(self, ctx, title):
        '''Make an announcement in #announcements.'''

        channels = await ctx.guild.get_all_channels()
        roles = await ctx.guild.get_all_roles()

        executiveRole = interactions.search_iterable(roles, name='Executive')[0]
        directorRole = interactions.search_iterable(roles, name='Director')[0]
        announcementsChannel = interactions.search_iterable(channels, name='announcements')[0]

        if executiveRole.id in ctx.author.roles or directorRole.id in ctx.author.roles:
            async def check(msg):
                if int(msg.author.id) == int(ctx.author.user.id):
                    return True
                else:
                    return False

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

            try:
                msg: interactions.Message = await wait_for(self.client, 'on_message_create', check = check, timeout = 60)

                if msg.content == 'cancel':
                    await ctx.send(
                        embeds = [
                            interactions.Embed(
                                color = 0x2F3136,
                                fields = [
                                    interactions.EmbedField(
                                        name = 'Action cancelled',
                                        value = 'Your announcement has been cancelled, nothing has been announced.'
                                    )
                                ]
                            )
                        ]
                    )
                else:
                    await announcementsChannel.send(
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

                    await msg.reply(
                        embeds = [
                            interactions.Embed(
                                color = 0x2F3136,
                                fields = [
                                    interactions.EmbedField(
                                        name = 'Action completed',
                                        value = f'Your announcement has been posted in <#{announcementsChannel.id}>, you may now tag people as you wish.'
                                    )
                                ]
                            )
                        ]
                    )

                    await log.command(ctx)



            except:
                await ctx.send(
                    embeds = [
                        interactions.Embed(
                            color = 0x2F3136,
                            fields = [
                                interactions.EmbedField(
                                    name = 'Error',
                                    value = 'It is most likely you took longer than 60 seconds to send a message.'
                                )
                            ]
                        )
                    ]
                )
        else:
            await ctx.send(
                embeds = [
                    interactions.Embed(
                        color = 0x2F3136,
                        fields = [
                            interactions.EmbedField(
                                name = 'Error',
                                value = 'You need the `Executive` or `Director` role to run this command.'
                            )
                        ]
                    )
                ]
            )
    
        

def setup(client):
    announce(client)