from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import platform
import sys
import time
import re

from googletrans import Translator
from gtts import gTTS
from tkinter import *

#必ず変更
startUrl = "https://novelpia.jp/viewer/51140"
startEp = 1
language = "en"
workUrl = "https://novelpia.jp/novel/2393"
endEpi = 100
resul = ""

id = "fa152008@bbt.ohmae.ac.jp"
pw = "novelpia_fa152008"

translator = Translator()
driver = webdriver.Chrome()

# 新規タブを開く。
driver.execute_script("window.open()")
# 新規タブに移動する。
driver.switch_to.window(driver.window_handles[-1])

# novelpiaにアクセスする。
driver.get(workUrl)

# 10秒間待機し、ブラウザを閉じる。
time.sleep(10)

driver.find_element_by_xpath("//div[@class='top-item-icon-wrapper']/div[1]").click()

time.sleep(3)

driver.find_element_by_id("novelpiaLogin").click()

time.sleep(3)

login_form = driver.find_element_by_id("login_box")

mail = login_form.find_element_by_name("email")
pwd = login_form.find_element_by_name("wd")

mail.clear
pwd.clear

mail.send_keys(id)
pwd.send_keys(pw)

mail.submit()

#login_form.find_element_by_xpath("//button").click()

time.sleep(5)

try:
  wait = WebDriverWait(driver, 30)
  wait.until(EC.alert_is_present())
  alert = driver.switch_to.alert
  print(alert.text)
  alert.accept()
except TimeoutException:
    print("アラートは発生しませんでした")
except Exception as e:
  print(e)

time.sleep(3)


# class kensaku
"""

indexList = driver.find_elements_by_class_name("ion-bookmark")
urlList = []
print(len(indexList))

for i in range(len(indexList)):
    urlList.append(indexList[i].get_attribute("id"))

print(urlList)

"""

def openURL(url, l, endEp):
   # kijiにアクセスする。
    driver.get(url)
    # 10秒間待機し、ブラウザを閉じる。
    time.sleep(3)
    save(driver, l, endEp)

def save(driver, l, endEp):

    title = driver.find_elements_by_class_name("cut_line_one")[1].text
    pattern = re.compile("[0-9a-zA-Zぁ-んァ-ヶｱ-ﾝﾞﾟ一-龠_]")


    if l > 999:
        fileName = 'ep'+ str(l) + '_' + title 
    elif l > 99:
        fileName = 'ep0'+ str(l) + '_' + title
    elif l > 9:
        fileName = 'ep00'+ str(l) + '_' + title
    else:
        fileName = 'ep000'+ str(l) + '_' + title


    f = open('pia/txt/'+ fileName +'.txt', 'w', encoding='UTF-8')
    ja = open('pia/ja/ja_' + fileName + '.mp3', 'wb')
    je = open('pia/ja-en/ja-'+ language + '_' + fileName + '.mp3', 'wb')
    en = open('pia/en/'+ language + '_' + fileName + '.mp3', 'wb')

    jaTxt = title
    f.write(jaTxt + "\n")
    jdg1 = pattern.search(jaTxt)
    if jdg1:
        enTxt = translator.translate(jaTxt,dest=language,src='ja').text
        f.write(enTxt + "\n")
        tts = gTTS(jaTxt, lang='ja')
        tts.write_to_fp(ja)
        tts.write_to_fp(je)
        time.sleep(3)
        tts = gTTS(enTxt, lang='en')
        tts.write_to_fp(en)
        tts.write_to_fp(je)
        time.sleep(3)
    
    # class kensaku
    txtList = driver.find_elements_by_class_name("line")
    pn = 1
    pne = len(txtList)
    for i in txtList:
        jaTxt = i.text
        # print(jaTxt)
        f.write(jaTxt + "\n")
        jdg1 = pattern.search(jaTxt)
        if jdg1:
            enTxt = translator.translate(jaTxt,dest=language,src='ja').text
            f.write(enTxt + "\n")
            for p in re.findall('[^。！？!?]+[。！？!?]?', jaTxt):
                jdg2 = pattern.search(p)
                #print(pattern.search(p))
                if jdg2:
                    #print(p)
                    tts = gTTS(p, lang='ja')
                    tts.write_to_fp(ja)
                    tts.write_to_fp(je)
                    time.sleep(3)
            for q in re.findall('[^.！？!?]+[.！？!?]?', enTxt):
                jdg3 = pattern.search(q)
                #print(pattern.search(q))
                if  jdg3:
                    #print(q)
                    tts = gTTS(q, lang='en')
                    tts.write_to_fp(en)
                    tts.write_to_fp(je)
                    time.sleep(3)
        print(F"\r\033[2K{pn/pne*100:.02f}% ({pn}/{pne})", end="")
        pn += 1

    try:        
        resul = resul + fileName + " downloaded \n"
        label_4['text'] = resul
    except:
        print("error")
        resul = fileName + " downloaded \n"
        label_4['text'] = resul

    # 保存
    print(fileName + " downloaded" )

    link = driver.find_element_by_id("next_epi_auto_url").get_attribute("value")
    if int(l) < int(endEp):
        url = "https://novelpia.jp" + link
        l = int(l) + 1
        openURL(url, l, endEp)


if __name__ == '__main__':
 
    root = Tk() # この下に画面構成を記述
    
    # ----------- ①Window作成 ----------- #
    root.title('ノベルピアダウンローダー')   # 画面タイトル設定
    root.geometry('500x800')       # 画面サイズ設定
    root.resizable(False, False)   # リサイズ不可に設定

    frame1 = Frame(root, width=500, height=500, borderwidth=2, relief='solid')
    frame1.propagate(False)
    frame1.grid(row=0, column=0)

    # テキストボックス（フレーム2右上）
    label_1 = Label(frame1, text="開始URL：", font=('System', 11))
    entry_1 = Entry(frame1, width=20)
    entry_1.insert(0, "https://novelpia.jp/viewer/118983")
    label_2 = Label(frame1, text="開始話数：", font=('System', 11))
    entry_2 = Entry(frame1, width=5)
    entry_2.insert(0, "232")
    label_3 = Label(frame1, text="終了話数：", font=('System', 11))
    entry_3 = Entry(frame1, width=5)
    entry_3.insert(0, "290")
    button_2b = Button(frame1, text='download', command=lambda: openURL(entry_1.get(), int(entry_2.get()), int(entry_3.get())))
    label_4 = Label(frame1, text=u"", font=('System', 11))
    label_1.grid(row=0, column=0)
    entry_1.grid(row=0, column=1, sticky = W+E)
    label_2.grid(row=1, column=0)
    entry_2.grid(row=1, column=1, sticky = W+E)
    label_3.grid(row=2, column=0)
    entry_3.grid(row=2, column=1, sticky = W+E)
    button_2b.grid(row=3, column=1)
    label_4.grid(row=4, column=0, columnspan = 2, sticky = W+E)
    root.mainloop()



# 10秒間待機し、ブラウザを閉じる。
time.sleep(10)
driver.quit()

