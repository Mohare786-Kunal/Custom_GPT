# ***RAG Bot with Streamlit and LangChain***

![RAG Bot]([https://your-image-link.com/banner.png](https://miro.medium.com/v2/resize:fit:1400/1*cHlQK5M1GRaeS_A-RbH1hw.jpeg)])  
*A Retrieval Augmented Generation (RAG) Bot built with Streamlit and LangChain.*

## **Table of Contents**
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## **Overview**
This project is a Retrieval Augmented Generation (RAG) bot built using **Streamlit** and **LangChain**. The bot combines the power of language models with retrieval mechanisms, enabling it to fetch and generate highly relevant information from a large dataset.

## **Features**
- 🔍 **Smart Retrieval**: Efficiently searches through your dataset to find the most relevant information.
- 🤖 **Custom GPT Integration**: Utilizes a custom GPT model to generate insightful responses.
- 🎨 **Interactive UI**: Powered by Streamlit, offering an intuitive and user-friendly interface.
- 🚀 **Real-Time Responses**: Provides instant answers based on the latest data.
- 🛠 **Configurable**: Easily tweak settings to suit your specific needs.

## **Installation**

### **Prerequisites**
- Python 3.8 or higher
- Streamlit
- LangChain
- OpenAI API Key

### **Step-by-Step Guide**
1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/rag-bot.git
    cd rag-bot
    ```

2. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your environment variables:**
   - Add your OpenAI API key in the `.env` file in the root directory
     ```
     OPENAI_API_KEY=your-openai-api-key
     ```

4. **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

## **Usage**
1. **Start the Streamlit app**: After running the command above, the app should open automatically in your default web browser.

2. **Interacting with the Bot**: 
   - Enter your query in the provided text box.
   - Hit "Submit" and watch the bot fetch relevant data and generate a response in real time.

3. **Customization**:
   - Modify the `config.yaml` file to adjust the bot's behavior, such as changing the retrieval model or tweaking response generation parameters.

## **Configuration**
- **`config.yaml`**: Contains settings for the bot, such as the model parameters and retrieval method.
- **`data/`**: Directory where your dataset is stored. You can load text files, PDFs, or any other supported formats.
- **`app.py`**: The main Streamlit application file where the UI is defined.

## **Contributing**
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature/bug fix.
3. Submit a pull request with a clear description of the changes.

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
