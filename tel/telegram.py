from datetime import datetime
import re
from srt.srt import *
import telegram
from telegram import *
from telegram.ext import *
import os
# import schedule

class Telegram():
    def __init__(self):
        self.this_year = "%04d" % (datetime.today().year)
        self.p = re.compile(r'(\w+)\s+(\w+)\s+(\d\d\d\d)\s+(\d\d)')
        self.token = #set your token
        self.chat_id = # set your id
        self.bot = telegram.Bot(self.token)
        self.only_one_chrome = 0
        self.trying = 0
        self.loop_cnt = 0
        self.last_info_time = 0
        self.option_status = 0
        self.target_options = [
            [InlineKeyboardButton("~1행", callback_data='t_1'),
             InlineKeyboardButton("~2행", callback_data='t_2'),
             InlineKeyboardButton("~3행", callback_data='t_3'),
             InlineKeyboardButton("~4행", callback_data='t_4'),
             InlineKeyboardButton("~5행", callback_data='t_5'),
             InlineKeyboardButton("~6행", callback_data='t_6'),
             InlineKeyboardButton("무한", callback_data='t_99')]
        ]
        self.class_type_options = [
            [InlineKeyboardButton("특실+일반실", callback_data='c_2'),
             InlineKeyboardButton("특실", callback_data='c_1'),
             InlineKeyboardButton("일반실", callback_data='c_0')]
        ]
        self.startrow_options = [
            [InlineKeyboardButton("1행", callback_data='i_1'),
             InlineKeyboardButton("2행", callback_data='i_2'),
             InlineKeyboardButton("3행", callback_data='i_3')]
        ]
        self.start_time_options = [
            [InlineKeyboardButton("지금", callback_data='s_1'),
             InlineKeyboardButton("03:00AM", callback_data='s_0')]
        ]

        # self.bot.sendMessage(self.chat_id, 'SRT Macro 구동중\n- 사용가능한 메뉴\n    "시작",  "종료",  "스샷",  "옵션"')
        self.bot.sendMessage(self.chat_id, '-- SRT Macro 구동중 --')
        self.bot.sendMessage(self.chat_id, '시작행을 선택하세요', reply_markup=InlineKeyboardMarkup(self.startrow_options))
        self.bot.sendMessage(self.chat_id, '마지막행을 선택하세요', reply_markup=InlineKeyboardMarkup(self.target_options))
        self.bot.sendMessage(self.chat_id, '객실타입을 선택하세요', reply_markup=InlineKeyboardMarkup(self.class_type_options))
        self.bot.sendMessage(self.chat_id, '시작시간을 선택하세요', reply_markup=InlineKeyboardMarkup(self.start_time_options))
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.srt = Srt()
        # cmd_handler = CommandHandler('cmd_name', func_name)
        self.msg_handler = MessageHandler(Filters.text & (~Filters.command), self.telegraming)
        self.dispatcher.add_handler(self.msg_handler)
        self.dispatcher.add_handler(CallbackQueryHandler(self.callback_get, pattern=r"^\w_"))
        self.updater.start_polling()



    def get_token():
        return '1828911985:AAGJDTwawT7rgaUslKNhrA4EyBhdj8wTz_k'

    def callback_get(self, update, context):
        txt = update.callback_query.data
        tx = txt[2:]
        if "t_" in txt:
            self.bot.edit_message_text(text=f"마지막행을 시작행으로부터 {tx}행으로 설정하였습니다.",
                                       chat_id=update.callback_query.message.chat_id,
                                       message_id=update.callback_query.message.message_id)
            self.srt.target_len = int(tx)
            self.option_status += 1
        elif "c_" in txt:
            self.bot.edit_message_text(text=f"객실타입을 {self.srt.class_type_txt[tx]}로 설정하였습니다.",
                                       chat_id=update.callback_query.message.chat_id,
                                       message_id=update.callback_query.message.message_id)
            self.srt.VIP = tx
            self.option_status += 1
        elif "i_" in txt:
            self.bot.edit_message_text(text=f"시작행을 {tx}행으로 설정하였습니다.",
                                       chat_id=update.callback_query.message.chat_id,
                                       message_id=update.callback_query.message.message_id)
            self.srt.interval = int(tx)
            self.option_status += 1
        elif "s_" in txt:
            self.bot.edit_message_text(text=f"시작시간을 {self.srt.start_time_txt[tx]}로 설정하였습니다.",
                                       chat_id=update.callback_query.message.chat_id,
                                       message_id=update.callback_query.message.message_id)
            self.srt.start_now = int(tx)
            self.option_status += 1

        if self.option_status == 4:
            if self.only_one_chrome == 0:
                self.only_one_chrome = 1
                self.bot.sendMessage(self.chat_id, '\n출발 도착 날짜 시간 을 입력하세요.(포맷준수)\nex) 동탄 김천 0305 18")')
                self.srt.start(self.chat_id, self.srt.srt_home)
            else:
                update.message.reply_text('이미 실행중입니다.\n출발 도착 날짜 시간 을 입력하세요.(포맷준수)\nex) 동탄 김천 0305 18')
                return 0



    def screenshot(self, str):
        self.bot.sendMessage(self.chat_id, str)
        self.srt.screenshot()
        photo = open("tmp_srt.png", 'rb')
        self.bot.sendPhoto(self.chat_id, photo)
        while self.trying & (self.up_id == self.updater.last_update_id - 1):
            self.try_loop()

    def telegraming(self, update, context):
        self.up_id = update.update_id
        self.chat_id = update.effective_chat.id
        self.m = update.message.text
        self.content_type = 'text'

        if self.content_type != 'text':
            self.bot.sendMessage(self.chat_id, "텍스트만 인식가능합니다.")

        if self.m == "시작":
            if self.only_one_chrome == 0:
                self.only_one_chrome = 1
                update.message.reply_text('SRT 매크로가 실행되었습니다.\n출발 도착 날짜 시간 을 입력하세요.(포맷준수)\nex) 동탄 김천 0305 18")')
                self.srt.start(self.chat_id, self.srt.srt_home)
            else:
                update.message.reply_text('이미 실행중입니다.\n출발 도착 날짜 시간 을 입력하세요.(포맷준수)\nex) 동탄 김천 0305 18')
                return 0
        elif self.m == "재시작":
            if self.only_one_chrome:
                update.message.reply_text('SRT 매크로가 재실행되었습니다.\n출발 도착 날짜 시간 을 입력하세요.(포맷준수)\nex) 동탄 김천 0305 18")')
                self.srt.restart(self.srt.srt_home)
            else:
                self.only_one_chrome = 1
                update.message.reply_text('SRT 매크로가 실행되었습니다.\n출발 도착 날짜 시간 을 입력하세요.(포맷준수)\nex) 동탄 김천 0305 18")')
                self.srt.start(self.chat_id, self.srt.srt_home)
        elif self.m == "종료":
            update.message.reply_text('SRT 매크로를 종료합니다.')
            self.srt.close()
            os._exit(0)
        elif self.m == "exit":
            update.message.reply_text('pc를 종료합니다.')
            # self.srt.close()
            # os._exit(0)
            os.system('C:/Users/seungmin/Desktop/shutdown.bat')
        elif self.m == "스샷":
            self.screenshot("스크린샷을 전송합니다.")
        elif self.m == "옵션":
            update.message.reply_text('시작행을 선택하세요', reply_markup=InlineKeyboardMarkup(self.startrow_options))
            update.message.reply_text('마지막행을 선택하세요', reply_markup=InlineKeyboardMarkup(self.target_options))
            update.message.reply_text('객실타입을 선택하세요', reply_markup=InlineKeyboardMarkup(self.class_type_options))
            update.message.reply_text('시작시간을 선택하세요', reply_markup=InlineKeyboardMarkup(self.start_time_options))

        elif self.p.fullmatch(self.m):
            self.trying = 1
            if re.fullmatch("\d\d\d\d", self.p.search(self.m).group(3)) == None:
                update.message.reply_text('날짜를 0305와 같이 포맷에 맞게 입력해주세요.\nex) 동탄 김천 0305 18')
                return 0
            self.dep_date = self.this_year + self.p.search(self.m).group(3)

            if int(self.p.search(self.m).group(4)) > 23:
                self.bot.sendMessage(self.chat_id, "출발시간은 24시를 넘을 수 없습니다. 출발시간을 정확하게 입력해주세요.\nex) 동탄 김천 0305 18")
                return 0
            self.dep_time = int(int(self.p.search(self.m).group(4)) / 2)
            input_time = int(self.p.search(self.m).group(4))
            self.dep_time = input_time+1 if (input_time % 2 != 0) else input_time
            self.dep_time = "%02d" % self.dep_time + '0000'

            self.dep = self.p.search(self.m).group(1)
            self.des = self.p.search(self.m).group(2)
            if self.dep == self.des:
                self.bot.sendMessage(self.chat_id, "출발지와 목적지가 동일합니다.다시 입력해주세요.\nex) 동탄 김천 0305 18")
                return 0

            self.start_time = int(datetime.now().strftime("%H%M"))
            self.last_info_time = self.start_time
            self.srt.get_info(self.dep_date, self.dep_time, self.dep, self.des)
            self.srt.select_menu()
            self.srt.print_info()
            while self.up_id == self.updater.last_update_id -1:
                self.try_loop()
        else:
            self.bot.sendMessage(self.chat_id, "포맷에 맞게 입력해주세요.\nex) 동탄 김천 0305 18")

    def msg_from_srt(self, msg='', img=1):
        self.bot = telegram.Bot(self.token)
        self.bot.sendMessage(self.chat_id, msg)
        if img:
            photo = open("tmp_srt.png", 'rb')
            self.bot.sendPhoto(self.chat_id, photo)

    def success(self):
        self.bot = telegram.Bot(self.token)
        photo = open("tmp_srt.png", 'rb')
        self.bot.sendPhoto(self.chat_id, photo)
        self.bot.sendMessage(self.chat_id, '{}, {}-{} 예매성공!\n매크로를 종료합니다.'.format(self.date, self.dep, self.des))
        self.close()
        os._exit(0)

    def try_loop(self):
        self.srt.trying()
        self.loop_cnt = self.loop_cnt + 1
        self.now_time = int(datetime.now().strftime("%H%M"))
        self.t_delta = (self.now_time - self.start_time) % (20)
        start_hour = str(self.start_time)[:-2]
        start_min = str(self.start_time)[-2:]
        print(f"{self.now_time}: {start_hour}:{start_min}에 시작하여 {self.loop_cnt}회 반복중, 좌석이 모두 매진이라 반복시도중입니다.")
        if self.now_time != self.last_info_time:
            if (self.now_time - self.last_info_time) % 30 == 0:
                self.last_info_time = self.now_time
                self.screenshot(f"{start_hour}:{start_min}에 시작하여 {self.loop_cnt}회 반복중, 좌석이 모두 매진이라 반복시도중입니다.")

