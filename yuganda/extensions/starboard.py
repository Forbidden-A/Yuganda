import lightbulb
import logging
import typing
import hikari
from random import randint
from yuganda import Yuganda, find

_LOGGER = logging.getLogger("yuganda.extensions.starboard")


class Starboard(lightbulb.Plugin):
    def __init__(self, bot):
        self.bot: Yuganda = bot
        super().__init__()

    def starboard_embed(
        self,
        message: hikari.Message,
        guild_id: int,
        channel: hikari.TextableGuildChannel,
        count: int,
    ) -> hikari.Embed:
        assert message.member is not None
        embed = (
            hikari.Embed(
                description=f"[Jump to message!]({message.make_link(guild_id)})",
                colour=randint(0x0, 0xFFFFFF),
            )
            .set_author(
                name=message.member.display_name, icon=message.member.avatar_url
            )
            .set_footer(text=f"#{channel.name}")
        )
        assert message.content is not None
        content = (
            (message.content[:150] + "..")
            if len(message.content) > 150
            else message.content
        )
        assert embed.description is not None
        embed.description += "\n" + content
        if message.attachments:
            for attachment in message.attachments:
                if attachment.media_type in (
                    "webp",
                    "gif",
                    "jepg",
                    "jpg",
                    "png",
                ):  # ? Lottie file type?
                    embed.set_image(attachment.proxy_url)
                    if len(message.attachments) > 1:
                        embed.description += "\n.. more attachments.."
                    break
        return embed

    @lightbulb.listener()
    async def on_reaction_add(self, event: hikari.GuildReactionAddEvent):
        if event.emoji_name != "⭐":
            return

        guild_options: dict[
            str, typing.Any
        ] = await self.bot.database.get_guild_options(event.guild_id)

        if (starboard_id := guild_options.get("starboard_id")) is None:
            return

        assert starboard_id is not None and starboard_id is int
        starboard = self.bot.cache.get_guild_channel(
            starboard_id
        ) or await self.bot.rest.fetch_channel(starboard_id)

        message = self.bot.cache.get_message(
            event.message_id
        ) or await self.bot.rest.fetch_message(event.channel_id, event.message_id)

        if event.user_id == message.author.id:
            return await message.remove_reaction("⭐", user=event.user_id)

        reaction: typing.Optional[hikari.Reaction] = find(
            message.reactions, lambda r: r.emoji == "⭐"
        )
        if reaction is None:
            return

        if reaction.count < self.bot.config.bot.starboard_threshold:
            return

        channel = (
            self.bot.cache.get_guild_channel(message.channel_id)
            or message.fetch_channel()
        )
        assert channel is not None
        if (
            starred_message := await self.bot.database.get_starred_message(message.id)
        ) is None:
            followup = await starboard.send(
                content=f"⭐ {reaction.count} {channel}",
                embed=self.starboard_embed(
                    message, event.guild_id, channel, reaction.count
                ),
            )
            await self.bot.database.create_starred_message(
                message.id, followup.id, reaction.count
            )
        else:
            followup: hikari.Message = self.bot.cache.get_message(
                followup_id := starred_message.get("followup_id")
            ) or await self.bot.rest.fetch_message(starboard, followup_id)
            await followup.edit(
                content=f"⭐ {reaction.count} {channel}",
                embed=self.starboard_embed(
                    message, event.guild_id, channel, reaction.count
                ),
            )
            await self.bot.database.update_starred_message(message.id, reaction.count)


def load(bot: Yuganda):
    bot.add_plugin(Starboard(bot))
