import streamlit as st
import subprocess
import sys
from pathlib import Path

# just messing around likely wqont be a used file at all

st.title("Boggle Streamlit Launcher")
st.write(
    "This page lets you launch the native `raylib` Boggle game (`board.py`) from Streamlit. "
    "The game will open in a separate desktop window."
)

root = Path(__file__).resolve().parent
board_path = root / "board.py"

if not board_path.exists():
    st.error(f"Could not find `board.py` in {root}")
else:
    st.markdown("### Launch the Boggle game")
    if st.button("Open Boggle Window"):
        try:
            creationflags = subprocess.CREATE_NEW_CONSOLE if sys.platform.startswith("win") else 0
            subprocess.Popen(
                [sys.executable, str(board_path)],
                cwd=str(root),
                creationflags=creationflags,
            )
            st.success("Launched the Boggle app. Check your desktop for the raylib window.")
        except Exception as exc:
            st.error(f"Failed to launch board.py: {exc}")

    st.markdown(
        "---\n"
        "#### Notes:\n"
        "- This does not embed `raylib` inside Streamlit. `raylib` runs in its own native window.\n"
        "- Make sure Streamlit and `pyray` are installed in the same Python environment.\n"
        "- Run this app with `python -m streamlit run streamlit_boggle.py` from the Boggle folder."
    )

    st.write("If the window does not appear, try launching `python board.py` directly from the same folder.")
