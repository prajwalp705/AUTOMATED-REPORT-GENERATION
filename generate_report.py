import pandas as pd
from fpdf import FPDF

# Step 1: Read Data
data = pd.read_csv("data2.csv")

# Step 2: Basic Analysis
summary = data.groupby("Department")["Sales"].agg(['sum', 'mean', 'count']).reset_index()

# Step 3: Generate PDF Report
class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Sales Report", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def create_table(self, dataframe, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True, align="L")
        self.set_font("Arial", "B", 10)

        col_widths = [50, 30, 30, 30]
        headers = ['Department', 'Total Sales', 'Average Sales', 'Entries']

        for i, header in enumerate(headers):
            self.cell(col_widths[i], 10, header, border=1)
        self.ln()

        self.set_font("Arial", "", 10)
        for index, row in dataframe.iterrows():
            self.cell(col_widths[0], 10, str(row['Department']), border=1)
            self.cell(col_widths[1], 10, f"${row['sum']:.2f}", border=1)
            self.cell(col_widths[2], 10, f"${row['mean']:.2f}", border=1)
            self.cell(col_widths[3], 10, str(int(row['count'])), border=1)
            self.ln()

# Create PDF
pdf = PDFReport()
pdf.add_page()
pdf.create_table(summary, "Sales Summary by Department")
pdf.output("sales_report.pdf")

print("PDF report generated: sales_report.pdf")
