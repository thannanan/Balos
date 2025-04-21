import streamlit as st

Set page config

st.set_page_config(page_title="Club Reservation", layout="centered")

st.markdown("""

<style>
    .stButton>button {
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stTextInput>div>input {
        border-radius: 12px;
    }
    .stNumberInput>div>input {
        border-radius: 12px;
    }
    .stSelectbox>div>div {
        border-radius: 12px;
    }
    .info-box {
        border-radius: 12px;
        background-color: #f0f2f6;
        padding: 10px;
        margin-top: 10px;
    }
    .info-box.red {
        background-color: #ffcccc;
    }
</style>""", unsafe_allow_html=True)

st.title("Club Reservation")

Initialize session state

if "couches" not in st.session_state: st.session_state.couches = 10 if "seats" not in st.session_state: st.session_state.seats = 30

Reservation form

choice = st.selectbox("What would you like to reserve?", ["Couch", "Seat"]) name = st.text_input("Your Name")

if st.button("Reserve"): if not name.strip(): st.error("Please enter your name.") elif choice == "Couch" and st.session_state.couches > 0: st.session_state.couches -= 1 st.success(f"Couch reserved for {name}. Total cost: 2 euros extra.") elif choice == "Seat" and st.session_state.seats > 0: st.session_state.seats -= 1 st.success(f"Seat reserved for {name}. Total cost: 2 euros extra.") else: st.error("No available reservations left for selected type.")

Info box color based on availability

if st.session_state.couches == 0 and st.session_state.seats == 0: box_class = "info-box red" else: box_class = "info-box"

st.markdown(f'<div class="{box_class}">Reservation costs an additional 2 euros.</div>', unsafe_allow_html=True)

Secret admin panel to change seat and couch availability

code = st.text_input("Enter secret code (admin only)", type="password") if code == "gogolis": new_couches = st.number_input("Set total number of couches", min_value=0, value=st.session_state.couches + (0 if choice != "Couch" else 1), key="admin_couches") new_seats = st.number_input("Set total number of seats", min_value=0, value=st.session_state.seats + (0 if choice != "Seat" else 1), key="admin_seats") if st.button("Update Availability"): st.session_state.couches = new_couches st.session_state.seats = new_seats st.success("Availability updated.")

