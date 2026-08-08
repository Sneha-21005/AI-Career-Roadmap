import streamlit as st
from google import genai
from dotenv import load_dotenv
from pathlib import Path
import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import re

# Load .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Google API key is not configured.")
    st.stop()

client = genai.Client(api_key=api_key)
pdfmetrics.registerFont(
    TTFont(
        "TimesNewRoman",
        "C:/Windows/Fonts/times.ttf"
    )
)

pdfmetrics.registerFont(
    TTFont(
        "TimesNewRoman-Bold",
        "C:/Windows/Fonts/timesbd.ttf"
    )
)
# ----------------------------
# PDF Function
# ----------------------------
# ----------------------------
# Professional PDF Function
# ----------------------------

# Register Times New Roman
pdfmetrics.registerFont(TTFont("Times", "times.ttf"))
pdfmetrics.registerFont(TTFont("Times-Bold", "timesbd.ttf"))

def create_pdf(text):

    pdf_file = "Career_Roadmap.pdf"

    doc = SimpleDocTemplate(
        pdf_file,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontName="Times-Bold",
        fontSize=20,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontName="Times-Bold",
        fontSize=16,
        spaceBefore=14,
        spaceAfter=10
    )

    subheading_style = ParagraphStyle(
        "SubHeading",
        parent=styles["Heading3"],
        fontName="Times-Bold",
        fontSize=14,
        spaceBefore=10,
        spaceAfter=8
    )

    normal_style = ParagraphStyle(
        "Normal",
        parent=styles["Normal"],
        fontName="Times",
        fontSize=12,

        # 1.5 LINE SPACING
        leading=18,

        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        "Bullet",
        parent=normal_style,
        leftIndent=20,
        bulletIndent=10
    )

    story = []

    story.append(Paragraph("AI Career Switch Roadmap", title_style))

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        # Remove markdown **
        line = line.replace("**", "")

        # Remove #
        line = re.sub(r"^#+\s*", "", line)

        # Remove AI footer
        if "Generated using Google Gemini AI + Streamlit" in line:
            continue

        # Main Heading
        if re.match(r"^\d+\.", line):
            story.append(Paragraph(line, heading_style))

        # Subheading
        elif line.endswith(":"):
            story.append(Paragraph(line, subheading_style))

        # Bullet
        elif line.startswith("-") or line.startswith("*"):
            line = line.lstrip("-* ").strip()
            story.append(
                Paragraph(
                    line,
                    bullet_style,
                    bulletText="•"
                )
            )

        else:
            story.append(Paragraph(line, normal_style))

    doc.build(story)

    return pdf_file

# ----------------------------
# Streamlit Page
# ----------------------------
st.set_page_config(
    page_title="AI Career Switch Roadmap",
    page_icon="🚀",
    layout="wide"
)

st.sidebar.title("🚀 AI Career Switch Roadmap")

st.sidebar.info("""
Generate a personalized AI career roadmap in seconds.

✔ Skill Gap Analysis
✔ 90-Day Plan
✔ Portfolio Projects
✔ Resume Points
✔ PDF Download
""")

st.title("🚀 AI Career Switch Roadmap Generator")

st.write("Generate a personalized 90-day career transition roadmap using AI.")

current_role = st.text_input("Current Role")
target_role = st.text_input("Target Role")
experience = st.text_input("Experience")
hours = st.text_input("Hours Available Per Week")
budget = st.text_input("Budget")

if st.button("🚀 Generate My AI Roadmap"):

    prompt = f"""
You are an expert AI Career Mentor.

Current Role: {current_role}
Target Role: {target_role}
Experience: {experience}
Hours Available Per Week: {hours}
Budget: {budget}

Generate:

# 1. Skill Gap Analysis

# 2. 90-Day Learning Plan (Week-by-week)

# 3. Three Portfolio Projects

# 4. Resume Bullet Points

# 5. Free Learning Resources

Format everything using Markdown headings and bullet points.
"""

    with st.spinner("Generating your roadmap..."):

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

    st.success("✅ Your personalized roadmap is ready!")
    st.balloons()

    st.subheader("📄 Your Career Roadmap")

    st.markdown(response.text)

    # ----------------------------
    # Create PDF
    # ----------------------------
    pdf_file = create_pdf(response.text)

    # ----------------------------
    # Download Button
    # ----------------------------
    with open(pdf_file, "rb") as file:
        st.download_button(
            label="📥 Download Roadmap as PDF",
            data=file,
            file_name="AI_Career_Roadmap.pdf",
            mime="application/pdf"
        )
