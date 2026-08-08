```python
import streamlit as st
from google import genai
from dotenv import load_dotenv
from pathlib import Path
import os
import re

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Career Switch Roadmap",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# LOAD API KEY
# ============================================================

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Streamlit Cloud Secrets first, local .env second
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Google API key is not configured.")
    st.info("Add GOOGLE_API_KEY in Streamlit Cloud → Settings → Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)


# ============================================================
# REGISTER TIMES NEW ROMAN
# ============================================================

# Look for Times New Roman in common locations.
font_paths = [
    # Windows local computer
    (
        "C:/Windows/Fonts/times.ttf",
        "C:/Windows/Fonts/timesbd.ttf"
    ),

    # Project folder (useful if you later add the fonts)
    (
        str(Path(__file__).parent / "fonts" / "times.ttf"),
        str(Path(__file__).parent / "fonts" / "timesbd.ttf")
    )
]

font_registered = False

for regular_font, bold_font in font_paths:
    if os.path.exists(regular_font) and os.path.exists(bold_font):
        pdfmetrics.registerFont(TTFont("TimesNewRoman", regular_font))
        pdfmetrics.registerFont(TTFont("TimesNewRoman-Bold", bold_font))
        font_registered = True
        break


# Fallback if Times New Roman is not available
if not font_registered:
    regular_font_name = "Times-Roman"
    bold_font_name = "Times-Bold"
else:
    regular_font_name = "TimesNewRoman"
    bold_font_name = "TimesNewRoman-Bold"


# ============================================================
# PDF FUNCTION
# ============================================================

def create_pdf(text):

    pdf_file = "Career_Roadmap.pdf"

    doc = SimpleDocTemplate(
        pdf_file,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Main title
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontName=bold_font_name,
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    # Main headings: 16
    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontName=bold_font_name,
        fontSize=16,
        leading=20,
        spaceBefore=14,
        spaceAfter=10
    )

    # Subheadings: 14
    subheading_style = ParagraphStyle(
        "CustomSubHeading",
        parent=styles["Heading3"],
        fontName=bold_font_name,
        fontSize=14,
        leading=18,
        spaceBefore=10,
        spaceAfter=8
    )

    # Normal text: 12 with 1.5 line spacing
    normal_style = ParagraphStyle(
        "CustomNormal",
        parent=styles["Normal"],
        fontName=regular_font_name,
        fontSize=12,
        leading=18,
        spaceAfter=9
    )

    # Bullet text
    bullet_style = ParagraphStyle(
        "CustomBullet",
        parent=normal_style,
        leftIndent=20,
        firstLineIndent=0,
        bulletIndent=8,
        spaceAfter=9
    )

    story = []

    # PDF title
    story.append(
        Paragraph(
            "AI Career Switch Roadmap",
            title_style
        )
    )

    # Process Gemini output
    for line in text.split("\n"):

        line = line.strip()

        # Skip empty lines
        if not line:
            story.append(Spacer(1, 6))
            continue

        # Remove Markdown bold markers
        line = line.replace("**", "")

        # Remove Markdown heading symbols
        line = re.sub(r"^#+\s*", "", line)

        # Remove Gemini footer
        if "Generated using Google Gemini AI + Streamlit" in line:
            continue

        # --------------------------------------------------------
        # Main numbered headings
        # Example:
        # 1. Skill Gap Analysis
        # 2. 90-Day Learning Plan
        # --------------------------------------------------------

        if re.match(r"^\d+\.\s+", line):

            story.append(
                Paragraph(
                    line,
                    heading_style
                )
            )

        # --------------------------------------------------------
        # Bullet points
        # Supports -, *, •
        # --------------------------------------------------------

        elif line.startswith("-") or line.startswith("*") or line.startswith("•"):

            line = line.lstrip("-*• ").strip()

            story.append(
                Paragraph(
                    line,
                    bullet_style,
                    bulletText="•"
                )
            )

        # --------------------------------------------------------
        # Subheadings
        # Example:
        # Python & Git
        # Portfolio Projects:
        # --------------------------------------------------------

        elif line.endswith(":"):

            story.append(
                Paragraph(
                    line,
                    subheading_style
                )
            )

        # --------------------------------------------------------
        # Normal paragraph
        # --------------------------------------------------------

        else:

            story.append(
                Paragraph(
                    line,
                    normal_style
                )
            )

    doc.build(story)

    return pdf_file


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🚀 AI Career Roadmap")

st.sidebar.write(
    "Create a personalized career transition plan using AI."
)

st.sidebar.markdown("---")

st.sidebar.subheader("📌 Includes")

st.sidebar.write("✔ Skill Gap Analysis")
st.sidebar.write("✔ 90-Day Learning Plan")
st.sidebar.write("✔ Portfolio Projects")
st.sidebar.write("✔ Resume Bullet Points")
st.sidebar.write("✔ Free Learning Resources")
st.sidebar.write("✔ Downloadable PDF")

st.sidebar.markdown("---")

st.sidebar.info(
    "💡 Fill in your details and generate your personalized roadmap."
)


# ============================================================
# MAIN UI
# ============================================================

st.title("🚀 AI Career Switch Roadmap Generator")

st.write(
    "Generate a personalized 90-day career transition roadmap using AI."
)


# ============================================================
# INPUT FIELDS
# ============================================================

current_role = st.text_input(
    "Current Role",
    placeholder="Example: Student"
)

target_role = st.text_input(
    "Target Role",
    placeholder="Example: AI Engineer"
)

experience = st.text_input(
    "Experience",
    placeholder="Example: 0 years"
)

hours = st.text_input(
    "Hours Available Per Week",
    placeholder="Example: 5 hours"
)

budget = st.text_input(
    "Budget",
    placeholder="Example: Free"
)


# ============================================================
# GENERATE ROADMAP
# ============================================================

if st.button("🚀 Generate My AI Roadmap", use_container_width=True):

    # Check required fields
    if not current_role or not target_role:

        st.warning(
            "Please enter your Current Role and Target Role."
        )

    else:

        prompt = f"""
You are an expert AI Career Mentor.

Create a practical and realistic career transition roadmap.

Current Role: {current_role}

Target Role: {target_role}

Experience: {experience}

Hours Available Per Week: {hours}

Budget: {budget}

Generate the following sections:

1. Skill Gap Analysis

2. 90-Day Learning Plan
Provide a week-by-week plan.

3. Three Portfolio Projects
For each project include:
- Project name
- Description
- Technologies
- Key features
- Expected outcome

4. Resume Bullet Points
Create realistic resume bullet points based on the projects.

5. Free Learning Resources
Recommend useful free learning resources.

Important formatting instructions:

Use clear headings.

Use bullet points for individual items.

Do not use ** markdown bold formatting.

Do not add any footer such as:
"Generated using Google Gemini AI + Streamlit"

Keep the roadmap practical for the user's available weekly hours and budget.
"""

        with st.spinner("🤖 Generating your personalized roadmap..."):

            try:

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

                roadmap_text = response.text

                st.success(
                    "✅ Your personalized roadmap is ready!"
                )

                st.balloons()

                st.subheader("📄 Your Career Roadmap")

                # Display roadmap
                st.markdown(roadmap_text)

                # ====================================================
                # CREATE PDF
                # ====================================================

                pdf_file = create_pdf(roadmap_text)

                st.success(
                    "📄 PDF generated successfully!"
                )

                # ====================================================
                # DOWNLOAD PDF
                # ====================================================

                with open(pdf_file, "rb") as file:

                    st.download_button(
                        label="📥 Download Roadmap as PDF",
                        data=file,
                        file_name="AI_Career_Roadmap.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

            except Exception as e:

                st.error(
                    "❌ Something went wrong while generating the roadmap."
                )

                st.exception(e)
```
