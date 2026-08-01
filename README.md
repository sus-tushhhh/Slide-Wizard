<div align='center'>

# 🪄 Slide Wizard

> **Generate AI-powered presentations, create news articles from real-time web data, and produce AI-generated images—all from one Streamlit application.**

SlideWizard AI is an intelligent content generation platform built using **Python**, **Streamlit**, **LangChain**, **Google Gemini**, **Tavily Search**, and **Pollinations.ai**. It helps users quickly generate presentation content, retrieve the latest news, and create AI-generated images using simple natural language prompts.

> **Note:** The presentation is currently exported as an **HTML file**, allowing it to be viewed directly in a web browser.

</div>

---

## ✨ Features

### 📊 AI Presentation Generator

- Generate complete presentations from a text prompt.
- Select the desired number of slides.
- AI creates structured slide titles and content.
- Download the presentation as an **HTML file**.
- Clean and responsive presentation layout.

---

### 🌟 Additional Features

#### 📰 AI News Article Generator

Stay updated with the latest information without leaving the application.

- Fetches real-time information using **Tavily Search**.
- Generates comprehensive and well-structured news articles.
- Perfect for research, blogs, and current affairs.

---

#### 🎨 AI Image Generator

Generate AI-powered images directly from text prompts.

- Powered by **Pollinations.ai**.
- Create visuals for presentations, articles, or creative projects.
- Download generated images with ease.

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Google Gemini API
- Tavily Python
- Pollinations.ai

---

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/SlideWizard-AI.git

cd SlideWizard-AI
```

---

## 🔑 Configure API Keys

This project uses **Streamlit Secrets** instead of environment variables.

Create the following file:

```text
.streamlit/secrets.toml
```

Add your API keys:

```toml
[api_key]
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
TAVILY_API_KEY = "YOUR_TAVILY_API_KEY"
```

---

## ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will automatically open in your default browser.

---

## 📖 Usage

### 📊 Generate a Presentation

1. Open the application.
2. Enter your presentation topic.
3. Select the number of slides.
4. Click **Generate**.
5. Download the generated presentation as an **HTML** file.

---

### 📰 Generate a News Article

1. Select the News Generator.
2. Enter a topic or keyword.
3. Tavily retrieves the latest information.
4. Gemini converts the search results into a well-formatted article.

---

### 🎨 Generate an Image

1. Open the Image Generator.
2. Enter a descriptive prompt.
3. Pollinations.ai creates an AI-generated image.
4. Download the generated image.

---

## 💡 Use Cases

- Student presentations
- Academic projects
- Research summaries
- Business presentations
- News writing
- Blog content
- AI-assisted content creation
- Marketing material
- Educational content

---

## 🔒 Security

API keys are securely managed using **Streamlit Secrets**.

Do **not** hardcode your API keys or commit the `.streamlit/secrets.toml` file to a public repository.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Developer

**Tushant**  
🔗 GitHub: https://github.com/sus-tushhhh
