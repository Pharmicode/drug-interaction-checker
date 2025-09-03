import streamlit as st

st.set_page_config(page_title="Drug Interaction Checker", page_icon="💊")

st.title("💊 Drug Interaction Checker (openFDA)")
st.write("Enter two drug names to fetch FDA label excerpts and check for cross-mentions.")

# Try to import helper + show any errors visibly
try:
    import src.openfda as openfda
    st.caption("Helper module `src.openfda` imported successfully.")
except Exception as e:
    st.error("Failed to import helper module `src.openfda`.")
    st.exception(e)
    st.stop()

drug1 = st.text_input("First drug name")
drug2 = st.text_input("Second drug name")

if st.button("Check Interactions"):
    if not drug1 or not drug2:
        st.warning("Please enter both drug names.")
        st.stop()

    with st.spinner("Fetching FDA label data..."):
        s1 = openfda.get_interaction_text(drug1)
        s2 = openfda.get_interaction_text(drug2)

    st.subheader(f"{drug1.capitalize()} Label Excerpts")
    if s1:
        for key, text in s1.items():
            st.markdown(f"**{key.replace('_',' ').title()}**")
            st.write(text[:1000] + ("..." if len(text) > 1000 else ""))
    else:
        st.info(f"No FDA label data found for {drug1}")

    st.subheader(f"{drug2.capitalize()} Label Excerpts")
    if s2:
        for key, text in s2.items():
            st.markdown(f"**{key.replace('_',' ').title()}**")
            st.write(text[:1000] + ("..." if len(text) > 1000 else ""))
    else:
        st.info(f"No FDA label data found for {drug2}")

    notes = openfda.simple_crosscheck(drug1, drug2)
    st.subheader("Cross-mention Check")
    if notes:
        for n in notes:
            st.success(n)
    else:
        st.write("No explicit cross-mentions found in 'Drug Interactions'.")
