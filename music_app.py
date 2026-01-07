import streamlit as st

# --- 1. โครงสร้างข้อมูล Song ---
class Song:
    def __init__(self, title, artist, audio_bytes):
        self.title = title
        self.artist = artist
        self.audio_bytes = audio_bytes
        self.next_song = None

# --- 2. ฟังก์ชันจัดการ Playlist (เชื่อมต่อกับ Session State) ---
def add_song_to_list(title, artist, audio_file):
    new_node = Song(title, artist, audio_file.read())
    if st.session_state.head is None:
        st.session_state.head = new_node
        st.session_state.current_node = new_node
    else:
        curr = st.session_state.head
        while curr.next_song:
            curr = curr.next_song
        curr.next_song = new_node
    st.session_state.total_songs += 1

def delete_song_from_list(title_to_delete):
    curr = st.session_state.head
    prev = None
    
    while curr:
        if curr.title == title_to_delete:
            if prev:
                prev.next_song = curr.next_song
            else:
                st.session_state.head = curr.next_song
            
            # หากลบเพลงที่กำลังเลือกอยู่ ให้เลื่อนไปเพลงแรก
            if st.session_state.current_node == curr:
                st.session_state.current_node = st.session_state.head
                
            st.session_state.total_songs -= 1
            return True
        prev = curr
        curr = curr.next_song
    return False

# --- 3. เริ่มต้น Session State (ป้องกันข้อมูลหายเมื่อ Refresh) ---
if 'head' not in st.session_state:
    st.session_state.head = None
    st.session_state.current_node = None
    st.session_state.total_songs = 0

# --- 4. การแสดงผลหน้าเว็บ (UI ตามรูปภาพ) ---
st.title("🎵 Music Playlist App")

# Sidebar: Add New Song
with st.sidebar:
    st.header("Add New Song")
    new_title = st.text_input("Title")
    new_artist = st.text_input("Artist")
    uploaded_file = st.file_uploader("Upload Audio File", type=['mp3', 'wav', 'ogg'])
    
    if st.button("Add Song to Playlist"):
        if new_title and uploaded_file:
            add_song_to_list(new_title, new_artist, uploaded_file)
            st.success(f"Added: {new_title}")
        else:
            st.warning("Please enter title and upload a file.")

    st.divider()
    st.header("Delete Song")
    del_title = st.text_input("Song Title to Delete")
    if st.button("Delete Song"):
        if delete_song_from_list(del_title):
            st.error(f"Deleted: {del_title}")
        else:
            st.warning("Song not found.")

# Main Area: Playlist Display
st.header("Your Current Playlist")
if st.session_state.head is None:
    st.info("Playlist is empty. Add some songs from the sidebar!")
else:
    # วนลูปแสดงรายชื่อเพลงจาก Linked List
    curr = st.session_state.head
    playlist_text = ""
    while curr:
        status = "▶️ " if curr == st.session_state.current_node else "• "
        playlist_text += f"{status} **{curr.title}** - {curr.artist}  \n"
        curr = curr.next_song
    st.write(playlist_text)

st.divider()

# Main Area: Playback Controls
st.header("Playback Controls")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⏪ Previous"):
        # หาเพลงก่อนหน้าใน Single Linked List
        if st.session_state.current_node == st.session_state.head:
            st.toast("Already at the first song")
        else:
            temp = st.session_state.head
            while temp.next_song != st.session_state.current_node:
                temp = temp.next_song
            st.session_state.current_node = temp

with col2:
    if st.button("▶️ Play Current"):
        pass # Streamlit จะเล่นเพลงจากโค้ด st.audio ด้านล่างโดยอัตโนมัติ

with col3:
    if st.button("⏩ Next"):
        if st.session_state.current_node and st.session_state.current_node.next_song:
            st.session_state.current_node = st.session_state.current_node.next_song
        else:
            st.toast("End of playlist")

# แสดงเครื่องเล่นเพลง
if st.session_state.current_node:
    st.write(f"Now Selected: **{st.session_state.current_node.title}**")
    st.audio(st.session_state.current_node.audio_bytes)
else:
    st.warning("Playlist is empty or no song is selected to play.")

st.caption(f"Total songs in playlist: {st.session_state.total_songs} song(s)")
