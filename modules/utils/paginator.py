import asyncio
import inspect
import itertools
import re
import discord


class CannotPaginate(Exception):
    pass


class Pages:
    """Implements a paginator that queries the user for the
    pagination interface.

    Pages are 1-index based, not 0-index based.

    If the user does not reply within 2 minutes then the pagination
    interface exits automatically.

    Parameters
    ------------
    ctx: Context
        The context of the command.
    lines: List[str]
        A list of lines to paginate.
    per_page: int
        How many lines show up per page.
    show_entry_count: bool
        Whether to show an entry count in the footer.

    Attributes
    -----------
    embed: discord.Embed
        The embed object that is being used to send pagination info.
        Feel free to modify this externally. Only the description,
        footer fields, and colour are internally modified.
    permissions: discord.Permissions
        Our permissions for the channel.
    """

    def __init__(self, ctx, *, lines, per_page=12, show_entry_count=True):
        self.bot = ctx.bot
        self.lines = lines
        self.message = ctx.message
        self.channel = ctx.channel
        self.author = ctx.author
        self.per_page = per_page
        pages, left_over = divmod(len(self.lines), self.per_page)
        if left_over:
            pages += 1
        self.maximum_pages = pages
        self.embed = discord.Embed(colour=discord.Colour.red())
        self.paginating = len(lines) > per_page
        self.show_entry_count = show_entry_count
        self.reaction_emojis = [
            ('\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}',
             self.first_page),
            ('\N{BLACK LEFT-POINTING TRIANGLE}', self.previous_page),
            ('\N{BLACK SQUARE FOR STOP}', self.stop_pages),
            ('\N{BLACK RIGHT-POINTING TRIANGLE}', self.next_page),
            ('\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}',
             self.last_page),
            ('\N{INPUT SYMBOL FOR NUMBERS}', self.numbered_page),
        ]

        if ctx.guild is not None:
            self.permissions = self.channel.permissions_for(ctx.guild.me)
        else:
            self.permissions = self.channel.permissions_for(ctx.bot.user)

        if not self.permissions.embed_links:
            raise CannotPaginate('Bot does not have embed links permission.')

        if not self.permissions.send_messages:
            raise CannotPaginate('Bot cannot send messages.')

        if self.paginating:
            # verify we can actually use the pagination session
            if not self.permissions.add_reactions:
                raise CannotPaginate(
                    'Bot does not have add reactions permission.')

            if not self.permissions.read_message_history:
                raise CannotPaginate(
                    'Bot does not have Read Message History permission.')

    def get_page(self, page):
        base = (page - 1) * self.per_page
        return self.lines[base:base + self.per_page]

    def prepare_embed(self, lines, page, *, first=False):
        p = []
        for index, entry in enumerate(lines, 1 + ((page - 1) * self.per_page)):
            p.append(f'{index}. {entry}')

        if self.maximum_pages > 1:
            if self.show_entry_count:
                text = f'Page {page}/{self.maximum_pages} ({len(self.lines)} lines)'
            else:
                text = f'Page {page}/{self.maximum_pages}'

            self.embed.set_footer(text=text)

        self.embed.description = '\n'.join(p)

    async def show_page(self, page, *, first=False):
        self.current_page = page
        lines = self.get_page(page)
        self.prepare_embed(lines, page, first=first)

        if not self.paginating:
            return await self.channel.send(embed=self.embed)

        if not first:
            await self.message.edit(embed=self.embed)
            return

        self.message = await self.channel.send(embed=self.embed)
        for (reaction, _) in self.reaction_emojis:
            if self.maximum_pages == 2 and reaction in ('\u23ed', '\u23ee'):
                continue

            await self.message.add_reaction(reaction)

    async def checked_show_page(self, page):
        if page != 0 and page <= self.maximum_pages:
            await self.show_page(page)

    async def first_page(self):
        await self.show_page(1)

    async def last_page(self):
        await self.show_page(self.maximum_pages)

    async def next_page(self):
        await self.checked_show_page(self.current_page + 1)

    async def previous_page(self):
        await self.checked_show_page(self.current_page - 1)

    async def show_current_page(self):
        if self.paginating:
            await self.show_page(self.current_page)

    async def numbered_page(self):
        to_delete = []
        to_delete.append(await self.channel.send('What page do you want to go to?'))

        def message_check(m):
            return m.author == self.author and \
                self.channel == m.channel and \
                m.content.isdigit()

        try:
            msg = await self.bot.wait_for('message', check=message_check, timeout=30.0)
        except asyncio.TimeoutError:
            to_delete.append(await self.channel.send('Took too long.'))
            await asyncio.sleep(5)
        else:
            page = int(msg.content)
            to_delete.append(msg)
            if page != 0 and page <= self.maximum_pages:
                await self.show_page(page)
            else:
                to_delete.append(await self.channel.send(f'Invalid page given. ({page}/{self.maximum_pages})'))
                await asyncio.sleep(5)

        try:
            await self.channel.delete_messages(to_delete)
        except Exception:
            pass

    async def stop_pages(self):
        """stops the interactive pagination session"""
        await self.message.delete()
        self.paginating = False

    def react_check(self, reaction, user):
        if user is None or user.id != self.author.id:
            return False

        if reaction.message.id != self.message.id:
            return False

        for (emoji, func) in self.reaction_emojis:
            if reaction.emoji == emoji:
                self.match = func
                return True
        return False

    async def paginate(self):
        first_page = self.show_page(1, first=True)
        if not self.paginating:
            await first_page
        else:
            # allow us to react to reactions right away if we're paginating
            self.bot.loop.create_task(first_page)

        while self.paginating:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=self.react_check, timeout=120.0)
            except asyncio.TimeoutError:
                self.paginating = False
                try:
                    await self.message.clear_reactions()
                except:
                    pass
                finally:
                    break

            try:
                await self.message.remove_reaction(reaction, user)
            except:
                pass  # can't remove it so don't bother doing so

            await self.match()


class FieldPages(Pages):
    """Similar to Pages except lines should be a list of
    tuples having (key, value) to show as embed fields instead.
    """

    def prepare_embed(self, lines, page, *, first=False):
        self.embed.clear_fields()
        self.embed.description = discord.Embed.Empty

        for key, value in lines:
            self.embed.add_field(name=key, value=value, inline=False)

        if self.maximum_pages > 1:
            if self.show_entry_count:
                text = f'Page {page}/{self.maximum_pages} ({len(self.lines)} lines)'
            else:
                text = f'Page {page}/{self.maximum_pages}'

            self.embed.set_footer(text=text)


# ?help
# ?help Cog
# ?help command
#   -> could be a subcommand
_mention = re.compile(r'<@\!?([0-9]{1,19})>')


def cleanup_prefix(bot, prefix):
    m = _mention.match(prefix)
    if m:
        user = bot.get_user(int(m.group(1)))
        if user:
            return f'@{user.name} '
    return prefix


async def _can_run(cmd, ctx):
    try:
        return await cmd.can_run(ctx)
    except:
        return False


def _command_signature(cmd):
    # this is modified from discord.py source
    # which I wrote myself lmao

    result = [cmd.qualified_name]
    if cmd.usage:
        result.append(cmd.usage)
        return ' '.join(result)

    params = cmd.clean_params
    if not params:
        return ' '.join(result)

    for name, param in params.items():
        if param.default is not param.empty:
            # We don't want None or '' to trigger the [name=value] case and instead it should
            # do [name] since [name=None] or [name=] are not exactly useful for the user.
            should_print = param.default if isinstance(
                param.default, str) else param.default is not None
            if should_print:
                result.append(f'[{name}={param.default!r}]')
            else:
                result.append(f'[{name}]')
        elif param.kind == param.VAR_POSITIONAL:
            result.append(f'[{name}...]')
        else:
            result.append(f'<{name}>')

    return ' '.join(result)


class HelpPaginator(Pages):
    def __init__(self, ctx, lines, *, per_page=4):
        super().__init__(ctx, lines=lines, per_page=per_page)
        self.total = len(lines)

    @classmethod
    async def from_cog(cls, ctx, cog):
        cog_name = cog.__class__.__name__

        # get the commands
        lines = sorted(ctx.bot.get_cog_commands(
            cog_name), key=lambda c: c.name)

        # remove the ones we can't run
        lines = [cmd for cmd in lines if (await _can_run(cmd, ctx)) and not cmd.hidden]

        self = cls(ctx, lines)
        self.title = f'{cog_name} Commands'
        self.description = inspect.getdoc(cog)
        self.prefix = cleanup_prefix(ctx.bot, ctx.prefix)

        # no longer need the database

        return self

    @classmethod
    async def from_command(cls, ctx, command):
        try:
            lines = sorted(command.commands, key=lambda c: c.name)
        except AttributeError:
            lines = []
        else:
            lines = [cmd for cmd in lines if (await _can_run(cmd, ctx)) and not cmd.hidden]

        self = cls(ctx, lines)
        self.title = command.signature

        if command.description:
            self.description = f'{command.description}\n\n{command.help}'
        else:
            self.description = command.help or 'No help given.'

        self.prefix = cleanup_prefix(ctx.bot, ctx.prefix)

        return self

    @classmethod
    async def from_bot(cls, ctx):
        def key(c):
            return c.cog_name or '\u200bMisc'

        lines = sorted(ctx.bot.commands, key=key)
        nested_pages = []
        per_page = 9

        # 0: (cog, desc, commands) (max len == 9)
        # 1: (cog, desc, commands) (max len == 9)
        # ...

        for cog, commands in itertools.groupby(lines, key=key):
            plausible = [cmd for cmd in commands if (await _can_run(cmd, ctx)) and not cmd.hidden]
            if len(plausible) == 0:
                continue

            description = ctx.bot.get_cog(cog)
            if description is None:
                description = discord.Embed.Empty
            else:
                description = inspect.getdoc(
                    description) or discord.Embed.Empty

            nested_pages.extend(
                (cog, description, plausible[i:i + per_page]) for i in range(0, len(plausible), per_page))

        # this forces the pagination session
        self = cls(ctx, nested_pages, per_page=1)
        self.prefix = cleanup_prefix(ctx.bot, ctx.prefix)

        # swap the get_page implementation with one that supports our style of pagination
        self.get_page = self.get_bot_page
        self._is_bot = True

        # replace the actual total
        self.total = sum(len(o) for _, _, o in nested_pages)
        return self

    def get_bot_page(self, page):
        cog, description, commands = self.lines[page - 1]
        self.title = f'{cog} Commands'
        self.description = description
        return commands

    def prepare_embed(self, lines, page, *, first=False):
        self.embed.clear_fields()
        self.embed.description = self.description
        self.embed.title = self.title

        if hasattr(self, '_is_bot'):
            value = 'Support server: https://discord.gg/HaCgM7y'
            self.embed.add_field(name='Support', value=value, inline=False)

        self.embed.set_footer(
            text=f'Use "{self.prefix}help command" for more info on a command.')

        signature = _command_signature

        for entry in lines:
            self.embed.add_field(name=signature(
                entry), value=entry.short_doc or "No help given", inline=False)

        if self.maximum_pages:
            self.embed.set_author(
                name=f'Page {page}/{self.maximum_pages} ({self.total} commands)')


        async def go_back_to_current_page():
            await asyncio.sleep(30.0)
            await self.show_current_page()

        self.bot.loop.create_task(go_back_to_current_page())

        async def go_back_to_current_page():
            await asyncio.sleep(30.0)
            await self.show_current_page()

        self.bot.loop.create_task(go_back_to_current_page())

