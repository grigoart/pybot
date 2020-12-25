## Prerequisites

python3+

## Usage

### Bot

#### Usage

`bot.py <gist_api_token> [<command_fetch_interval[s]> <bot_id> <init_datetime>]`

* `<gist_api_token>` - token for the gist api
* `<command_fetch_interval[s]>` - command fetch interval (in seconds, default = 1)
* `<bot_id>` - id of the preregistered bot (if none provided, it will be registered)
* `<init_datetime>` - init time to fetch commands (format '%Y-%m-%dT%H:%M:%SZ', default = '1900-01-01T00:00:00Z')

### Bot master

#### Usage

`bot_master.py <gist_api_token>`

* `<gist_api_token>` - token for the gist api

#### Interactive usage

* `bots` - list all bots
* `select <bot_id>` - select a bot
* `send <local_source_file> <remote_target_file>` - send file to a current bot's environment
* `cm <command>` - send a command (to current bot). Available commands:
  * `ls <dir path>` - list files in the directory
  * `cp <source> <target>` - copy a remote file
  * `exec <os command and args>` - execute OS command
* `history` - print a command history (of selected bot)
* `result <command_id>` - print the result of a command (of current bot)
* `info` - print info about environment (of current bot)
* `last` - print the result of the last executed command (of current bot)
* `help` - for help
* `exit` - to exit

## Example

___1. Run bots in two different environments:___

_Bot #1:_
```
username@hostname:~/$ python3 bot.py 349ab29asxtabw423bva5hca5623bc39b8c8
25/12/2020 14:03:20 [INFO] Registering the bot...
25/12/2020 14:03:22 [INFO] Successfully registered. Bot id = b569e438c685b70458e51907b40e51e5
25/12/2020 14:03:22 [INFO] Fetching new commands...
25/12/2020 14:03:22 [INFO] Fetched 0 new commands.
```

_Bot #2:_
```
C:\app>python bot_master.py 349ab29asxtabw423bva5hca5623bc39b8c8
25/12/2020 15:06:29 [INFO] Registering the bot...
25/12/2020 15:06:30 [INFO] Successfully registered. Bot id = 198a0a574b6b3e0c6a89753a853c4e6d
25/12/2020 15:06:30 [INFO] Fetching new commands...
25/12/2020 15:06:30 [INFO] Fetched 0 new commands.
```

___2. Run bot master and check the list of registered bots:___
```
username@hostname:~/$ python3 bot_master.py 349ab29asxtabw423bva5hca5623bc39b8c8
[None]: bots
[None]: {'id': '198a0a574b6b3e0c6a89753a853c4e6d', 'registered': '2020-12-25T14:06:31Z', 'updated': '2020-12-25T14:06:32Z'}
[None]: {'id': 'b569e438c685b70458e51907b40e51e5', 'registered': '2020-12-25T14:03:21Z', 'updated': '2020-12-25T14:03:22Z'}
```
___3. Send commands to bots:___

_select a bot:_
```
[None]: select 198a0a574b6b3e0c6a89753a853c4e6d
[b569e438c685b70458e51907b40e51e5]: Selected b569e438c685b70458e51907b40e51e5
```

_info:_
```
[b569e438c685b70458e51907b40e51e5]: info
[b569e438c685b70458e51907b40e51e5]: ['Linux-4.12.0-1-amd64-x86_64-with-debian-10.5', 'hacker', ['192.168.8.21', '172.16.1.21']]
```

_send some commands:_
```
[b569e438c685b70458e51907b40e51e5]: cm ls /
[b569e438c685b70458e51907b40e51e5]: Sent command id: gASVDgAAAAAAAABdlCiMAmxzlIwBL5RlLg==
[b569e438c685b70458e51907b40e51e5]: cm ls /usr
[b569e438c685b70458e51907b40e51e5]: Sent command id: gASVEQAAAAAAAABdlCiMAmxzlIwEL3VzcpRlLg==
```

_get result of the last command:_
```
[b569e438c685b70458e51907b40e51e5]: last
[b569e438c685b70458e51907b40e51e5]:
['ls', '/usr']
['include', 'share', 'lib', 'src', 'local', 'games', 'bin', 'lib32', 'sbin']
```

_checking the command history:_
```
[b569e438c685b70458e51907b40e51e5]: history
[b569e438c685b70458e51907b40e51e5]: {'command_id': 'gASVDgAAAAAAAABdlCiMAmxzlIwBL5RlLg==', 'command': ['ls', '/']}
[b569e438c685b70458e51907b40e51e5]: {'command_id': 'gASVEQAAAAAAAABdlCiMAmxzlIwEL3VzcpRlLg==', 'command': ['ls', '/usr']}
```

_get result of the command from history:_
```
[b569e438c685b70458e51907b40e51e5]: result gASVDgAAAAAAAABdlCiMAmxzlIwBL5RlLg==
[b569e438c685b70458e51907b40e51e5]:
['ls', '/']
['dev', 'ClassData', 'opt', 'run', 'lib', 'sys', 'var', 'media', 'boot', 'mnt', 'srv', 'flag', 'etc', 'pro
c', 'TeamsData', '.dockerenv', 'bin', 'usr', 'home', 'lib32', 'sbin', 'lib64', 'root', 'tmp']
```

_select another bot and send commands:_
```
[b569e438c685b70458e51907b40e51e5]: select 198a0a574b6b3e0c6a89753a853c4e6d
[198a0a574b6b3e0c6a89753a853c4e6d]: Selected 198a0a574b6b3e0c6a89753a853c4e6d
[198a0a574b6b3e0c6a89753a853c4e6d]: cm ls D:/tmp
[198a0a574b6b3e0c6a89753a853c4e6d]: Sent command id: gASVEwAAAAAAAABdlCiMAmxzlIwGRDovdG1wlGUu
[198a0a574b6b3e0c6a89753a853c4e6d]: last
[198a0a574b6b3e0c6a89753a853c4e6d]:
['ls', 'D:/tmp']
['app.log']
```

_send a local file to bot:_
```
[198a0a574b6b3e0c6a89753a853c4e6d]: send /home/user/bot.py D:/tmp/bot.py
[198a0a574b6b3e0c6a89753a853c4e6d]: Uploading file content /home/user/bot.py
[198a0a574b6b3e0c6a89753a853c4e6d]: Successfully uploaded: file id = b17f883fa593eb2f8ac309c1094110bc
[198a0a574b6b3e0c6a89753a853c4e6d]: Sent command id: gASVPQAAAAAAAABdlCiMAmRklIwNRDovdG1wL2JvdC5weZSMIGIxN2Y4ODNmYTU5M2ViMmY4YWMzMDljMTA5NDExMGJjlGUu
[198a0a574b6b3e0c6a89753a853c4e6d]: last
[198a0a574b6b3e0c6a89753a853c4e6d]:
['dd', 'D:/tmp/bot.py', 'b17f883fa593eb2f8ac309c1094110bc']
Created: D:/tmp/bot.py
[198a0a574b6b3e0c6a89753a853c4e6d]: cm ls D:/tmp/
[198a0a574b6b3e0c6a89753a853c4e6d]: Sent command id: gASVFAAAAAAAAABdlCiMAmxzlIwHRDovdG1wL5RlLg==
[198a0a574b6b3e0c6a89753a853c4e6d]: last
[198a0a574b6b3e0c6a89753a853c4e6d]:
['ls', 'D:/tmp/']
['app.log', 'bot.py']
```

_change bot and execute OS command:_
```
[198a0a574b6b3e0c6a89753a853c4e6d]: select b569e438c685b70458e51907b40e51e5
[b569e438c685b70458e51907b40e51e5]: Selected b569e438c685b70458e51907b40e51e5
[b569e438c685b70458e51907b40e51e5]: cm exec ls -la
[b569e438c685b70458e51907b40e51e5]: Sent command id: gASVFwAAAAAAAABdlCiMBGV4ZWOUjAJsc5SMAy1sYZRlLg==
[b569e438c685b70458e51907b40e51e5]: last
[b569e438c685b70458e51907b40e51e5]:
['exec', 'ls', '-la']
total 40
drwxr-xr-x 3 username username 4096 Dec 25 14:03 .
drwxr-xr-x 3 username username 4096 Dec 25 14:02 ..
-rw-r--r-- 1 username username    7 Dec 25 13:36 README.md
-rw-r--r-- 1 username username 4791 Dec 25 13:36 bot.py
-rw-r--r-- 1 username username 6187 Dec 25 13:36 bot_master.py
-rw-r--r-- 1 username username 1532 Dec 25 13:36 gist.py
-rw-r--r-- 1 username username 1572 Dec 25 13:36 util.py
```

## Additional info:

* registered bot is represented as a gist with description "bot"
* command is represented as a gist-file
* result of the command is represented as a content of the gist-file
* file transfer implementation:
  * bot master creates a gist with description "data"
  * this data gist contains a single gist-file "data"
  * this data gist-file contains a base64 encoded content of the choosen file
  * bot decodes the gist-file content and saves to a target file
