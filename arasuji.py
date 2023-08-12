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
language = "en"
endEp = 5
resul = ""

translator = Translator()


driver = webdriver.Chrome()
# 新規タブを開く。
driver.execute_script("window.open()")
# 新規タブに移動する。
driver.switch_to.window(driver.window_handles[-1])

# kijiにアクセスする。
url = "https://ddnavi.com/serial/1077934/a/"

def openURL(url, language, endEp):
   # kijiにアクセスする。
    driver.get(url)
    # 10秒間待機し、ブラウザを閉じる。
    time.sleep(3)
    save(driver, language, endEp)

def save(driver, language, endEp):

    txtList = driver.find_elements_by_class_name("article-body")
    title = txtList[0].find_elements_by_tag_name("h1")[0].text
    article = txtList[0].find_elements_by_tag_name("p")
    pattern = re.compile("[0-9a-zA-Zぁ-んァ-ヶｱ-ﾝﾞﾟ一-龠_]")


    fileName = title

    f = open('arasuji/txt/'+ fileName +'.txt', 'w', encoding='UTF-8')
    ja = open('arasuji/ja/ja_' + fileName + '.mp3', 'wb')
    je = open('arasuji/ja-en/ja-'+ language + '_' + fileName + '.mp3', 'wb')
    en = open('arasuji/en/'+ language + '_' + fileName + '.mp3', 'wb')

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
    
    pn = 1
    pne = len(article)
    for i in article:
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

        i += 1
    # 保存
    print(fileName + " downloaded" )
    try:        
        resul = resul + fileName + " downloaded \n"
        label_4['text'] = resul
    except:
        print("error")
        resul = fileName + " downloaded \n"
        label_4['text'] = resul

    url = driver.find_elements_by_class_name("next")[0].get_attribute("href")
    if int(l) < int(endEp):
        l = int(l) + 1
        openURL(url, l, endEp)


if __name__ == '__main__':
 
    root = Tk() # この下に画面構成を記述
    
    # ----------- ①Window作成 ----------- #
    root.title('あらすじダウンローダー')   # 画面タイトル設定
    root.geometry('500x800')       # 画面サイズ設定
    root.resizable(False, False)   # リサイズ不可に設定

    frame1 = Frame(root, width=500, height=500, borderwidth=2, relief='solid')
    frame1.propagate(False)
    frame1.grid(row=0, column=0)

    # テキストボックス（フレーム2右上）
    label_1 = Label(frame1, text="開始URL：", font=('System', 11))
    entry_1 = Entry(frame1, width=20)
    entry_1.insert(0, "https://ddnavi.com/serial/1151932/a/")
    label_2 = Label(frame1, text="言語：", font=('System', 11))
    entry_2 = Entry(frame1, width=5)
    entry_2.insert(0, "en")
    label_3 = Label(frame1, text="保存話数：", font=('System', 11))
    entry_3 = Entry(frame1, width=5)
    entry_3.insert(0, "5")
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
