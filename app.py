import secrets
import streamlit as st
from supabase import create_client

st.set_page_config(
    page_title="Digital Health Information Study",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    font-weight: bold;
}
.sub-header {
    font-size: 1.2rem;
    text-align: center;
    color: #555555;
    margin-bottom: 2rem;
}
.code-box {
    padding: 1rem;
    border: 2px solid #1f77b4;
    border-radius: 10px;
    text-align: center;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

positive_form = "https://forms.office.com/pages/responsepage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAMAABWgDfdUREc3Q1hWQTQ5MlZBNEgxRTNPUUFVMkVTTi4u&origin=lprLink&route=shorturl"
negative_form = "https://forms.office.com/pages/responsepage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAMAABWgDfdUMkVOVjRYMThIMllRWVZFT0xUN1RUWEM4Ni4u&origin=lprLink&route=shorturl"
neutral_form = "https://forms.office.com/pages/responsepage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAMAABWgDfdUM1Q4VU9JNjQxWE9KSVI5UlgzMFBCV0dJRy4u&origin=lprLink&route=shorturl"

form_links = {
    "Positive": positive_form,
    "Negative": negative_form,
    "Neutral": neutral_form
}

@st.cache_resource
def connect_to_supabase():
    return create_client(
        st.secrets["supabase"]["url"],
        st.secrets["supabase"]["service_role_key"]
    )

try:
    supabase = connect_to_supabase()
except Exception:
    st.error(
        "The study database could not be connected. "
        "Please contact the researcher or try again later."
    )
    st.stop()

def generate_participant_code():
    characters = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    random_part = "".join(secrets.choice(characters) for _ in range(8))
    return f"DH-{random_part}"

def get_assignment(participant_code):
    result = (
        supabase.table("participant_assignments")
        .select("participant_code, assigned_condition, status")
        .eq("participant_code", participant_code)
        .limit(1)
        .execute()
    )

    if result.data:
        return result.data[0]

    return None

def create_assignment():
    for _ in range(10):
        participant_code = generate_participant_code()

        try:
            result = supabase.rpc(
                "assign_participant",
                {"p_code": participant_code}
            ).execute()

            if result.data:
                record = result.data[0]

                return {
                    "participant_code": record["participant_code"],
                    "assigned_condition": record["assigned_condition"],
                    "status": "assigned"
                }

        except Exception:
            continue

    raise RuntimeError("Unable to generate a unique participant assignment.")

def restore_assignment_from_url():
    participant_code = st.query_params.get("code", "").strip().upper()

    if not participant_code:
        return

    try:
        assignment = get_assignment(participant_code)
    except Exception:
        st.warning(
            "Your previous assignment could not be restored. "
            "Please refresh the page."
        )
        return

    if assignment:
        st.session_state.participant_code = assignment["participant_code"]
        st.session_state.assigned_condition = assignment["assigned_condition"]
        st.session_state.assignment_status = assignment["status"]
    else:
        try:
            del st.query_params["code"]
        except Exception:
            pass

        st.warning(
            "The participant code in this link is invalid. "
            "A new code can be generated after you provide consent."
        )

if "participant_code" not in st.session_state:
    restore_assignment_from_url()

st.markdown(
    '<div class="main-header">Digital Health Information Study</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-header">'
    'Understanding how people respond to information provided by digital health services'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "Thank you for your interest in this research. "
    "Please read the Participant Information Sheet before continuing."
)

with st.expander(
    "Participant Information Sheet: Please click to open and read",
    expanded=False
):
    st.markdown("### What is the purpose of the study?")

    st.write(
        "This study examines how people interpret information provided by "
        "digital health services and how this information affects their views "
        "about using such services. You will be shown a short scenario about "
        "a digital health portal and asked to provide your views about it."
    )

    st.markdown("### Why have I been invited to take part?")

    st.write(
        "You may take part if you meet all the following criteria:"
    )

    st.markdown("""
- You are aged 18 years or above.
- You can read and understand English.
- You are capable of making your own decisions.
- You have experience using at least one digital service, such as social media, a health application or online banking.
- You have internet access to complete the survey.
""")

    st.markdown("### Do I have to take part?")

    st.write(
        "Participation is voluntary. You are under no obligation to take part "
        "and will not experience any penalty or loss of benefit if you choose "
        "not to participate. You may stop completing the study at any point "
        "before submitting your survey response."
    )

    st.markdown("### What will I have to do?")

    st.write(
        "You will be asked to complete a short online survey. You will read "
        "a scenario about a digital health portal and answer questions about "
        "your views of the portal and your willingness to share personal "
        "health data. You will also answer a small number of demographic "
        "questions. The survey should take approximately 10 to 15 minutes "
        "and should only be completed once. There are no right or wrong answers."
    )

    st.markdown("### Participant code")

    st.write(
        "After providing consent, you will be allocated a unique anonymous "
        "participant code. The code will determine which version of the survey "
        "you receive. You must enter this code into the first question of the "
        "Microsoft Form. The code does not contain your name or personal details."
    )

    st.markdown("### Confidentiality and data storage")

    st.write(
        "Your name will not be requested in the study. Your survey response "
        "will be connected only to your anonymous participant code. Research "
        "data will be stored securely and handled in accordance with relevant "
        "data-protection requirements and Northumbria University research policies."
    )

    st.markdown("### Contact for further information")

    st.write("**Researcher:** shekinah.ikilizi@northumbria.ac.uk")
    st.write("**Supervisor:** m.cholerzynski@northumbria.ac.uk")

st.divider()

st.markdown("### Eligibility")

eligibility = st.checkbox(
    "I confirm that I am aged 18 years or above, can understand English, "
    "and meet the participation criteria listed above.",
    key="eligibility_checkbox"
)

st.markdown("### Informed consent")

consent = st.checkbox(
    "I confirm that I have read and understood the Participant Information "
    "Sheet. I understand that participation is voluntary, and I agree to "
    "take part in this study.",
    key="consent_checkbox"
)

st.divider()

if not eligibility or not consent:
    st.warning(
        "You must confirm your eligibility and provide consent before "
        "continuing to the survey."
    )

else:
    if "participant_code" not in st.session_state:
        st.success(
            "Thank you for confirming your eligibility and consent. "
            "Select the button below to receive your survey."
        )

        if st.button(
            "Assign My Survey",
            type="primary",
            use_container_width=True
        ):
            try:
                with st.spinner("Preparing your survey..."):
                    assignment = create_assignment()

                st.session_state.participant_code = assignment["participant_code"]
                st.session_state.assigned_condition = assignment["assigned_condition"]
                st.session_state.assignment_status = assignment["status"]

                st.query_params["code"] = assignment["participant_code"]
                st.rerun()

            except Exception:
                st.error(
                    "Your survey could not be assigned. Please refresh the "
                    "page and try again. If the problem continues, contact "
                    "the researcher."
                )

    else:
        participant_code = st.session_state.participant_code
        assigned_condition = st.session_state.assigned_condition
        assignment_status = st.session_state.get(
            "assignment_status",
            "assigned"
        )

        if assignment_status == "completed":
            st.success(
                "This participant code has already been recorded as completed. "
                "Thank you for taking part."
            )
            st.stop()

        assigned_form = form_links.get(assigned_condition)

        if not assigned_form:
            st.error(
                "The assigned survey could not be found. "
                "Please contact the researcher."
            )
            st.stop()

        st.success("Your survey has been assigned successfully.")

        st.markdown("### Your participant code")

        st.code(participant_code, language=None)

        st.warning(
            "Please copy or write down this code. You must enter it exactly "
            "as shown in the first question of the Microsoft Form."
        )

        st.markdown(
            """
**Before opening the form:**

1. Copy the participant code displayed above.
2. Open the assigned survey using the button below.
3. Enter the code into the first question.
4. Complete and submit the survey only once.
5. Do not share your code or survey link with another person.
"""
        )

        st.link_button(
            "Open My Assigned Survey",
            assigned_form,
            type="primary",
            use_container_width=True
        )

        st.caption(
            "Opening the survey does not automatically submit a response. "
            "You must complete and submit the Microsoft Form."
        )
