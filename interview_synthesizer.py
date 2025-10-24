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
        ["Board Directors", "CEOs", "Senior Executives", "HR Leaders", "General Business Audience"],
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
                    
                    # Define audience-specific prompts with dramatic differentiation
                    audience_prompts = {
                        "Board Directors": f"""Analyze this executive interview transcript and create a board-level synthesis focused on governance, oversight, and fiduciary responsibilities.

TRANSCRIPT:
{transcript}

{focus_context}

Please provide:

1. HEADLINE OPTIONS: Generate {num_headlines} headlines (maximum 8 words each) that emphasize governance implications, strategic oversight, or board-level decisions. Frame them as questions or imperatives that boards must address.

2. EXECUTIVE BRIEFING ({word_count} words): Write in a deliberative, governance-focused style with these subheadings:
   - **Strategic Oversight Implications**: What board-level decisions or oversight questions emerge?
   - **Risk & Governance Considerations**: What risks, compliance issues, or governance practices are highlighted?
   - **Fiduciary Takeaways**: What should boards be monitoring, challenging, or ensuring?
   
   Open with the most critical governance implication. Emphasize long-term value creation, stakeholder accountability, and board effectiveness. Use cautious, considered tone appropriate for fiduciary decision-making. Bold key governance facts.

3. CRITICAL INSIGHTS FOR BOARDS: List 5 insights specifically relevant to board oversight and governance

4. QUESTIONS FOR THE BOARD TO CONSIDER: Provide 5 probing questions that boards should discuss in executive session or with management

5. MOST IMPACTFUL QUOTES: Extract 5 powerful quotes (maximum 33 words each) that reveal governance wisdom, board dynamics, or strategic oversight insights. For each quote:
   - Provide the exact quote (in quotation marks)
   - Add 1-2 sentences explaining why this matters for board effectiveness or what governance principle it illustrates
   - Choose quotes that address fiduciary duty, oversight, risk, or strategic governance""",

                        "CEOs": f"""Analyze this executive interview transcript and create a CEO-focused synthesis emphasizing decisions, execution, and competitive positioning.

TRANSCRIPT:
{transcript}

{focus_context}

Please provide:

1. HEADLINE OPTIONS: Generate {num_headlines} action-oriented headlines (maximum 8 words each) that frame decisions, trade-offs, or competitive moves. Make them direct and decisive.

2. EXECUTIVE DECISION BRIEF ({word_count} words): Write in a direct, pragmatic style with these subheadings:
   - **The Decision on the Table**: What choices must be made NOW?
   - **Execution Challenges & Trade-offs**: What are the hard choices and implementation realities?
   - **Competitive Implications**: How does this affect market position and competitive advantage?
   
   Open with the most urgent decision or competitive insight. Emphasize speed, execution, and results. Write with urgency and decisiveness. Bold key decision points and metrics.

3. STRATEGIC INSIGHTS: List 5 insights about strategy, competition, or execution that matter for CEO decision-making

4. IMMEDIATE ACTIONS: List 5 specific decisions or initiatives the CEO should launch this quarter

5. MOST IMPACTFUL QUOTES: Extract 5 powerful quotes (maximum 33 words each) that reveal decision-making wisdom, execution insights, or competitive thinking. For each quote:
   - Provide the exact quote (in quotation marks)
   - Add 1-2 sentences explaining why this matters for CEO effectiveness or what it reveals about strategic decision-making
   - Choose quotes that are tactical, decisive, or reveal hard-won lessons about leading organizations""",

                        "Senior Executives": f"""Analyze this executive interview transcript and create a synthesis focused on implementation, capability-building, and leading change.

TRANSCRIPT:
{transcript}

{focus_context}

Please provide:

1. HEADLINE OPTIONS: Generate {num_headlines} headlines (maximum 8 words each) that emphasize implementation challenges, organizational capabilities, or change management imperatives.

2. LEADERSHIP IMPLEMENTATION GUIDE ({word_count} words): Write in a practical, team-oriented style with these subheadings:
   - **The Implementation Challenge**: What does this mean for translating strategy into action?
   - **Organizational Capabilities Required**: What skills, structures, or cultural shifts are needed?
   - **Leading the Change**: How should senior executives mobilize their teams and manage resistance?
   
   Open with the most critical implementation challenge. Emphasize people, processes, and change management. Write with empathy for the messy reality of execution. Bold key capability gaps and team dynamics.

3. CRITICAL SUCCESS FACTORS: List 5 insights about what separates successful implementation from failure

4. HOW TO APPLY THIS IN YOUR ORGANIZATION: Provide 5 specific actions senior executives can take with their teams in the next 30 days

5. MOST IMPACTFUL QUOTES: Extract 5 powerful quotes (maximum 33 words each) that reveal implementation wisdom, change leadership insights, or team dynamics. For each quote:
   - Provide the exact quote (in quotation marks)
   - Add 1-2 sentences explaining why this matters for execution or what it reveals about leading organizational change
   - Choose quotes that are practical, honest about challenges, or reveal lessons about mobilizing teams""",

                        "HR Leaders": f"""Analyze this executive interview transcript and create a synthesis focused on talent development, organizational culture, and leadership capabilities.

TRANSCRIPT:
{transcript}

{focus_context}

Please provide:

1. HEADLINE OPTIONS: Generate {num_headlines} headlines (maximum 8 words each) that emphasize leadership competencies, culture shifts, talent development, or people challenges.

2. TALENT & LEADERSHIP INSIGHTS ({word_count} words): Write in a developmental, people-centered style with these subheadings:
   - **Leadership Competencies on Display**: What leadership capabilities, behaviors, or mindsets are demonstrated?
   - **Talent & Culture Implications**: What does this reveal about developing leaders, building culture, or managing talent?
   - **Application for Executive Development**: How can HR leaders use these insights in leadership programs or succession planning?
   
   Open with the most compelling leadership or talent insight. Emphasize competency development, culture-building, and how leaders grow. Write with a developmental mindset focused on unlocking human potential. Bold key leadership behaviors and cultural attributes.

3. KEY LEADERSHIP LESSONS: List 5 insights about leadership effectiveness, talent development, or organizational culture

4. APPLICATIONS FOR HR LEADERS: Provide 5 specific ways to apply these insights in leadership development programs, coaching, or talent processes

5. MOST IMPACTFUL QUOTES: Extract 5 powerful quotes (maximum 33 words each) that reveal leadership wisdom, authentic experiences, or compelling insights. For each quote:
   - Provide the exact quote (in quotation marks)
   - Add 1-2 sentences explaining why this quote matters for leadership development or what it reveals about effective leadership
   - Choose quotes that are vivid, honest, surprising, or particularly instructive""",

                        "General Business Audience": f"""Analyze this executive interview transcript and create an accessible synthesis for a broad business audience.

TRANSCRIPT:
{transcript}

{focus_context}

Please provide:

1. HEADLINE OPTIONS: Generate {num_headlines} engaging, accessible headlines (maximum 8 words each) that capture the most interesting or surprising elements for a general business reader.

2. EXECUTIVE PERSPECTIVE ({word_count} words): Write in clear, journalistic style with these subheadings:
   - **The Big Picture**: What's the overarching insight or trend?
   - **Why It Matters**: How does this affect businesses, leaders, or the competitive landscape?
   - **What's Changing**: What's different now compared to conventional wisdom?
   
   Open with the most compelling or surprising finding. Provide context for readers who may not be experts. Use accessible language and real-world examples. Bold key statistics and turning points.

3. KEY TAKEAWAYS: List 5 insights that any business professional should understand

4. PRACTICAL APPLICATIONS: List 5 ways readers can apply these insights in their own roles or organizations

5. MOST IMPACTFUL QUOTES: Extract 5 powerful quotes (maximum 33 words each) that are memorable, surprising, or particularly instructive for a business audience. For each quote:
   - Provide the exact quote (in quotation marks)
   - Add 1-2 sentences explaining why this matters or what makes it noteworthy
   - Choose quotes that are accessible, thought-provoking, or challenge conventional business thinking"""
                    }
                    
                    # Select the appropriate prompt based on audience
                    prompt = audience_prompts.get(audience, audience_prompts["General Business Audience"])

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
