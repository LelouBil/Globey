import discord.ext.commands
import Globey

with open("helptext.txt") as c:
    helpText: str = "".join(c.readlines())



class GlobeyHelpFormatter(discord.ext.commands.HelpFormatter):

    def format(self):
        Globey.log.info("Emojii result")
        import Globey.apicall as apicall
        Globey.log.info(apicall.get_endpoint("/guilds/507651328428998676/emojis").content)
        return [helpText]

    def get_ending_note(self):
        command_name = self.context.invoked_with
        return "Type {0}{1} command for more info on a command.\n" \
               "You can also type {0}{1} category for more info on a category.".format(self.clean_prefix, "help")

# todo later
#     if message.content.startswith("help"):
#         embed2 = discord.Embed(title="**Help menu**",
#                                description=f"**Hello {message.author.name}, here are all comands (with prefix_):** \n"
#                                            f"hi, invite, server, redriot, amiuseful, spam, invite. \n"
#                                            f"**admin command:**\n"
#                                            f"ban, warn, kick",
#                                color=message.author.color)
#         embed2.set_thumbnail(url=message.author.avatar_url)
#         embed2.set_footer(text="send by god")
#         await client.send_message(message.channel, embed=embed2)
