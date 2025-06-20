import streamlit as st
from datetime import datetime, timedelta
from main import main # Import the main function from your modularized code

def app():
    """
    Streamlit application for planning travel itineraries.
    Allows users to input location and dates, then displays a trip summary.
    """
    st.set_page_config(page_title="Smart Travel Planner", layout="centered")

    st.title("✈️ Smart Travel Planner")
    st.markdown("Plan your next trip with AI-powered itineraries and cost estimates!")

    st.sidebar.header("About")
    st.sidebar.info(
        "This application uses AI to plan travel itineraries, check weather, "
        "and estimate costs (including hotels and entrance fees) for your desired destination and dates. "
        "It leverages LangGraph for workflow orchestration and various APIs for data."
    )

    # --- Input Form ---
    with st.form("travel_form"):
        st.header("Where and When Do You Want to Go?")

        location = st.text_input("Destination City", placeholder="e.g., Chennai, London, Paris")

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=datetime.now() + timedelta(days=7))
        with col2:
            end_date = st.date_input("End Date", value=datetime.now() + timedelta(days=10))

        # Convert dates to string format required by the backend
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        submit_button = st.form_submit_button("Plan My Trip!")

    # --- Display Results ---
    if submit_button:
        if not location:
            st.error("Please enter a destination city.")
        elif start_date >= end_date:
            st.error("End date must be after start date.")
        else:
            with st.spinner("Planning your dream trip... This might take a moment!"):
                try:
                    # Call the main function from your modularized code
                    # The main function should now return the summary string
                    trip_summary = main(location, start_date_str, end_date_str)
                    print(trip_summary)
                    st.success("Trip planned successfully!")
                    st.subheader("Your Trip Summary:")
                    st.markdown(trip_summary) # Display the markdown formatted summary

                except Exception as e:
                    st.error(f"An error occurred during planning: {e}")
                    st.info("Please ensure your API keys are correctly set in the .env file.")

if __name__ == "__main__":
    app()
