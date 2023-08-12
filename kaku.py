import time
import re
from urllib import request
from bs4 import BeautifulSoup
from googletrans import Translator
import sys
from gtts import gTTS
from tkinter import *


 

def download(url, bgn, end):

    # must change!

    start_episode = int(bgn)
    end_episode = int(end)
    language = 'en'
    # act 2023/07/06 1-70
    code = url.split("/")
    ncode = code[4]  # 取得したい小説のNコードを指定


    # 全部分数を取得
    info_url = "https://kakuyomu.jp/works/" + ncode
    info_res = request.urlopen(info_url)
    soup = BeautifulSoup(info_res, "html.parser")
    pre_info = soup.select_one(".js-vertical-composition-item").text
    num_parts = int(re.search(r"全([0-9]+)話", pre_info).group(1))


    # オリジナル　エピソードURL取得
    epi_url = soup.select('a.widget-toc-episode-episodeTitle')
    episodeUrl = []

    translator = Translator()

    for i in range(len(epi_url)):
        episodeUrl.append(epi_url[i].get('href'))

    for j in range(start_episode-1, end_episode):
        # 作品本文ページのURL
        url = "https://kakuyomu.jp" + episodeUrl[j]

        res = request.urlopen(url)
        soup = BeautifulSoup(res, "html.parser")

        pattern = re.compile("[0-9a-zA-Zぁ-んァ-ヶｱ-ﾝﾞﾟ一-龠_]")

        ttl = soup.select_one("p.widget-episodeTitle").text
        # 保存
        #tts = gTTS(en_text, lang='en')
        if j+1 > 999:
            fileName = 'ep'+ str(j+1) + '_' + ttl
            #fileName = 'ja-' + language + '_ep'+ str(j+1) + '_' + ttl
        elif j+1 > 99:
            fileName = 'ep0'+ str(j+1) + '_' + ttl
        elif j+1 > 9:
            fileName = 'ep00'+ str(j+1) + '_' + ttl
        else:
            fileName = 'ep000'+ str(j+1) + '_' + ttl

        tx = open('hikikomori/txt/'+ fileName +'.txt', 'w', encoding='UTF-8')
        ja = open('hikikomori/ja/ja_' + fileName + '.mp3', 'wb')
        je = open('hikikomori/ja-en/ja-'+ language + '_' + fileName + '.mp3', 'wb')
        en = open('hikikomori/en/'+ language + '_' + fileName + '.mp3', 'wb')

        jaTxt = ttl
        tx.write(jaTxt + "\n")
        jdg1 = pattern.search(jaTxt)
        if jdg1:
            enTxt = translator.translate(jaTxt,dest=language,src='ja').text
            tx.write(enTxt + "\n")
            tts = gTTS(jaTxt, lang='ja')
            tts.write_to_fp(ja)
            tts.write_to_fp(je)
            time.sleep(3)
            tts = gTTS(enTxt, lang='en')
            tts.write_to_fp(en)
            tts.write_to_fp(je)
            time.sleep(3)
        
        txtList = soup.select("div.widget-episodeBody > p")
        pn = 1
        pne = len(txtList)
        for i in txtList:
            jaTxt = i.text
            # print(jaTxt)
            tx.write(jaTxt + "\n")
            jdg1 = pattern.search(jaTxt)
            if jdg1:
                enTxt = translator.translate(jaTxt,dest=language,src='ja').text
                tx.write(enTxt + "\n")
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


        print("part {} downloaded (total: {:d} parts)".format(j+1, num_parts))  # 進捗を表示
        try:        
            resul = resul + fileName + " downloaded \n"
            label_4['text'] = resul
        except:
            print("error")
            resul = fileName + " downloaded \n"
            label_4['text'] = resul

        time.sleep(3)  # 次の部分取得までは1分の時間を空ける

if __name__ == '__main__':
 
    root = Tk() # この下に画面構成を記述
    
    # ----------- ①Window作成 ----------- #
    root.title('カクヨムダウンローダー')   # 画面タイトル設定
    root.geometry('500x800')       # 画面サイズ設定
    #root.resizable(False, False)   # リサイズ不可に設定

    frame1 = Frame(root, width=500, height=500, borderwidth=2, relief='solid')
    #frame1.propagate(False)
    frame1.grid(row=0, column=0)

    # テキストボックス（フレーム2右上）
    label_1 = Label(frame1, text="作品URL：", font=('System', 11))
    entry_1 = Entry(frame1, width=20)
    entry_1.insert(0, "https://kakuyomu.jp/works/16816700428600671727")
    label_2 = Label(frame1, text="開始話数：", font=('System', 11))
    entry_2 = Entry(frame1, width=5)
    entry_2.insert(0, "187")
    label_3 = Label(frame1, text="終了話数：", font=('System', 11))
    entry_3 = Entry(frame1, width=5)
    entry_3.insert(0, "250")
    button_2b = Button(frame1, text='download', command=lambda: download(entry_1.get(), entry_2.get(), entry_3.get()))
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

 
