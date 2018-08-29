from datetime import datetime, timedelta
import json

import pinhook.plugin


@pinhook.plugin.register('!botany')
def run(msg):
    who = msg.nick
    if msg.arg:
        nick = msg.arg
    else:
        nick = msg.nick
    try:
        with open('/home/{}/.botany/{}_plant_data.json'.format(nick, nick)) as plant_json:
            plant = json.load(plant_json)

        last_watered = datetime.utcfromtimestamp(plant['last_watered'])
        water_diff = datetime.now() - last_watered

        if plant['is_dead'] or water_diff.days >= 5:
            return pinhook.plugin.message('{}: {}\'s {} is dead. RIP'.format(who, nick, plant['description']))
        elif water_diff.days == 0:
            hours = str(round(water_diff.seconds / 3600))
            water_time = ''
            if hours == '0':
                water_time = str(round(water_diff.seconds / 60)) + ' minutes'
            elif hours == '1':
                water_time = '1 hour'
            else:
                water_time = hours + ' hours'
            msg = '{}: {}\'s {} was watered today! (About {} ago)'.format(
                who, nick, plant['description'], water_time)
            return pinhook.plugin.message(msg)
        elif 1 <= water_diff.days:
            days = str(water_diff.days)
            w_days = ''
            if days == '1':
                w_days = '1 day'
            else:
                w_days = days + ' days'
            hours = str(round(water_diff.seconds / 3600))
            w_hours = ''
            if hours == '1':
                w_hours = '1 hour'
            else:
                w_hours = hours + ' hours'
            msg = "{}: {}'s {} hasn't been watered today! (Last watered about {} and {} ago)".format(
                who, nick, plant['description'], w_days, w_hours)
            return pinhook.plugin.message(msg)
    except FileNotFoundError:
        return pinhook.plugin.message('{}: Are you sure {} has a plant in our beautiful garden?'.format(who, nick))
