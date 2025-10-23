import streamlit as st
import anthropic
import os

# Page configuration
st.set_page_config(
    page_title="Executive Interview Synthesizer",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Executive Interview Synthesizer")
st.markdown("""
Transform interview transcripts into polished executive summaries with multiple format options.
Upload a transcript and select your preferences to generate professional content instantly.
""")

# Sidebar for API key and settings
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Anthropic API Key", type="password", help="Enter your Anthropic API key")
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This tool uses Claude to analyze executive interviews and generate professional summaries tailored to your audience.")

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Input")
    
    # Transcript input
    transcript = st.text_area(
        "Interview Transcript",
        height=400,
        placeholder="Paste your interview transcript here...",
        help="Copy and paste the full interview transcript"
    )
    
    # Audience selection
    audience = st.selectbox(
        "Target Audience",
        ["Board Directors", "CEOs", "Senior Executives", "General Business Audience"],
        help="Who will be reading this summary?"
    )
    
    # Word count
    word_count = st.selectbox(
        "Word Count",
        [350, 500, 800],
        index=1,
        help="Desired length of the narrative summary"
    )
    
    # Number of headlines
    num_headlines = st.slider(
        "Number of Headline Options",
        min_value=3,
        max_value=7,
        value=5,
        help="How many headline variations to generate"
    )
    
    # Focus areas
    focus_options = st.multiselect(
        "Focus Areas (optional)",
        ["Leadership Insights", "Strategic Decisions", "Board Governance", 
         "Stakeholder Management", "Organizational Culture", "Innovation & Technology",
         "Crisis Management", "Succession Planning"],
        help="Select specific themes to emphasize in the analysis"
    )
    
    # Generate button
    generate_button = st.button("🚀 Generate Summary", type="primary", use_container_width=True)

with col2:
    st.header("Output")
    
    if generate_button:
        if not api_key:
            st.error("⚠️ Please enter your Anthropic API key in the sidebar")
        elif not transcript:
            st.error("⚠️ Please paste an interview transcript")
        else:
            with st.spinner("Analyzing transcript and generating content..."):
                try:
                    # Initialize Anthropic client
                    client = anthropic.Anthropic(api_key=api_key)
                    
                    # Build focus area context
                    focus_context = ""
                    if focus_options:
                        focus_context = f"\n\nPay special attention to these themes: {', '.join(focus_options)}"
                    
                    # Create the prompt
                    prompt = f"""Analyze this executive interview transcript and create a comprehensive synthesis for an audience of {audience}.

TRANSCRIPT:
{transcript}

{focus_context}

Please provide:

1. HEADLINE OPTIONS: Generate {num_headlines} compelling, punchy headlines that capture the key insight or most surprising element. Make them journalistic and engaging - avoid generic phrases. Each headline should offer a distinct angle or emphasis.

2. NARRATIVE SUMMARY: Write a {word_count}-word synthesis in narrative, journalistic style with 2-3 descriptive subheadings. Structure:
   - Open with the most compelling or surprising insight
   - Use natural transitions between ideas
   - Include specific examples, quotes, or anecdotes from the transcript
   - Highlight surprising, counterintuitive, or actionable insights
   - End with pragmatic takeaways
   - Write in clear, active voice
   - Bold key facts for scannability

3. KEY INSIGHTS: List 5 interesting or surprising insights from the interview (bullet points OK here)

4. ACTIONABLE TAKEAWAYS: List 3-5 specific, pragmatic actions that {audience.lower()} can apply

Format your response with clear section headers."""

                    # Call Claude API
                    message = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=4000,
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )
                    
                    # Display results
                    result = message.content[0].text
                    
                    # Add download button
                    st.download_button(
                        label="📥 Download Summary",
                        data=result,
                        file_name="executive_summary.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                    st.markdown("---")
                    
                    # Display the generated content
                    st.markdown(result)
                    
                except anthropic.APIError as e:
                    st.error(f"❌ API Error: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>Built with Claude & Streamlit | Powered by Anthropic API</p>
</div>
""", unsafe_allow_html=True)
