import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from fake_useragent import UserAgent
from user_agent import generate_user_agent, generate_navigator
if __name__ != "__main__":
    from tel.telegram import *
else:
    import sys
    import re
    from datetime import datetime

class Srt():
    def __init__(self):
        self.srt_home = 'https://etk.srail.kr/main.do'
        self.payment_url = 'https://etk.srail.kr/hpg/hra/02/selectReservationList.do?pageId=TK0102010000'
        self.class_type_txt = {'2':"특실+일반실", '1':"특실", '0':"일반실"}
        self.start_time_txt = {'1': "지금바로", '0': "새벽3시"}
        self.class_type = {'2':[6,7], '1':[6], '0':[7]}
        self.station_dic = {'수서': 0, '동탄': 1, '평택지제': 2, '천안아산': 3, '오송': 4, '대전': 5, '김천구미': 6, '서대구': 7, '동대구': 8,
                            '신경주': 9, '울산': 10, '부산': 11, '공주': 12, '익산': 13, '정읍': 14, '광주송정': 15, '나주': 16, '목포': 17}
        self.id = #set your id
        self.pw = # set your pw
        self.card_info = #set your card info
        self.mobile = #set your phone number
        self.interval = 1
        self.start_row = 1
        self.target_len = 1
        self.start_now = 1
        self.VIP = '0'
        self.chat_id = '0'
        self.depature = ''
        self.seat_only = 1  # 좌석, 입석+좌석
        self.target_time = 0
        if __name__ != "__main__":
            self.token = Telegram.get_token()

    def waiting_click(self, click_xpath, txt=''):
        while 1:
            try:
                self.driver.find_element(By.XPATH, click_xpath).click()
                break
            except:
                time.sleep(0.3)
            finally:
                # print(f'waiting... {txt}')
                pass

    def start(self, chat_id, url):
        if self.start_now == 0:
            nowtime = int(datetime.now().strftime("%H%M"))
            while (nowtime > int("0425") or nowtime < int("0307")):
                nowtime = int(datetime.now().strftime("%H%M"))
                print(f"대기중.. {nowtime}")
                time.sleep(60)
        self.chat_id = chat_id
        options = Options()
        options.add_argument("--incognito") # 시크릿모드

        print(generate_user_agent(os=('win', 'mac'), device_type='desktop'))
        userAgent = generate_user_agent(os=('win', 'mac'), device_type='desktop')

        # userAgent = UserAgent(use_cache_server=True).random
        # print(re.findall('\(([\w\s\d\;\:\/\.\-]+)\)', userAgent)[0])
        options.add_argument(f'user-agent={userAgent}')  # fake_useragent로 옵션값 설정
        self.driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=options)
        self.driver.maximize_window()  # 크롬창 최대화
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="wrap"]/div[3]/div[1]/div/a[2]')))

        ## login
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//*[@id="wrap"]/div[3]/div[1]/div/a[2]').click()
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="srchDvNm01"]')))
        self.driver.find_element(By.XPATH, '//*[@id="srchDvNm01"]').send_keys(self.id)
        self.driver.find_element(By.XPATH, '//*[@id="hmpgPwdCphd01"]').send_keys(self.pw)
        self.driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[1]/div[1]/div[2]/div/div[2]/input').click()


    def close(self):
        self.driver.quit()

    def screenshot(self, slp=1):
        self.driver.save_screenshot("tmp_srt.png")
        time.sleep(int(slp))

    def get_info(self, dep_date, dep_time ,dep, des):
        self.date = dep_date
        self.time = dep_time[0:2]
        self.dep_time = dep_time
        self.target_time = dep_time
        # if self.dep_time % 2 == 1:
        #     self.dep_time -= 1
        self.dep = dep
        self.des = des

        for s in self.station_dic.keys():
            if dep in s:
                self.depature = self.station_dic[s] + 1
                self.dep = s
                break
        for s in self.station_dic.keys():
            if des in s:
                self.destination = self.station_dic[s] + 1
                self.des = s
                break

    def get_info_disabled_kr(self, dep_date, dep_time ,dep, des):
        self.date = dep_date
        self.time = dep_time[0:2]
        self.dep_time = dep_time
        self.dep = dep
        self.des = des

        self.depature = int(dep) + 1
        self.destination = int(des) + 1

    def select_menu(self):
        Select(self.driver.find_element(By.XPATH, '//*[@id="dptRsStnCd"]')).select_by_index(self.depature)
        Select(self.driver.find_element(By.XPATH, '//*[@id="arvRsStnCd"]')).select_by_index(self.destination)
        self.driver.find_element(By.XPATH, '//*[@id="search-form"]/fieldset/a').click()
        WebDriverWait(self.driver, 10).until(lambda driver: driver.current_url == "https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000")
        only_srt = self.driver.find_element(By.XPATH, '//*[@id="trnGpCd300"]').send_keys(Keys.SPACE)
        Select(self.driver.find_element(By.XPATH, '//*[@id="dptDt"]')).select_by_value(self.date)
        Select(self.driver.find_element(By.XPATH, '//*[@id="dptTm"]')).select_by_value(self.dep_time)
        search_btn = self.driver.find_element(By.XPATH, '//*[@id="search_top_tag"]/input').click()
        time.sleep(1)

    def print_info(self):
        self.screenshot(0)
        print(f"<{self.dep} => {self.des}>\n{self.date}, {self.time}시 이후 열차 시도중\
            \n타겟 라인 : ~{self.target_len}행\ninterval : {self.interval}~{self.interval+1}초\n객실타입 : {self.class_type_txt[self.VIP]}")
        try:
            Telegram.msg_from_srt(self, f"[{self.dep} => {self.des}]\n{self.date}, {self.time}시 이후 열차 시도중\
                \n타겟 라인 : ~{self.target_len}행\ninterval : {self.interval}~{self.interval+1}초\n객실타입 : {self.class_type_txt[self.VIP]}")
        except:
            pass

    def restart(self, url):
        self.close()
        time.sleep(2)
        self.start(self.chat_id, url)
        time.sleep(1)
        self.select_menu()
        while(1):
            self.trying()

    def fill_payment(self):
        self.waiting_click('// *[ @ id = "list-form"] / fieldset / div[11] / a[1] / span', '"결제하기" 버튼')
        # self.waiting_click('//*[@id="select-form"]/fieldset/div[2]/ul/li[1]/a', '신용카드')
        self.waiting_click('// *[ @ id = "stlCrCrdNo14_tk_btn"] / label', '보안키패드1')
        self.waiting_click('// *[ @ id = "vanPwd1_tk_btn"] / label', '보안키패드2')
        time.sleep(1)
        sel_mon = Select(self.driver.find_element(By.XPATH, '//*[@id="crdVlidTrm1M"]')).select_by_value(
            self.card_info["exp_month"])
        sel_year = Select(self.driver.find_element(By.XPATH, '//*[@id="crdVlidTrm1Y"]')).select_by_value(
            self.card_info["exp_year"])
        # self.waiting_click('// *[ @ id = "agree1"]', '동의 체크박스')
        self.waiting_click('// *[ @ id = "select-form"] / fieldset / div[11] / div[2] / ul / li[2] / a', '스마트폰 발권')
        self.driver.switch_to.alert.accept()
        time.sleep(5)
        for i in range(1, 5):
            self.driver.find_element(By.XPATH, f'// *[ @ id = "stlCrCrdNo1{i}"]').click()
            card_num = self.driver.find_element(By.XPATH, f'// *[ @ id = "stlCrCrdNo1{i}"]').send_keys(
                self.card_info["card_num"][i - 1])
            time.sleep(1)
        pw_box = self.driver.find_element(By.XPATH, '// *[ @ id = "vanPwd1"]').send_keys(self.card_info["pw"])
        verif_box = self.driver.find_element(By.XPATH, '//*[@id="athnVal1"]').send_keys( self.card_info['verif_code'])
        time.sleep(1)
        self.waiting_click('//*[@id="requestIssue1"]/span', "최종 결제 버튼")
        self.final_txt = self.driver.switch_to.alert.text
        self.driver.switch_to.alert.accept()

    def success_process(self):
        time.sleep(3)
        self.screenshot()
        if __name__ != "__main__":
            Telegram.success(self)
        time.sleep(30000)

    def trying(self):
        room_type = self.class_type[self.VIP]
        row_list = self.driver.find_elements(By.CSS_SELECTOR,
                                        '#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr')
        max_len = len(row_list)+1 if ((int(self.start_row)+int(self.target_len)-1) > len(row_list)) else int(self.start_row)+int(self.target_len)
        print(f"start_row : {self.start_row}, target : {self.target_len}, rowlist : {len(row_list)}, max_len : {max_len}, room_type : {room_type}")
        try:
            is_success = ''
            now_time = str(datetime.now().strftime("%H:%M"))
            for row in range(int(self.start_row), int(max_len)):
                if "예약하기" in is_success:
                    break
                for cl in range(0, len(room_type)):
                    print(f"  for loop : row:{row}, cl:{room_type[cl]}, ({now_time})")
                    if "예약하기" in is_success:
                        next
                    try:
                        if (self.seat_only):
                            # print(f"row:{row}, cl:{room_type[cl]}, ")
                            # departure_time = self.driver.find_element(
                            #     By.XPATH,
                            #     f'//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[{row}]/td[4]/em').text
                            # if int(departure_time[0:2]) < self.target_time:
                            #     print(f"deptime{departure_time[0:2]} is low target{str(self.target_time)}")
                            #     sleep(3)
                            #     next
                            remain_seat_type = self.driver.find_element(
                                By.XPATH, f'//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[{row}]/td[{room_type[cl]}]/a').text
                            print(f"  버튼명 : {remain_seat_type}")
                            if ('입석' in remain_seat_type):
                                next
                            elif ('예약하기' in remain_seat_type or '신청하기' in remain_seat_type):
                                self.driver.find_element(
                                    By.XPATH,
                                    '//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[{}]/td[{}]/a'.format(row,
                                                                                                                room_type[
                                                                                                                    cl])).click()
                        else:
                            self.driver.find_element(
                                By.XPATH, '//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[{}]/td[{}]/a'.format(row, room_type[cl])).click()
                        is_available_reserve_btn = self.driver.find_element(
                            By.CSS_SELECTOR, f'#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({row}) > td:nth-child(8)').text
                        # if ('-' not in is_available_reserve_btn):
                        if ('신청하기' in is_available_reserve_btn):
                            self.driver.find_element(
                                By.XPATH, '//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[{}]/td[{}]/a'.format( row, 8)).click()
                            is_success = self.driver.find_element(By.XPATH, '//*[@id="wrap"]/div[4]/div/div[1]/h2').text
                            print("  예약대기 성공!")
                    except:
                        is_success = self.driver.find_element(By.XPATH, '//*[@id="wrap"]/div[4]/div/div[1]/h2').text
                        if "예약하기" in is_success:
                            print("  예약하기 클릭 성공!")
                            break
        except:
            pass


        if "예약하기" in is_success:
            try:
                sold_out = self.driver.find_element(By.XPATH, '// *[ @ id = "wrap"] / div[4] / div / div[2] / div[5]').text
                if "잔여석없음" in sold_out:
                    print(f'{sold_out} 으로 다시 홈페이지가서 새로고침(is_success : {is_success}')
                    self.driver.get(self.srt_home)
                    self.select_menu()
                    self.driver.refresh()
                    if __name__ != "__main__":
                        Telegram.msg_from_srt(self, f"errmsg : {sold_out}\n새로고침합니다.")
                    time.sleep(2)
                else:
                    print("< 예매 성공 >")
                    if __name__ != "__main__":
                        self.screenshot(1)
                        Telegram.msg_from_srt(self, f"예매성공!\n결제중..", 0)
                    time.sleep(2)
                    try:  # 예약대기팝업
                        self.driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/button').click()
                        print("예약대기 팝업 떠서 클릭함")
                    except:
                        pass
            except:
                print("soldout html 못찾음")

            try:
                time.sleep(3)
                info_text = self.driver.find_element(By.XPATH, '//*[@id="wrap"]/div[4]/div/div[2]/div[4]').text
                print(f'info_text : {info_text}')
                if "예약대기" in info_text:
                    self.waiting_click('//*[@id="agree"]', "개인정보수집동의")
                    self.waiting_click('//*[@id="smsY"]', "SMS동의")
                    time.sleep(1)
                    self.driver.switch_to.alert.accept()
                    self.driver.find_element(By.XPATH, '//*[@id="phoneNum1"]').send_keys(self.mobile[0])
                    self.driver.find_element(By.XPATH, '//*[@id="phoneNum2"]').send_keys(self.mobile[1])
                    self.waiting_click('//*[@id="diffSeatY"]', "다른차실 동의")
                    time.sleep(1)
                    self.waiting_click('//*[@id="moveTicketList"]', "확인")
                    self.driver.switch_to.alert.accept()
                    self.success_process()
                elif "10분 내에 결제하지" in info_text:
                    self.fill_payment()
                    while "카드번호" in self.final_txt:
                        if __name__ != "__main__":
                            Telegram.msg_from_srt(self, f"카드번호 입력불가로 재결제 시도합니다.")
                        self.restart(self.payment_url)
                        WebDriverWait(self.driver, 10).until(
                            ec.presence_of_element_located((By.XPATH, '//*[@id="reserveTbl"]/tbody/tr[1]/td[10]/a')))
                        self.driver.find_element(By.XPATH, '//*[@id="reserveTbl"]/tbody/tr[1]/td[10]/a').click()
                        self.fill_payment()
                    else:
                        self.success_process()
            except:
                pass

        ran_time = float(str(random.randint(self.interval, self.interval+1)) + '.' + str(random.randint(1, 3)))
        time.sleep(ran_time)
        self.driver.refresh()
        time.sleep(0.5)
        if self.start_now == 0:
            nowtime = int(datetime.now().strftime("%H%M"))
            if (nowtime > int("0425")):
                print(f"{nowtime} : 새벽 매크로를 정지합니다... ")
                time.sleep(60000)

if __name__ == "__main__":
    s = Srt()
    date = str(sys.argv[1])
    deptime = str(sys.argv[2])
    dep = str(sys.argv[3])
    des = str(sys.argv[4])
    s.start_row = str(sys.argv[5])
    s.target_len = str(sys.argv[6])
    s.interval = 1
    s.VIP = "0"  #'2':"특실+일반실", '1':"특실", '0':"일반실"
    s.start_now = 0
    # self.station_dic = {'수서': 0, '동탄': 1, '평택지제': 2, '천안아산': 3, '오송': 4, '대전': 5, '김천구미': 6, '서대구': 7, '동대구': 8,
    #                     '신경주': 9, '울산': 10, '부산': 11, '공주': 12, '익산': 13, '정읍': 14, '광주송정': 15, '나주': 16, '목포': 17}


    s.start("undef", s.srt_home)
    print(date, s.target_len)
    s.get_info_disabled_kr(date, deptime, dep, des)
    s.select_menu()
    # s.print_info()
    while (1):
        s.trying()


# setInterval(function() {
#     var ifrm = document.getElementById('sub_frame1').contentWindow.document.getElementById('bodyf').contentWindow.document;
#     var timer = ifrm.getElementsByClassName('timer')[0].textContent;
#     var ti_min = timer.substr(0,2);
#     var ti_sec = timer.substr(3,2);
#     var timer_total = ifrm.getElementsByClassName('timertotal')[0].textContent;
#     var to_min = timer_total.substr(0,2);
#     var to_sec = timer_total.substr(3,2);
#     ti_sum = ti_min*60 + ti_sec;
#     to_sum = to_min*60 + to_sec;
#     if (ti_sum == to_sum) {
#         console.log(ti_sum, to_sum);
#         console.log(ifrm.getElementsByClassName('selected')[1]);
#         ifrm.getElementsByClassName('selected')[1].click();
#     }
#     else {
#         console.log("waiting", ti_sum, to_sum);
#     }
# }, 5000);
#
# setInterval(function() {
#     var ifrm = document.getElementById('sub_frame1').contentWindow.document.getElementById('bodyf').contentWindow.document;
#     var timer = ifrm.getElementsByClassName('curTime')[0].textContent;
#     var ti_min = timer.substr(0,2);
#     var ti_sec = timer.substr(3,2);
#     var timer_total = ifrm.getElementsByClassName('totalTime')[0].textContent;
#     var to_min = timer_total.substr(0,2);
#     var to_sec = timer_total.substr(3,2);
#     ti_sum = ti_min*60 + ti_sec;
#     to_sum = to_min*60 + to_sec;
#     if (ti_sum == to_sum) {
#         console.log(ti_sum, to_sum);
#         console.log(ifrm.getElementsByClassName('nextBtn')[0]);
#         ifrm.getElementsByClassName('nextBtn')[0].click();
#     }
#     else {
#         console.log("waiting", ti_sum, to_sum);
#     }
# }, 5000);

# setInterval(function() {
#     var ifrm = document.getElementById('sub_frame1').contentWindow.document.getElementById('bodyf').contentWindow.document;
#     var timer = ifrm.getElementsByClassName('button digClock curTime')[0].textContent;
#     var ti_min = timer.substr(0,2);
#     var ti_sec = timer.substr(3,2);
#     var timer_total = ifrm.getElementsByClassName('button digClock totalTime')[0].textContent;
#     var to_min = timer_total.substr(0,2);
#     var to_sec = timer_total.substr(3,2);
#     ti_sum = ti_min*60 + ti_sec;
#     to_sum = to_min*60 + to_sec;
#     if (ti_sum == to_sum) {
#         console.log(ti_sum, to_sum);
#         console.log(ifrm.getElementsByClassName('button moveNext')[0]);
#         ifrm.getElementsByClassName('button moveNext')[0].click();
#     }
#     else {
#         console.log("waiting", ti_sum, to_sum);
#     }
# }, 5000);