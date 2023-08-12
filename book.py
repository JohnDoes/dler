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


#毎回変更する
#記録：　7/6 ~10
start = 11
end = 50
language = "en"

translator = Translator()

driver = webdriver.Chrome()
# 新規タブを開く。
driver.execute_script("window.open()")
# 新規タブに移動する。
driver.switch_to.window(driver.window_handles[-1])

def openURL(language, start, end):
    pattern = re.compile("[0-9a-zA-Zぁ-んァ-ヶｱ-ﾝﾞﾟ一-龠_]")

    i = start
    while i < end+1:
        # kijiにアクセスする。
        driver.get("https://www.sinkan.jp/news/" + str(i) + "?page=1")
        # 10秒間待機し、ブラウザを閉じる。
        time.sleep(5)

        errorList = []
        errorList = driver.find_elements_by_class_name("error-page")

        if len(errorList) != 0:
            i += 1
        else:
            # class kensaku
            txtList = driver.find_elements_by_class_name("article")

            fileName = driver.find_elements_by_class_name("article-title")[0].text

            tx = open('book/txt/'+ fileName +'.txt', 'w', encoding='UTF-8')
            ja = open('book/ja/ja_' + fileName + '.mp3', 'wb')
            je = open('book/ja-en/ja-'+ language + '_' + fileName + '.mp3', 'wb')
            en = open('book/en/'+ language + '_' + fileName + '.mp3', 'wb')

            tx.write("https://www.sinkan.jp/news/" + str(i) + "?page=1" + "\n")

            pn = 1
            jaTxt = txtList[0].text
            #print(jaTxt)
            jdg1 = pattern.search(jaTxt)
            if jdg1:
                pne = len(re.findall('[^。！？!?]+[。！？!?]?', jaTxt))
                for p in re.findall('[^。！？!?]+[。！？!?]?', jaTxt):
                    jdg2 = pattern.search(p)
                    #print(pattern.search(p))
                    if jdg2:
                        enTxt = translator.translate(p,dest=language,src='ja').text
                        tx.write(p + "\n")
                        tx.write(enTxt + "\n")
                        #print(p)
                        tts = gTTS(p, lang='ja')
                        tts.write_to_fp(ja)
                        tts.write_to_fp(je)
                        time.sleep(3)
                        tts = gTTS(enTxt, lang='en')
                        tts.write_to_fp(en)
                        tts.write_to_fp(je)
                        time.sleep(3)
                    print(F"\r\033[2K{pn/pne*100:.02f}% ({pn}/{pne})", end="")
                    pn += 1

            print(str(i) + " downloaded" )
            try:        
                resul = resul + str(i) + " downloaded \n"
                label_4['text'] = resul
            except:
                print("error")
                resul = str(i) + " downloaded \n"
                label_4['text'] = resul
            i += 1

if __name__ == '__main__':
 
    root = Tk() # この下に画面構成を記述
    
    # ----------- ①Window作成 ----------- #
    root.title('要約ダウンローダー')   # 画面タイトル設定
    root.geometry('500x800')       # 画面サイズ設定
    #root.resizable(False, False)   # リサイズ不可に設定

    frame1 = Frame(root, width=500, height=500, borderwidth=2, relief='solid')
    #frame1.propagate(False)
    frame1.grid(row=0, column=0)

    # テキストボックス（フレーム2右上）
    label_1 = Label(frame1, text="言語：", font=('System', 11))
    entry_1 = Entry(frame1, width=10)
    entry_1.insert(0, "en")
    label_2 = Label(frame1, text="開始話数：", font=('System', 11))
    entry_2 = Entry(frame1, width=5)
    entry_2.insert(0, "51")
    label_3 = Label(frame1, text="終了話数：", font=('System', 11))
    entry_3 = Entry(frame1, width=5)
    entry_3.insert(0, "150")
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

