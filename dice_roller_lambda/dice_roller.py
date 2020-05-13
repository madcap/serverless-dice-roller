import re
import random
import json

DICE_ROLL_PATTERN = re.compile("^[0-9]*d[0-9]+")
MAX = 512


def invalid_dice_roll(message):
    return {
        'statusCode': 400,
        'headers': {
            "Access-Control-Allow-Origin": "*"
        },
        'body': message
    }


def lambda_handler(event, context):
    
    if 'queryStringParameters' not in event:
        return invalid_dice_roll('event format not recognized')
    
    if 'diceRoll' not in event['queryStringParameters']:
        return invalid_dice_roll('diceRoll not defined')

    dice_roll = event['queryStringParameters']['diceRoll']

    if not isinstance(dice_roll, str):
        return invalid_dice_roll('diceRoll is not a string')

    dice_roll = dice_roll.lower()

    if not DICE_ROLL_PATTERN.match(dice_roll):
        return invalid_dice_roll('diceRoll does not match <COUNT>d<SIDES> or d<SIDES>')

    split = dice_roll.split('d')
    if split[0] == '':
        split[0] = '1'

    count = int(split[0])
    sides = int(split[1])

    if count < 1 or sides < 1:
        return invalid_dice_roll('COUNT and SIDES must be 1 or more')

    if count > 512 or sides > 512:
        return invalid_dice_roll('COUNT and SIDES cannot exceed 512')

    result = {
        'roll': {
            'sides': sides,
            'count': count,
        },
        'total': 0,
        'rolls': [],
    }
    total = 0

    for i in range(count):
        roll = random.randint(1, sides)
        total = total + roll
        result['rolls'].append(roll)

    result['total'] = total

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps(result)
    }
