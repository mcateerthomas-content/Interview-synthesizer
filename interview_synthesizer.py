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
        ["Board Directors + CEOs", "Senior Executives + HR Leaders", "CEOs + HR Leaders", "Group Leader Resources"],
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
                        "Board Directors + CEOs": f"""Analyze this executive interview transcript and create an integrated synthesis for both Board Directors (governance oversight) and CEOs (strategic execution).

TRANSCRIPT:
{transcript}

{focus_context}

Please provide:

1. HEADLINE OPTIONS: Generate {num_headlines} headlines (maximum 8 words each) that frame both governance implications AND strategic decisions. Bridge board oversight with CEO execution.

2. LEADERSHIP + STRATEGY SYNTHESIS ({word_count} words): Write in a deliberative yet action-oriented style with these subheadings:
   - **Governance Oversight + Strategic Decision**: What requires board approval AND what the CEO must execute?
   - **Risk, Opportunity & Execution Trade-offs**: What risks need board monitoring AND what execution challenges the CEO faces?
   - **Board-CEO Collaboration Framework**: How boards and CEOs must work together for success
   
   Open with the most critical decision requiring both board oversight and CEO execution. Balance fiduciary caution with strategic urgency. Show interdependence between governance and management. Bold key oversight points and decision junctures.

3. GOVERNANCE + STRATEGIC INSIGHTS: List 5 insights spanning both board oversight responsibilities and CEO execution imperatives

4. DIFFERENTIATED ACTIONS:
   - 3 Board Oversight Items: What boards must monitor, approve, or ensure
   - 3 CEO Decisions: Strategic moves the CEO must make immediately
   - 2 Board-CEO Collaborative Actions: Joint initiatives requiring aligned leadership

5. MOST IMPACTFUL QUOTES: Extract 5 powerful quotes that reveal both governance wisdom AND strategic thinking. For each quote:
   - Provide the exact quote (in quotation marks)
   - Add 1-2 sentences explaining why this matters for both board effectiveness AND CEO decision-making
   - Choose quotes that bridge oversight and execution (aim for 2-3 governance-focused and 2-3 strategy-focused quotes)
   - Prioritize impact over brevity - include full context needed for the quote to be truly instructive""",

                        "Senior Executives + HR Leaders": f"""Analyze this executive interview transcript and create an integrated synthesis for both Senior Executives (implementation) and HR Leaders (talent development).

TRANSCRIPT:
{transcript}

{focus_context}

Please provide:

1. HEADLINE OPTIONS: Generate {num_headlines} headlines (maximum 8 words each) that frame both implementation challenges AND talent implications. Bridge execution with people development.

2. EXECUTION + TALENT SYNTHESIS ({word_count} words): Write in a practical, people-centered style with these subheadings:
   - **Implementation Challenge + Talent Requirements**: What must be executed AND what capabilities are needed?
   - **Organizational Capabilities + Cultural Shifts**: What skills, structures, and culture changes enable success?
   - **Integrated Change + Development Plan**: How execution leaders and HR must collaborate
   
   Open with the most critical implementation challenge that requires significant talent development. Balance execution pragmatism with people development. Show how implementation and capability-building are inseparable. Bold key execution milestones and capability gaps.

3. EXECUTION + TALENT INSIGHTS: List 5 insights spanning both implementation effectiveness and talent development, showing their connection

4. DIFFERENTIATED ACTIONS:
   - 3 Senior Executive Actions: Implementation steps for the next 30 days
   - 3 HR Leader Initiatives: Talent programs to launch immediately  
   - 2 Collaborative Execution + HR Actions: Joint initiatives requiring both leaders

5. MOST IMPACTFUL QUOTES: Extract 5 powerful quotes that reveal both implementation wisdom AND talent development insights. For each quote:
   - Provide the exact quote (in quotation marks)
   - Add 1-2 sentences explaining why this matters for both execution success AND people development
   - Choose quotes that show how execution and capability-building interconnect (aim for 2-3 execution-focused and 2-3 talent-focused quotes)
   - Prioritize impact over brevity - include full context needed for the quote to be truly instructive""",

                        "CEOs + HR Leaders": f"""Analyze this executive interview transcript and create an integrated synthesis for both CEOs (strategic decisions) and HR Leaders (talent implications).

TRANSCRIPT:
{transcript}

{focus_context}

Please provide:

1. HEADLINE OPTIONS: Generate {num_headlines} headlines (maximum 8 words each) that frame both strategic decisions AND talent implications. Make them bridge business strategy and people strategy.

2. INTEGRATED EXECUTIVE SYNTHESIS ({word_count} words): Write in a strategic yet people-aware style with these subheadings:
   - **Strategic Decision + Talent Implications**: What business decisions must be made AND what talent/leadership is required?
   - **Organizational Capabilities Required**: What skills, culture, leadership bench, and HR systems are needed?
   - **Integrated Action Plan**: How CEOs and HR leaders must collaborate to execute successfully
   
   Open with the most critical strategic decision that has major talent implications. Balance business outcomes with people development. Show how strategy and talent are inseparable. Bold key integration points between strategy and people.

3. STRATEGIC + TALENT INSIGHTS: List 5 insights that span both business strategy and talent strategy, showing how they connect

4. INTEGRATED ACTIONS: Provide specific actions for:
   - 3 CEO Decisions: Strategic moves the CEO must make
   - 3 HR Initiatives: Talent programs HR must launch
   - 2 Collaborative CEO + HR Actions: Joint initiatives requiring both leaders

5. MOST IMPACTFUL QUOTES: Extract 5 powerful quotes that reveal the intersection of strategy and talent. For each quote:
   - Provide the exact quote (in quotation marks)
   - Add 1-2 sentences explaining why this matters for both strategic execution AND talent development
   - Choose quotes that show how business decisions and people decisions are interdependent (aim for 2-3 strategy-focused quotes and 2-3 people-focused quotes)
   - Prioritize impact over brevity - include full context needed for the quote to be truly instructive""",

                        "Group Leader Resources": f"""Analyze this executive interview transcript and create a facilitation toolkit for peer learning communities, executive coaches, and leadership development professionals.

TRANSCRIPT:
{transcript}

{focus_context}

Please provide:

1. HEADLINE OPTIONS: Generate {num_headlines} headlines (maximum 8 words each) that frame leadership themes, developmental questions, or key competencies demonstrated.

2. LEADERSHIP CASE STUDY ({word_count} words): Write in a reflective, developmental style with these subheadings:
   - **The Leadership Challenge**: What situation did the leader face? What made it difficult? What was at stake?
   - **Leadership Competencies in Action**: What specific capabilities, behaviors, or mindsets were demonstrated? What could other leaders learn?
   - **Application for Executive Development**: How can facilitators use this in programs? What discussions does this enable? What exercises does this support?
   
   Open with the most compelling leadership challenge or growth moment. Emphasize learning over judging. Use evidence-based developmental language. Bold key competencies and turning points.

3. KEY COMPETENCIES DEMONSTRATED: List 5 specific leadership competencies with:
   - **Competency name** (e.g., "Strategic Courage")
   - **How it showed up** (specific behavior from transcript)
   - **Why it mattered** (impact on outcomes)
   - **Development implication** (how to build this in others)

4. FACILITATION TOOLKIT: Provide 5 practical tools for peer learning sessions:
   - **Discussion Prompts** (2-3 open-ended questions to spark dialogue)
   - **Small Group Exercise** (one 15-20 minute breakout activity)
   - **Self-Reflection Questions** (2-3 individual journaling prompts)
   - **Application Planning** (one 30-day challenge or commitment)
   - **Case Study Variation** (one "What if..." scenario for deeper exploration)

5. MOST IMPACTFUL QUOTES: Extract 5 quotes with developmental power - revealing authentic struggles, vulnerability, growth moments, or challenging conventional thinking. For each quote:
   - Provide the exact quote (in quotation marks)
   - **Developmental insight:** What competency or principle this illustrates
   - **Facilitation tip:** How to use this quote in a learning session (be specific about timing, framing, or follow-up questions)
   - Prioritize impact over brevity - include full context, setup, and payoff needed for the quote to land powerfully in a learning environment"""
                    }
                    
                    # Select the appropriate prompt based on audience
                    prompt = audience_prompts.get(audience, audience_prompts["Board Directors + CEOs"])

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
