import sqlite3
import time
conn = sqlite3.connect('Youtube_videos.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,            
        time TEXT NOT NULL, 
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,                 
        updated_at DATETIME NULL                   
    )
''')
def list_all_videos():
    cursor.execute("SELECT * FROM videos")
    print('\n')
    print('*' * 70)
    for row in cursor.fetchall():
        print(f"id: {row[0]}, Name: {row[1]},  Time: {row[2]}")
    print('*' * 70)

def add_video(name, time):
    cursor.execute("INSERT INTO videos (name, time) VALUES (?, ?)", (name, time))
    conn.commit()
    
def update_video(id, name, time, current_timestamp):
    cursor.execute("UPDATE videos SET name = ?, time = ?, updated_at = ? WHERE id = ?", (name, time, current_timestamp, id))
    conn.commit()

def delete_video(id):
    cursor.execute("DELETE FROM videos WHERE id = ?", (id,))
    conn.commit()
    
def main():
    while True:
        print("\n Youtube Video App || Choose Option")
        print(" 1. List All Videos")
        print(" 2. Add Video")
        print(" 3. Update Video")
        print(" 4. Delete Video")
        print(" 5. Exit App")
    
        choice = input("Enter Your Choice: ")

        match choice:   
            case '1':
                list_all_videos()

            case '2':
                video_name = input('Enter Video Name: ')
                video_time = input('Enter Video Time: ')
                add_video(video_name, video_time)

            case '3':
                id = int(input('Enter Video Id: '))
                video_name = input('Enter Video Video Name: ')
                video_time = input('Enter Video Video Time: ')
                # Local time in SQLite CURRENT_TIMESTAMP format
                current_timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                update_video(id, video_name, video_time, current_timestamp)
            case '4':
                id = int(input('Enter Video Id: '))
                delete_video(id)
            case '5':
                break
            case _ :
                print('Invalid Choice')

    conn.close()

if __name__ == "__main__":
    main()