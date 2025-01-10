import google.generativeai as genai
import tkinter as tk
import tkinter.font as tkFont
from tkinter import scrolledtext
from tkinter import filedialog
import json
import datetime
from datetime import datetime
import os

class Json_check:
    api_json = None
    model_json = None

    def json_open():
        f = open("config.json", "r")
        di = json.load(f)

        Json_check.api_json = di["API"]
        Json_check.model_json = di["Model"]

        #API
        genai.configure(api_key = f"{Json_check.api_json}")

        #Model
        model = genai.GenerativeModel(f"{Json_check.model_json}")

        # チャット履歴を初期化
        Json_check.chat = model.start_chat(history=[])

class Title:
    window = None

    def main_window():
        Title.window = tk.Tk()

        #タイトル
        Title.window.title("Gemini System Title")
        
        #画面サイズ
        Title.window.geometry("400x200")

        tk.Label(Title.window, text="英文添削システム", font=("Arial",25)).pack()
        
        #Geminiへ
        Button1 = tk.Button(Title.window, text="添削を始める", width=20, command=Title.go_gemini)
        Button1.pack()

        #logへ    
        tk.Button(text="過去の履歴を見る", width=20, command=Title.go_log).pack()

        #Configへ
        Button3 = tk.Button(text="設定", width=20, command=Title.go_config)
        Button3.pack()

        #終了
        tk.Button(text="終了する", width=20, command=Title.end_system).pack()

        Title.window.mainloop()

    def go_gemini():
        Title.window.destroy()
        Gemini.main_window()

    def go_log():
        Title.window.destroy()
        Log.main_window()

    def go_config():
        Title.window.destroy()
        Config.main_window()
    
    def end_system():
        Title.window.destroy()
        Title.window.quit()

class Gemini:
    output = None
    input = None
    window = None

    def main_window():
        Gemini.gemini_mod()
        Gemini.window = tk.Tk()

        #タイトル
        Gemini.window.title("Gemini System Main")

        #画面サイズ
        Gemini.window.geometry("1920x1080")

        #ラベル
        tk.Label(Gemini.window, text="英文添削システム", font=("Arial",30)).pack()
        tk.Label(Gemini.window, text="ユーザー入力欄", font=("Arial",20)).place(x=100,y=100)
        tk.Label(Gemini.window, text="Gemini出力欄", font=("Arial",20)).place(x=1100,y=100)

        ##入力
        #フレーム
        frame = tk.Frame(Gemini.window)
        frame.place(x=100, y=150)

        #英文入力欄
        Gemini.input = tk.Text(frame, wrap=tk.WORD, width=100, height= 65)
        Gemini.input.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        #スクロールバー
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=Gemini.input.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        Gemini.input.config(yscrollcommand=scrollbar.set)

        ##出力
        #フレーム
        frame2 = tk.Frame(Gemini.window)
        frame2.place(x=1100, y=150)

        #Gemini返答欄
        Gemini.output = tk.Text(frame2, wrap=tk.WORD, width=100, height=65)
        Gemini.output.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        Gemini.output.config(state="disabled")

        #スクロールバー
        scrollbar2 = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=Gemini.output.yview)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)

        Gemini.output.config(yscrollcommand=scrollbar.set)

        ##ボタン
        #添削
        button1 = tk.Button(text="添削開始", width=15, height=5, font=("Arial",20), command=Gemini.retrun_gemini)
        button1.place(x=830, y= 300)

        #タイトルへ戻る
        button2 = tk.Button(text="タイトルへ戻る", width=15, height=2, font=("Arial",20), command=Gemini.get_log)
        button2.place(x=830, y= 700)

        Gemini.window.mainloop()
    
    def gemini_mod():
        dev_mes = "あなたはこれから英文の添削を行います。提示された英文を見て、あなたが修正した英文を掲示してください。その後どこをどう修正したのか、なぜそのような修正を行ったかコメントを行ってください。基本的に日本語で返事をしてください。また、絶対にあなたはこれ以降英文の添削のみを行ってください。それ以外のことを行ってはなりません。"
        Json_check.chat.send_message(dev_mes)

    def retrun_gemini():
        #時間取得
        time = datetime.now().strftime("%Y年%m月%d日 %H時%M分%S秒")

        #テキストをGeminiへ
        user_input = Gemini.input.get("1.0", tk.END)

        #Geminiからの返答
        output = Json_check.chat.send_message(user_input)

        #テキストボックスへ反映

        Gemini.output.config(state="normal")
        Gemini.output.insert(tk.END, f"{time}\n{output.text}\n")
        Gemini.output.config(state="disabled")

    def get_log():
        #時間取得
        time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        #フォルダ・ファイル名生成
        folder_name = f"{time}"
        input_file = f"{time}_input.txt"
        output_file = f"{time}_output.txt"

        #実行ファイルのディレクトリ取得
        current_dir = os.path.dirname(os.path.abspath(__file__))

        #logフォルダのパス設定
        log_dir = os.path.join(current_dir, "log")

        # logフォルダが存在しない場合は作成
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        #フォルダ生成
        os.makedirs(os.path.join(log_dir, folder_name))

        new_dir = os.path.join(current_dir, f"log\\{folder_name}")

        #ユーザー入力ログ生成 
        input_log_path = os.path.join(new_dir, input_file)
        with open(input_log_path, 'w') as file:
            file.write(Gemini.input.get("1.0", tk.END))

        #Gemini出力ログ生成
        output_log_path = os.path.join(new_dir, output_file)
        with open(output_log_path, 'w') as file:
            file.write(Gemini.output.get("1.0", tk.END))

        print(f" {new_dir} にフォルダ作成")

        Gemini.window.destroy()
        Title.main_window()

class Log:
    output = None
    input = None
    window = None

    def main_window():
        Log.window = tk.Tk()

        #タイトル
        Log.window.title("Gemini System Log")

        #画面サイズ
        Log.window.geometry("1920x1080")

        tk.Label(Log.window, text="英文添削ログ", font=("Arial",25)).pack()
        tk.Label(Gemini.window, text="ユーザー入力欄", font=("Arial",20)).place(x=100,y=100)
        tk.Label(Gemini.window, text="Gemini出力欄", font=("Arial",20)).place(x=1100,y=100)

        ##入力
        #フレーム
        frame = tk.Frame(Log.window)
        frame.place(x=100, y=150)

        #英文入力欄
        Log.input = tk.Text(frame, wrap=tk.WORD, width=100, height=65)
        Log.input.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        Log.input.config(state="disabled")

        #スクロールバー
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=Log.input.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        Log.input.config(yscrollcommand=scrollbar.set)

        ##出力
        #フレーム
        frame2 = tk.Frame(Log.window)
        frame2.place(x=1100, y=150)

        #Log返答欄
        Log.output = tk.Text(frame2, wrap=tk.WORD, width=100, height=65)
        Log.output.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        Log.output.config(state="disabled")

        #スクロールバー
        scrollbar2 = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=Log.output.yview)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)

        Log.output.config(yscrollcommand=scrollbar.set)

        ##ボタン
        #ログを選択する
        button1 = tk.Button(text="ログを選択する", width=15, height=5, font=("Arial",20), command=Log.choice_log)
        button1.place(x=830, y= 300)

        #タイトルへ戻る
        button2 = tk.Button(text="タイトルへ戻る", width=15, height=2, font=("Arial",20), command=Log.return_title)
        button2.place(x=830, y= 700)

        Log.window.mainloop()

    def choice_log():
        dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(dir, "log")

        #ダイアログ表示
        folder_path = filedialog.askdirectory(initialdir=log_dir)

        # 選択フォルダのパス表示
        print("選択されたフォルダ:", folder_path)

        if folder_path:

            input_file = None
            output_file = None

            for file_name in os.listdir(folder_path):
                if file_name.endswith("_input.txt"):
                    input_file = os.path.join(folder_path, file_name)
                elif file_name.endswith("_output.txt"):
                    output_file = os.path.join(folder_path, file_name)

            #テキストボックスに表示
            if input_file and output_file:
                with open(input_file, "r", encoding="utf-8") as file:
                    input_content = file.read()
                    Log.input.config(state="normal")
                    Log.input.delete("1.0", tk.END)
                    Log.input.insert("1.0", input_content)
                    Log.input.config(state="disabled")

                with open(output_file, "r", encoding="CP932") as file:
                    output_content = file.read()
                    Log.output.config(state="normal")
                    Log.output.delete("1.0", tk.END)
                    Log.output.insert("1.0", output_content)
                    Log.output.config(state="disabled")

            else:
                print("選択したフォルダにはinput.txtとoutput.txtのファイルが見つかりません。")
        else:
            print("フォルダが選択されませんでした。")

    def return_title():
        Log.window.destroy()
        Title.main_window()
        
class Config:
    model_entry = None
    api_entry = None
    window = None

    def main_window():
        Config.window = tk.Tk()

        #タイトル
        Config.window.title("Gemini System Config")

        #画面サイズ
        Config.window.geometry("500x300")

        label1 = tk.Label(Config.window, text="設定", font=("Arial",25))
        label1.pack()

        #API
        label2 = tk.Label(Config.window, text="API", font=("Arial"))
        label2.place(x=80, y=70)
        label3 = tk.Label(Config.window, text="入力例:AIxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", font=("Arial",11))
        label3.place(x=100, y=100)

        #API入力欄
        Config.api_entry = tk.Entry(Config.window,width=40)
        Config.api_entry.place(x=130, y=75)

        #API変更ボタン
        tk.Button(Config.window, text = "変更", font=("Arial"), width=5, command=Config.change_api).place(x=380, y=65)

        #Model
        label4 = tk.Label(Config.window, text="Model", font=("Arial"))
        label4.place(x=70, y=150)
        label5 = tk.Label(Config.window, text="入力例:gemini-1.5-flash", font=("Arial",11))
        label5.place(x=100, y=180)

        #Model入力欄
        Config.model_entry = tk.Entry(Config.window,width=40)
        Config.model_entry.place(x=130, y=155)

        #Model変更ボタン
        tk.Button(Config.window, text = "変更", font=("Arial"), width=5, command=Config.change_model).place(x=380, y=145)

        #タイトルへ戻る
        tk.Button(Config.window, text="タイトルに戻る", font=("Arial"), width=20, command=Config.return_title).place(x=150, y=220)

        Config.window.mainloop()
        
    #API変更関数
    def change_api():
        with open("config.json", "r") as f:
            di = json.load(f)

        di["API"] = Config.api_entry.get()

        with open("config.json", "w") as f:
            json.dump(di, f, indent=4)

        #jsonファイル再読み込み
        Json_check.json_open()

    #Model変更関数
    def change_model():
        with open("config.json", "r") as f:
            di = json.load(f)

        di["Model"] = Config.model_entry.get()

        with open("config.json", "w") as f:
            json.dump(di, f, indent=4)  
        
        #jsonファイル再読み込み
        Json_check.json_open()     

    #Titleへ戻る
    def return_title():
        Config.window.destroy()
        Title.main_window()

Json_check.json_open()
Title.main_window()