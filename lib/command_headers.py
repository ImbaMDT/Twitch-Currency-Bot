## Commands Definierung

import globals

commands = {
    '!treats': {
        'limit': 0,
        'return': 'command',
        'argc': 3,
        'ul': 'mod',
        'usage': '!treats [add/remove/set] [username] [number]'
    },
    '!report': {
        'limit': 200,
        'argc': 1,
        'return': 'command',
        'space_case': True,
        'ul': 'mod',
        'usage': "!report [insert bug report text here]"
    },
    '!commands': {
        'limit': 10,
        'argc': 0,
        'return': 'command',
        'usage': '!commands'
    },
    '!opinion': {
        'limit': 0,
        'argc': 0,
        'return': 'command',
        'ul': 'reg',
        'usage': '!opinion',
        'user_limit': 30
    },
    '!shots': {
        'limit': 0,
        'return': 'command',
        'argc': 2,
        'ul': 'mod',
        'usage': '!shots [add/remove/set] [number]'
    },
    '!help': {
        'limit': 15,
        'return': 'There is a super useful README for lorenzo at http://www.twitch.tv/lorenzotherobot',
        'usage': '!help',
        'user_limit': 30
    },
    '!highlight': {
        'limit': 15,
        'return': 'command',
        'argc': 0,
        'usage': '!highlight'
    },
    '!followers': {
        'limit': 30,
        'return': 'command',
        'argc': 0,
        'usage': '!followers',
        'user_limit': 30,
    },
    '!follower': {
        'limit': 0,
        'return': 'command',
        'argc': 1,
        'usage': '!follower [username]',
        'ul': 'mod'
    },
    '!uptime': {
        'limit': 15,
        'return': 'command',
        'argc': 0,
        'usage': '!uptime',
        'user_limit': 30,
    },
    '!stream': {
        'limit': 0,
        'return': 'command',
        'argc': 0,
        'usage': '!stream'
    },
    '!gift': {
        'limit': 0,
        'argc': 3,
        'return': 'command',
        'ul': 'mod',
        'usage': "!gift [username] [item] [item_number]"
    },
    '!nickname': {
        'limit': 0,
        'argc': 2,
        'return': 'command',
        'usage': '!nickname [position_to_update] [nickname(must not contain spaces)]'
    },
    '!popularity': {
        'limit': 0,
        'argc': 1,
        'return': 'command',
        'space_case': True,
        'usage': '!popularity [name_of_game]'
    },
    '!check': {
        'limit': 10,
        'argc': 1,
        'return': 'command',
        'usage': "!check ['trades'/'market'/'items'/'inventory'/username]",
        'user_limit': 30
    },
    '!leaderboard': {
        'limit': 300,
        'argc': 0,
        'return': 'command',
        'usage': '!leaderboard',
        'user_limit': 300,
    },
    '!stats': {
        'limit': 0,
        'argc': 0,
        'return': 'command',
        'usage': '!stats',
        'user_limit': 1000,
    },
    '!define': {
        'limit': 6,
        'user_limit': 300,
        'argc': 1,
        'space_case': True,
        'return': 'command',
        'usage': '!define [insert_word_here]'
    },
    '!caster': {
        'limit': 0,
        'argc': 1,
        'return': 'command',
        'usage': '!caster [streamer_username]',
        'ul': 'mod'
    },
    '!add': {
        'limit': 0,
        'argc': 4,
        'return': 'command',
        'usage': '!add [!command_name] [user_level (reg/mod)] [response (to add a custom user, use "{}") (to include message count, use "[]")]',
        'ul': 'mod'
    },
    '!rem': {
        'limit': 0,
        'argc': 1,
        'return': 'command',
        'usage': '!rem [!command_name]',
        'ul': 'mod'
    },
    '!edit': {
        'limit': 0,
        'argc': 4,
        'return': 'command',
        'usage': '!edit [!command_name] [user_level (reg/mod)] [response (to add a custom user, use "{}")]',
        'ul': 'mod'
    },
    '!weather': {
        'limit': 0,
        'argc': 2,
        'return': 'command',
        'usage': '!weather [units (metric/imperial)] [location (any format)]',
        'ul': 'mod'
    },
    '!addquote': {
        'limit': 0,
        'argc': 1,
        'user_limit': 15,
        'return': 'command',
        'usage': '!addquote [quote]',
        'space_case': True
    },
    '!quote': {
        'limit': 0,
        'argc': 0,
        'user_limit': 5,
        'return': 'command',
        'usage': '!quote'
    },
    '!subcount': {
        'limit': 0,
        'argc': 0,
        'ul': 'mod',
        'return': 'command',
        'usage': '!subcount'
    },
    '!testcommand': {
        'limit': 0,
        'argc': 0,
        'ul': 'mod',
        'return': 'command',
        'usage': '!testcommand'
    },
    '!blacklist': {
        'limit': 0,
        'argc': 0,
        'ul': 'superuser',
        'return': 'command',
        'usage': '!blacklist ["add"/"remove"] [username]'
    }
}

user_cooldowns = {"channels": {}}


def initalize_commands_after_runtime(channel):
    if channel not in user_cooldowns["channels"]:
        user_cooldowns["channels"][channel] = {"commands": {}}
        for command in commands:
            commands[command][channel] = {}
            commands[command][channel]['last_used'] = 0
            if "user_limit" in commands[command]:
                user_cooldowns["channels"][channel]["commands"][command] = {
                    "users": {}}
        channel = channel.lstrip('#')


def deinitialize_commands_after_runtime(channel):
    if channel in user_cooldowns["channels"]:
        for command in commands:
            commands[command][channel] = {}
            commands[command][channel]['last_used'] = 0
            if "user_limit" in commands[command]:
                user_cooldowns["channels"][channel]["commands"][command] = {
                    "users": {}}
        del user_cooldowns["channels"][channel]
        channel = channel.lstrip('#')
        del globals.CHANNEL_INFO[channel]


def initalize_commands(config):
    for channel in config['channels']:
        user_cooldowns["channels"][channel] = {"commands": {}}
        if "rooms" in config:
            if channel in config["rooms"]:
                globals.CHANNEL_INFO[channel.lstrip("#")] = {
                    "rooms": config["rooms"][channel]
                }
                for room in config["rooms"]:
                    globals.CHAT_ROOMS[room[1]] = channel
        for command in commands:
            commands[command][channel] = {}
            commands[command][channel]['last_used'] = 0
            if "user_limit" in commands[command]:
                user_cooldowns["channels"][channel]["commands"][command] = {
                    "users": {}}
