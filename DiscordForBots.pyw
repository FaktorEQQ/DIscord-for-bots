import tkinter
from tkinter import messagebox
import requests


def login():
    window_login = tkinter.Tk()
    window_login.title("Login")
    window_login.geometry("500x150")
    window_login.resizable(False, False)

    label = tkinter.Label(window_login, text="Token:", font=("Arial", 25))
    label.pack()

    token = tkinter.Text(window_login, width=30, height=1, font=("Arial", 20))
    token.pack()

    def callback():
        get_code_data = requests.get("https://discord.com/api/v10/users/@me", headers={"Authorization":f"Bot {token.get('1.0','end-1c')}"}).json()
        try:
            get_code_data["code"]
            messagebox.showerror("Error", "Wrong token was given!")
        except:
            program(token=token.get('1.0','end-1c'), window_login=window_login)
    button = tkinter.Button(text="Login", command=callback, width=20, height=1)
    button.pack()

    window_login.mainloop()




def program(token, window_login):
    window_login.destroy()

    window_program = tkinter.Tk()
    window_program.title("Discord for bots")
    window_program.geometry("962x982")
    window_program.resizable(False, False)


    guilds_canvas = tkinter.Canvas(window_program, width=200, height=982)
    guilds_canvas.pack(side="left", anchor="nw", expand=False)
    guilds_frame = tkinter.Frame(guilds_canvas, width=200, height=982)
    guilds_canvas.create_window((0, 0), window=guilds_frame, anchor="nw")

    channels_canvas = tkinter.Canvas(window_program, width=200, height=982)
    channels_canvas.pack(side="left", anchor="nw", expand=False)
    channels_frame = tkinter.Frame(channels_canvas, width=200, height=982)
    channels_canvas.create_window((0, 0), window=channels_frame, anchor="nw")

    send_message_frame = tkinter.Frame(window_program, width=800, height=100)
    send_message_frame.pack(side="bottom", expand=False)

    messages_canvas = tkinter.Canvas(window_program, width=400, height=882)
    messages_canvas.pack(side="left", anchor="nw", expand=False)
    messages_frame = tkinter.Frame(messages_canvas, width=400, height=882)
    messages_canvas.create_window((0, 0), window=messages_frame, anchor="nw")

    send_message_frame.pack_propagate(0)
    messages_frame.pack_propagate(0)



    guilds_data = requests.get("https://discord.com/api/v10/users/@me/guilds", headers={"Authorization":f"Bot {token}"}).json()

    def create_menu_message(e, channel_id, message_id):
        menu = tkinter.Menu(messages_frame)

        def delete_message():
            req = requests.delete(f"https://discord.com/api/v10/channels/{channel_id}/messages/{message_id}", headers={"Authorization":f"Bot {token}"}).json()
            try:
                req["message"]
                messagebox.showerror("Error", "Message not deleted!")
            except:
                None
        def pin_message():
            requests.put(f"https://discord.com/api/v10/channels/{channel_id}/pins/{message_id}", headers={"Authorization":f"Bot {token}"})

        menu.add_command(label="Delete message", command=delete_message)
        menu.add_command(label="Pin message", command=pin_message)

        menu.post(e.x_root, e.y_root)

    def create_message_buttons(channel_id, channel_name):
        for btn in messages_frame.winfo_children():
            btn.destroy()

        for btn_send_message in send_message_frame.winfo_children():
            btn_send_message.destroy()

        #scrollbar
        messages_scrollbar = tkinter.Scrollbar(messages_frame, orient="vertical", command=messages_canvas.yview)
        messages_scrollbar.pack(side="right", fill="y")
        messages_canvas.config(yscrollcommand=messages_scrollbar.set)

        channel_name_label = tkinter.Label(messages_frame, text=f"#{channel_name}", font="Arial 20")
        channel_name_label.pack()
        
        messages_data = requests.get(f"https://discord.com/api/v10/channels/{channel_id}/messages", headers={"Authorization":f"Bot {token}"}).json()
        for message in reversed(messages_data):
            try:
                if not message["author"]["global_name"] == None:
                    button = tkinter.Button(messages_frame, text=f"{message['author']['global_name']} | {message['content']}")
                    button.bind("<Button-1>", lambda e,channel_id=channel_id,message_id=message["id"]: create_menu_message(e, channel_id=channel_id, message_id=message_id))
                    button.pack(side="top")
            except:
                None

            #scrollbar
            messages_canvas.configure(scrollregion=messages_canvas.bbox("all"))
        
        content_text = tkinter.Text(send_message_frame, width=55, height=5)
        content_text.place(x=-200, y=1)

        def send_callback():
            try:
                req = requests.post(f"https://discord.com/api/v10/channels/{channel_id}/messages", data={"content":content_text.get('1.0','end-1c')}, headers={"Authorization":f"Bot {token}"}).json()
                req["id"]

                created_btn = tkinter.Button(messages_frame, text=f"{req['author']['username']} | {req['content']}")
                created_btn.bind("<Button-1>", lambda e,channel_id=channel_id,message_id=req["id"]: create_menu_message(e, channel_id=channel_id, message_id=message_id))
                created_btn.pack()
            except:
                messagebox.showerror("Error", "No message sent!")

        send_message_button = tkinter.Button(send_message_frame, text="Send", command=send_callback, width=20, height=3)
        send_message_button.place(x=300, y=5)

    def create_channel_buttons(guild_id):
        for btn in channels_frame.winfo_children():
            btn.destroy()

        #scrollbar
        channels_scrollbar = tkinter.Scrollbar(channels_frame, orient="vertical", command=channels_canvas.yview)
        channels_scrollbar.pack(side="right", fill="y")
        channels_canvas.config(yscrollcommand=channels_scrollbar.set)

        channels_data = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers={"Authorization":f"Bot {token}"}).json()
        for channel in channels_data:
            if channel["type"] == 0:
                    button = tkinter.Button(channels_frame, text=f"#{channel['name']}", command=lambda channel_id=channel["id"],channel_name=channel["name"]: create_message_buttons(channel_id=channel_id, channel_name=channel_name))
                    button.pack(side="top")

        #scrollbar
        channels_canvas.configure(scrollregion=channels_canvas.bbox("all"))

    def create_guild_buttons(guild):
        button = tkinter.Button(guilds_frame, text=guild["name"], command=lambda guild_id=guild["id"]: create_channel_buttons(guild_id=guild_id))
        button.pack(side="top")


    #scrollbar
    guilds_scrollbar = tkinter.Scrollbar(guilds_frame, orient="vertical", command=guilds_canvas.yview)
    guilds_scrollbar.pack(side="right", fill="y")
    guilds_canvas.config(yscrollcommand=guilds_scrollbar.set)

    for guild in guilds_data:
        create_guild_buttons(guild=guild)

    #scrollbar
    guilds_canvas.configure(scrollregion=guilds_canvas.bbox("all"))

    window_program.mainloop()







login()