from langchain_openai import ChatOpenAI, OpenAIEmbeddings  # Import OpenAI integrations from new package
from langchain import PromptTemplate, LLMChain

# Define a prompt for threat analysis
analysis_prompt = PromptTemplate(
    input_variables=["title", "content"],
    template=(
        "You are a cybersecurity threat analyst. Read the following news article and determine if it "
        "describes any cybersecurity threats or incidents. If so, summarize the threat and its potential impact, "
        "and assess its relevance.\n\n"
        "Title: {title}\n"
        "Content: {content}\n\n"
        "Threat Analysis:"
        "\n- Severity Level (Low, Medium, High, Critical):\n"
        "- Confidence (Low, Medium, High):\n"
        "- Recommended action in concise bullet points:\n"
        "- Key Indicators of Compromise (IOCs):\n"
        "- Affected systems or sectors:\n"
        "- Mitigation strategies or recommendations:\n"
        "- Potential threat actors or groups involved:\n"
        "- Historical context or similar incidents:\n"
        "- Summary of the threat and its potential impact:\n"
        "- Relevance to current cybersecurity landscape:\n"
        "- Additional notes or comments:\n"
        "- CVE references or related vulnerabilities:\n"
        "\nProvide your answer clearly formatted."
        )
)

# Initialize the OpenAI chat model (ChatGPT) with desired parameters
llm = ChatOpenAI(model="gpt-4", temperature=0)  # model param replaces deprecated model_name&#8203;:contentReference[oaicite:3]{index=3}

# Create a LangChain LLMChain for the analysis task
analysis_chain = LLMChain(llm=llm, prompt=analysis_prompt)

def analyze_article(title: str, content: str) -> str:
    """Run the threat analysis LLM chain on a single article."""
    try:
        result = analysis_chain.run(title=title, content=content)
        # .run passes the inputs to the prompt; using keywords for multiple variables (no deprecation warnings).
        return result.strip()
    except Exception as err:
        # Handle exceptions (e.g., API errors) gracefully
        return f"Error during analysis: {err}"
