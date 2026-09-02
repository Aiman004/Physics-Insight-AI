# Physics Insight AI

Physics Insight AI is a lightweight scientific data-analysis application designed to help users explore structured physics datasets without writing code.

## Overview

The application allows users to upload a CSV dataset or use a built-in physics sample dataset. It performs statistical analysis, interactive visualization, relationship analysis, anomaly detection, and preliminary physics-model exploration.

## Key Features

- CSV dataset upload
- Built-in physics sample dataset
- Automatic dataset profiling
- Missing-value detection
- Numerical-variable detection
- Descriptive statistics
- Interactive scatter plots
- Pearson correlation analysis
- IQR-based anomaly detection
- Distribution histograms
- Correlation heatmap
- Box-plot visualization
- Linear model analysis
- Quadratic curve fitting
- R² model comparison
- Residual analysis
- Preliminary physics-model suggestions
- Evidence-based scientific insights
- Professional Markdown report generation
- Reproducibility information

## Scientific Methods

- Mean
- Median
- Standard deviation
- Minimum and maximum values
- Pearson correlation
- 1.5 × IQR anomaly detection
- Linear least-squares fitting
- Quadratic least-squares fitting
- R² model comparison
- Residual analysis

## Example Physics Dataset

The included sample dataset represents approximately uniformly accelerated motion and contains Time, Position, Velocity, and Acceleration measurements.

The dataset contains 21 observations and 4 variables.

## AI and Scientific Safety

Physics Insight AI provides preliminary computational observations rather than authoritative scientific conclusions.

The system is designed to:

- Ground interpretations in calculated evidence
- Avoid inventing measurements
- Distinguish observations from hypotheses
- Avoid treating correlation as causation
- Flag unsupported numerical claims
- Flag strong causal or certainty language
- Report limitations alongside interpretations

## Limitations

- It does not replace experimental validation.
- Statistical correlation does not establish causation.
- IQR-based anomaly detection may not identify every unusual observation.
- Model suggestions are preliminary.
- Experimental uncertainty may not be fully represented.
- Uploaded datasets must currently be provided in CSV format.

## Project Structure

Physics_Insight_AI/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── physics_sample.csv
├── reports/
│   └── Physics_Insight_AI_Professional_Report.md
└── screenshots/

## Installation

Install the required packages:

pip install -r requirements.txt

## Running the Application

Start the Streamlit application with:

streamlit run app.py

## Example Workflow

1. Open Physics Insight AI.
2. Upload a CSV dataset or use the built-in sample.
3. Inspect the dataset summary.
4. Review descriptive statistics.
5. Explore interactive visualizations.
6. Examine correlations and potential anomalies.
7. Review preliminary physics-model analysis.
8. Read the evidence-based scientific insights.
9. Download the professional analysis report.

## Reproducibility

The project records important analysis information including software versions, dataset dimensions, statistical methods, anomaly-detection method, and model-fitting methods.

## Future Development

- Measurement units and unit validation
- Uncertainty propagation
- Advanced curve fitting
- Dimensional-analysis automation
- Astronomy-specific data formats
- Domain-specific physics models
- Improved AI-assisted scientific interpretation
- Reproducible analysis pipelines
- Additional report formats

## Disclaimer

Physics Insight AI provides preliminary computational analysis and educational research support. Its outputs should be reviewed in the context of the experimental setup, measurement uncertainty, physical theory, and scientific literature.

## Author

Developed as a physics-focused scientific data-analysis and AI research project.
