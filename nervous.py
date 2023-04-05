import sys
import time
from g_python.gextension import Extension
from g_python.hmessage import Direction

extension_info = {
    "title": "Nervous Bot",
    "description": ":nervcmd to see commands",
    "version": "0.1",
    "author": "Yarkin"
}

ext = Extension(extension_info, sys.argv, silent=True)
ext.start()

nervous = False
x = 0
y = 0
ms = 0.0


def coords(coord):
    global x, y, nervous
    if nervous:
        _, x, y, _ = coord.packet.read("iiii")
        ext.send_to_client('{in:Whisper}{i:-1}{s:"Coords set to: x: ' +str(x)+ ' y: '+str(y)+ '"}{i:0}{i:34}{i:0}{i:-1}')

def handitem(item):
    global x, y, nervous, ms
    if nervous:
        user, itemid = item.packet.read('ii')
        if itemid == 3:
            time.sleep(ms)
            ext.send_to_server('{out:MoveAvatar}{i:' + str(x) + '}{i:' + str(y) + '}')

def message(message):
    global nervous, ms
    (text, color, index) = message.packet.read('sii')
    if text.lower().startswith(':nervon'):
        message.is_blocked = True
        nervous = True
        ext.send_to_client('{in:Whisper}{i:-1}{s:"Nervous Bot is On"}{i:0}{i:34}{i:0}{i:-1}')

    elif text.lower().startswith(':nervoff'):
        message.is_blocked = True
        nervous = False
        ext.send_to_client('{in:Whisper}{i:-1}{s:"Nervous Bot is Off"}{i:0}{i:34}{i:0}{i:-1}')

    elif nervous and text.lower().startswith(':nms'):
        message.is_blocked = True
        words = text.split()
        try:
            ms = float(words[1])
        except ValueError:
            ext.send_to_client('{in:Whisper}{i:-1}{s:"Invalid delay time. Please use a number."}{i:0}{i:34}{i:0}{i:-1}')
            return
        if ms < 0:
            ext.send_to_client('{in:Whisper}{i:-1}{s:"Delay time must be greater than zero."}{i:0}{i:34}{i:0}{i:-1}')
            return
        ext.send_to_client('{in:Whisper}{i:-1}{s:"Delay time set to ' + str(ms) + ' seconds."}{i:0}{i:34}{i:0}{i:-1}')

    elif text.lower().startswith(':nervcmd'):
        message.is_blocked = True
        ext.send_to_client('{in:Whisper}{i:-1}{s:":nervon turns the bot on\n:nervoff turns the bot off\n:nms "number" to set delay\nPress "alt" and move the furni where you wanna walk"}{i:0}{i:34}{i:0}{i:-1}')

ext.intercept(Direction.TO_CLIENT, handitem, 'CarryObject', mode='async')
ext.intercept(Direction.TO_SERVER, message, 'Chat')
ext.intercept(Direction.TO_SERVER, coords, 'MoveObject')