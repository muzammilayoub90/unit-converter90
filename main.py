import streamlit as st

# Conversion factors
conversion_factors = {
    "Length": {
        "meter": 1, "kilometer": 0.001, "inch": 39.3701, "foot": 3.28084, "yard": 1.09361, "mile": 0.000621371
    },
    "Mass": {
        "kilogram": 1, "gram": 1000, "pound": 2.20462, "ounce": 35.274, "stone": 0.157473
    },
    "Speed": {
        "meter per second": 1, "kilometer per hour": 3.6, "mile per hour": 2.23694
    },
    "Time": {
        "second": 1, "minute": 1/60, "hour": 1/3600, "day": 1/86400, "week": 1/604800, "month": 1/2.628e+6, "year": 1/3.154e+7
    }
}

# Store conversion history
if "history" not in st.session_state:
    st.session_state.history = []

# App Title
st.title("⚖️ Unit Converter")

# User Input
col1, col2 = st.columns(2)
with col1:
    category = st.selectbox("Select a category", list(conversion_factors.keys()) + ["Temperature"])
with col2:
    value = st.number_input("Enter a value", value=0.0, step=0.1, format="%.2f")

col3, col4, col5 = st.columns([3, 1, 3])
if category == "Temperature":
    temp_units = ["celsius", "fahrenheit", "kelvin"]
    with col3:
        from_unit = st.selectbox("Convert from", temp_units)
    with col5:
        to_unit = st.selectbox("Convert to", temp_units)
else:
    with col3:
        from_unit = st.selectbox("Convert from", conversion_factors[category].keys())
    with col5:
        to_unit = st.selectbox("Convert to", conversion_factors[category].keys())

# Swap Button
with col4:
    if st.button("🔄 Swap"):
        from_unit, to_unit = to_unit, from_unit

# Convert Button
convert = st.button("Convert")

if convert:
    try:
        if category == "Temperature":
            if from_unit == "celsius" and to_unit == "fahrenheit":
                result = (value * 9/5) + 32
            elif from_unit == "fahrenheit" and to_unit == "celsius":
                result = (value - 32) * 5/9
            elif from_unit == "celsius" and to_unit == "kelvin":
                result = value + 273.15
            elif from_unit == "kelvin" and to_unit == "celsius":
                result = value - 273.15
            elif from_unit == "fahrenheit" and to_unit == "kelvin":
                result = (value - 32) * 5/9 + 273.15
            elif from_unit == "kelvin" and to_unit == "fahrenheit":
                result = (value - 273.15) * 9/5 + 32
            else:
                result = value  
        else:
            base_value = value / conversion_factors[category][from_unit]
            result = base_value * conversion_factors[category][to_unit]

        # Store conversion in history
        st.session_state.history.insert(0, f"{value} {from_unit} = {result:.4f} {to_unit}")
        st.session_state.history = st.session_state.history[:5]  # Keep last 5 conversions

        st.success(f"✅ {value} {from_unit} is equal to **{result:.4f} {to_unit}**")

    except Exception as e:
        st.error(f"❌ Error: {e}")

# Show Conversion History
if st.session_state.history:
    st.markdown("### 🕘 Conversion History")
    for item in st.session_state.history:
        st.write(f"- {item}")

st.markdown("---")
st.markdown("🔹 **Created by Muzammil Ayoub** | Powered by Streamlit")