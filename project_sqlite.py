import sqlite3
import time
import json
import os

conn = sqlite3.connect('Youtube_videos.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,            
        time TEXT NOT NULL, 
        video_link TEXT NOT NULL, 
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,                 
        updated_at DATETIME NULL                   
    )
''')
def list_all_videos():
    cursor.execute("SELECT * FROM videos")
    print('\n')
    print('*' * 70)
    for row in cursor.fetchall():
        print(f"id: {row[0]}, Name: {row[1]},  Time: {row[2]}, Link: {row[3]}")
    print('*' * 70)

def add_video(name, time, video_link):
    cursor.execute("INSERT INTO videos (name, time, video_link) VALUES (?, ?, ?)", (name, time, video_link))
    conn.commit()
    
def update_video(id, name, time, video_link, current_timestamp):
    cursor.execute("UPDATE videos SET name = ?, time = ?, video_link = ? updated_at = ? WHERE id = ?", (name, time, video_link, current_timestamp, id))
    conn.commit()

def delete_video(id):
    cursor.execute("DELETE FROM videos WHERE id = ?", (id,))
    conn.commit()

def check_video(video_name, video_time):
    cursor.execute("SELECT name, time FROM videos WHERE name = ? AND time = ?", (video_name,video_time,))
    video = cursor.fetchone()
    if video:
        return video
    else:
        return False


def add_videos_by_file(file_name, file_path):
    videos = read_file(file_name, file_path)
    if not read_file:
        return "Please Provide a valid json file." 
    else:
        if not isinstance(videos, list):
            raise TypeError("Expected videos to be a list")
        
        for index ,video in enumerate(videos, start = 1):
            # print(f"{index}: Name: {video['name']}, Duration: {video['time']}")
            check_video_existance = check_video(video['name'], video['time'])
            if check_video_existance:
                print(f"{index}: Video with same name: {check_video_existance[0]} and time: {check_video_existance[1]} already exists")
                # return False
            else:
                add_video(video['name'],video['time'], video['video_link'])
            

def read_file(file_name, file_path):
    # Creating full path
    full_path = os.path.join(file_path, file_name)

    # *****Error Handeling******
    # Check whether directory exists
    if not os.path.isdir(file_path):
        print(f"Directory not found: {file_path}")
        return False

    # Handle file existence
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        return False
    
    if file_path in ('', '.'):
        full_path = file_name
    else:
        full_path = os.path.join(file_path, file_name)
        
    try:
        # File read start
        with open(full_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("File not found:", full_path)
        return []
    except json.JSONDecodeError:
        print("File exists but contains invalid JSON.")
        return []
    except Exception as e:
        print("An unexpected error occurred:", e)
        return []

    
def main():
    while True:
        print("\n Youtube Video App || Choose Option")
        print(" 1. List All Videos")
        print(" 2. Add Video")
        print(" 3. Update Video")
        print(" 4. Delete Video")
        print(" 5. Add videos by file")
        print(" 6. Exit App")
    
        choice = input("Enter Your Choice: ")

        match choice:   
            case '1':
                list_all_videos()

            case '2':
                video_name = input('Enter Video Name: ')
                video_time = input('Enter Video Time: ')
                video_link = input('Enter Video link: ')
                add_video(video_name, video_time, video_link)

            case '3':
                id = int(input('Enter Video Id: '))
                video_name = input('Enter Video Video Name: ')
                video_time = input('Enter Video Video Time: ')
                video_link = input('Enter Video Video Link: ')
                # Local time in SQLite CURRENT_TIMESTAMP format
                current_timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                update_video(id, video_name, video_time, video_link, current_timestamp)
            case '4':
                id = int(input('Enter Video Id: '))
                delete_video(id)
            case '5':
                print("* Please provide a json file")
                file_name = input("Please enter file name: ").strip()
                file_path = input("Enter path or '.' for current folder: ").strip()
                add_videos_by_file(file_name, file_path)
            case '6':
                break
            case _ :
                print('Invalid Choice')

    conn.close()

if __name__ == "__main__":
    main()