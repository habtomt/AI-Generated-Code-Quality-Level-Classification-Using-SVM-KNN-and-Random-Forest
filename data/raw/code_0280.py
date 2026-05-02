import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration, WebRtcMode
import av

# Configuration for NAT traversal (Google's public STUN servers)
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

def main():
    st.set_page_config(page_title="Open-Source Video Conf", layout="wide")
    
    st.title("🚀 Real-Time Video Conference")
    st.sidebar.header("Participant Management")
    
    # --- UI Layout ---
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("Live Feed")
        # WebRTC Streamer - Handles video/audio transport via UDP
        webrtc_ctx = webrtc_streamer(
            key="video-conf",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=RTC_CONFIGURATION,
            media_stream_constraints={
                "video": True,
                "audio": True,
            },
            async_processing=True,
        )

    with col2:
        st.subheader("Chat & Features")
        
        # Simple Participant Management Simulation
        username = st.text_input("Display Name", value="Junior_Dev")
        if webrtc_ctx.state.playing:
            st.success(f"Connected as: {username}")
        else:
            st.warning("Offline")

        # Chat Feature
        st.write("---")
        if "messages" not in st.session_state:
            st.session_state.messages = []

        chat_input = st.text_input("Message", key="chat_input")
        if st.button("Send"):
            st.session_state.messages.append(f"{username}: {chat_input}")

        st.text_area("Room Chat", 
                     value="\n".join(st.session_state.messages), 
                     height=300)

    # --- Screen Sharing Toggle ---
    st.sidebar.write("---")
    st.sidebar.info(
        "To Share Screen: Use the built-in browser media selector "
        "when the 'Start' button is pressed."
    )

if __name__ == "__main__":
    main()