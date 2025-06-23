import streamlit as st
import random

# Set page config
st.set_page_config(page_title="Club Reservation", layout="centered")

# Custom CSS styling
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
    </style>
""", unsafe_allow_html=True)

st.title("Club Reservation")

# Initialize session state
if "couches" not in st.session_state:
    st.session_state.couches = 10
if "seats" not in st.session_state:
    st.session_state.seats = 30
if "reservations" not in st.session_state:
    st.session_state.reservations = {"Couch": [], "Seat": []}  # List of dicts: {"name": ..., "code": ...}

# Reservation form
st.subheader("Make a Reservation")
choice = st.selectbox("What would you like to reserve?", ["Couch", "Seat"])
name = st.text_input("Your Name")

if st.button("Reserve"):
    if not name.strip():
        st.error("Please enter your name.")
    else:
        unique_code = f"{random.randint(100, 999)}"

        if choice == "Couch" and st.session_state.couches > 0:
            st.session_state.couches -= 1
            st.session_state.reservations["Couch"].append({"name": name, "code": unique_code})
            st.success(f"Couch reserved for {name}. Total cost: 2 euros extra.\n\n📌 Your reservation code: **{unique_code}**\nPlease save this code to cancel your reservation later.")

        elif choice == "Seat" and st.session_state.seats > 0:
            st.session_state.seats -= 1
            st.session_state.reservations["Seat"].append({"name": name, "code": unique_code})
            st.success(f"Seat reserved for {name}. Total cost: 2 euros extra.\n\n📌 Your reservation code: **{unique_code}**\nPlease save this code to cancel your reservation later.")

        else:
            st.error("No available reservations left for selected type.")

# Display reservation summary
st.subheader("Reserved Seats and Couches")

if len(st.session_state.reservations["Couch"]) > 0:
    st.write("### Couches Reserved:")
    for res in st.session_state.reservations["Couch"]:
        st.write(f"- {res['name']}")

if len(st.session_state.reservations["Seat"]) > 0:
    st.write("### Seats Reserved:")
    for res in st.session_state.reservations["Seat"]:
        st.write(f"- {res['name']}")

# Info box for reservation cost
box_class = "info-box red" if st.session_state.couches == 0 and st.session_state.seats == 0 else "info-box"
st.markdown(f'<div class="{box_class}">Reservation costs an additional 2 euros.</div>', unsafe_allow_html=True)

# Cancel reservation
st.subheader("Cancel Reservation")
cancel_code = st.text_input("Enter your reservation code to cancel")

if st.button("Cancel Reservation"):
    found = False
    for category in ["Couch", "Seat"]:
        for res in st.session_state.reservations[category]:
            if res["code"] == cancel_code:
                st.session_state.reservations[category].remove(res)
                if category == "Couch":
                    st.session_state.couches += 1
                else:
                    st.session_state.seats += 1
                st.success(f"Reservation for {res['name']} ({category}) has been cancelled.")
                found = True
                break
        if found:
            break
    if not found:
        st.error("No reservation found with that code.")

# Admin Panel (hidden by password)
code = st.text_input("Enter secret code (admin only)", type="password", label_visibility="collapsed", placeholder="Enter admin code")

if code == "gogolis":
    st.header("🔐 Admin Panel")

    st.write("### 🧾 Reservation List")
    for category in ["Couch", "Seat"]:
        st.write(f"**{category}s ({len(st.session_state.reservations[category])}):**")
        for i, res in enumerate(st.session_state.reservations[category], start=1):
            st.write(f"{i}. {res['name']} (code: {res['code']})")

    st.write("### 🛠️ Update Availability")
    new_couches = st.number_input("Set total number of couches", min_value=0, value=st.session_state.couches, key="admin_couches")
    new_seats = st.number_input("Set total number of seats", min_value=0, value=st.session_state.seats, key="admin_seats")

    if st.button("Update Availability"):
        st.session_state.couches = new_couches
        st.session_state.seats = new_seats
        st.success("Availability updated.")
