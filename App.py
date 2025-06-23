import streamlit as st

# Set page config
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
    </style>
""", unsafe_allow_html=True)

st.title("Club Reservation")

# Initialize session state
if "couches" not in st.session_state:
    st.session_state.couches = 10
if "seats" not in st.session_state:
    st.session_state.seats = 30

if "reservations" not in st.session_state:
    st.session_state.reservations = {"Couch": [], "Seat": []}

# Reservation form
choice = st.selectbox("What would you like to reserve?", ["Couch", "Seat"])
name = st.text_input("Your Name")

if st.button("Reserve"):
    if not name.strip():
        st.error("Please enter your name.")
    elif choice == "Couch" and st.session_state.couches > 0:
        st.session_state.couches -= 1
        st.session_state.reservations["Couch"].append(name)
        st.success(f"Couch reserved for {name}. Total cost: 2 euros extra.")
    elif choice == "Seat" and st.session_state.seats > 0:
        st.session_state.seats -= 1
        st.session_state.reservations["Seat"].append(name)
        st.success(f"Seat reserved for {name}. Total cost: 2 euros extra.")
    else:
        st.error("No available reservations left for selected type.")

# Display reservation summary
st.subheader("Reserved Seats and Couches")

if len(st.session_state.reservations["Couch"]) > 0:
    st.write("### Couches Reserved:")
    for person in st.session_state.reservations["Couch"]:
        st.write(f"- {person}")

if len(st.session_state.reservations["Seat"]) > 0:
    st.write("### Seats Reserved:")
    for person in st.session_state.reservations["Seat"]:
        st.write(f"- {person}")

# Info box color based on availability
if st.session_state.couches == 0 and st.session_state.seats == 0:
    box_class = "info-box red"
else:
    box_class = "info-box"

st.markdown(f'<div class="{box_class}">Reservation costs an additional 2 euros.</div>', unsafe_allow_html=True)

# --- Hidden Admin Section ---
code = st.text_input("Enter secret code (admin only)", type="password", label_visibility="collapsed", placeholder="Enter admin code")

if code == "gogolis":
    st.header("🔐 Admin Panel")

    # Show all reservations by type
    st.write("### 🧾 Reservation List")

    for category in ["Couch", "Seat"]:
        st.write(f"**{category}s ({len(st.session_state.reservations[category])}):**")
        for i, person in enumerate(st.session_state.reservations[category], start=1):
            st.write(f"{i}. {person}")

    # Update availability
    st.write("### 🛠️ Update Availability")
    new_couches = st.number_input("Set total number of couches", min_value=0, value=st.session_state.couches, key="admin_couches")
    new_seats = st.number_input("Set total number of seats", min_value=0, value=st.session_state.seats, key="admin_seats")

    if st.button("Update Availability"):
        st.session_state.couches = new_couches
        st.session_state.seats = new_seats
        st.success("Availability updated.")
