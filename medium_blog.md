---
title: "Building a YouTube Video Downloader with Python and Streamlit"
author: "Gemini"
date: "2026-03-21"
tags: ["Python", "Streamlit", "YouTube", "pytubefix", "GUI"]
---

# Building a YouTube Video Downloader with Python and Streamlit

Have you ever wanted to download a YouTube video for offline viewing or just to save the audio of your favorite song? In this blog post, I'll walk you through a simple yet powerful YouTube video downloader I built using Python, Streamlit, and the `pytubefix` library.

## Why I Built This

I often find myself wanting to save educational videos, tutorials, or music from YouTube to access them later without an internet connection. While there are many online tools available, I wanted a solution that was ad-free, secure, and that I could customize to my liking. Building my own downloader was a fun and rewarding project that gave me full control over the process.

## The Tech Stack

This project is built with a few key libraries:

*   **Python:** The core programming language.
*   **Streamlit:** A fantastic open-source framework for building and sharing web apps for machine learning and data science, but it's also great for creating simple and beautiful user interfaces for any Python script.
*   **pytubefix:** A lightweight, dependency-free Python library for downloading YouTube videos.

## The Core Logic: `app.py`

The main application logic resides in `app.py`. Let's break down how it works.

### 1. Getting User Input

The first step is to get the YouTube video URL from the user. Streamlit makes this incredibly easy with its `text_input` function:

```python
import streamlit as st

st.title(":red[▶️] Download Youtube video for free")
url = st.text_input("Enter the url of the YouTube video", placeholder = "Paste the url")
```

### 2. Fetching Video Information with `pytubefix`

Once we have the URL, we use `pytubefix` to create a `YouTube` object. This object gives us access to all the video's metadata, like the title and thumbnail.

```python
from pytubefix import YouTube
from pytubefix.cli import on_progress

if url:
    yt = YouTube(url, on_progress_callback = on_progress)
    st.divider()
    title = yt.title
    thumnail = yt.thumbnail_url

    st.header(f":link: {title}")
    st.image(thumnail)
```

### 3. Choosing Download Options

I wanted the user to have the flexibility to download only the audio, only the video, or both. Streamlit's `radio` button is perfect for this:

```python
video_type = st.radio("Select The Type", ["only music", "only video", "music + video"], horizontal = True)
```

The user can also select the desired quality ("low" or "high"):

```python
quality = st.radio("select the quality", ["low", "high"], horizontal = True)
```

### 4. Downloading the Content

Based on the user's selection, we filter the available streams and download the appropriate file.

For **audio-only**, we filter for audio streams and order them by their average bitrate (ABR):

```python
if video_type == 'only music':
    if quality == 'low':
        audio = yt.streams.filter(adaptive = True, only_audio = True).order_by("abr").first()
    else:
        audio = yt.streams.filter(adaptive = True, only_audio = True).order_by("abr").desc().first()
    
    if st.button("Download"):
        with st.spinner(text="Downloading.....", show_time=True):
            audio.download(filename = f"{title}_audio.mp4")
            st.success(f"Audio track ---- {title}_audio.mp4 --- downloaded successfully")
```

For **video-only**, we filter for video streams and order them by resolution:

```python
elif video_type == 'only video':
    if quality == 'low':
        video = yt.streams.filter(adaptive = True, only_video = True).order_by("resolution").first()
    else:
        video = yt.streams.filter(adaptive = True, only_video = True).order_by("resolution").desc().first()
    
    if st.button("Download"):
        with st.spinner(text="Downloading.....", show_time=True):
            video.download(filename = f"{title}_video.mp4")
            st.success(f"Video file ---- {title}_video.mp4 --- downloaded successfully")
```

For the **full video with audio**, we filter for progressive streams (which contain both video and audio):

```python
else:
    if quality == 'low':
        full_video = yt.streams.filter(progressive = True).order_by("resolution").first()
    else:
        full_video = yt.streams.filter(progressive = True).order_by("resolution").desc().first()
    
    if st.button("Download"):
        with st.spinner(text="Downloading.....", show_time=True):
            full_video.download(filename = f"{title}_video.mp4")
            st.success(f"Audio + Video ---- {title}_video.mp4 --- downloaded successfully")
```

## The User Interface

Streamlit provides a clean and intuitive user interface out of the box. The user simply pastes the YouTube URL, selects their desired options, and clicks the "Download" button. The `st.spinner` provides visual feedback during the download process.

## Running the Application

To make the application easy to run, I've included a `run_app.py` script. This script uses the `streamlit` command-line interface to run the `app.py` file.

```python
import sys
import os
import streamlit.web.cli as stcli

def get_app_path():
    if hasattr(sys, "_MEIPASS"):
        # Running inside PyInstaller bundle
        return os.path.join(sys._MEIPASS, "app.py")
    else:
        # Running normally
        return os.path.join(os.path.dirname(__file__), "app.py")

if __name__ == "__main__":
    app_path = get_app_path()
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--global.developmentMode=false",
        "--server.headless=true",
        "--browser.gatherUsageStats=false"
        ]
    sys.exit(stcli.main())
```

Besides using `run_app.py`, there are several other convenient ways to run the application:

1.  **Directly with Streamlit:** If you have Streamlit installed, you can run the main application file directly from your terminal:
    ```bash
    streamlit run app.py
    ```
    This will open the application in your default web browser.

2.  **Using the Executable (PyInstaller):** A standalone executable is generated for easier distribution. You can run it directly after building the project:
    ```bash
    ./dist/YTDownloaderApp
    ```
    This will launch the application without needing a Python environment setup.

3.  **Using Docker:** For containerized deployment, you can build and run the Docker image. First, build the image:
    ```bash
    docker build -t youtube-downloader .
    ```
    Then, run the container, mapping the port:
    ```bash
    docker run -p 8501:8501 youtube-downloader
    ```
    Access the application in your browser at `http://localhost:8501`.

## Conclusion

This project is a great example of how you can use Python and Streamlit to build useful and interactive applications with minimal effort. The `pytubefix` library makes it easy to work with YouTube videos, and Streamlit provides a simple way to create a user-friendly interface.

I encourage you to check out the project on GitHub [placeholder for GitHub link] and try it out for yourself. Feel free to fork the repository and add your own features!
