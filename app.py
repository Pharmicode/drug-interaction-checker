import streamlit as st

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Runestone Holdings – Drug Interaction Checker",
    page_icon="💊",
    layout="centered"
)

# ---- LIGHT CSS FOR A MORE PROFESSIONAL LOOK ----
st.markdown("""
<style>
/* Constrain width */
.main > div {
    max-width: 900px;
    margin: 0 auto;
}

/* Card container */
.app-card {
    background-color: #0f172a1a; /* works in dark + light themes */
    padding: 1.4rem 1.6rem;
    border-radius: 0.9rem;
    border: 1px solid rgba(148, 163, 184, 0.4);
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.35);
    margin-bottom: 1.3rem;
}

/* Muted helper text */
.muted {
    color: #94a3b8;
    font-size: 0.9rem;
}

/* Result badges */
.result-ok {
    background: #ecfdf5;
    border-left: 4px solid #16a34a;
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;
    color: #14532d;
    font-size: 0.95rem;
}
.result-info {
    background: #eff6ff;
    border-left: 4px solid #2563eb;
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;
    color: #1d4ed8;
    font-size: 0.95rem;
}
.result-warn {
    background: #fef3c7;
    border-left: 4px solid #f59e0b;
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;
    color: #78350f;
    font-size: 0.95rem;
}

/* Clean up Streamlit chrome if desired */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---- HEADER ----
st.markdown(
    "<h2 style='text-align: center;'>Runestone Holdings – Drug Interaction Label Checker</h2>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style='text-align:center' class='muted'>
      Prototype clinical tool to retrieve FDA label excerpts and screen for potential
      cross-mentions between two medications.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style='text-align:center; margin-top:0.25rem;' class='muted'>
      Built for demonstration and learning purposes • Data source: openFDA Drug Labels API
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")  # this is the bar, now clearly separating header from the form


# ---- SIDEBAR (INFO ONLY) ----
with st.sidebar:
    st.markdown("### About")
    st.markdown(
        "<div class='muted'>"
        "Internal prototype developed for educational and workflow support. "
        "Data sourced from openFDA drug labels API."
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='muted'>Developer: Jonathan Crandall, PharmD Candidate.</div>",
        unsafe_allow_html=True
    )
    st.markdown("**Version**  \n0.1.0")
    st.markdown("**Stack**  \nPython · Streamlit · openFDA Drug Labels API")

# ---- IMPORT BACKEND ----
try:
    import src.openfda as openfda
    import_ok = True
except Exception as e:
    import_ok = False
    st.error("Failed to import helper module `src.openfda`. Please verify project structure.")
    st.exception(e)

# ---- INPUT CARD ----
st.markdown('<div class="app-card">', unsafe_allow_html=True)

st.subheader("Drug selection")

st.markdown(
    "<div class='muted'>"
    "Enter two drug names to retrieve key sections from the FDA label and identify any explicit cross-mentions "
    "in interaction-related text."
    "</div>",
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)
with col1:
    drug1 = st.text_input("First drug name", placeholder="e.g., warfarin")
with col2:
    drug2 = st.text_input("Second drug name", placeholder="e.g., trimethoprim-sulfamethoxazole")

st.caption("Spelling matters – prefer generic names where possible.")

check_btn = st.button("Check interactions", type="primary")

st.markdown('</div>', unsafe_allow_html=True)  # close app-card


# ---- HELPER TO RENDER LABEL TEXT ----
def render_label_sections(drug_name: str, sections: dict):
    """Display label sections for a given drug."""
    st.markdown(f"#### {drug_name.capitalize()} – label excerpts")

    if not sections:
        st.info("No FDA label data found for this drug.")
        return

    st.markdown(
        "<div class='result-info'>"
        "These excerpts are truncated. Refer to the full FDA label or an interaction database for complete information."
        "</div>",
        unsafe_allow_html=True
    )

    for key, text in sections.items():
        section_title = key.replace("_", " ").title()
        with st.expander(section_title, expanded=False):
            preview = text[:1600] + ("..." if len(text) > 1600 else "")
            st.write(preview)


# ---- MAIN ACTION ----
if check_btn:
    if not import_ok:
        st.stop()

    if not drug1 or not drug2:
        st.warning("Please enter both drug names before checking interactions.")
    else:
        with st.spinner("Fetching FDA label data and scanning for cross-mentions..."):
            s1 = openfda.get_interaction_text(drug1)
            s2 = openfda.get_interaction_text(drug2)
            notes = openfda.simple_crosscheck(drug1, drug2)

        # RESULT CARD
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.subheader("Label-based interaction review")

        render_label_sections(drug1, s1)
        st.markdown("---")
        render_label_sections(drug2, s2)

        

        st.markdown("### Cross-mention check")
        st.markdown(
            "<div class='muted'>In consideration of workflow tools the Suggested next step: confirm any potential interactions using your "
            "organization’s primary interaction resource (e.g., Lexicomp, Micromedex) before making clinical decisions.</div>",
            unsafe_allow_html=True
            )
        if notes:
            st.markdown(
                "<div class='result-warn'><strong>Potential interaction signals detected.</strong><br>"
                "One medication appears to be referenced in the other’s interaction-related sections. "
                "Review in context using full-label or dedicated interaction resources.</div>",
                unsafe_allow_html=True
            )
            for n in notes:
                st.write(f"• {n}")
        else:
            st.markdown(
                "<div class='result-ok'><strong>No explicit cross-mentions identified in the sampled "
                "interaction text.</strong><br>"
                "Absence of cross-mention does not rule out clinically significant interactions.</div>",
                unsafe_allow_html=True
            )

        


        st.markdown('</div>', unsafe_allow_html=True)  # close result card

# ---- FOOTER / DISCLAIMER ----
st.markdown("---")
st.caption(
    "⚠️ Educational prototype only — not a clinical decision support system. "
    "Always consult authoritative interaction resources (e.g., Lexicomp, Micromedex) and a pharmacist."
)
