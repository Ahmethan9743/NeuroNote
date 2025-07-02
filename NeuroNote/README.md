# NeuroNote - AI-Powered Note-Taking Application

NeuroNote is a modern, AI-powered note-taking application designed to make your note management smarter, faster, and more productive. With advanced artificial intelligence features, NeuroNote helps you organize, summarize, and export your notes with ease. The app supports both English and Turkish languages, and you can switch between them instantly from the interface.

---

## Features

- **AI Summarization**: Instantly generate summaries of your notes using artificial intelligence (Summa and Transformers support).
- **Note Management**: Add, edit, and delete notes with a clean and intuitive interface.
- **Smart Grouping**: Organize your notes into categories (future versions will include advanced AI-based categorization).
- **Trash Bin**: Deleted notes are moved to a trash bin, where you can restore or permanently delete them.
- **Export**: Export all your notes as PDF or TXT files with one click.
- **Clipboard Support**: Copy notes directly to your clipboard for quick sharing.
- **Light/Dark Theme**: Easily switch between light and dark modes for comfortable use.
- **Language Toggle**: Instantly switch the entire app between English and Turkish.
- **Unit Tested**: Core features are covered by unit tests for reliability and maintainability.
- **Secure Export**: Export functions are protected against path-injection vulnerabilities.

---

## Installation

1. Clone this repository:
    ```
    git clone https://github.com/yourusername/NeuroNote.git
    cd NeuroNote
    ```
2. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

---

## Usage

To start the application, run:
```
python src/app.py
```
The application will launch and open in your browser.

---

## Project Structure

```
NeuroNote/
│
├── src/
│   ├── app.py             # Main application file (Flet UI)
│   ├── ai/
│   │   └── summarizer.py  # AI-based summarization and grouping
│   ├── test_app.py        # Unit tests for core functions
│   └── notlar.json        # Notes, trash, and summaries (auto-generated)
│
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── LICENSE                # MIT License
```

---

## Contributing

Contributions are welcome! Please open a pull request or submit an issue with your suggestions or bug reports.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Credits

- [Flet](https://flet.dev/) for the UI framework
- [Summa](https://github.com/summanlp/textrank) and [Transformers](https://huggingface.co/transformers/) for AI summarization
- [FPDF](https://pyfpdf.github.io/fpdf2/) for PDF export

---

**NeuroNote** is developed to make note-taking smarter, faster, and more productive with the power of AI.