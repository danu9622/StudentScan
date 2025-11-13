# 🎓 StudentScan

StudentScan - a smart attendance tool that uses image recognition to read student IDs from cards and verify their presence automatically.

**StudentScan** is a Python-based attendance verification system that uses **OCR (Optical Character Recognition)** to read student IDs directly from student card photos.  
It compares the extracted ID with a local database to confirm valid students and automatically marks attendance with timestamps.

---

## ✨ Features
- 🔍 Extracts student ID numbers from card images using [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- 📁 Verifies IDs against a local database (`students.txt`)
- 🕒 Automatically logs attendance to `attendance.txt`
- 💻 Works fully offline — no internet connection needed
- 🧾 Simple, lightweight, and easy to customize

---

## 🧠 How It Works
1. Take or upload a photo of the student card  
2. StudentScan processes the image and reads the ID number  
3. The program checks if the ID exists in the student database  
4. If valid, the student is marked **present** with the date and time

---
