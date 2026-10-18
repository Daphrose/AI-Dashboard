
import sys
from pathlib import Path

import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Supermarket AI Assistant    ",
    page_icon="🛒",
    layout="wide",
)

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------


PROJECT_DIR = Path(__file__).resolve().parent
SRC_DIR = PROJECT_DIR / "src"
SQL_DIR = SRC_DIR / "sql"
RAG_DIR = SRC_DIR / "rag"

for path in [SRC_DIR, SQL_DIR, RAG_DIR]:
    path_string = str(path)

    if path_string not in sys.path:
        sys.path.insert(0, path_string)


# --------------------------------------------------
# IMPORT EXISTING AI ANALYST
# --------------------------------------------------

from sql.master_analyst import run_master_analyst

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title(" Supermarket AI Assistant")

st.markdown(
    """
    Ask questions about supermarket sales, products,
    profitability, customers, and business performance.

    Explore business knowledge and get answers based on
    your sales data.
    """
)

st.divider()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.header("AI Data Assistant")
    st.caption("Supermarket sales intelligence")

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("**Try asking:**")
    st.markdown("- What is COGS?")
    st.markdown("- Which product generated the most revenue?")
    st.markdown("- Which city had the highest profit?")
    st.markdown("- How did the business perform overall?")

# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------------------------------
# QUESTION INPUT AND AI RESPONSE
# --------------------------------------------------

question = st.chat_input(
    "Ask a question about your supermarket data..."
)

if question:
    # Display and save the user's question
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Call the existing AI pipeline
    with st.chat_message("assistant"):
        with st.spinner(
            "Analyzing your question... This may take a moment."
        ):
            try:
                answer = run_master_analyst(question)

                if not isinstance(answer, str) or not answer.strip():
                    answer = (
                        "The analyst did not return an answer. "
                        "Please try asking your question again."
                    )

            except Exception as error:
                # Detailed error stays in the terminal for debugging
                print("Streamlit AI integration error:", repr(error))

                answer = (
                    "Sorry, something went wrong while analyzing "
                    "your question. Check the VS Code terminal "
                    "for the technical error."
                )

        st.markdown(answer)

    # Save the assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )
