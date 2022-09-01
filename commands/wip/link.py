import interactions
from functions import get

class link(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client
    
    @interactions.extension_command(
        name = 'link',
        description = 'Link your ROBLOX account to your Discord account.'
    )
    async def link_command(self, ctx):
        try:
            data = get.ROBLOX(ctx.author.id)
            roles = await ctx.guild.get_all_roles()

            standardRole = interactions.search_iterable(roles, name=data['role'])[0]

            await ctx.member.add_role(standardRole, guild_id=int(ctx.guild_id))
            await ctx.author.modify(nick=data['username'], guild_id=int(ctx.guild_id))

            if data['extra'] != None:
                extraRole = interactions.search_iterable(roles, name=data['extra'])[0]
                await ctx.member.add_role(extraRole, guild_id=int(ctx.guild_id))
            
            await ctx.send(
                embeds = [
                    interactions.Embed(
                        color = 0xe2231a,
                        fields = [
                            interactions.EmbedField(
                                name = 'Account linked',
                                value = f'Your Discord account has been linked successfully to your ROBLOX account using the Bloxlink API.'
                            )
                        ]
                    )
                ],
                ephemeral = False
            )
        except:
            await ctx.send(
                embeds = [
                    interactions.Embed(
                        color = 0xe2231a,
                        fields = [
                            interactions.EmbedField(
                                name = 'Error',
                                value = f'An error occured during the verification process, this has been logged. You may contact <@490941018334822403> for assistance.'
                            )
                        ]
                    )
                ],
                ephemeral = False
            )

def setup(client):
    link(client)