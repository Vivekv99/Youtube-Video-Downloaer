import tkinter as tk
from tkinter import ttk, messagebox
from pytube import YouTube
import threading

def fetch_video_info():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube video URL.")
        return

    try:
        yt = YouTube(url)
        title_var.set(yt.title)
        author_var.set(yt.author)
        length_var.set(f"{yt.length // 60} min {yt.length % 60} sec")
        views_var.set(f"{yt.views:,} views")
        date_var.set(yt.publish_date.strftime("%Y-%m-%d"))

        resolutions = list(set([stream.resolution for stream in yt.streams.filter(progressive=True, file_extension='mp4') if stream.resolution]))
        resolutions.sort(key=lambda x: int(x.replace("p", "")))
        resolution_menu['values'] = resolutions

        if resolutions:
            resolution_menu.current(0)
        else:
            resolution_menu.set('No resolutions')

        download_button.config(state='normal')

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch video info: {str(e)}")

def start_fetch_thread():
    threading.Thread(target=fetch_video_info, daemon=True).start()

def download_video():
    url = url_entry.get()
    resolution = resolution_menu.get()

    if not resolution or resolution == 'No resolutions':
        messagebox.showwarning("Warning", "Please select a valid resolution.")
        return

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()
        if stream:
            stream.download()
            messagebox.showinfo("Success", f"Video downloaded successfully in {resolution}.")
        else:
            messagebox.showerror("Error", f"Could not find video stream with resolution {resolution}.")
    except Exception as e:
        messagebox.showerror("Error", f"Download failed: {str(e)}")

# UI Setup
root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("600x400")
root.configure(bg="#f8f9fa")

style = ttk.Style()
style.configure("TLabel", background="#f8f9fa", font=("Segoe UI", 10))
style.configure("TEntry", padding=5)
style.configure("TButton", padding=5)
style.configure("TCombobox", padding=5)

url_label = ttk.Label(root, text="YouTube URL:")
url_label.pack(pady=(20, 5))
url_entry = ttk.Entry(root, width=70)
url_entry.pack()

fetch_button = ttk.Button(root, text="Fetch Info", command=start_fetch_thread)
fetch_button.pack(pady=10)

info_frame = ttk.Frame(root)
info_frame.pack(pady=10)

title_var = tk.StringVar()
author_var = tk.StringVar()
length_var = tk.StringVar()
views_var = tk.StringVar()
date_var = tk.StringVar()

for label, var in zip(["Title", "Author", "Duration", "Views", "Published"],
                      [title_var, author_var, length_var, views_var, date_var]):
    row = ttk.Frame(info_frame)
    row.pack(fill='x', pady=2)
    ttk.Label(row, text=f"{label}:", width=15).pack(side='left')
    ttk.Label(row, textvariable=var).pack(side='left')

resolution_label = ttk.Label(root, text="Select Resolution:")
resolution_label.pack(pady=(20, 5))
resolution_menu = ttk.Combobox(root, state="readonly")
resolution_menu.pack()

download_button = ttk.Button(root, text="Download Video", command=download_video, state='disabled')
download_button.pack(pady=20)

root.mainloop()

# Run the GUI
if __name__ == "__main__":
    create_gui()
