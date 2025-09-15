import streamlit as st
import pandas as pd
import time
from serpapi import GoogleSearch  # pip install google-search-results

st.set_page_config(page_title="URL Index Checker", layout="centered")
st.title("🔍 Google Index Checker")

st.markdown("""
### Steps to Find API Key:
1. Visit [Serp API](https://www.searchapi.io/)
2. Sign Up to Get Free 100 Requests  
3. Dashboard will appear  
4. Copy the API Key and Paste in the dialog box below  
""")

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

        # Dropdown filter
        filter_option = st.selectbox(
            "Select which URLs to view:",
            ["Indexed URLs", "Not Indexed URLs", "View All URLs"]
        )

        total_urls = len(df)

        if filter_option == "Indexed URLs":
            filtered_df = df[df['Status'] == "✅ Indexed"]
            count = len(filtered_df)
            st.write(f"**{count} of {total_urls} URLs are Indexed.**")

        elif filter_option == "Not Indexed URLs":
            filtered_df = df[df['Status'] == "❌ Not Indexed"]
            count = len(filtered_df)
            st.write(f"**{count} of {total_urls} URLs are Not Indexed.**")

        else:  # View All
            filtered_df = df
            count = len(filtered_df)
            st.write(f"**{count} of {total_urls} URLs (All).**")

        st.dataframe(filtered_df)

        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download Filtered Results as CSV",
            data=csv,
            file_name="indexing_results.csv",
            mime="text/csv"
        )
