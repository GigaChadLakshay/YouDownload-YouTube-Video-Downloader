import os
import sys
from pytube import YouTube
import requests
import ttkbootstrap as ttk
import PIL
from PIL import ImageTk, Image
import random
from tkinter.filedialog import askdirectory
import time

app = ttk.Window(themename="journal")
app.title("YouDownload")
app.geometry("750x460")
app.resizable(False, False)
res_dict = {}


# Please Change The Path While Importing External Assets

def get_video_details():
    global video_title
    global thumbnail_url
    global other_info
    global video
    try:
        video = YouTube(urlText.get())
        for index, stream in enumerate(video.streams.filter(progressive=True).all()):
            info_list = str(stream).split(" ")
            info_list = info_list[2].split('"')
            if 'video/mp4' in info_list[1] or 'video/3gpp' in info_list[1]:
                info_list = ((str(stream).split(" "))[3].split('"'))[1]
                res_dict.update({index: info_list})

    except:
        message_label.config(text="Invalid URL!", foreground="red")
        print("Please Enter Valid URL")
        return None
    video_title = video.title
    thumbnail_url = video.thumbnail_url
    fetch_thumbnail(thumbnail_url)
    other_info = {"Length": f"{(video.length / 60).__round__(2)} Minutes", "Creator": video.author,
                  "Uploaded": str(video.publish_date).split(" ")[0], "Views": video.views}
    print(f"Title: {video_title}\nThumbnail URL: {thumbnail_url}")
    video_details_page()


def fetch_thumbnail(thumbnailURL):
    response = requests.get(thumbnailURL)
    with open("C:\\Users\\HP\\PycharmProjects\\RevisingPython\\dist\\Assets\\thumbnail.jpg", "wb") as image:
        image.write(response.content)


def video_details_page(res_dict=res_dict):
    def back():
        video_details_frame.pack_forget()
        message_label.configure(text="")
        download_message.pack_forget()

        yt_logo_label.pack()
        input_widgets_frame.pack(pady=10)
        back_button.destroy()

    def download():
        save_directory = askdirectory(title="Save Video At")
        if resolutions_dropdown_value.get() == "" and save_directory == "":
            download_message.config(text="Please Select Video Quality And Path!", foreground="red")
            return None
        if resolutions_dropdown_value.get() == "":
            download_message.config(text="Please Select Video Quality!", foreground="red")
            return None
        if save_directory == "":
            download_message.config(text="Please Select Path!", foreground="red")
            return None
        downloaded = random.randint(0, 10000)
        selected_resolution = resolutions_dropdown_value.get()
        index_of_res = int()
        for key in res_dict.keys():
            if res_dict[key] == selected_resolution:
                index_of_res = key
        (video.streams.filter(progressive=True).all())[index_of_res].download(filename=f"{save_directory}\\YTDownload{downloaded}.mp4")
        download_message.config(text=f"Downloaded At {save_directory}", foreground="green")

    temp = []
    temp_dict = {}

    for key, value in res_dict.items():
        if value not in temp:
            temp.append(value)
            temp_dict.update({key: value})
    res_dict.clear()
    res_dict.update(temp_dict)
    resolutions = list(res_dict.values())
    print(resolutions)

    input_widgets_frame.pack_forget()
    yt_logo_label.pack_forget()

    video_details_frame = ttk.Frame(master=app)
    back_button_image = ImageTk.PhotoImage(
        PIL.Image.open("C:\\Users\\HP\\PycharmProjects\\RevisingPython\\dist\\Assets\\home_icon.png").resize((55, 55)))
    back_button = ttk.Button(master=app, command=back, image=back_button_image, style="link")
    back_button.place(x=5, y=5)
    back_button.image = back_button_image

    thumbnail = ImageTk.PhotoImage(
        PIL.Image.open("C:\\Users\\HP\\PycharmProjects\\RevisingPython\\dist\\Assets\\thumbnail.jpg").resize(
            (410, 200)))

    thumbnail_img = ttk.Label(master=video_details_frame, image=thumbnail)
    detail_app_title = ttk.Label(master=video_details_frame, text="Results", font="Calibri 25 bold")
    video_title_label = ttk.Label(master=video_details_frame, text=video_title, font="Calibri 10 bold")
    other_info_textvariable = str()
    other_info_label = ttk.Label(master=video_details_frame, text="", font="Calibri 10 bold")
    for info in other_info.keys():
        other_info_textvariable = other_info_textvariable + "\n" + f"{info}: {other_info[info]}"
    other_info_label.config(text=other_info_textvariable)
    resolutions_dropdown_value = ttk.StringVar()
    temp_label = ttk.Label(master=video_details_frame, text="")
    temp_label2 = ttk.Label(master=video_details_frame, text="")
    resolutions_dropdown = ttk.Combobox(master=video_details_frame, textvariable=resolutions_dropdown_value,
                                        values=sorted(resolutions), state="readonly")
    download_button = ttk.Button(master=video_details_frame, text="Download", command=download)
    download_message = ttk.Label(master=app, text="")
    # download_button = ttk.Button(master=app, text="Download", command=download, width=45)

    detail_app_title.pack()
    thumbnail_img.pack()
    thumbnail_img.image = thumbnail
    video_title_label.pack()
    other_info_label.pack()
    temp_label.pack(side="left", padx=78)
    temp_label2.pack(side="right", padx=78)
    resolutions_dropdown.pack(side="left")  # place(x=150,y=395)
    download_button.pack(side="left")
    video_details_frame.pack(pady=3)
    download_message.pack()


input_widgets_frame = ttk.Frame(master=app)
yt_logo = ImageTk.PhotoImage(
    PIL.Image.open(resource_path("C:\\Users\\HP\\PycharmProjects\\RevisingPython\\dist\\Assets\\yt_logo.png")).resize(
        (275, 190)))
yt_logo_label = ttk.Label(image=yt_logo)
watermark = ttk.Label(master=app, text="AtonX", font="Calibri 7 bold")
app_title = ttk.Label(master=input_widgets_frame, text="YouTube Video Downloader", font="Calibri 30 bold")
urlText = ttk.StringVar()
url = ttk.Entry(master=input_widgets_frame, width=30, textvariable=urlText, font="Calibri 15 ", )
find_button = ttk.Button(master=input_widgets_frame, text="Search", command=get_video_details, width=48)
message_label = ttk.Label(master=input_widgets_frame, text="", foreground="red")
yt_logo_label.pack()
yt_logo_label.image = yt_logo
watermark.place(x=707, y=0)
app_title.pack()
url.pack()
find_button.pack()
message_label.pack(pady=1)
input_widgets_frame.pack(pady=10)
app.mainloop()