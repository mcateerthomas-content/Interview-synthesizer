# Executive Interview Synthesizer

A powerful web application that transforms interview transcripts into polished executive summaries with multiple format options.

## Features

- **Multiple Headline Options**: Generate 3-7 compelling headline variations
- **Narrative Summaries**: Create 350, 500, or 800-word journalistic syntheses
- **Audience Targeting**: Tailor content for Board Directors, CEOs, or Senior Executives
- **Focus Areas**: Emphasize specific themes like Leadership, Strategy, or Governance
- **Key Insights**: Extract surprising and actionable findings automatically
- **One-Click Download**: Export summaries as text files

## Quick Start

### Option 1: Run Locally (Recommended)

1. **Install Python** (if you don't have it):
   - Download from https://www.python.org/downloads/
   - Version 3.8 or higher required

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your Anthropic API key**:
   - Go to https://console.anthropic.com/
   - Sign up or log in
   - Navigate to API Keys
   - Create a new key and copy it

4. **Run the app**:
   ```bash
   streamlit run interview_synthesizer.py
   ```

5. **Open your browser**:
   - The app will automatically open at http://localhost:8501
   - If not, paste that URL into your browser

6. **Use the app**:
   - Paste your API key in the sidebar
   - Paste your transcript
   - Select your preferences
   - Click "Generate Summary"

### Option 2: Deploy to Cloud (Streamlit Community Cloud - Free)

1. **Create a GitHub repository**:
   - Upload `interview_synthesizer.py` and `requirements.txt`

2. **Deploy to Streamlit Cloud**:
   - Go to https://streamlit.io/cloud
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Deploy!

3. **Add API Key as Secret**:
   - In Streamlit Cloud settings, add your Anthropic API key as a secret
   - You can then modify the code to read from secrets instead of user input

## How to Use

1. **Paste Your Transcript**: Copy the full interview text into the input box
2. **Select Audience**: Choose who will read this (Board Directors, CEOs, etc.)
3. **Choose Word Count**: Pick 350, 500, or 800 words for your summary
4. **Select Focus Areas**: (Optional) Highlight specific themes
5. **Generate**: Click the button and wait 10-30 seconds
6. **Download**: Save your formatted summary

## Example Workflow

```
Input: 45-minute interview transcript with Sue Wagner about board leadership

Settings:
- Audience: Board Directors  
- Word Count: 500
- Headlines: 5 options
- Focus: Board Governance, Stakeholder Management

Output:
✓ 5 headline options to choose from
✓ 500-word narrative with 3 subheadings
✓ 5 key insights extracted
✓ 4 actionable takeaways
✓ Downloadable text file
```

## Tips for Best Results

- **Paste complete transcripts**: More context = better insights
- **Be specific with focus areas**: Guide the analysis toward your needs
- **Try multiple word counts**: Different lengths for different uses
- **Iterate on headlines**: Generate multiple times for more options
- **Save your API key**: Browser will remember it for the session

## Cost Estimate

- Each summary uses ~3,000-4,000 tokens
- At Claude Sonnet 4 pricing (~$3 per million input tokens):
- **Cost per summary: $0.01-0.03**
- 100 summaries = ~$1-3

## Customization Ideas

Want to modify the app? Here are easy changes:

1. **Add more audience types**: Edit line 51
2. **Change word count options**: Edit line 59
3. **Add new focus areas**: Edit lines 70-75
4. **Modify the prompt**: Edit lines 105-135
5. **Change the model**: Edit line 141 (try claude-opus-4 for higher quality)

## Troubleshooting

**"API Error: Invalid API Key"**
- Double-check your key from console.anthropic.com
- Make sure there are no extra spaces

**"Module not found"**
- Run: `pip install -r requirements.txt`

**"Port already in use"**
- Close other Streamlit apps or use: `streamlit run interview_synthesizer.py --server.port 8502`

**Slow generation**
- Normal for 500-800 word summaries (20-30 seconds)
- Try reducing word count for faster results

## Next Steps

Once you're comfortable with this tool, consider:

1. **Add a template library**: Save common audience/focus combinations
2. **Batch processing**: Upload multiple transcripts at once
3. **Style customization**: Define your writing preferences
4. **Integration**: Connect to your document management system
5. **Comparison mode**: Analyze multiple interviews side-by-side

## Support

Questions or issues? This was built as a custom tool for your workflow. To modify or extend it, just describe what you want changed in natural language and I (Claude) can generate the updated code.

---

**Built with**: Claude Sonnet 4 + Streamlit  
**License**: Private use  
**Version**: 1.0
