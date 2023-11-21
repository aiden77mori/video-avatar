import streamlit as st
import requests
from dotenv import load_dotenv
import time

# Load variables from .env file
load_dotenv()

avatarlist = {
    "Male": "https://www.thesun.co.uk/wp-content/uploads/2021/10/2394f46a-c64f-4019-80bd-445dacda2880.jpg?w=670",
    "Female": "https://create-images-results.d-id.com/DefaultPresenters/Noelle_f/image.jpeg"
}

# Function to generate video based on the prompt and avatar selection
def generate_video(prompt, avatar_url, gender):
    url = "https://api.d-id.com/talks"
    headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik53ek53TmV1R3ptcFZTQjNVZ0J4ZyJ9.eyJodHRwczovL2QtaWQuY29tL2ZlYXR1cmVzIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9zdHJpcGVfcHJvZHVjdF9pZCI6IiIsImh0dHBzOi8vZC1pZC5jb20vc3RyaXBlX2N1c3RvbWVyX2lkIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9zdHJpcGVfcHJvZHVjdF9uYW1lIjoidHJpYWwiLCJodHRwczovL2QtaWQuY29tL3N0cmlwZV9zdWJzY3JpcHRpb25faWQiOiIiLCJodHRwczovL2QtaWQuY29tL3N0cmlwZV9iaWxsaW5nX2ludGVydmFsIjoibW9udGgiLCJodHRwczovL2QtaWQuY29tL3N0cmlwZV9wbGFuX2dyb3VwIjoiZGVpZC10cmlhbCIsImh0dHBzOi8vZC1pZC5jb20vc3RyaXBlX3ByaWNlX2lkIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9zdHJpcGVfcHJpY2VfY3JlZGl0cyI6IiIsImh0dHBzOi8vZC1pZC5jb20vY2hhdF9zdHJpcGVfc3Vic2NyaXB0aW9uX2lkIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9jaGF0X3N0cmlwZV9wcmljZV9jcmVkaXRzIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9jaGF0X3N0cmlwZV9wcmljZV9pZCI6IiIsImh0dHBzOi8vZC1pZC5jb20vcHJvdmlkZXIiOiJnb29nbGUtb2F1dGgyIiwiaHR0cHM6Ly9kLWlkLmNvbS9pc19uZXciOmZhbHNlLCJodHRwczovL2QtaWQuY29tL2FwaV9rZXlfbW9kaWZpZWRfYXQiOiIyMDIzLTExLTIxVDA3OjA3OjUyLjI5OFoiLCJodHRwczovL2QtaWQuY29tL29yZ19pZCI6IiIsImh0dHBzOi8vZC1pZC5jb20vYXBwc192aXNpdGVkIjpbIlN0dWRpbyJdLCJodHRwczovL2QtaWQuY29tL2N4X2xvZ2ljX2lkIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9jcmVhdGlvbl90aW1lc3RhbXAiOiIyMDIzLTExLTIxVDA2OjU5OjIyLjIxM1oiLCJodHRwczovL2QtaWQuY29tL2FwaV9nYXRld2F5X2tleV9pZCI6InJpMzBlZDkxd2giLCJodHRwczovL2QtaWQuY29tL2hhc2hfa2V5IjoiVHVNaTZPU2JDOU5KeGJ2NjNEZi01IiwiaHR0cHM6Ly9kLWlkLmNvbS9wcmltYXJ5Ijp0cnVlLCJodHRwczovL2QtaWQuY29tL2VtYWlsIjoiZGFuaWxscHBpb250MTA2QGdtYWlsLmNvbSIsImh0dHBzOi8vZC1pZC5jb20vc3R1ZGlvX3BsYW5fb3JpZ2luIjoid2ViIiwiaHR0cHM6Ly9kLWlkLmNvbS9zaWdudXBfb3JpZ2luIjoid2ViIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLmQtaWQuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTEzNDgwNTMyMzIxOTQ1ODEyMDI1IiwiYXVkIjpbImh0dHBzOi8vZC1pZC51cy5hdXRoMC5jb20vYXBpL3YyLyIsImh0dHBzOi8vZC1pZC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzAwNTU3MTg3LCJleHAiOjE3MDA2NDM1ODcsImF6cCI6Ikd6ck5JMU9yZTlGTTNFZURSZjNtM3ozVFN3MEpsUllxIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCByZWFkOmN1cnJlbnRfdXNlciB1cGRhdGU6Y3VycmVudF91c2VyX21ldGFkYXRhIG9mZmxpbmVfYWNjZXNzIn0.yNljabM0dSR9-_G5XqNvDwudXZaVuuO9Tjr12yGdhzZgQ38qD2BRjsMrnJ1H6oP7HFtCtd0pbpu7F5YNc0vYeGJDYgyJUNX1bHO3SREpy7ljVkxE-hODo5Ok3kfHsKCOrjhJaA7q7yXD2O5GkPSjr2FsD24b5kShisLa8qknhyQmXHuCQcB75yJP0J1_gr4M9rLZg5qK67AcocwLMIuPY-ih4nKmbSXbC592bHZKb3Vz54L2C4YxC0dQZjC__5rARo4d9YT3mEb_IQec2Bh6Ru-g2525SjzRtp9hVAQSLr6SB94nH4RBSnDxfAn7Fwo17QY0EbHanKwKOczraGuC0g"
    }
    if gender == "Female":
        payload = {
            "script": {
                "type": "text",
                "subtitles": "false",
                "provider": {
                    "type": "microsoft",
                    "voice_id": "en-US-JennyNeural"
                },
                "ssml": "false",
                "input":prompt
            },
            "config": {
                "fluent": "false",
                "pad_audio": "0.0"
            },
            "source_url": avatar_url
        }
    if gender == "Male":
        payload = {
            "script": {
                "type": "text",
                "subtitles": "false",
                "provider": {
                    "type": "microsoft",
                    "voice_id": "en-US-BrandonNeural"
                },
                "ssml": "false",
                "input":prompt
            },
            "config": {
                "fluent": "false",
                "pad_audio": "0.0"
            },
            "source_url": avatar_url
        }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            print(response.text)
            res = response.json()
            id = res["id"]
            status = "created"
            while status == "created":
                getresponse =  requests.get(f"{url}/{id}", headers=headers)
                print(getresponse)
                if getresponse.status_code == 200:
                    status = res["status"]
                    res = getresponse.json()
                    print(res)
                    if res["status"] == "done":
                        video_url =  res["result_url"]
                    else:
                        time.sleep(10)
                else:
                    status = "error"
                    video_url = "error"
        else:
            video_url = "error"   
    except Exception as e:
        print(e)      
        video_url = "error"      
        
    return video_url

def main():
    st.set_page_config(page_title="Avatar Video Generator", page_icon=":movie_camera:")

    st.title("Generate Avatar Video")

    # Text prompt input
    prompt = st.text_area("Enter Text Prompt", "Once upon a time...")

    # Dropdown box for avatar selection
    avatar_options = ["Male", "Female"]
    avatar_selection = st.selectbox("Choose Avatar", avatar_options)
    avatar_url = avatarlist[avatar_selection]

    # Generate video button
    if st.button("Generate Video"):
        st.text("Generating video...")
        try:
            video_url = generate_video(prompt, avatar_url, avatar_selection)  # Call your video generation function here
            if video_url!= "error":
                st.text("Video generated!")

                # Placeholder for displaying generated video
                st.subheader("Generated Video")
                st.video(video_url)  # Replace with the actual path
            else:
                st.text("Sorry... Try again")
        except Exception as e:
            print(e)
            st.text("Sorry... Try again")


if __name__ == "__main__":
    main()
