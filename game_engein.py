from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton
from random import choice


class Pixelway:
    doc = {0:'⬜️', 1:'⬛️', 2:'🟥', 3:'🟧', 4:'🟪' , 5:'🟦', 6:'🟩', 7:'🟨'}
    kdoc = { '🔼':'up', '🔽':'down', '◀️':'left', "✖️":'push','▶️':'right'}

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.img = []
        self.dct = {}
        self._keys = None
        self.x, self.y = self.h-1, self.w-1
        self.head = '...'
        self.inv = 0
        self.win = 0

    def mover(f):
        def wrp(cls):
            x,y = cls.x, cls.y
            f(cls)
            if (x,y) == (cls.x,cls.y):
                cls.inv += 1
                cls.heat = 'invalid move' + ( '.' *cls.inv )
            elif cls.x == 0 and cls.y == 0: cls.win = 1
            else: cls.head = '...'
        return wrp

    @mover
    def up(self):
        x,y = self.x, self.y
        if self.dct.get((x-1,y)):
            if self.img[x-1][y] != 1:
                self.img[x][y], self.img[x-1][y] = self.img[x-1][y], self.img[x][y]
            if self.img[x-1][y] == 1:
                if self.dct.get((x-2,y)) and self.img[x-2][y] != 1:
                    self.img[x][y], self.img[x-1][y], self.img[x-2][y] = self.img[x-2][y], self.img[x][y], self.img[x-1][y]
                else:
                    return
            self.x = x-1


    @mover
    def down(self):
        x,y = self.x, self.y
        if self.dct.get((x+1,y)):
            if self.img[x+1][y] != 1:
                self.img[x][y], self.img[x+1][y] = self.img[x+1][y], self.img[x][y]
            if self.img[x+1][y] == 1:
                if self.dct.get((x+2,y)) and self.img[x+2][y] != 1:
                    self.img[x][y], self.img[x+1][y],self.img[x+2][y] = self.img[x+2][y], self.img[x][y], self.img[x+1][y]
                else:
                    return
            self.x = x+1


    @mover
    def left(self):
        x,y = self.x, self.y
        if self.dct.get((x,y-1)):
            if self.img[x][y-1] != 1:
                self.img[x][y], self.img[x][y-1] = self.img[x][y-1], self.img[x][y]
            if self.img[x][y-1] == 1:
                if self.dct.get((x,y-2)) and self.img[x][y-2] != 1:
                    self.img[x][y], self.img[x][y-1],self.img[x][y-2] = self.img[x][y-2], self.img[x][y], self.img[x][y-1]
                else:
                    return
            self.y = y-1


    @mover
    def right(self):
        x,y = self.x, self.y
        if self.dct.get((x,y+1)):
            if self.img[x][y+1] != 1:
                self.img[x][y], self.img[x][y+1] = self.img[x][y+1], self.img[x][y]
            if self.img[x][y+1] == 1:
                if self.dct.get((x,y+2)) and self.img[x][y+2] != 1:
                    self.img[x][y], self.img[x][y+1],self.img[x][y+2] = self.img[x][y+2], self.img[x][y], self.img[x][y+1]
                else:
                    return
            self.y = y+1


    def gen(self):
        self.img = []
        self.x, self.y = self.h-1, self.w-1
        for x in range(self.h):
            tmp = []
            for y in range(self.w):
                elm = choice([1,0,0,1,0,1,0,0,1])
                tmp += [elm]
                self.dct[(x,y)] = 1 #elm
            self.img.append(tmp)
        self.img[self.x][self.y] = 6
        self.img[0][0],self.img[0][1], self.img[1][0] = 7 ,0, 0
        self.img[self.x//2][self.y//2] = 0


    def keys(self):
        markup = InlineKeyboardMarkup(row_width=2)
        kbox = []
        empt = InlineKeyboardButton(' ', callback_data=' ')
        refr = InlineKeyboardButton('🔄', callback_data='refr')
        for k,v in self.kdoc.items():
            kbox.append(InlineKeyboardButton(k, callback_data=v))
        markup.row(refr, kbox[0], empt)
        markup.row(*kbox[2:])
        markup.row(empt, kbox[1], empt)
        self._keys = markup


    def refr(self):
        self.gen()


    @property
    def text(self):
        if self.win:
            self.win = 0
            self.gen()
            print('winnnnn')
            return 'cool you win......!!!!!'
        return   self.head + '\n' + '\n'.join(''.join(self.doc.get(x) for x in e) for e in self.img)