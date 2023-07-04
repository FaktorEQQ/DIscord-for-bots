import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import Menu
import requests
from io import BytesIO
from PIL import Image, ImageTk
import os
from datetime import datetime
import webbrowser


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


    guilds_frame = ctk.CTkScrollableFrame(window_program, width=75, height=982, fg_color="#242424")
    guilds_frame.pack_propagate(0)
    guilds_frame.pack(side="left", fill="y")

    guild_name_frame = ctk.CTkFrame(window_program, width=260, height=50, fg_color="#2b2d31", bg_color="#242424")
    guild_name_frame.pack_propagate(0)
    guild_name_frame.place(anchor="nw", relx=0.1)
    guild_name_label = ctk.CTkLabel(guild_name_frame, text="", font=ctk.CTkFont(family="Arial", size=15, weight="bold"))
    guild_name_label.pack(expand=True)

    channels_frame = ctk.CTkScrollableFrame(window_program, width=240, height=882, fg_color="#2b2d31")
    channels_frame.pack_propagate(0)
    channels_frame.pack(side="left")

    channel_name_frame = ctk.CTkFrame(window_program, width=420, height=50, fg_color="#313338")
    channel_name_frame.pack_propagate(0)
    channel_name_frame.pack(side="left", anchor="n")
    channel_name_label = ctk.CTkLabel(channel_name_frame, text="", font=ctk.CTkFont(family="Arial", size=15, weight="bold"))
    channel_name_label.pack(expand=True)

    messages_frame = ctk.CTkScrollableFrame(window_program, width=400, height=832, fg_color="#313338")
    messages_frame.pack_propagate(0)
    messages_frame.place(anchor="s", relx=0.590, rely=0.90)

    send_message_frame = ctk.CTkFrame(window_program, width=420, height=100, fg_color="#383a40")
    send_message_frame.pack_propagate(0)
    send_message_frame.place(anchor="s", relx=0.590, rely=1.0)

    members_frame = ctk.CTkScrollableFrame(window_program, width=160, height=982, fg_color="#2b2d31")
    members_frame.pack_propagate(0)
    members_frame.pack(side="right", fill="y")

    profile_frame = ctk.CTkFrame(window_program, width=260, height=50, fg_color="#232428")
    profile_frame.pack_propagate(0)
    profile_frame.place(anchor="s", relx=0.235, rely=1.0)


    def profile():
        profile_data = requests.get("https://discord.com/api/v10/users/@me", headers={"Authorization":f"Bot {token}"}).json()
        if profile_data["avatar"]:
            image_data = requests.get(f"https://cdn.discordapp.com/avatars/{profile_data['id']}/{profile_data['avatar']}").content
            image = Image.open(BytesIO(image_data))
            image_tk = ctk.CTkImage(image)
            avatar_label = ctk.CTkLabel(profile_frame, text="", image=image_tk)
            avatar_label.pack()
        name_label = ctk.CTkLabel(profile_frame, text=profile_data["username"])
        name_label.pack()
    profile()

    def check_version():
        req = requests.get("https://api.github.com/repos/FaktorEQQ/Discord-for-bots/releases/latest").json()
        app_version = "2-version"
        if not req["tag_name"] == app_version:
            frame = ctk.CTkFrame(window_program, width=650, height=200)
            frame.pack_propagate(0)
            frame.place(relx=0.5, rely=0.5, anchor="center")

            label = ctk.CTkLabel(frame, text="New update is available", font=ctk.CTkFont(family="Arial", size=30, weight="bold"))
            label.pack(side="left")

            def button_update_callback():
                webbrowser.open("https://github.com/FaktorEQQ/Discord-for-bots/releases/latest")

            button_update = ctk.CTkButton(frame, text="Update", command=button_update_callback)
            button_update.pack(side="left")

            def button_later_callback():
                frame.destroy()

            button_later = ctk.CTkButton(frame, text="Later", command=button_later_callback)
            button_later.pack(side="left")
    check_version()

    def create_menu_role(e, guild_id, role_id, role_button):
        menu = Menu(window_program, tearoff=False)

        def delete_role():
            req = requests.delete(f"https://discord.com/api/v10/guilds/{guild_id}/roles/{role_id}", headers={"Authorization":f"Bot {token}"}).json()
            try:
                req["message"]
                CTkMessagebox(title="Error", message=req["message"], icon="cancel")
            except:
                role_button.destroy()
        
        def copy_id():
            window_program.clipboard_clear()
            window_program.clipboard_append(role_id)
        
        menu.add_command(label="Delete role", command=delete_role)
        menu.add_command(label="Copy ID", command=copy_id)
        menu.tk_popup(x=e.x_root, y=e.y_root)


    def create_menu_channel(e, channel_data, channel_button):
        menu = Menu(window_program, tearoff=False)

        def channel_settings():
            frame = ctk.CTkFrame(window_program, width=962, height=982)
            frame.pack_propagate(0)
            frame.place(relx=0.5, rely=0.5, anchor="center")

            def button_close_callback():
                frame.destroy()
        
            button_close = ctk.CTkButton(frame, text="X", fg_color="red", command=button_close_callback, width=50, height=30, font=ctk.CTkFont(family="Arial", size=15, weight="bold"))
            button_close.pack(anchor="ne")

            options_frame = ctk.CTkScrollableFrame(frame, width=200, height=952, fg_color="#2b2d31")
            options_frame.pack_propagate(0)
            options_frame.pack(side="left", anchor="s")

            settings_frame = ctk.CTkScrollableFrame(frame, width=792, height=952, fg_color="#313338")
            settings_frame.pack_propagate(0)
            settings_frame.pack(side="right", anchor="s")
            settings_frame.columnconfigure(0, weight=1)

            def button_overview_callback():
                for item in settings_frame.winfo_children():
                    item.destroy()

                channel_name_label = ctk.CTkLabel(settings_frame, text="Channel name", font=ctk.CTkFont(family="Arial", size=15, weight="bold"))
                channel_name_label.grid()
                channel_name_entry = ctk.CTkEntry(settings_frame, width=500, height=20, font=ctk.CTkFont(family="Arial", size=20), fg_color="#1e1f22")
                channel_name_entry.insert(0, channel_data["name"])
                channel_name_entry.grid()

                def change_name_callback():
                    req = requests.patch(f"https://discord.com/api/v10/channels/{channel_data['id']}", json={"name":channel_name_entry.get()}, headers={"Authorization":f"Bot {token}"}).json()
                    try:
                        req["message"]
                        CTkMessagebox(title="Error", message=req["message"], icon="cancel")
                    except:
                        channel_button.configure(text=f"#{channel_name_entry.get()}")

                change_name_button = ctk.CTkButton(settings_frame, text="Change channel name", command=change_name_callback)
                change_name_button.grid()

                channel_topic_label = ctk.CTkLabel(settings_frame, text="Channel topic", font=ctk.CTkFont(family="Arial", size=15, weight="bold"))
                channel_topic_label.grid()
                channel_topic_textbox = ctk.CTkTextbox(settings_frame, font=ctk.CTkFont(family="Arial", size=15), width=500, height=75, fg_color="#1e1f22")
                if channel_data["topic"]:
                    channel_topic_textbox.insert("1.0", channel_data["topic"])
                channel_topic_textbox.grid()

                def change_topic_callback():
                    req = requests.patch(f"https://discord.com/api/v10/channels/{channel_data['id']}", json={"topic":channel_topic_textbox.get("1.0", "end-1c")}, headers={"Authorization":f"Bot {token}"}).json()
                    try:
                        req["message"]
                        CTkMessagebox(title="Error", message=req["message"], icon="cancel")
                    except:
                        None

                change_topic_button = ctk.CTkButton(settings_frame, text="Change channel topic", command=change_topic_callback)
                change_topic_button.grid()

                channel_slowmode_label = ctk.CTkLabel(settings_frame, text="Slowmode", font=ctk.CTkFont(family="Arial", size=15, weight="bold"))
                channel_slowmode_label.grid()
                if channel_data["rate_limit_per_user"] == 0:
                    channel_slowmode_count_label = ctk.CTkLabel(settings_frame, text="Off")
                else:
                    channel_slowmode_count_label = ctk.CTkLabel(settings_frame, text=f"{channel_data['rate_limit_per_user']}s")
                channel_slowmode_count_label.grid()
                slowmode_options = {"Off":0, "5s":5, "10s":10, "15s":15, "30s":30, "1m":60, "2m":120, "5m":300, "10m":600, "15m":900, "30m":1800, "1h":3600, "2h":7200, "6h":21600}
                def slowmode_slider_callback(value):
                    value = list(slowmode_options.keys())[int(value)]
                    channel_slowmode_count_label.configure(text=value)
                channel_slowmode_slider = ctk.CTkSlider(settings_frame, from_=0, to=13, number_of_steps=13, width=500, command=slowmode_slider_callback)
                channel_slowmode_slider.grid()

                def change_slowmode_callback():
                    value = list(slowmode_options.keys())[int(channel_slowmode_slider.get())]
                    slow_mode_time = slowmode_options[value]
                    req = requests.patch(f"https://discord.com/api/v10/channels/{channel_data['id']}", json={"rate_limit_per_user":slow_mode_time}, headers={"Authorization":f"Bot {token}"}).json()
                    try:
                        req["message"]
                        CTkMessagebox(title="Error", message=req["message"], icon="cancel")
                    except:
                        None

                change_slowmode_button = ctk.CTkButton(settings_frame, text="Change channel slowmode", command=change_slowmode_callback)
                change_slowmode_button.grid()

                channel_nsfw_label = ctk.CTkLabel(settings_frame, text="Nsfw", font=ctk.CTkFont(family="Arial", size=15, weight="bold"))
                channel_nsfw_label.grid()
                def nsfw_switch_callback():
                    if channel_nsfw_switch.get() == 1:
                        channel_nsfw_switch.configure(text="On")
                    else:
                        channel_nsfw_switch.configure(text="Off")
                channel_nsfw_switch = ctk.CTkSwitch(settings_frame, command=nsfw_switch_callback)
                if channel_data["nsfw"]:
                    channel_nsfw_switch.select()
                    channel_nsfw_switch.configure(text="On")
                else:
                    channel_nsfw_switch.deselect()
                    channel_nsfw_switch.configure(text="Off")
                channel_nsfw_switch.grid()
                def change_nsfw_callback():
                    if channel_nsfw_switch.get() == 1:
                        req = requests.patch(f"https://discord.com/api/v10/channels/{channel_data['id']}", json={"nsfw":True}, headers={"Authorization":f"Bot {token}"}).json()
                    else:
                        req = requests.patch(f"https://discord.com/api/v10/channels/{channel_data['id']}", json={"nsfw":False}, headers={"Authorization":f"Bot {token}"}).json()
                    try:
                        req["message"]
                        CTkMessagebox(title="Error", message=req["message"], icon="cancel")
                    except:
                        None
                change_nsfw_button = ctk.CTkButton(settings_frame, text="Change channel nsfw", command=change_nsfw_callback)
                change_nsfw_button.grid()

            button_overview = ctk.CTkButton(options_frame, text="Overview", fg_color="#2b2d31", command=button_overview_callback, width=200, height=50, font=ctk.CTkFont(family="Arial", size=15))
            button_overview.grid()

            button_overview_callback()

        def copy_id():
            window_program.clipboard_clear()
            window_program.clipboard_append(channel_data["id"])

        menu.add_command(label="Edit channel", command=channel_settings)
        menu.add_command(label="Copy ID", command=copy_id)
        menu.tk_popup(x=e.x_root, y=e.y_root)


    def create_menu_guild(e, guild_data, guild_button=None):
        menu = Menu(guilds_frame, tearoff=False)

        def server_settings():
            frame = ctk.CTkFrame(window_program, width=962, height=982)
            frame.pack_propagate(0)
            frame.place(relx=0.5, rely=0.5, anchor="center")

            def button_close_callback():
                frame.destroy()
        
            button_close = ctk.CTkButton(frame, text="X", fg_color="red", command=button_close_callback, width=50, height=30, font=ctk.CTkFont(family="Arial", size=15, weight="bold"))
            button_close.pack(anchor="ne")


            options_frame = ctk.CTkScrollableFrame(frame, width=200, height=952, fg_color="#2b2d31")
            options_frame.pack_propagate(0)
            options_frame.pack(side="left", anchor="s")

            settings_frame = ctk.CTkScrollableFrame(frame, width=792, height=952, fg_color="#313338")
            settings_frame.pack_propagate(0)
            settings_frame.pack(side="right", anchor="s")
            settings_frame.columnconfigure(0, weight=1)

            def button_overview_callback():
                for item in settings_frame.winfo_children():
                    item.destroy()

                guild_name_label = ctk.CTkLabel(settings_frame, text="Server name", font=ctk.CTkFont(family="Arial", size=15, weight="bold"))
                guild_name_label.grid()

                guild_name_entry = ctk.CTkEntry(settings_frame, width=500, height=20, font=ctk.CTkFont(family="Arial", size=20), fg_color="#1e1f22")
                guild_name_entry.insert(0, guild_data["name"])
                guild_name_entry.grid()

                def change_name_callback():
                    req = requests.patch(f"https://discord.com/api/v10/guilds/{guild_data['id']}", json={"name":guild_name_entry.get()}, headers={"Authorization":f"Bot {token}"}).json()
                    try:
                        req["message"]
                        CTkMessagebox(title="Error", message=req["message"], icon="cancel")
                    except:
                        if guild_button:
                            if not guild_button.cget("image"):
                                guild_button.configure(text=guild_name_entry.get())

                change_name_button = ctk.CTkButton(settings_frame, text="Change server name", command=change_name_callback)
                change_name_button.grid()

            def button_roles_callback():
                for item in settings_frame.winfo_children():
                    item.destroy()

                req = requests.get(f"https://discord.com/api/v10/guilds/{guild_data['id']}/roles", headers={"Authorization":f"Bot {token}"}).json()

                def create_role_frame(role_data, e=None):
                    roles_frame = ctk.CTkFrame(frame, width=962, height=982)
                    roles_frame.pack_propagate(0)
                    roles_frame.place(relx=0.5, rely=0.5, anchor="center")

                    def button_close_callback():
                        roles_frame.destroy()
                    button_close = ctk.CTkButton(roles_frame, text="X", fg_color="red", command=button_close_callback, width=50, height=30, font=ctk.CTkFont(family="Arial", size=15, weight="bold"))
                    button_close.pack(anchor="ne")

                    all_roles_frame = ctk.CTkScrollableFrame(roles_frame, width=200, height=952, fg_color="#2b2d31")
                    all_roles_frame.pack_propagate(0)
                    all_roles_frame.pack(side="left", anchor="s")
                    def role_button_callback(role_data):
                        for item in settings_frame.winfo_children():
                            item.destroy()
                        role_name_label = ctk.CTkLabel(settings_frame, text="Role name", font=ctk.CTkFont(family="Arial", size=15, weight="bold"))
                        role_name_label.grid()
                        role_name_entry = ctk.CTkEntry(settings_frame, width=500, height=20, font=ctk.CTkFont(family="Arial", size=20), fg_color="#1e1f22")
                        role_name_entry.insert(0, role_data["name"])
                        role_name_entry.grid()
                        def change_name_callback():
                            reqq = requests.patch(f"https://discord.com/api/v10/guilds/{guild_data['id']}/roles/{role_data['id']}", json={"name":role_name_entry.get()}, headers={"Authorization":f"Bot {token}"}).json()
                            try:
                                reqq["message"]
                                CTkMessagebox(title="Error", message=reqq["message"], icon="cancel")
                            except:
                                None
                        change_name_button = ctk.CTkButton(settings_frame, text="Change role name", command=change_name_callback)
                        change_name_button.grid()
                    for role in req:
                        button_role = ctk.CTkButton(all_roles_frame, text=role["name"], width=200, height=50, fg_color="#2b2d31", command=lambda role_data=role: role_button_callback(role_data=role_data))
                        button_role.grid()
                    settings_frame = ctk.CTkScrollableFrame(roles_frame, width=792, height=952, fg_color="#313338")
                    settings_frame.pack_propagate(0)
                    settings_frame.pack(side="right", anchor="s")
                    settings_frame.columnconfigure(0, weight=1)

                    role_button_callback(role_data=role_data)

                for role in req:
                    role_frame = ctk.CTkFrame(settings_frame, width=792, height=50)
                    role_frame.grid()

                    button_role = ctk.CTkButton(role_frame, text=role['name'], fg_color="#2b2d31", width=792, height=50, font=ctk.CTkFont(family="Arial", size=15))
                    button_role.bind("<Button-1>", lambda e,role_data=role: create_role_frame(e=e, role_data=role_data))
                    button_role.bind("<Button-3>", lambda e,guild_id=guild_data["id"],role_id=role["id"],role_button=role_frame: create_menu_role(e, guild_id=guild_id, role_id=role_id, role_button=role_button))
                    button_role.grid()

                    label_color = ctk.CTkLabel(role_frame, text="|", font=ctk.CTkFont(family="Arial", weight="bold", size=50), text_color=f"#{format(role['color'], '06x')}", height=50)
                    label_color.grid(sticky="w", row=0)


            button_overview = ctk.CTkButton(options_frame, text="Overview", fg_color="#2b2d31", command=button_overview_callback, width=200, height=50, font=ctk.CTkFont(family="Arial", size=15))
            button_overview.grid()

            button_roles = ctk.CTkButton(options_frame, text="Roles", fg_color="#2b2d31", command=button_roles_callback, width=200, height=50, font=ctk.CTkFont(family="Arial", size=15))
            button_roles.grid()

            button_overview_callback()


        def copy_id():
            window_program.clipboard_clear()
            window_program.clipboard_append(guild_data["id"])

        menu.add_command(label="Server settings", command=server_settings)
        menu.add_command(label="Copy ID", command=copy_id)
        menu.tk_popup(x=e.x_root, y=e.y_root)

    def create_profile_frame(e, member_data):
        profile_frame = ctk.CTkFrame(window_program, width=300, height=350)
        profile_frame.pack_propagate(0)
        profile_frame.place(relx=0.5, rely=0.5, anchor="center")


        def button_close_callback():
            profile_frame.destroy()
        
        button_close = ctk.CTkButton(profile_frame, text="X", fg_color="red", command=button_close_callback, width=50, height=30, font=ctk.CTkFont(family="Arial", size=15, weight="bold"))
        button_close.pack(anchor="ne")

        if member_data["user"]["avatar"]:
            image_data = requests.get(f"https://cdn.discordapp.com/avatars/{member_data['user']['id']}/{member_data['user']['avatar']}").content
            image = Image.open(BytesIO(image_data)).resize((100, 100))
            image_tk = ImageTk.PhotoImage(image)
            image_label = ctk.CTkLabel(profile_frame, image=image_tk, text="")
            image_label.pack()
        
        if member_data["user"]["display_name"]:
            display_name_label = ctk.CTkLabel(profile_frame, text=member_data["user"]["display_name"], font=ctk.CTkFont(family="Arial", size=15, weight="bold"))
            display_name_label.pack()

        if member_data["user"]["discriminator"] == "0":
            username_label = ctk.CTkLabel(profile_frame, text=member_data["user"]["username"], font=ctk.CTkFont(family="Arial", size=15))
            username_label.pack()
        else:
            username_label = ctk.CTkLabel(profile_frame, text=f"{member_data['user']['username']}#{member_data['user']['discriminator']}", font=ctk.CTkFont(family="Arial", size=15))
            username_label.pack()

        joined_at = datetime.strptime(member_data["joined_at"], "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%b %d, %Y")
        ctk.CTkLabel(profile_frame, text=f"Joined at\n{joined_at}").pack()


    def create_menu_member(e, member_id, guild_id, member_button):
        menu = Menu(members_frame, tearoff=False)

        def kick_member():
            req = requests.delete(f"https://discord.com/api/v10/guilds/{guild_id}/members/{member_id}", headers={"Authorization":f"Bot {token}"}).json()
            try:
                req["message"]
                CTkMessagebox(title="Error", message=req["message"], icon="cancel")
            except:
                member_button.destroy()

        def ban_member():
            req = requests.put(f"https://discord.com/api/v10/guilds/{guild_id}/bans/{member_id}", headers={"Authorization":f"Bot {token}"}).json()
            try:
                req["message"]
                CTkMessagebox(title="Error", message=req["message"], icon="cancel")
            except:
                member_button.destroy()

        def copy_id():
            window_program.clipboard_clear()
            window_program.clipboard_append(member_id)

        menu.add_command(label="Kick member", command=kick_member)
        menu.add_command(label="Ban member", command=ban_member)
        menu.add_command(label="Copy ID", command=copy_id)
        menu.tk_popup(x=e.x_root, y=e.y_root)

    def create_menu_message(e, channel_id, message_id, message_button):
        menu = Menu(messages_frame, tearoff=False)

        def delete_message():
            req = requests.delete(f"https://discord.com/api/v10/channels/{channel_id}/messages/{message_id}", headers={"Authorization":f"Bot {token}"})
            try:
                req["message"]
                CTkMessagebox(title="Error", message=req["message"], icon="cancel")
            except:
                message_button.destroy()

        def pin_message():
            req = requests.put(f"https://discord.com/api/v10/channels/{channel_id}/pins/{message_id}", headers={"Authorization":f"Bot {token}"}).json()
            try:
                req["message"]
                CTkMessagebox(title="Error", message=req["message"], icon="cancel")
            except:
                None

        def copy_id():
            window_program.clipboard_clear()
            window_program.clipboard_append(message_id)

        menu.add_command(label="Delete message", command=delete_message)
        menu.add_command(label="Pin message", command=pin_message)
        menu.add_command(label="Copy ID", command=copy_id)
        menu.tk_popup(x=e.x_root, y=e.y_root)


    def create_message_buttons(channel_id, channel_name):
        channel_name_label.configure(text=f"#{channel_name}")

        for btn in messages_frame.winfo_children():
            btn.destroy()

        for btn_send_message in send_message_frame.winfo_children():
            btn_send_message.destroy()


        messages_data = requests.get(f"https://discord.com/api/v10/channels/{channel_id}/messages", headers={"Authorization":f"Bot {token}"}).json()
        for message in reversed(messages_data):
            try:
                if message["content"]:
                    button = ctk.CTkButton(messages_frame, text=f"{message['author']['username']} | {message['content']}", width=400, anchor="w")
                    button.bind("<Button-3>", lambda e,channel_id=channel_id,message_id=message["id"],message_button=button: create_menu_message(e, channel_id=channel_id, message_id=message_id, message_button=message_button))
                    button.grid(sticky="ew")
                else:
                    button = ctk.CTkButton(messages_frame, text=f"{message['author']['username']} | {message['embeds'][0]['title']}", width=400, anchor="w")
                    button.bind("<Button-3>", lambda e,channel_id=channel_id,message_id=message["id"],message_button=button: create_menu_message(e, channel_id=channel_id, message_id=message_id, message_button=message_button))
                    button.grid(sticky="ew")
            except:
                None

        content_entry = ctk.CTkEntry(send_message_frame, width=350, height=28)
        content_entry.grid(sticky="ew", pady=10)

        def send_callback():
            try:
                req = requests.post(f"https://discord.com/api/v10/channels/{channel_id}/messages", headers={"Authorization":f"Bot {token}"}, data={"content":content_entry.get()}).json()
                req["id"]

                created_btn = ctk.CTkButton(messages_frame, text=f"{req['author']['username']} | {req['content']}", width=400, anchor="w")
                created_btn.bind("<Button-3>", lambda e,channel_id=channel_id,message_id=req["id"],message_button=created_btn: create_menu_message(e, channel_id=channel_id, message_id=message_id, message_button=message_button))
                created_btn.grid(sticky="ew")
            except:
                CTkMessagebox(title="Error", message="No message sent!", icon="cancel")

        send_message_button = ctk.CTkButton(send_message_frame, text="Send", command=send_callback)
        send_message_button.grid(sticky="ew", pady=10)



    def create_channel_buttons(guild):
        guild_name_label.configure(text=guild["name"])
        guild_name_label.unbind("<Button-1>")
        guild_name_label.unbind("<Button-3>")
        guild_name_label.bind("<Button-1>", lambda e,guild_data=guild: create_menu_guild(e, guild_data=guild_data))
        guild_name_label.bind("<Button-3>", lambda e,guild_data=guild: create_menu_guild(e, guild_data=guild_data))

        guild_name_frame.unbind("<Button-1>")
        guild_name_frame.unbind("<Button-3>")
        guild_name_frame.bind("<Button-1>", lambda e,guild_data=guild: create_menu_guild(e, guild_data=guild_data))
        guild_name_frame.bind("<Button-3>", lambda e,guild_data=guild: create_menu_guild(e, guild_data=guild_data))

        for btn in channels_frame.winfo_children():
            btn.destroy()

        for btn in members_frame.winfo_children():
            btn.destroy()

        
        
        
        channels_data = requests.get(f"https://discord.com/api/v10/guilds/{guild['id']}/channels", headers={"Authorization":f"Bot {token}"}).json()
        for channel in channels_data:
            if channel["type"] == 0:
                if len(channel["name"]) > 60:
                    button = ctk.CTkButton(channels_frame, text=f"#{channel['name'][:60]+'...'}", command=lambda channel_id=channel["id"],channel_name=channel["name"]: create_message_buttons(channel_id=channel_id, channel_name=channel_name), fg_color="#2b2d31", width=240)
                else:
                    button = ctk.CTkButton(channels_frame, text=f"#{channel['name']}", command=lambda channel_id=channel["id"],channel_name=channel["name"]: create_message_buttons(channel_id=channel_id, channel_name=channel_name), fg_color="#2b2d31", width=240)
                button.bind("<Button-3>", lambda e,channel_data=channel,channel_button=button: create_menu_channel(e, channel_data=channel_data, channel_button=channel_button))
                button.grid(sticky="NSEW")
                

        members_data = requests.get(f"https://discord.com/api/v10/guilds/{guild['id']}/members?limit=50", headers={"Authorization":f"Bot {token}"}).json()
        for member in members_data:
            button = ctk.CTkButton(members_frame, text=member["user"]["username"], fg_color="#2b2d31", width=160)
            button.bind("<Button-1>", lambda e,member_data=member: create_profile_frame(e, member_data=member_data))
            button.bind("<Button-3>", lambda e,member_id=member["user"]["id"], guild_id=guild["id"], member_button=button: create_menu_member(e, member_id=member_id, guild_id=guild_id, member_button=member_button))
            button.grid(sticky="NSEW")


    def create_guild_images(guild):
        if guild["icon"]:
            image_data = requests.get(f"https://cdn.discordapp.com/icons/{guild['id']}/{guild['icon']}").content
            image = Image.open(BytesIO(image_data)).resize((65, 65))
            image_tk = ImageTk.PhotoImage(image)

            button = ctk.CTkButton(guilds_frame, text="", image=image_tk, width=75, height=75, command=lambda guild=guild:create_channel_buttons(guild=guild), fg_color="#242424")
            button.bind("<Button-3>", lambda e,guild_data=guild,guild_button=button: create_menu_guild(e, guild_data=guild_data, guild_button=guild_button))
            button.grid()
        else:
            if len(guild["name"].split()[0]) > 10:
                button = ctk.CTkButton(guilds_frame, text=guild["name"].split()[0][:10]+"...", width=75, height=75, command=lambda guild=guild:create_channel_buttons(guild=guild), fg_color="#242424")
            else:
                button = ctk.CTkButton(guilds_frame, text=guild["name"].split()[0], width=75, height=75, command=lambda guild=guild:create_channel_buttons(guild=guild), fg_color="#242424")
            button.bind("<Button-3>", lambda e,guild_data=guild,guild_button=button: create_menu_guild(e, guild_data=guild_data, guild_button=guild_button))
            button.grid()

    guilds_data = requests.get("https://discord.com/api/v10/users/@me/guilds", headers={"Authorization":f"Bot {token}"}).json()
    for guild in guilds_data:
        create_guild_images(guild=guild)

    window_program.mainloop()









login()
