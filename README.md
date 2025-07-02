# NeuroNote - AI-Powered Note-Taking Application

**NeuroNote** is a modern, multilingual, AI-powered note-taking application designed to streamline how you capture, organize, and summarize ideas. Whether you are a student, researcher, or professional, NeuroNote provides an intelligent and distraction-free writing experience.

---

## 🧠 Features

* **Note Creation**: Quickly create notes with a clean, intuitive interface.
* **Edit/Delete Notes**: Modify or remove notes at any time.
* **Trash Bin & Restore**: Accidentally deleted something? Restore it easily from the Trash.
* **Speech-to-Text**: Create notes by speaking — perfect for hands-free capture.
* **Export as PDF or TXT**: Save your notes in PDF or TXT format with one click.
* **AI Summarization**: Automatically summarize your notes using advanced NLP models.
* **Fullscreen View**: Expand individual notes to view them in fullscreen mode.
* **Copy to Clipboard**: Copy entire notes with a single click.
* **Dark/Light Mode**: Toggle between themes for comfortable reading.
* **Multilingual Support**: Switch between English and Turkish instantly.
* **Secure Exporting**: Exports are sanitized to protect against path-based vulnerabilities.

### 🔜 Coming in Next Update

* **German Language Support (Deutsch)**
* **Plugin System**: Extend NeuroNote with modular plugins for customization and advanced features.

---

## 🚀 Getting Started

### Installation

```bash
git clone https://github.com/yourusername/NeuroNote.git
cd NeuroNote
pip install -r requirements.txt
```

### Run the App

```bash
python src/app.py
```

The app will open in your browser.

---

## 📁 Project Structure

```
NeuroNote/
│
├── src/
│   ├── app.py             # Main Flet-based application
│   ├── ai/
│   │   └── summarizer.py  # Handles AI text summarization
│   ├── test_app.py        # Unit tests for key functionality
│   └── notlar.json        # Note data storage (auto-generated)
│
├── screenshots/           # App screenshots for documentation
│   ├── home.png
│   └── summary_dark_mode.png
│
├── requirements.txt       # Python dependencies
├── README.md              # You're reading it :)
└── LICENSE                # MIT License
```

---

## 📸 Screenshots

### 🏠 Home Page

![Home Page](screenshots/home.png)

### 🌓 Note Summary in Dark Mode

![Summary Dark Mode](screenshots/summary_dark_mode.png)

---

## 🤝 Contributing

We welcome contributions from developers around the world! If you'd like to suggest features, report bugs, or submit pull requests, feel free to open an issue or fork the repository.

---

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for full details.

---

## 🙌 Credits

* [Flet](https://flet.dev/) - UI framework
* [Summa](https://github.com/summanlp/textrank) - Extractive summarization engine
* [Transformers](https://huggingface.co/transformers/) - AI model support
* [FPDF](https://pyfpdf.github.io/fpdf2/) - PDF generation

---

**NeuroNote** — Write Ahmethan. Remember faster. Stay focused.
