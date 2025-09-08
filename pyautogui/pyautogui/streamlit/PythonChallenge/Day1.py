import streamlit as st
import pandas as pd
import uuid
import io
from datetime import date

# Title and description
st.set_page_config(page_title="GenAI Workshop Registration", layout="wide")
st.title("🚀 GenAI Workshop — Registration & Prework Intake")
st.markdown("Fill this form to register for the upcoming GenAI hands-on workshop. The data you provide will help us tailor the sessions and prework materials.")

# Helper functions

def _generate_access_code():
    return str(uuid.uuid4()).split('-')[0].upper()


def _validate_email(email: str) -> bool:
    return "@" in email and "." in email


def _save_submission(df: pd.DataFrame, filename: str = "submissions.csv"):
    try:
        existing = pd.read_csv(filename)
        merged = pd.concat([existing, df], ignore_index=True)
    except FileNotFoundError:
        merged = df
    merged.to_csv(filename, index=False)

# Layout: two columns for nicer UI
col1, col2 = st.columns([2, 1])

with col1:
    with st.form("registration_form"):
        st.header("Personal & Contact")
        name = st.text_input("Full name", placeholder="e.g. Priya Kumar")
        email = st.text_input("Email address", placeholder="you@company.com")
        linkedin = st.text_input("LinkedIn / GitHub (optional)")

        st.markdown("---")
        st.header("Background & Preferences")
        role = st.selectbox("Current role", ["Student", "Developer", "Data Scientist", "Researcher", "Product Manager", "Other"])
        experience = st.slider("Years of experience in programming/ML", 0, 20, 2)
        topics = st.multiselect("Topics you're most interested in (choose up to 4)",
                                ["Prompt Engineering", "Fine-tuning", "Evaluation & Metrics", "LLM Safety", "Deployments & APIs", "RAG (Retrieval-Augmented Generation)", "Tools: LangChain/AutoGPT", "Inference Optimization"],
                                help="Select what you want hands-on material for")

        st.markdown("---")
        st.header("Logistics")
        preferred_session = st.radio("Preferred session (time)", ["Morning (9–11 AM)", "Afternoon (2–4 PM)", "Evening (6–8 PM)"])
        pref_date = st.date_input("Preferred workshop date", value=date.today())
        time_slot = st.selectbox("Preferred time slot (choose one)", ["Slot A", "Slot B", "Slot C"]) 

        st.markdown("---")
        st.header("Uploads & Prework")
        profile_pic = st.file_uploader("Profile picture (optional)", type=["png", "jpg", "jpeg"])
        resume = st.file_uploader("Resume / CV (optional)", type=["pdf", "docx"])
        prior_code = st.text_area("Link to a small public repo or paste a short code snippet (optional)", height=80)

        accept_terms = st.checkbox("I consent to receive workshop materials and agree to the code of conduct.")

        submitted = st.form_submit_button("Register")

    # Post-submit handling
    if submitted:
        errors = []
        if not name.strip():
            errors.append("Name is required.")
        if not _validate_email(email):
            errors.append("Please enter a valid email.")
        if not accept_terms:
            errors.append("You must accept terms to register.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            access_code = _generate_access_code()
            summary = {
                "name": name,
                "email": email,
                "linkedin": linkedin,
                "role": role,
                "experience": experience,
                "topics": ", ".join(topics),
                "preferred_session": preferred_session,
                "preferred_date": pref_date.isoformat(),
                "time_slot": time_slot,
                "access_code": access_code
            }
            df = pd.DataFrame([summary])

            # Save to local CSV for host (in real deployment, push to DB)
            _save_submission(df, filename="submissions.csv")

            st.success(f"Thanks {name.split()[0].title()} — you're registered! 🎉")
            st.markdown(f"**Access code:** `{access_code}` — save this for joining the workshop.")
            st.write("### Your registration summary")
            st.table(df)

            # Provide a CSV download for the single submission
            csv_bytes = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download your submission (CSV)", data=csv_bytes, file_name=f"registration_{access_code}.csv")

with col2:
    st.header("Why we ask these questions")
    st.markdown("- **Topics** let us prepare focused prework and split participants into small groups.\n- **Experience** helps us tune difficulty.\n- **Uploads** let mentors review code/resumes ahead of time.")

    st.markdown("---")
    st.header("Prework checklist (recommended)")
    st.write("1. Install Python 3.11+ and create a virtual environment.\n2. Install `pip install -r requirements.txt` (we'll email this).\n3. Bring a laptop with Wi‑Fi and admin rights.\n4. If using Google Colab, ensure your GitHub repo is public or share a link.")

    st.markdown("---")
    st.header("Quick tips for participants")
    st.info("If you're new to LLMs: focus on prompts and evaluation. If you're experienced: pick a topic like fine-tuning or deployment for the group project.")

    st.markdown("---")
    st.caption("App generated for Day 1 of the 15-day challenge — adapt or extend for team registration, automated emails, or Zoom integration.")
