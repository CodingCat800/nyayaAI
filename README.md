# NyayaAI --- Consumer Refund Assistant

**An AI-powered consumer refund assistant for Indian consumers.**

NyayaAI helps consumers organize refund-related complaints, identify
missing information, preserve relevant evidence, understand possible
next steps, and generate editable complaint drafts.

## Problem

Consumers often struggle to obtain refunds after cancelling an order,
returning a product, or cancelling a service. Important information is
spread across order confirmations, emails, payment records, and
customer-support conversations.

NyayaAI turns an unstructured refund complaint into an organized case
with practical next steps.

## Features

-   **Natural-language intake:** Describe a refund issue in plain
    language.
-   **Case analysis:** Generate a structured summary of the issue.
-   **Timeline reconstruction:** Organize key events and dates.
-   **Missing-information detection:** Highlight details needed to
    understand the case.
-   **Evidence checklist:** Identify documents and records worth
    preserving.
-   **Suggested next steps:** Provide practical guidance for pursuing
    the refund.
-   **Complaint generation:** Create an editable complaint draft for the
    seller or platform.
-   **LLM integration:** Use an OpenAI-compatible Chat Completions API,
    with a deterministic fallback when the LLM is unavailable.

## Tech Stack

-   Python
-   Streamlit
-   OpenAI-compatible LLM API
-   Requests
-   python-dotenv

## Project Structure

``` text
NyayaAI/
│
├── app.py
├── nyayaai/
│   ├── engine.py
│   └── legal.py
├── tests/
├── outputs/
├── .env.example
├── requirements.txt
└── README.md
```

*The folders shown above should match the files included in the
repository.*

## Setup and Installation

### Prerequisites

-   Python 3.10 or newer
-   pip
-   An API key from a supported OpenAI-compatible LLM provider
    (optional; the deterministic fallback can be used without LLM
    credentials)

### 1. Clone the repository

``` bash
git clone https://github.com/YOUR_USERNAME/NyayaAI.git
cd NyayaAI
```

### 2. Create a virtual environment

``` bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows --- Command Prompt:**

``` cmd
.venv\Scripts\activate
```

**Windows --- PowerShell:**

``` powershell
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

``` bash
source .venv/bin/activate
```

### 4. Install dependencies

``` bash
pip install -r requirements.txt
```

### 5. Configure the LLM (optional)

Create a file named `.env` in the project root, in the same directory as
`app.py`. Use `.env.example` as a template.

For example, with a compatible provider:

``` env
NYAYAI_LLM_BASE_URL=https://api.groq.com/openai/v1
NYAYAI_LLM_API_KEY=your_api_key
NYAYAI_LLM_MODEL=your_supported_model
```

Use a model currently supported by your provider. If LLM credentials are
not configured, the application can use its deterministic fallback.

**Security:** Do not upload or commit `.env`. Keep the real API key
private. Only upload `.env.example` with placeholder values.

### 6. Run the application

From the project root, execute:

``` bash
streamlit run app.py
```

Streamlit will print a local URL in the terminal, usually:

``` text
http://localhost:8501
```

Open that URL in your browser to use NyayaAI.

To stop the application, press `Ctrl + C` in the terminal.

## Example

**User input:**

> I ordered a shirt for ₹1,000 online. I cancelled the order, but I
> haven't received my refund yet. Customer support keeps asking me to
> wait. What should I do?

NyayaAI can produce:

-   A structured case summary.
-   A timeline of events and facts.
-   A list of missing information.
-   An evidence checklist.
-   Suggested next steps.
-   An editable complaint draft.

## Future Scope

The current prototype demonstrates the core refund-assistance workflow.
Potential future extensions include:

-   **Retrieval-Augmented Generation (RAG):** Ground responses in
    verified government legislation, regulations, and
    consumer-protection resources.
-   **Document OCR:** Extract information from invoices, receipts,
    emails, and screenshots.
-   **Multilingual support:** Allow consumers to interact in Indian
    languages.
-   **Voice input:** Let users describe complaints through speech.
-   **Case tracking:** Track complaint progress and important dates.
-   **Human review:** Support review of complex cases by qualified
    professionals.

These are proposed extensions and are not represented as implemented
features of the current prototype.

## Limitations and Disclaimer

NyayaAI is an informational assistance tool. It is not a law firm and
does not replace a qualified lawyer or professional legal advice.

-   It does not represent consumers or automatically file complaints.
-   Its suggestions should be independently verified.
-   LLM-generated outputs may contain inaccuracies.
-   The current prototype demonstrates a focused workflow; it is not a
    complete legal case-management platform.

## Contributing

Suggestions, bug reports, and contributions are welcome. You can fork
the repository and submit a pull request.

## Author

**Juswin Jaimathew**

Built as an AI product prototype exploring how AI can make consumer
grievance resolution more accessible, structured, and understandable.
