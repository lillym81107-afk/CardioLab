import streamlit as st
import pandas as pd
import numpy as np

# --------------------------------
# PAGE SETTINGS
# --------------------------------

st.set_page_config(
    page_title="CardioLab | Sports Science",
    page_icon="❤️",
    layout="wide"
)

# --------------------------------
# CUSTOM DESIGN
# --------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #101827;
    color: #F3F4F6;
}

[data-testid="stSidebar"] {
    background-color: #172235;
}

h1, h2, h3 {
    color: #F3F4F6;
}

div[data-testid="stMetric"] {
    background-color: #1D2B40;
    border: 1px solid #34445C;
    padding: 18px;
    border-radius: 12px;
}

div[data-testid="stMetricLabel"] {
    color: #B8C5D6;
}

div[data-testid="stMetricValue"] {
    color: #FFFFFF;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# LOAD ATHLETE DATA
# --------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("athlete_data.csv")

try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "athlete_data.csv was not found. "
        "Make sure it is in your CardioLab folder."
    )
    st.stop()

# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.title("CARDIOLAB")
st.sidebar.caption("Human Performance Analytics")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Athlete Explorer",
        "Data Explorer",
        "Analytics",
        "Athlete Comparison"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Version 1.0 | Educational Project"
)

# --------------------------------
# HEADER
# --------------------------------

st.title("CARDIOLAB")
st.subheader("Cardiovascular Performance Dashboard")

st.markdown(
    "Explore cardiovascular measurements, "
    "heart-rate recovery, and athlete data."
)

st.warning(
    "Educational demonstration: all athlete measurements "
    "in this version are simulated, not real health data."
)

# --------------------------------
# OVERVIEW PAGE
# --------------------------------

if page == "Overview":

    st.header("Performance Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Athletes",
        len(df)
    )

    col2.metric(
        "Average Resting HR",
        f"{df['Resting_HR'].mean():.1f} bpm"
    )

    col3.metric(
        "Average Exercise HR",
        f"{df['Exercise_End_HR'].mean():.1f} bpm"
    )

    col4.metric(
        "Average 1-Min Recovery",
        f"{df['Recovery_1_Min'].mean():.1f} bpm"
    )

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Heart Rate Measurements")

        chart_data = df[
            [
                "Resting_HR",
                "Exercise_End_HR",
                "HR_1_Min",
                "HR_2_Min",
                "HR_3_Min"
            ]
        ]

        st.line_chart(chart_data)

    with right:
        st.subheader("Resting HR vs Recovery")

        st.scatter_chart(
            df,
            x="Resting_HR",
            y="Recovery_1_Min"
        )

    st.divider()

    st.subheader("Average Recovery Measurements")

    recovery_summary = pd.DataFrame({
        "Recovery Time": [
            "1 Minute",
            "2 Minutes",
            "3 Minutes"
        ],
        "Average Recovery (BPM)": [
            df["Recovery_1_Min"].mean(),
            df["Recovery_2_Min"].mean(),
            df["Recovery_3_Min"].mean()
        ]
    })

    st.bar_chart(
        recovery_summary.set_index("Recovery Time")
    )

# --------------------------------
# ATHLETE EXPLORER
# --------------------------------

elif page == "Athlete Explorer":

    st.header("Individual Athlete Explorer")

    athlete_id = st.selectbox(
        "Select an Athlete",
        df["Athlete_ID"].tolist()
    )

    athlete = df[
        df["Athlete_ID"] == athlete_id
    ].iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Resting HR",
        f"{athlete['Resting_HR']:.1f} bpm"
    )

    col2.metric(
        "Exercise-End HR",
        f"{athlete['Exercise_End_HR']:.1f} bpm"
    )

    col3.metric(
        "1-Minute Recovery",
        f"{athlete['Recovery_1_Min']:.1f} bpm"
    )

    st.subheader("Athlete Heart Rate Profile")

    profile = pd.DataFrame({
        "Heart Rate": [
            athlete["Exercise_End_HR"],
            athlete["HR_1_Min"],
            athlete["HR_2_Min"],
            athlete["HR_3_Min"]
        ]
    }, index=[
        "Exercise End",
        "1 Minute",
        "2 Minutes",
        "3 Minutes"
    ])

    st.line_chart(profile)

    st.subheader("Complete Athlete Record")

    st.dataframe(
        athlete.to_frame(name="Measurement"),
        use_container_width=True
    )

# --------------------------------
# DATA EXPLORER
# --------------------------------

elif page == "Data Explorer":

    st.header("Athlete Dataset")
    st.subheader("Upload Your Own Dataset")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        uploaded_df = pd.read_csv(uploaded_file)

        required_columns = [
            "Athlete_ID",
            "Resting_HR",
            "Exercise_End_HR",
            "HR_1_Min",
            "HR_2_Min",
            "HR_3_Min",
            "Recovery_1_Min",
            "Recovery_2_Min",
            "Recovery_3_Min"
        ]

        missing_columns = [
            column for column in required_columns
            if column not in uploaded_df.columns
        ]

        if missing_columns:
            st.error(
                f"Your file is missing: {missing_columns}"
            )

        elif uploaded_df.empty:
            st.error("Your uploaded dataset is empty.")

        else:
            df = uploaded_df
            st.success(
                f"Successfully loaded {len(df)} athlete records!"
            )
    st.write(
        "Explore and filter the simulated cardiovascular dataset."
    )

    minimum_hr = float(df["Resting_HR"].min())
    maximum_hr = float(df["Resting_HR"].max())

    selected_range = st.slider(
        "Filter by resting heart rate",
        min_value=minimum_hr,
        max_value=maximum_hr,
        value=(minimum_hr, maximum_hr)
    )

    filtered_df = df[
        df["Resting_HR"].between(
            selected_range[0],
            selected_range[1]
        )
    ]

    st.metric(
        "Athletes matching filter",
        len(filtered_df)
    )

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    csv_file = filtered_df.to_csv(index=False)

    st.download_button(
        label="Download Filtered Dataset",
        data=csv_file,
        file_name="cardiolab_athlete_data.csv",
        mime="text/csv"
    )


# --------------------------------
# ANALYTICS PAGE
# --------------------------------

elif page == "Analytics":

    st.header("Cardiovascular Analytics")

    st.write(
        "Explore statistical relationships "
        "between cardiovascular measurements."
    )

    # Choose variables
    x_variable = st.selectbox(
        "Select your first variable",
        [
            "Resting_HR",
            "Exercise_End_HR",
            "Recovery_1_Min",
            "Recovery_2_Min",
            "Recovery_3_Min"
        ]
    )

    y_variable = st.selectbox(
        "Select your second variable",
        [
            "Resting_HR",
            "Exercise_End_HR",
            "Recovery_1_Min",
            "Recovery_2_Min",
            "Recovery_3_Min"
        ],
        index=2
    )

    # Calculate correlation
    correlation = df[x_variable].corr(df[y_variable])

    # Calculate regression
    x = df[x_variable].to_numpy()
    y = df[y_variable].to_numpy()

    if x_variable == y_variable:
        st.warning("Choose two different variables to compare.")
    else:
        slope, intercept = np.polyfit(x, y, 1)

        r_squared = correlation ** 2

        # Display statistics
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Correlation",
            f"{correlation:.3f}"
        )

        col2.metric(
            "R-squared",
            f"{r_squared:.3f}"
        )

        col3.metric(
            "Slope",
            f"{slope:.3f}"
        )

        # Create regression chart
        chart_df = pd.DataFrame({
            "X": x,
            "Observed": y,
            "Predicted": slope * x + intercept
        }).sort_values("X")

        st.subheader("Relationship Visualization")

        st.scatter_chart(
            chart_df,
            x="X",
            y="Observed"
        )

        st.line_chart(
            chart_df.set_index("X")["Predicted"]
        )

        # Interpret correlation
        st.subheader("Statistical Interpretation")

        if correlation >= 0.7:
            st.success("Strong positive linear association.")
        elif correlation >= 0.3:
            st.info("Moderate positive linear association.")
        elif correlation <= -0.7:
            st.success("Strong negative linear association.")
        elif correlation <= -0.3:
            st.info("Moderate negative linear association.")
        else:
            st.warning("Weak linear association.")

        st.caption(
            "These results use simulated athlete data. "
            "Correlation does not establish causation."
        )

# --------------------------------
# ATHLETE COMPARISON
# --------------------------------

elif page == "Athlete Comparison":

    st.header("Athlete Comparison")

    st.write(
        "Compare cardiovascular measurements "
        "between two athletes."
    )

    athlete_ids = df["Athlete_ID"].tolist()

    col1, col2 = st.columns(2)

    with col1:
        athlete_a_id = st.selectbox(
            "Select Athlete A",
            athlete_ids,
            index=0
        )

    with col2:
        athlete_b_id = st.selectbox(
            "Select Athlete B",
            athlete_ids,
            index=1
        )

    if athlete_a_id == athlete_b_id:

        st.warning("Please select two different athletes.")

    else:

        athlete_a = df[
            df["Athlete_ID"] == athlete_a_id
        ].iloc[0]

        athlete_b = df[
            df["Athlete_ID"] == athlete_b_id
        ].iloc[0]

        st.divider()

        st.subheader("Cardiovascular Measurements")

        measurements = [
            ("Resting HR", "Resting_HR"),
            ("Exercise-End HR", "Exercise_End_HR"),
            ("1-Minute Recovery", "Recovery_1_Min"),
            ("2-Minute Recovery", "Recovery_2_Min"),
            ("3-Minute Recovery", "Recovery_3_Min")
        ]

        comparison = []

        for label, column in measurements:

            comparison.append({
                "Measurement": label,
                f"Athlete {athlete_a_id}": athlete_a[column],
                f"Athlete {athlete_b_id}": athlete_b[column]
            })

        comparison_df = pd.DataFrame(comparison)

        st.dataframe(
            comparison_df.round(1),
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("Heart Rate Recovery Comparison")

        chart_data = pd.DataFrame({
            f"Athlete {athlete_a_id}": [
                athlete_a["Exercise_End_HR"],
                athlete_a["HR_1_Min"],
                athlete_a["HR_2_Min"],
                athlete_a["HR_3_Min"]
            ],
            f"Athlete {athlete_b_id}": [
                athlete_b["Exercise_End_HR"],
                athlete_b["HR_1_Min"],
                athlete_b["HR_2_Min"],
                athlete_b["HR_3_Min"]
            ]
        }, index=[
            "Exercise End",
            "1 Minute",
            "2 Minutes",
            "3 Minutes"
        ])

        st.line_chart(chart_data)

        st.caption(
            "Comparison uses simulated athlete measurements. "
            "Differences do not establish differences in health "
            "or cardiovascular fitness."
        )

# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.caption(
    "CardioLab | Built with Python, Pandas, and Streamlit"
)
