import streamlit as st
from groq import Groq
import os

# Step 1: Retrieve API Key from Hugging Face Secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Step 2: Initialize Groq Client
if GROQ_API_KEY is None:
    st.error("Groq API key is missing. Please add the API key in Secrets.")
else:
    groq_client = Groq(api_key=GROQ_API_KEY)

    # Step 3: Function to interact with Groq
    def enhance_with_groq(query):
        try:
            chat_completion = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": query}],
                model="llama-3.3-70b-versatile",
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error with Groq API: {str(e)}"

    # Step 4: Add Background Image using Custom CSS
    background_image_url = "https://static.vecteezy.com/ti/fotos-gratis/t1/21196013-futurista-tecnologia-fundo-azul-linha-onda-luz-tela-abstrato-ilustracao-foto.jpg"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{background_image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .stApp * {{
            color: white !important;
            text-shadow: 1px 1px 2px black;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Step 5: Build Streamlit UI
    st.title("🌐 NetBridge: Bridging Connectivity Gaps 🌍")
    st.markdown("""
    Welcome to **NetBridge**!  
    This app helps you with:  
    - Finding affordable internet solutions tailored to your location and needs.  
    - Tips for boosting your internet signal in remote areas.  
    - Offline tools for education, healthcare, and business continuity.  
    - Recommendations for connectivity systems based on your inputs.  
    - Addressing custom queries to assist with connectivity challenges.  
    """)

    # Sidebar User Inputs
    st.sidebar.header("Input Your Details")
    location = st.sidebar.text_input("Enter Your Location (e.g., City, District)")
    needs = st.sidebar.selectbox("What do you need?", [
        "Internet Provider",
        "Signal Boosting Tips",
        "Offline Tools",
        "Types of Internet Connections",
        "Educational Resources",
        "Energy-Efficient Connectivity Solutions",
        "Recommend Connectivity System"
    ])

    # Fetch and Enhance Suggestions
    if needs != "Recommend Connectivity System" and st.sidebar.button("Get Suggestions"):
        if location:
            query = f"Provide suggestions for {needs} in {location}, especially affordable options and tips."
            st.subheader(f"Suggestions for {needs} in {location}")
            groq_response = enhance_with_groq(query)
            st.write("Suggestions from Groq:")
            st.write(groq_response)
        else:
            st.warning("Please enter your location to get recommendations.")

    # "Recommend Connectivity System" Option
    if needs == "Recommend Connectivity System":
        st.subheader("Recommend Connectivity System")
        st.markdown("Provide the following details to get a personalized recommendation for your connectivity system:")

        # Inputs from the user
        user_budget = st.number_input("Enter your budget (in USD):", min_value=10, step=10)
        num_users = st.number_input("Number of users:", min_value=1, step=1)
        connection_preference = st.selectbox("Preferred Connection Type:", [
            "Satellite Internet",
            "4G/5G LTE",
            "Fiber Optic",
            "DSL",
            "Fixed Wireless",
            "No Preference"
        ])

        # Get recommendation on button click
        if st.button("Get Recommendation"):
            if user_budget and num_users:
                recommendation_query = (
                    f"Recommend a suitable connectivity system for a rural area. "
                    f"Budget: ${user_budget}, Number of Users: {num_users}, "
                    f"Connection Preference: {connection_preference}."
                )
                recommendation_response = enhance_with_groq(recommendation_query)
                st.subheader("Recommended Connectivity System")
                st.write(recommendation_response)
            else:
                st.warning("Please fill in all required fields.")

    # Optional Query Box for Additional Questions
    st.sidebar.header("Have Another Query?")
    user_query = st.sidebar.text_input("Ask a Question (Optional)", "")
    
    if user_query:
        st.subheader(f"Your Query: {user_query}")
        query_response = enhance_with_groq(user_query)
        st.write("Response from Groq:")
        st.write(query_response)

# Add a bottom-left corner credit
st.markdown("""
    <style>
    .bottom-left {
        position: fixed;
        bottom: 0;
        left: 0;
        padding: 10px;
        font-size: 14px;
        font-family: 'Arial', sans-serif;
        color: white;
        background-color: rgba(0, 0, 0, 0.5);
        border-top-right-radius: 8px;
    }
    </style>
    <div class="bottom-left">
        Created by Team Materio 🚀
    </div>
""", unsafe_allow_html=True)
