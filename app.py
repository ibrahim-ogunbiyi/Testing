import streamlit as st

st.title("Digital Health Portal Study")
st.write("Thank you for agreeing to take part in this research.")
st.write("Please click the button below to proceed to the survey. The survey will open in a new tab.")

# Define your Microsoft Forms links
positive_form = "https://forms.office.com/pages/responsepage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAMAABWgDfdUREc3Q1hWQTQ5MlZBNEgxRTNPUUFVMkVTTi4u&origin=lprLink&route=shorturl"
negative_form = "https://forms.office.com/pages/responsepage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAMAABWgDfdUMkVOVjRYMThIMllRWVZFT0xUN1RUWEM4Ni4u&origin=lprLink&route=shorturl"
neutral_form = "https://forms.office.com/pages/responsepage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAMAABWgDfdUM1Q4VU9JNjQxWE9KSVI5UlgzMFBCV0dJRy4u&origin=lprLink&route=shorturl"

# Put the links into a list
form_links = [positive_form, negative_form, neutral_form]

# Create a global counter that persists across all visitors
@st.cache_resource
def get_assignment_tracker():
    return {"current_index": 0}

tracker = get_assignment_tracker()

# Assign the link sequentially to guarantee equal groups
if 'assigned_link' not in st.session_state:
    # Determine the form based on the current index (0, 1, or 2)
    form_index = tracker["current_index"] % 3
    st.session_state.assigned_link = form_links[form_index]
    
    # Move the tracker forward for the next visitor
    tracker["current_index"] += 1

# Create a button that directs the user to their assigned form
st.link_button("Start Survey", st.session_state.assigned_link)
