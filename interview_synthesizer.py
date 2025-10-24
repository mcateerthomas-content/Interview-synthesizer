import streamlit as st
import anthropic
from datetime import datetime
import re

# Page configuration
st.set_page_config(
    page_title="Executive Interview Synthesizer",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS for better formatting
st.markdown("""
    <style>
    .audience-header {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .stMultiSelect > label {
        font-size: 1.2em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("🎯 Executive Interview Synthesizer")
st.markdown("Transform interview transcripts into targeted summaries for multiple audiences simultaneously.")

# Check for API key in Streamlit Secrets
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    api_key_configured = True
except:
    api_key_configured = False

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.info("This tool processes interview transcripts and generates customized summaries for different executive audiences with distinct perspectives and priorities.")
    
    if api_key_configured:
        st.success("✅ API key configured securely")
    else:
        st.error("⚠️ API key not found in Streamlit Secrets")
        st.markdown("""
        **Setup Instructions:**
        1. Go to your Streamlit app settings
        2. Navigate to 'Secrets' section
        3. Add: `ANTHROPIC_API_KEY = "your-key-here"`
        4. Save and reboot the app
        """)
    
    st.divider()
    st.markdown("### 📊 Usage Statistics")
    if 'total_summaries' not in st.session_state:
        st.session_state.total_summaries = 0
    st.metric("Total Summaries Generated", st.session_state.total_summaries)

# Main content area
if not api_key_configured:
    st.error("🔐 **API Key Not Configured**")
    st.markdown("""
    This app requires an Anthropic API key to be configured in Streamlit Secrets.
    
    **For App Administrator:**
    1. Go to [Streamlit Cloud Dashboard](https://app.streamlit.io)
    2. Click on your app's settings (⋮ menu)
    3. Select "Settings" → "Secrets"
    4. Add the following:
    ```toml
    ANTHROPIC_API_KEY = "sk-ant-xxxxx"
    ```
    5. Save and restart the app
    
    **For Team Members:**
    Please contact your administrator to ensure the API key is configured.
    """)
else:
    # Create two columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Input")
        
        # Multi-select for audiences
        selected_audiences = st.multiselect(
            "Select Target Audiences:",
            ["Board Directors", "CEOs", "Senior Executives", "HR Leaders", "General Business Audience"],
            default=["CEOs"],
            help="Select one or more audiences to generate tailored summaries"
        )
        
        # Transcript input
        transcript = st.text_area(
            "Paste Interview Transcript:",
            height=400,
            placeholder="Paste the full interview transcript here..."
        )
        
        # Generate button
        if st.button("🚀 Generate Summaries", type="primary", disabled=not (transcript and selected_audiences)):
            if not selected_audiences:
                st.error("Please select at least one target audience")
            elif transcript:
                with st.spinner(f"Generating summaries for {len(selected_audiences)} audience(s)..."):
                    try:
                        # Initialize Anthropic client with secret key
                        client = anthropic.Anthropic(api_key=api_key)
                        
                        # Store results
                        results = {}
                        
                        # Generate summary for each selected audience
                        for audience in selected_audiences:
                            
                            # Audience-specific prompts
                            audience_prompts = {
                                "Board Directors": """
                                Create a Board Directors summary focusing on:
                                - Governance implications
                                - Strategic oversight considerations  
                                - Risk management insights
                                - Long-term value creation
                                
                                Structure:
                                1. ONE headline (max 8 words, compelling and strategic)
                                2. Strategic Overview (100 words) - Focus on governance and oversight implications
                                3. Key Governance Insights - 3 specific insights relevant to board oversight
                                4. Risk Considerations - 2-3 potential risks or opportunities boards should monitor
                                5. Questions for Management - 3 specific questions directors should ask
                                6. Impactful Quotes - 3 verbatim quotes (max 33 words each) that resonate with board priorities
                                """,
                                
                                "CEOs": """
                                Create a CEO summary focusing on:
                                - Strategic decisions and trade-offs
                                - Organizational transformation
                                - Competitive positioning
                                - Leadership lessons
                                
                                Structure:
                                1. ONE headline (max 8 words, action-oriented)
                                2. Executive Summary (100 words) - Focus on strategic implications and decisions
                                3. Strategic Imperatives - 3 critical actions or decisions
                                4. Implementation Challenges - 2-3 key obstacles and how to address them  
                                5. Leadership Lessons - 3 specific lessons for CEO-level leadership
                                6. Impactful Quotes - 3 verbatim quotes (max 33 words each) that CEOs would find compelling
                                """,
                                
                                "Senior Executives": """
                                Create a Senior Executive summary focusing on:
                                - Operational implementation
                                - Team leadership applications
                                - Cross-functional collaboration
                                - Execution excellence
                                
                                Structure:
                                1. ONE headline (max 8 words, implementation-focused)
                                2. Operations Overview (100 words) - Focus on execution and team implications
                                3. Implementation Roadmap - 3 specific steps for execution
                                4. Team Applications - 3 ways to cascade insights to teams
                                5. Cross-Functional Opportunities - 2-3 collaboration points
                                6. Impactful Quotes - 3 verbatim quotes (max 33 words each) relevant to execution
                                """,
                                
                                "HR Leaders": """
                                Create an HR Leaders summary focusing on:
                                - Talent development implications
                                - Leadership pipeline building
                                - Culture and capability development
                                - Organizational effectiveness
                                
                                Structure:
                                1. ONE headline (max 8 words, talent-focused)
                                2. Talent Overview (100 words) - Focus on people and capability implications
                                3. Leadership Development Applications - 3 specific ways to develop leaders
                                4. Culture Building Insights - 3 cultural elements to reinforce or change
                                5. Capability Gaps to Address - 2-3 skill or competency areas to develop
                                6. Impactful Quotes - 3 verbatim quotes (max 33 words each) about talent or culture
                                """,
                                
                                "General Business Audience": """
                                Create a General Business summary focusing on:
                                - Accessible business insights
                                - Practical applications
                                - Professional development
                                - Industry trends
                                
                                Structure:
                                1. ONE headline (max 8 words, broadly appealing)
                                2. Overview (100 words) - Accessible explanation of key insights
                                3. Key Takeaways - 3 main lessons in plain language
                                4. Practical Applications - 3 ways any professional can apply these insights
                                5. Industry Implications - 2-3 broader trends or changes highlighted
                                6. Impactful Quotes - 3 verbatim quotes (max 33 words each) that resonate broadly
                                """
                            }
                            
                            prompt = f"""
                            Analyze this interview transcript and create a targeted summary for {audience}.
                            
                            {audience_prompts[audience]}
                            
                            Requirements:
                            - Headlines must be 8 words or less
                            - All quotes must be verbatim from transcript, maximum 33 words
                            - Make each audience version DRAMATICALLY different in focus and language
                            - Be specific and actionable, not generic
                            
                            Transcript:
                            {transcript}
                            """
                            
                            message = client.messages.create(
                                model="claude-3-5-sonnet-20241022",
                                max_tokens=1500,
                                temperature=0.3,
                                messages=[{"role": "user", "content": prompt}]
                            )
                            
                            results[audience] = message.content[0].text
                        
                        # Display results in the second column
                        with col2:
                            st.header("🎯 Generated Summaries")
                            
                            # Create tabs for each audience if multiple selected
                            if len(selected_audiences) > 1:
                                tabs = st.tabs(selected_audiences)
                                for i, (tab, audience) in enumerate(zip(tabs, selected_audiences)):
                                    with tab:
                                        st.markdown(f'<div class="audience-header"><h3>{audience}</h3></div>', 
                                                  unsafe_allow_html=True)
                                        st.markdown(results[audience])
                                        st.divider()
                                        
                                        # Download button for individual summary
                                        st.download_button(
                                            label=f"📥 Download {audience} Summary",
                                            data=results[audience],
                                            file_name=f"{audience.lower().replace(' ', '_')}_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                                            mime="text/plain",
                                            key=f"download_{audience}"
                                        )
                            else:
                                # Single audience display
                                audience = selected_audiences[0]
                                st.markdown(f'<div class="audience-header"><h3>{audience}</h3></div>', 
                                          unsafe_allow_html=True)
                                st.markdown(results[audience])
                                st.divider()
                                
                                # Download button for single summary
                                st.download_button(
                                    label=f"📥 Download {audience} Summary",
                                    data=results[audience],
                                    file_name=f"{audience.lower().replace(' ', '_')}_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                                    mime="text/plain"
                                )
                            
                            # If multiple audiences selected, offer combined download
                            if len(selected_audiences) > 1:
                                st.divider()
                                combined_content = ""
                                for audience in selected_audiences:
                                    combined_content += f"\n{'='*50}\n"
                                    combined_content += f"AUDIENCE: {audience.upper()}\n"
                                    combined_content += f"{'='*50}\n\n"
                                    combined_content += results[audience]
                                    combined_content += "\n\n"
                                
                                st.download_button(
                                    label="📥 Download All Summaries (Combined)",
                                    data=combined_content,
                                    file_name=f"all_summaries_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                                    mime="text/plain",
                                    type="secondary"
                                )
                        
                        st.success(f"✅ Successfully generated {len(selected_audiences)} audience summary/summaries!")
                        st.session_state.total_summaries += len(selected_audiences)
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        st.info("Please check your API key and try again.")
            else:
                st.warning("Please paste a transcript to analyze")
    
    with col2:
        if not transcript or not selected_audiences:
            st.header("🎯 Generated Summaries")
            st.info("Your generated summaries will appear here once you:\n1. Select one or more target audiences\n2. Paste a transcript\n3. Click 'Generate Summaries'")
            
            # Show example of what's possible
            with st.expander("💡 Multi-Select Examples"):
                st.markdown("""
                **Single Audience:** Select just "CEOs" for a focused CEO perspective
                
                **Leadership Team:** Select "CEOs" + "Senior Executives" for C-suite and their direct reports
                
                **Board Package:** Select "Board Directors" + "CEOs" for board meeting preparation
                
                **Full Organization:** Select all five audiences to create comprehensive communications for different levels
                
                **HR Initiative:** Select "HR Leaders" + "Senior Executives" for talent development rollout
                """)

# Footer
st.divider()
st.caption("Executive Interview Synthesizer | Powered by Claude")
