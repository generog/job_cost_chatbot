
import pandas as pd
import streamlit as st
import datetime

st.set_page_config(page_title="Job Cost Summary Chatbot", layout="wide")
st.title("📋 Job Cost Summary Chatbot")

st.markdown("""
This chatbot collects project data and generates a cost summary similar to your FM-026 spreadsheet.
Fill in the form below step-by-step. When finished, your summary will appear on the right.
""")

st.sidebar.header("🔧 Project Setup")

# 1. Registration Info
with st.sidebar.expander("1. Registration Form"):
    job_date = st.date_input("Job Date", value=datetime.date.today())
    project_number = st.text_input("Project Number")
    job_name = st.text_input("Job Name")
    contractor = st.text_input("Contractor")
    salesperson = st.text_input("Salesperson")

# 2. Breakout (Changes / Deductions / Additions)
with st.sidebar.expander("2. Breakout Summary"):
    hw_deducts = st.number_input("Hardware Deducts ($)", value=0.0)
    hw_adds = st.number_input("Hardware Adds ($)", value=0.0)
    wd_deducts = st.number_input("Wood Deducts ($)", value=0.0)
    wd_adds = st.number_input("Wood Adds ($)", value=0.0)
    labor_adds = st.number_input("Labor Adds ($)", value=0.0)

# 3. Pricing & Margin
with st.sidebar.expander("3. Pricing Setup"):
    hw_base_cost = st.number_input("Hardware Total Cost ($)", value=0.0)
    wd_base_cost = st.number_input("Wood Total Cost ($)", value=0.0)
    margin_percent = st.slider("Markup Percentage", 0.0, 100.0, 20.0)

# Calculation logic
hw_total = hw_base_cost - hw_deducts + hw_adds
wd_total = wd_base_cost - wd_deducts + wd_adds
material_total = hw_total + wd_total
margin_multiplier = 1 + (margin_percent / 100)
plus_margin_total = material_total * margin_multiplier
final_total = plus_margin_total + labor_adds

# Output Summary
st.header("📊 Summary Output")
sum_data = {
    "Category": ["HW Cost", "WD Cost", "Material Subtotal", "With Margin", "Labor Adds", "Final Total"],
    "Amount ($)": [round(hw_total, 2), round(wd_total, 2), round(material_total, 2), round(plus_margin_total, 2), round(labor_adds, 2), round(final_total, 2)]
}
df_summary = pd.DataFrame(sum_data)
st.dataframe(df_summary, use_container_width=True)

# Export to Excel
if st.button("📥 Download Summary as Excel"):
    export_df = df_summary.copy()
    export_df.insert(0, "Job", [job_name]*len(export_df))
    export_df.insert(1, "Project #", [project_number]*len(export_df))
    export_df.insert(2, "Contractor", [contractor]*len(export_df))
    export_df.insert(3, "Salesperson", [salesperson]*len(export_df))
    export_df.insert(4, "Date", [job_date]*len(export_df))

    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        export_df.to_excel(writer, index=False, sheet_name='Summary')
        writer.save()
        st.download_button(
            label="Download Excel File",
            data=output.getvalue(),
            file_name=f"Cost_Summary_{project_number}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
