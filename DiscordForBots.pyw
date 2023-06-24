import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import Menu
import requests
from io import BytesIO
from PIL import Image
import os


def login():
    window_login = ctk.CTk()
    window_login.title("Discord for bots | Login")

    icon_directory = f"{os.environ['USERPROFILE']}\Discord for bots"
    icon = requests.get("https://raw.githubusercontent.com/FaktorEQQ/DIscord-for-bots/main/icon.ico").content
    if not os.path.exists(icon_directory):
        os.makedirs(icon_directory)
        with open(f"{icon_directory}\icon.ico", "wb") as file:
            file.write(icon)
    window_login.iconbitmap(f"{icon_directory}\icon.ico")


    window_login.geometry("500x150")
    window_login.resizable(False, False)

    frame = ctk.CTkFrame(window_login, width=400, height=100)
    frame.pack_propagate(0)
    frame.pack(expand=True)

    label = ctk.CTkLabel(frame, text="Token:", font=("font1", 15))
    label.pack()

    token_entry = ctk.CTkEntry(frame, width=350, height=28)
    token_entry.pack()

    def callback():
        data = requests.get("https://discord.com/api/v10/users/@me", headers={"Authorization":f"Bot {token_entry.get()}"}).json()
        try:
            data["code"]
            CTkMessagebox(title="Error", message="Wrong token was given!", icon="cancel")
        except:
            token = token_entry.get()
            window_login.destroy()
            program(token=token)
    login_button = ctk.CTkButton(frame, text="Login", command=callback)
    login_button.pack(expand=True)

    window_login.mainloop()


def program(token):
    window_program = ctk.CTk()
    window_program.title("Discord for bots")

    icon_directory = f"{os.environ['USERPROFILE']}\Discord for bots"
    icon = requests.get("https://raw.githubusercontent.com/FaktorEQQ/DIscord-for-bots/main/icon.ico").content
    if not os.path.exists(icon_directory):
        os.makedirs(icon_directory)
        with open(f"{icon_directory}\icon.ico", "wb") as file:
            file.write(icon)
    window_program.iconbitmap(f"{icon_directory}\icon.ico")

    window_program.geometry("962x982")
    window_program.resizable(False, False)


    guilds_frame = ctk.CTkFrame(window_program, width=75, height=982, fg_color="#242424")
    guilds_frame.pack_propagate(0)
    guilds_frame.pack(side="left")

    guild_name_frame = ctk.CTkFrame(window_program, width=240, height=50, fg_color="#2b2d31", bg_color="#242424")
    guild_name_frame.pack_propagate(0)
    guild_name_frame.place(anchor="nw", relx=0.080)
    guild_name_label = ctk.CTkLabel(guild_name_frame, text="", font=ctk.CTkFont(family="Arial", size=15, weight="bold"))
    guild_name_label.pack(expand=True)

    channels_frame = ctk.CTkFrame(window_program, width=240, height=932, fg_color="#2b2d31")
    channels_frame.pack_propagate(0)
    channels_frame.pack(side="left", anchor="s")

    channel_name_frame = ctk.CTkFrame(window_program, width=400, height=50, fg_color="#313338")
    channel_name_frame.pack_propagate(0)
    channel_name_frame.pack(side="left", anchor="n")
    channel_name_label = ctk.CTkLabel(channel_name_frame, text="", font=ctk.CTkFont(family="Arial", size=15, weight="bold"))
    channel_name_label.pack(expand=True)

    messages_frame = ctk.CTkFrame(window_program, width=400, height=832, fg_color="#313338")
    messages_frame.pack_propagate(0)
    messages_frame.place(anchor="s", relx=0.535, rely=0.90)

    send_message_frame = ctk.CTkFrame(window_program, width=400, height=100, fg_color="#383a40")
    send_message_frame.pack_propagate(0)
    send_message_frame.place(anchor="s", relx=0.535, rely=1.0)


    def create_menu_message(e, channel_id, message_id, message_button):
        menu = Menu(messages_frame, tearoff=False)

        def delete_message():
            req = requests.delete(f"https://discord.com/api/v10/channels/{channel_id}/messages/{message_id}", headers={"Authorization":f"Bot {token}"})
            try:
                req["message"]
                CTkMessagebox(title="Error", message="Message not deleted!", icon="cancel")
            except:
                message_button.destroy()
        def pin_message():
            requests.put(f"https://discord.com/api/v10/channels/{channel_id}/pins/{message_id}", headers={"Authorization":f"Bot {token}"})

        menu.add_command(label="Delete message", command=delete_message)
        menu.add_command(label="Pin message", command=pin_message)
        menu.tk_popup(x=e.x_root, y=e.y_root)


    def create_message_buttons(channel_id, channel_name):
        channel_name_label.configure(text=f"#{channel_name}")

        for btn in messages_frame.winfo_children():
            btn.destroy()

        for btn_send_message in send_message_frame.winfo_children():
            btn_send_message.destroy()


        messages_data = requests.get(f"https://discord.com/api/v10/channels/{channel_id}/messages", headers={"Authorization":f"Bot {token}"}).json()
        for message in messages_data:
            try:
                if message["content"]:
                    button = ctk.CTkButton(messages_frame, text=f"{message['author']['username']} | {message['content']}")
                    button.bind("<Button-1>", lambda e,channel_id=channel_id,message_id=message["id"],message_button=button: create_menu_message(e, channel_id=channel_id, message_id=message_id, message_button=message_button))
                    button.pack(side="bottom")
                else:
                    button = ctk.CTkButton(messages_frame, text=f"{message['author']['username']} | No content")
                    button.bind("<Button-1>", lambda e,channel_id=channel_id,message_id=message["id"],message_button=button: create_menu_message(e, channel_id=channel_id, message_id=message_id, message_button=message_button))
                    button.pack(side="bottom")
            except:
                None

        content_entry = ctk.CTkEntry(send_message_frame, width=350, height=28)
        content_entry.pack(expand=True)

        def send_callback():
            try:
                req = requests.post(f"https://discord.com/api/v10/channels/{channel_id}/messages", headers={"Authorization":f"Bot {token}"}, data={"content":content_entry.get()}).json()
                req["id"]

                created_btn = ctk.CTkButton(messages_frame, text=f"{req['author']['username']} | {req['content']}")
                created_btn.bind("<Button-1>", lambda e,channel_id=channel_id,message_id=req["id"],message_button=created_btn: create_menu_message(e, channel_id=channel_id, message_id=message_id, message_button=message_button))
                created_btn.pack(side="bottom")
            except:
                CTkMessagebox(title="Error", message="No message sent!", icon="cancel")

        send_message_button = ctk.CTkButton(send_message_frame, text="Send", command=send_callback)
        send_message_button.pack(expand=True)



    def create_channel_buttons(guild):
        guild_name_label.configure(text=guild["name"])

        for btn in channels_frame.winfo_children():
            btn.destroy()
        
        
        channels_data = requests.get(f"https://discord.com/api/v10/guilds/{guild['id']}/channels", headers={"Authorization":f"Bot {token}"}).json()
        for channel in channels_data:
            if channel["type"] == 0:
                button = ctk.CTkButton(channels_frame, text=f"#{channel['name']}", command=lambda channel_id=channel["id"],channel_name=channel["name"]: create_message_buttons(channel_id=channel_id, channel_name=channel_name), fg_color="#2b2d31")
                button.pack()


    def create_guild_images(guild):
        if guild["icon"]:
            image_data = requests.get(f"https://cdn.discordapp.com/icons/{guild['id']}/{guild['icon']}").content
            image = Image.open(BytesIO(image_data))
            image = image.resize((75, 75))
            image_tk = ctk.CTkImage(image)

            label = ctk.CTkButton(guilds_frame, text="", image=image_tk, width=75, height=75, command=lambda guild=guild:create_channel_buttons(guild=guild), fg_color="#242424")
            label.pack()
        else:
            label = ctk.CTkButton(guilds_frame, text=guild["name"].split()[0], width=75, height=75, command=lambda guild=guild:create_channel_buttons(guild=guild), fg_color="#242424")
            label.pack()

    guilds_data = requests.get("https://discord.com/api/v10/users/@me/guilds", headers={"Authorization":f"Bot {token}"}).json()
    for guild in guilds_data:
        create_guild_images(guild=guild)

    window_program.mainloop()









login()
