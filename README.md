# Library Management System

A modern GUI-based Library Management System with an easy-to-use interface.

## Using the Executable Version

1. Go to the `dist` folder
2. Copy these files to any location on your computer:
   - `library_gui.exe` (the main program)
   - `books.json` (book database)
   - `borrowed_books.json` (borrowing records)

3. Double-click `library_gui.exe` to run the program

**Important Notes:**
- Keep all files in the same folder
- Don't modify the JSON files manually
- The program will save all changes automatically

## Features
- View and manage books
- Add new books
- Search books
- Borrow and return books
- Track overdue books
- Modern, user-friendly interface

## Installation Instructions

1. Make sure you have Python 3.x installed on your computer
   - Download Python from [python.org](https://www.python.org/downloads/)
   - During installation, make sure to check "Add Python to PATH"

2. Download or clone this repository to your computer

3. Open a terminal/command prompt in the project folder

4. Install required packages:
```bash
pip install -r requirements.txt
```

## Running the Program

1. Make sure all these files are present in your folder:
   - library_gui.py
   - books.json
   - borrowed_books.json
   - requirements.txt

2. Run the program:
```bash
python library_gui.py
```

## Data Files
- `books.json`: Contains the library's book collection
- `borrowed_books.json`: Tracks borrowed books and due dates

## Troubleshooting

If you encounter "No module named 'tkinter'" error:
- Windows: Reinstall Python and make sure to check "tcl/tk and IDLE" during installation
- Linux: Run `sudo apt-get install python3-tk`
- Mac: Python from python.org includes tkinter by default

If the program doesn't start:
1. Make sure all files are in the same folder
2. Try running as administrator
3. Check if any antivirus is blocking the program
4. Make sure the JSON files are not corrupted

For any other issues, make sure:
1. All required files are in the same folder
2. Python is properly installed and added to PATH
3. All dependencies are installed using pip
