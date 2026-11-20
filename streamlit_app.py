import uuid

import pandas as pd
import streamlit as st

from config import settings
from app.graph import build_graph
from app.nodes import load_sent_emails

st.set_page_config(page_title="Job Emails Sender", layout="wide")
st.title("Automated Job Emails Sender")

# ---------- Sidebar: run settings ----------
with st.sidebar:
    st.header("Run settings")
    max_posts = st.number_input(
        "Max posts to scrape", min_value=1, max_value=30, value=10, step=1
    )
    run_clicked = st.button("Run", type="primary")

    st.divider()
    if settings.DRY_RUN:
        st.info("DRY_RUN is on: emails are printed in the terminal, nothing is sent.")
    else:
        st.warning("DRY_RUN is off: this run will send real emails.")

# ---------- Run the graph ----------
if run_clicked:
    with st.spinner(f"Scraping and scanning up to {int(max_posts)} posts..."):
        try:
            graph = build_graph()
            result = graph.invoke(
                {"maxposts": int(max_posts), "unique_email": load_sent_emails()},
                config={
                    "configurable": {"thread_id": str(uuid.uuid4())},
                    "recursion_limit": int(max_posts) * 5 + 10,
                },
            )
            st.session_state["result"] = result
        except Exception as e:
            st.session_state.pop("result", None)
            st.error(f"Run failed: {e}")



# ---------- Results ----------
result = st.session_state.get("result")

if result:
    relevant = result.get("total_relevant_jobs", [])
    skipped = result.get("total_irrelevant", [])

    c1, c2, c3 = st.columns(3)
    c1.metric("Posts scanned", result.get("count_scraped_posts", 0))
    c2.metric("Relevant jobs", len(relevant))
    c3.metric("Skipped jobs", len(skipped))

    st.subheader("Relevant jobs")
    st.subheader("1. Email")
    if relevant:
        base = pd.DataFrame(relevant)

        df = base[base["contact_email"].notna()].reset_index(drop=True)
        columns = [
            "company",
            "role",
            "location",
            "min_experience_years",
            "contact_email",
            "application_requirements",
        ]
        df.index += 1
        st.dataframe(
            df[columns],
            hide_index=False,
            column_config={"apply_link": st.column_config.LinkColumn("apply_link")},
        )


        st.subheader("2. Link")
        df = base[base["apply_link"].notna()].reset_index(drop=True)
        columns = [
            "company",
            "role",
            "location",
            "min_experience_years",
            "apply_link",
            "application_requirements",
        ]
        df.index += 1
        st.dataframe(
            df[columns],
            hide_index=False,
            column_config={"apply_link": st.column_config.LinkColumn("apply_link")},
        )


        st.subheader("3. Whatsapp")
        df = base[base["whatsapp_or_phone"].notna()].reset_index(drop=True)
        columns = [
            "company",
            "role",
            "location",
            "min_experience_years",
            "whatsapp_or_phone",
            "application_requirements",
        ]
        df.index += 1
        st.dataframe(
            df[columns],
            hide_index=False,
        )


        st.subheader("4. Linkedin DM")
        df = base[base["is_dm_on_linkedin"] == True].reset_index(drop=True)
        columns = [
            "company",
            "role",
            "location",
            "min_experience_years",
            "is_dm_on_linkedin",
            "application_requirements",
        ]
        df.index += 1
        st.dataframe(
            df[columns],
            hide_index=False,
        )

    else:
        st.info("No relevant jobs found in this run.")

    st.subheader("Rejected_jobs")
    if skipped:
        df1 = pd.DataFrame(skipped)
        columns = [
            "company",
            "reason",
            "role",
            "application_requirements",
            "location",
            "min_experience_years",
        ]
        df1.index += 1
        st.dataframe(
            df1[columns],
            hide_index=False,
        )
    else:
        st.info("No jobs Rejected")

elif not run_clicked:
    st.caption("Set the max posts in the sidebar and press Run.")