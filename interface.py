# http://apprendre-python.com/page-tkinter-interface-graphique-python-tutoriel
# https://www.tutorialspoint.com/python/python_gui_programming.htm
# https://docs.python.org/3/library/tkinter.ttk.html#notebook
# http://tkinter.fdex.eu/index.html

from tkinter.filedialog import *
from tkinter.ttk import *

import twitter_collect


class Application(Frame):
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master)
        super().__init__(master, **kw)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        # --------- Example ---------
        # Creation
        # self.hi_there = Button(self)
        # # Different parameters
        # self.hi_there["text"] = "Quit",
        # self.hi_there["command"] = self.quit  # or self.say_hi
        # # Placement in the frame
        # self.hi_there.pack({"side": "bottom"})

        # --------- Ours ---------
        self.display = Notebook(self, name="nb")  # tab manager
        self.display.grid()

        # create the content for the user, where he can choose the action to perform
        self.create_user_panel(self.display)

        # TODO : maybe we should only create this tab when there is something to show
        # self.create_viewer_panel(self.display)  # create the content to visualize the action chosen by rhe user

    # Example of function we can call
    # def say_hi(self):
    #     print("hi there, everyone!")

    def create_user_panel(self, display):
        fen_user = Frame(display, name="fen_user")

        self.toggle_language = StringVar()
        self.toggle_language.set("Français")

        Checkbutton(fen_user, textvariable=self.toggle_language, variable=self.toggle_language, onvalue="Français",
                    offvalue="English").grid(column=0, row=0)

        self.value_submit = StringVar()
        self.value_submit.set("Soumettre un texte")

        def default_submit_text(arg):
            if self.value_submit.get() == "Soumettre un texte":
                self.value_submit.set("")
            elif not self.value_submit.get():
                self.value_submit.set("Soumettre un texte")

        text_submit = Entry(fen_user, textvariable=self.value_submit)
        text_submit.bind("<Enter>", default_submit_text)
        text_submit.bind("<Leave>", default_submit_text)

        text_submit.grid(column=0, row=1)

        def text_analysis():
            if self.value_submit != "Soumettre un texte":
                pass  # function_to_call(self.value_submit)

        Button(fen_user, text="Soumettre texte", command=text_analysis).grid(column=1, row=1)

        def ask_file():
            file_name = askopenfile(title="Ouvrir fichier de tweets",
                                    filetypes=[('txt files', '.txt'), ('csv files', '.csv')])
            pass  # function_to_call(open(file_name, "r").read())

        Button(fen_user, text="Choisir un fichier à analyser", command=ask_file).grid(column=0, row=2)

        self.user_query = StringVar()
        self.user_query.set("Soumettre un '#' à regarder")

        def default_query_text(arg):
            if self.user_query.get() == "Soumettre un '#' à regarder":
                self.user_query.set("")
            elif not self.user_query.get():
                self.user_query.set("Soumettre un '#' à regarder")

        text_submit = Entry(fen_user, textvariable=self.user_query)

        text_submit.bind("<Enter>", default_query_text)
        text_submit.bind("<Leave>", default_query_text)

        text_submit.grid(column=0, row=3)

        def query_analysis():
            if self.user_query != "Soumettre un '#' à regarder" and '#' in self.user_query:
                twitter_collect.search_sample(self.user_query)
            elif self.user_query != "Soumettre un '#' à regarder":
                twitter_collect.search_sample('#' + self.user_query.get())

        Button(fen_user, text="Echantillon de la requête", command=query_analysis).grid(column=1, row=3)

        self.number_tweets = StringVar()
        self.number_tweets.set(5)

        Spinbox(fen_user, from_=1, to=222, increment=1, textvariable=self.number_tweets,
                justify='center').grid(column=0, row=4)

        def collect_tweet_stream():
            twitter_collect.collect_tweet(self.number_tweets)

        Button(fen_user, text="Collecter 'x' tweets", command=collect_tweet_stream).grid(column=1, row=4)

        display.add(fen_user, text="Options")

    def create_viewer_panel(self, display):
        fen_visualiser = Frame(display, name="fen_visualiser")

        display.add(fen_visualiser, text="Visualiseur")
