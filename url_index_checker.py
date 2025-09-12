import streamlit as st
import pandas as pd
import time
from serpapi import GoogleSearch  # <── change this line

st.set_page_config(page_title="URL Index Checker", layout="centered")
st.title("🔍 Google Index Checker")

# Input for API key
api_key = st.text_input("Enter your SerpAPI Key", type="password")

# Textarea for URLs
urls_input = st.text_area("Paste URLs (one per line):")

if st.button("Check Indexing Status"):
    if not api_key:
        st.error("Please enter your SerpAPI Key.")
    elif not urls_input.strip():
        st.error("Please paste at least one URL.")
    else:
        urls = [line.strip() for line in urls_input.strip().splitlines() if line.strip()]

        results_list = []

        progress = st.progress(0)
        status_text = st.empty()

        for i, url in enumerate(urls, start=1):
            status_text.text(f"Checking {i}/{len(urls)}: {url}")
            params = {
                "engine": "google",
                "q": f"site:{url}",
                "api_key": api_key
            }
            try:
                search = GoogleSearch(params)
                results = search.get_dict()
                if results.get("organic_results"):
                    status = "✅ Indexed"
                else:
                    status = "❌ Not Indexed"
            except Exception as e:
                status = f"⚠️ Error: {e}"

            results_list.append({"URL": url, "Status": status})
            progress.progress(i / len(urls))
            time.sleep(2)  # polite delay

        status_text.text("Done!")

        # Convert to DataFrame
        df = pd.DataFrame(results_list)

        st.subheader("Results")
        st.dataframe(df)

        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="indexing_results.csv",
            mime="text/csv"
        )

