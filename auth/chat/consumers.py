import asyncio
import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer

from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from auth_app.models import User

player = 0

import time
import math
width = 600
height = 300
hh = 80
ww = 10
racket_speed = 1

class racket:
    def __init__(self, y, side):
        self.h = hh
        self.w = ww
        self.y = y
        self.vy = 0
        self.side = side
        self.score = 0
    def serialize_racket(self):
        return {
            'y': self.y,
            'h': self.h,
            'w': self.w,
            'side': self.side,
            'score':self.score,
        }

class ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 10
        self.angl = 10
        self.speed = 0.6
        self.vx = math.cos(self.angl * math.pi / 180) * self.speed
        self.vy = math.sin(self.angl * math.pi / 180) * self.speed
    def serialize_ball(self):
        return{
            'x':self.x,
            'y':self.y,
            'r':self.r,
        }

class   pingpong:
    def __init__(self):
        self.racket1 = racket(100, 'RIGHT')
        self.racket2 = racket(100, 'LEFT')
        self.b = ball(width / 2, height / 2)
    def move(self):
        if (self.b.x + self.b.r < 0):
            self.racket1.score += 1
            self.b.x = width / 2
            self.b.y = height / 2
            # time.sleep(2)
        if (self.b.x - self.b.r > width):
            self.racket2.score += 1
            self.b.x = width / 2
            self.b.y = height / 2
            # time.sleep(2)
        if (self.b.vx > 0):
            if ((self.b.x + self.b.r) + self.b.vx < (width - ww)):
                self.b.x += self.b.vx
            else:
                if ((self.b.y) < self.racket1.y or self.b.y >self.racket1.y + hh):
                    self.b.x += self.b.vx
                else:
                    self.b.x += (width - ww) - (self.b.x + self.b.r)
                    self.b.vx = -self.b.vx
        else:
            if (self.b.y < self.racket2.y or self.b.y >self.racket2.y + hh or (self.b.x - self.b.r) + self.b.vx > ww):
                self.b.x += self.b.vx
            else:
                self.b.x = ww + self.b.r
                self.b.vx = -self.b.vx
        if (self.b.vy > 0):
            if (self.b.y + self.b.r + self.b.vy < (height - 0)):
                self.b.y += self.b.vy
            else:
                self.b.y = (height - 0) - self.b.r
                self.b.vy = -self.b.vy
        else:
            if ((self.b.y - self.b.r) + self.b.vy > 0):
                self.b.y += self.b.vy
            else:
                self.b.y = self.b.r + 0
                self.b.vy = -self.b.vy
        if (self.racket1.y + self.racket1.vy > 0 and self.racket1.y + self.racket1.vy < (height - hh)):
            self.racket1.y += self.racket1.vy
        if (self.racket2.y + self.racket2.vy > 0 and self.racket2.y + self.racket2.vy < (height - hh)):
            self.racket2.y += self.racket2.vy

def serialize_pingpong(o):
    return {
        'racket1': o.racket1.serialize_racket(),
        'racket2': o.racket2.serialize_racket(),
        'b':o.b.serialize_ball(),
    }

rooms = []
index = 0

class RacetCunsumer(AsyncWebsocketConsumer):
    async def connect(self):
        global player
        global index
        player += 1
        self.group_name = 'racet_group' + str(index)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        access_token = self.scope['query_string'].decode().split('=')[1]
        user = await sync_to_async(User.objects.get)(token_access=access_token)
        # print("user:", user.login,"--------->", user.is_available)
        self.index = index
        if (player == 1):
            self.side = 'RIGHT'
        elif (player == 2):
            self.side = 'LEFT'
            player = 0
            index += 1
            rooms.append(pingpong())
            asyncio.create_task(self.pingpong_state())

    async def receive(self, text_data):
        global rooms
        data = json.loads(text_data)
        # if (self.side == 'RIGHT'):
        #     if (data == 'Up'):
        #         rooms[self.index].racket1.vy = -racket_speed
        #     elif (data == 'Down'):
        #         rooms[self.index].racket1.vy = racket_speed
        #     elif (data == 'Stop'):
        #         rooms[self.index].racket1.vy = 0
        # elif (self.side == 'LEFT'):
        #     if (data == 'Up'):
        #         rooms[self.index].racket2.vy = -racket_speed
        #     elif (data == 'Down'):
        #         rooms[self.index].racket2.vy = racket_speed
        #     elif (data == 'Stop'):
        #         rooms[self.index].racket2.vy = 0
    
        if (data == 'w'):
            rooms[self.index].racket2.vy = -racket_speed
        elif (data == 's'):
            rooms[self.index].racket2.vy = racket_speed
        elif (data == 'Stop2'):
            rooms[self.index].racket2.vy = 0
        if (data == 'Up'):
            rooms[self.index].racket1.vy = -racket_speed
        elif (data == 'Down'):
            rooms[self.index].racket1.vy = racket_speed
        elif (data == 'Stop1'):
            rooms[self.index].racket1.vy = 0

    async def pingpong_state(self):
        global rooms
        while 1:
            rooms[self.index].move()
            # await self.channel_layer.group_send(self.group_name,
            await self.channel_layer.group_send(self.group_name,
                {
                    'type': 'send_info',
                    'pingpong':json.dumps(rooms[self.index], default=serialize_pingpong)
                })
            await asyncio.sleep(0.001)

    async def send_info(self, event):
        # print(self.index)
        await self.send(event['pingpong'])

    async def disconnect(self, close_code):
        print("---------disconnect-----------")
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

# from channels.generic.websocket import WebsocketConsumer

# class   join_game(WebsocketConsumer):
#     def connect(self):
#         print("hhhhhhhhhhhhhhhhh")
#         self.accept()
#         self.send("owwwwwwwwwwaaaa")