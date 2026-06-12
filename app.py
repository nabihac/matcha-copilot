import streamlit as st
import os
import google.genai as genai  # <-- ADD THIS LINE HERE AT THE TOP

# 1. Setup Page App Titles
st.set_page_config(page_title="Matcha Mondays Co-Pilot", layout="centered")
st.title("🍵 Matcha Mondays: Pop-Up AI Co-Pilot")
st.write("Calculate base inventory demands and generate strategic AI operational insights.")

# 2. Sidebar Form Layout
st.sidebar.header("📋 Event Variables")
attendance = st.sidebar.slider("Expected Attendance", min_value=50, max_value=300, value=150)
weather = st.sidebar.selectbox("Weather Forecast", ["Sunny", "Rainy", "Cold"])
marketing = st.sidebar.selectbox("Marketing Effort", ["Low", "Medium", "High"])

st.sidebar.header("📦 Current Inventory")
current_matcha = st.sidebar.number_input("Matcha Powder (grams)", min_value=0, value=500)
current_milk = st.sidebar.number_input("Milk (Cartons)", min_value=0, value=10)
current_cups = st.sidebar.number_input("Cups Available", min_value=0, value=100)

# 3. Quick Core Logic Math (Saves AI Tokens)
base_matcha_needed = attendance * 5  # 5g per cup
base_milk_needed = round(attendance * 0.25, 1)  # 0.25 cartons per cup
base_cups_needed = attendance

if weather == "Rainy":
    base_matcha_needed = int(base_matcha_needed * 0.7)
    base_milk_needed = round(base_milk_needed * 0.7, 1)
    base_cups_needed = int(base_cups_needed * 0.7)

# Display Baseline Results
st.subheader("📊 Calculated Baseline Demands")
col1, col2, col3 = st.columns(3)
col1.metric("Matcha Powder", f"{base_matcha_needed}g", f"Have: {current_matcha}g")
col2.metric("Milk Cartons", f"{base_milk_needed} units", f"Have: {current_milk}")
col3.metric("Cups Needed", f"{base_cups_needed} units", f"Have: {current_cups}")

# import google.genai as genai

# 4. AI Strategic Actions
st.subheader("💡 AI Strategy & Action Plan")
if st.button("Generate AI Strategy Brief"):
    # Securely pull the key from your computer's terminal session
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        st.error("Please add your Gemini API Key string to the code to run.")
    else:
        try:
            with st.spinner("Consulting operational data via Gemini..."):
                # Initialize the standard Google GenAI client
                client = genai.Client(api_key=api_key)
                
                context_prompt = f"""
                Event Context:
                - Expected Base Attendance: {attendance}
                - Weather Pattern: {weather}
                - Marketing Level: {marketing}
                
                Calculated Baseline Demand:
                - Target Matcha: {base_matcha_needed}g (Current Stock: {current_matcha}g)
                - Target Milk: {base_milk_needed} cartons (Current Stock: {current_milk} cartons)
                - Target Cups: {base_cups_needed} cups (Current Stock: {current_cups} cups)
                """
                
                # Call the free, active Gemini Flash model
                response = client.models.generate_content(
                    model='gemini-2.5-flash',  # <-- UPDATE THIS STRING HERE
                    contents=context_prompt,
                    config=genai.types.GenerateContentConfig(
                        system_instruction="You are a startup operations and logistics manager. Compare the required baseline metrics against the current stock on hand. Write a sharp, punchy executive directive explaining: 1) Exactly what supplies to order or hold back on based on the gaps, and 2) Two quick, creative operational or marketing moves to maximize sales given the current weather variable. Keep it structured and short."
                    )
                )
                
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Error communicating with Gemini: {e}")