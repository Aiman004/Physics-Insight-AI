import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Physics Insight AI",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Physics Insight AI")
st.write(
    "Scientific data analysis, visualization, and preliminary "
    "physics-model exploration."
)

st.info(
    "⚠️ This tool provides preliminary statistical observations "
    "and model suggestions. It does not replace scientific "
    "judgement, experimental validation, or peer review."
)

# ---------------------------------------------------------
# SAMPLE DATA
# ---------------------------------------------------------

np.random.seed(42)

time = np.arange(0, 10.5, 0.5)

position = (
    2 * time
    + 0.5 * time**2
    + np.random.normal(0, 0.4, len(time))
)

velocity = (
    2 + time
    + np.random.normal(0, 0.15, len(time))
)

acceleration = (
    np.ones(len(time))
    + np.random.normal(0, 0.05, len(time))
)

sample_data = pd.DataFrame({
    "Time (s)": time,
    "Position (m)": position,
    "Velocity (m/s)": velocity,
    "Acceleration (m/s²)": acceleration
})

# ---------------------------------------------------------
# DATA INPUT
# ---------------------------------------------------------

st.header("📂 Dataset")

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=None,
    accept_multiple_files=False,
    help="Select your CSV file from your device."
)

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        st.success("Your dataset was uploaded successfully!")
    except Exception as error:
        st.error(
            f"Unable to read this CSV file: {error}"
        )
        st.stop()
else:
    data = sample_data
    st.success(
        "Using the built-in physics sample dataset."
    )

# ---------------------------------------------------------
# DATA QUALITY
# ---------------------------------------------------------

st.header("🔎 Data Quality")

missing_values = data.isnull().sum()
total_missing = int(missing_values.sum())

if total_missing == 0:
    st.success(
        "No missing values were detected in the dataset."
    )
else:
    st.warning(
        f"The dataset contains {total_missing} missing values."
    )

    missing_table = pd.DataFrame({
        "Column": missing_values.index,
        "Missing Values": missing_values.values
    })

    missing_table = missing_table[
        missing_table["Missing Values"] > 0
    ]

    st.dataframe(
        missing_table,
        hide_index=True,
        use_container_width=True
    )

numeric_columns = data.select_dtypes(
    include=np.number
).columns.tolist()

if len(numeric_columns) > 0:
    st.write(
        f"Detected **{len(numeric_columns)} numerical variable(s):**"
    )
    st.write(", ".join(numeric_columns))
else:
    st.warning(
        "No numerical variables were detected."
    )

# ---------------------------------------------------------
# DATASET SUMMARY DASHBOARD
# ---------------------------------------------------------

st.header("📊 Dataset Summary")

summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

with summary_col1:
    st.metric("Observations", data.shape[0])

with summary_col2:
    st.metric("Variables", data.shape[1])

with summary_col3:
    st.metric(
        "Numerical Variables",
        len(numeric_columns)
    )

with summary_col4:
    st.metric(
        "Missing Values",
        total_missing
    )

# ---------------------------------------------------------
# RAW DATA
# ---------------------------------------------------------

st.subheader("Dataset Preview")

st.dataframe(
    data.head(10),
    use_container_width=True
)

# ---------------------------------------------------------
# DESCRIPTIVE STATISTICS
# ---------------------------------------------------------

if len(numeric_columns) > 0:

    st.header("📈 Descriptive Statistics")

    numeric_data = data[numeric_columns]

    statistics = pd.DataFrame({
        "Mean": numeric_data.mean(),
        "Median": numeric_data.median(),
        "Standard Deviation": numeric_data.std(),
        "Minimum": numeric_data.min(),
        "Maximum": numeric_data.max()
    })

    st.dataframe(
        statistics.round(4),
        use_container_width=True
    )

# ---------------------------------------------------------
# INTERACTIVE VISUALIZATION
# ---------------------------------------------------------

if len(numeric_columns) >= 2:

    st.header("📉 Interactive Visualization")

    col_x, col_y = st.columns(2)

    with col_x:
        x_axis = st.selectbox(
            "Select X-axis",
            numeric_columns,
            index=0
        )

    with col_y:
        y_axis = st.selectbox(
            "Select Y-axis",
            numeric_columns,
            index=1
        )

    fig = px.scatter(
        data,
        x=x_axis,
        y=y_axis,
        title=f"{y_axis} vs {x_axis}",
        trendline="ols"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------------------------------
    # CORRELATION
    # -----------------------------------------------------

    correlation = data[x_axis].corr(
        data[y_axis]
    )

    st.subheader("🔗 Correlation Analysis")

    st.metric(
        "Pearson Correlation",
        f"{correlation:.3f}"
    )

    if correlation >= 0.7:
        interpretation = "Strong positive relationship"
    elif correlation >= 0.3:
        interpretation = "Moderate positive relationship"
    elif correlation > -0.3:
        interpretation = "Weak or little linear relationship"
    elif correlation > -0.7:
        interpretation = "Moderate negative relationship"
    else:
        interpretation = "Strong negative relationship"

    st.write(
        f"**Interpretation:** {interpretation}"
    )

    st.caption(
        "Correlation describes linear association only. "
        "It does not establish causation."
    )

# ---------------------------------------------------------
# ANOMALY DETECTION
# ---------------------------------------------------------

if len(numeric_columns) > 0:

    st.header("🚨 Potential Anomaly Detection")

    anomaly_results = []

    for column in numeric_columns:

        q1 = data[column].quantile(0.25)
        q3 = data[column].quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        anomalies = data[
            (data[column] < lower_bound)
            |
            (data[column] > upper_bound)
        ][column]

        anomaly_results.append({
            "Variable": column,
            "Potential Anomalies": len(anomalies),
            "Lower Bound": lower_bound,
            "Upper Bound": upper_bound
        })

    anomaly_table = pd.DataFrame(
        anomaly_results
    )

    st.dataframe(
        anomaly_table.round(4),
        hide_index=True,
        use_container_width=True
    )

    st.caption(
        "Potential anomalies are identified using the "
        "1.5 × IQR rule. An anomaly is not necessarily an error."
    )

# ---------------------------------------------------------
# DISTRIBUTIONS
# ---------------------------------------------------------

if len(numeric_columns) > 0:

    st.header("📊 Variable Distributions")

    distribution_column = st.selectbox(
        "Select variable",
        numeric_columns,
        key="distribution"
    )

    fig_distribution = px.histogram(
        data,
        x=distribution_column,
        nbins=10,
        title=f"Distribution of {distribution_column}"
    )

    st.plotly_chart(
        fig_distribution,
        use_container_width=True
    )

# ---------------------------------------------------------
# CORRELATION HEATMAP
# ---------------------------------------------------------

if len(numeric_columns) >= 2:

    st.header("🔥 Correlation Heatmap")

    correlation_matrix = data[
        numeric_columns
    ].corr()

    fig_heatmap = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        aspect="auto",
        title="Correlation Matrix"
    )

    st.plotly_chart(
        fig_heatmap,
        use_container_width=True
    )

# ---------------------------------------------------------
# BOX PLOT
# ---------------------------------------------------------

if len(numeric_columns) > 0:

    st.header("📦 Box Plot")

    box_column = st.selectbox(
        "Select variable",
        numeric_columns,
        key="boxplot"
    )

    fig_box = px.box(
        data,
        y=box_column,
        title=f"Box Plot — {box_column}"
    )

    st.plotly_chart(
        fig_box,
        use_container_width=True
    )

# ---------------------------------------------------------
# AUTOMATIC SCIENTIFIC INSIGHTS
# ---------------------------------------------------------

st.header("🤖 Evidence-Based Scientific Insights")

insights = []

if len(numeric_columns) >= 2:

    correlation = data[x_axis].corr(
        data[y_axis]
    )

    if correlation >= 0.7:
        relationship = "strong positive"
    elif correlation >= 0.3:
        relationship = "moderate positive"
    elif correlation > -0.3:
        relationship = "weak or little linear"
    elif correlation > -0.7:
        relationship = "moderate negative"
    else:
        relationship = "strong negative"

    insights.append(
        f"{x_axis} and {y_axis} show a "
        f"{relationship} linear relationship "
        f"(Pearson correlation = {correlation:.3f})."
    )

insights.append(
    f"The dataset contains {data.shape[0]} observations "
    f"and {data.shape[1]} variables."
)

if total_missing == 0:
    insights.append(
        "No missing values were detected in the dataset."
    )
else:
    insights.append(
        "Missing values were detected and should be "
        "considered before drawing conclusions."
    )

if len(numeric_columns) > 0:

    total_anomalies = sum(
        result["Potential Anomalies"]
        for result in anomaly_results
    )

    if total_anomalies == 0:
        insights.append(
            "No potential anomalies were detected "
            "using the 1.5 × IQR rule."
        )
    else:
        insights.append(
            f"{total_anomalies} potential anomalous "
            "observation(s) were detected using "
            "the 1.5 × IQR rule."
        )

for number, insight in enumerate(
    insights,
    start=1
):
    st.write(
        f"**{number}.** {insight}"
    )

st.caption(
    "These are preliminary computational observations, "
    "not confirmed scientific conclusions."
)

# ---------------------------------------------------------
# PHYSICS MODEL ANALYSIS
# ---------------------------------------------------------

if (
    "Time (s)" in data.columns
    and "Position (m)" in data.columns
    and len(data) >= 3
):

    st.header("⚛️ Physics Model Analysis")

    x = data["Time (s)"].values
    y = data["Position (m)"].values

    # Linear model
    linear_coefficients = np.polyfit(
        x, y, 1
    )

    linear_prediction = np.polyval(
        linear_coefficients,
        x
    )

    # Quadratic model
    quadratic_coefficients = np.polyfit(
        x, y, 2
    )

    quadratic_prediction = np.polyval(
        quadratic_coefficients,
        x
    )

    ss_total = np.sum(
        (y - np.mean(y)) ** 2
    )

    linear_r2 = 1 - (
        np.sum(
            (y - linear_prediction) ** 2
        )
        / ss_total
    )

    quadratic_r2 = 1 - (
        np.sum(
            (y - quadratic_prediction) ** 2
        )
        / ss_total
    )

    model_col1, model_col2 = st.columns(2)

    with model_col1:
        st.metric(
            "Linear Model R²",
            f"{linear_r2:.4f}"
        )

    with model_col2:
        st.metric(
            "Quadratic Model R²",
            f"{quadratic_r2:.4f}"
        )

    if quadratic_r2 > linear_r2 + 0.01:

        st.success(
            "The data are better represented by a "
            "quadratic relationship than by a linear model."
        )

        st.write(
            "Possible physics interpretation: uniformly "
            "accelerated motion, where position can depend "
            "quadratically on time."
        )

    elif linear_r2 >= 0.7:

        st.success(
            "The data show a strong linear relationship."
        )

        st.write(
            "Possible physics interpretation: "
            "approximately constant-rate motion."
        )

    else:

        st.warning(
            "Neither a simple linear nor quadratic model "
            "provides a strong representation of the data."
        )

    st.caption(
        "⚠️ Model suggestions are preliminary and "
        "require physical and experimental validation."
    )

# ---------------------------------------------------------
# REPORT GENERATION
# ---------------------------------------------------------

st.header("📄 Professional Analysis Report")

report_lines = []

report_lines.append(
    "# Physics Insight AI — Scientific Data Analysis Report"
)

report_lines.append("")
report_lines.append("## 1. Analysis Overview")
report_lines.append("")
report_lines.append(
    "This report presents a preliminary statistical "
    "and physics-oriented analysis of the supplied dataset."
)

report_lines.append("")
report_lines.append("## 2. Dataset Summary")
report_lines.append("")
report_lines.append(
    f"- Observations: {data.shape[0]}"
)
report_lines.append(
    f"- Variables: {data.shape[1]}"
)
report_lines.append(
    f"- Numerical variables: {len(numeric_columns)}"
)
report_lines.append(
    f"- Missing values: {total_missing}"
)

report_lines.append("")
report_lines.append("## 3. Statistical Analysis")
report_lines.append("")

if len(numeric_columns) > 0:

    for column in numeric_columns:

        report_lines.append(
            f"### {column}"
        )

        report_lines.append(
            f"- Mean: {data[column].mean():.4f}"
        )

        report_lines.append(
            f"- Median: {data[column].median():.4f}"
        )

        report_lines.append(
            f"- Standard deviation: "
            f"{data[column].std():.4f}"
        )

        report_lines.append(
            f"- Minimum: "
            f"{data[column].min():.4f}"
        )

        report_lines.append(
            f"- Maximum: "
            f"{data[column].max():.4f}"
        )

        report_lines.append("")

report_lines.append(
    "## 4. Relationship Analysis"
)

report_lines.append("")

if len(numeric_columns) >= 2:

    report_lines.append(
        f"- X variable: {x_axis}"
    )

    report_lines.append(
        f"- Y variable: {y_axis}"
    )

    report_lines.append(
        f"- Pearson correlation: "
        f"{data[x_axis].corr(data[y_axis]):.4f}"
    )

report_lines.append("")
report_lines.append("## 5. Anomaly Analysis")
report_lines.append("")
report_lines.append(
    f"- Detection method: 1.5 × IQR rule"
)

if len(numeric_columns) > 0:

    report_lines.append(
        f"- Total potential anomalies: "
        f"{total_anomalies}"
    )

report_lines.append("")
report_lines.append(
    "## 6. Physics Model Analysis"
)
report_lines.append("")

if (
    "Time (s)" in data.columns
    and "Position (m)" in data.columns
    and len(data) >= 3
):

    report_lines.append(
        f"- Linear model R²: {linear_r2:.4f}"
    )

    report_lines.append(
        f"- Quadratic model R²: "
        f"{quadratic_r2:.4f}"
    )

    report_lines.append(
        "- Model suggestions are preliminary."
    )

report_lines.append("")
report_lines.append(
    "## 7. Evidence-Based Insights"
)
report_lines.append("")

for insight in insights:
    report_lines.append(
        f"- {insight}"
    )

report_lines.append("")
report_lines.append("## 8. Limitations")
report_lines.append("")
report_lines.append(
    "- Statistical relationships do not establish causation."
)
report_lines.append(
    "- Potential anomalies are not necessarily measurement errors."
)
report_lines.append(
    "- Model suggestions are preliminary."
)
report_lines.append(
    "- Experimental conditions and measurement uncertainty "
    "may not be fully represented."
)

report_lines.append("")
report_lines.append(
    "## 9. Scientific Disclaimer"
)
report_lines.append("")
report_lines.append(
    "This report provides preliminary computational "
    "observations and should not be treated as a confirmed "
    "scientific conclusion."
)

report_lines.append("")
report_lines.append(
    "## 10. Reproducibility Information"
)
report_lines.append("")
report_lines.append(
    f"- Pandas version: {pd.__version__}"
)
report_lines.append(
    f"- NumPy version: {np.__version__}"
)
report_lines.append(
    "- Anomaly detection: 1.5 × IQR rule"
)
report_lines.append(
    "- Model fitting: Linear and quadratic "
    "least-squares fitting"
)

report_lines.append("")
report_lines.append(
    "## 11. Visualizations and Analysis Results"
)
report_lines.append("")
report_lines.append(
    "- Interactive scatter plot"
)
report_lines.append(
    "- Variable distribution histogram"
)
report_lines.append(
    "- Correlation heatmap"
)
report_lines.append(
    "- Box plot"
)
report_lines.append(
    "- Physics model comparison"
)

report = "\n".join(report_lines)

st.download_button(
    label="⬇️ Download Analysis Report",
    data=report,
    file_name="Physics_Insight_AI_Professional_Report.md",
    mime="text/markdown"
)

st.success(
    "Analysis completed successfully."
)
