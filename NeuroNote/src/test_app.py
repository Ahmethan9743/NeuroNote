import unittest
import os
import json
from app import (
    summarize_text, load_data, save_data, DATA_FILE
)

# Class that tests the basic functions of the NeuroNote application
class TestNeuroNote(unittest.TestCase):
    def setUp(self):
        # Runs before each test: Prepares the file and sample data to be used for testing
        self.test_file = "test_notlar.json"  # File name to be used during the test
        self.notes = [
            {"title": "Başlık1", "content": "İçerik1. Bu bir testtir."},
            {"title": "Başlık2", "content": "İçerik2. Bu da başka bir testtir."}
        ]
        self.trash = [
            {"title": "Çöp", "content": "Çöp içeriği"}
        ]
        self.summaries = ["Özet1", "Özet2"]
        # Redirect the DATA_FILE variable to the test file (backup the global variable)
        global DATA_FILE
        self._old_data_file = DATA_FILE
        DATA_FILE = self.test_file

    def tearDown(self):
        # Runs after each test: Deletes the test file and restores DATA_FILE to its old value
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        global DATA_FILE
        DATA_FILE = self._old_data_file

    def test_save_and_load_data(self):
        # After saving notes, trash, and summaries, reading them again should return the same data
        save_data(self.notes, self.trash, self.summaries, data_file=self.test_file)
        notes, trash, summaries = load_data(data_file=self.test_file)
        self.assertEqual(notes, self.notes)         # Are notes correct?
        self.assertEqual(trash, self.trash)         # Is trash correct?
        self.assertEqual(summaries, self.summaries) # Are summaries correct?

    def test_summarize_text(self):
        # summarize_text function should return a summary and this summary should be a string
        text = "Yapay zeka, günümüzde birçok alanda kullanılmaktadır. Eğitim, sağlık ve finans gibi sektörlerde önemli rol oynamaktadır."
        summary = summarize_text(text)
        self.assertTrue(isinstance(summary, str))  # Is the result a string?
        self.assertTrue(len(summary) > 0)          # Is the result not empty?

    def test_load_data_empty(self):
        # If the file does not exist, load_data function should return empty lists
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        notes, trash, summaries = load_data(data_file=self.test_file)
        self.assertEqual(notes, [])      # Are notes empty?
        self.assertEqual(trash, [])      # Is trash empty?
        self.assertEqual(summaries, [])  # Are summaries empty?

    def test_save_data_creates_file(self):
        # save_data function should create a file and it should contain the correct keys
        save_data(self.notes, self.trash, self.summaries, data_file=self.test_file)
        self.assertTrue(os.path.exists(self.test_file))  # Was the file created?
        with open(self.test_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertIn("notes",