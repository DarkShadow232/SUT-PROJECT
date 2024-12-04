import json
import datetime
from datetime import datetime, timedelta
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import tkinter.font as tkfont

class LibraryGUI:
    def __init__(self):
        self.books = []
        self.borrowed_books = []
        self.load_data()
        
        # GUI Setup
        self.app = tk.Tk()
        self.app.title("Library Management System")
        self.app.geometry("1200x700")
        
        # Color scheme
        self.primary_color = "#2c3e50"  # Dark blue
        self.secondary_color = "#3498db"  # Light blue
        self.accent_color = "#e74c3c"  # Red
        self.bg_color = "#ecf0f1"  # Light gray
        self.text_color = "#2c3e50"  # Dark blue
        self.success_color = "#2ecc71"  # Green

        # Configure fonts
        self.title_font = Font(family="Helvetica", size=24, weight="bold")
        self.subtitle_font = Font(family="Helvetica", size=16, weight="bold")
        self.button_font = Font(family="Helvetica", size=11)
        self.text_font = Font(family="Helvetica", size=10)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure custom styles
        self.configure_styles()
        
        # Configure main window
        self.app.configure(bg=self.bg_color)
        
        # Create gradient header
        self.create_header()

        # Create main container
        self.main_container = ttk.Frame(self.app, style='Main.TFrame')
        self.main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Create sidebar and content area
        self.create_sidebar()
        self.content_frame = ttk.Frame(self.main_container, style='Content.TFrame')
        self.content_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))

        # Initialize with books view
        self.show_books_view()

    def configure_styles(self):
        # Frame styles
        self.style.configure('Main.TFrame', background=self.bg_color)
        self.style.configure('Content.TFrame', background=self.bg_color)
        self.style.configure('Sidebar.TFrame', background=self.primary_color)
        
        # Button styles
        self.style.configure('Sidebar.TButton',
                           font=self.button_font,
                           background=self.primary_color,
                           foreground='white',
                           padding=10)
        
        self.style.map('Sidebar.TButton',
                      background=[('active', self.secondary_color)],
                      foreground=[('active', 'white')])
        
        # Label styles
        self.style.configure('Title.TLabel',
                           font=self.title_font,
                           background=self.bg_color,
                           foreground=self.text_color)
        
        self.style.configure('Subtitle.TLabel',
                           font=self.subtitle_font,
                           background=self.bg_color,
                           foreground=self.text_color)
        
        # Entry styles
        self.style.configure('Custom.TEntry',
                           font=self.text_font,
                           padding=5)
        
        # Treeview styles
        self.style.configure('Custom.Treeview',
                           font=self.text_font,
                           rowheight=30,
                           background=self.bg_color,
                           fieldbackground=self.bg_color,
                           foreground=self.text_color)
        
        self.style.configure('Custom.Treeview.Heading',
                           font=self.button_font,
                           background=self.primary_color,
                           foreground='white')
        
        self.style.map('Custom.Treeview',
                      background=[('selected', self.secondary_color)],
                      foreground=[('selected', 'white')])
        
        # Delete button style
        self.style.configure('Delete.TButton',
                           font=self.button_font,
                           background=self.accent_color,
                           foreground='white',
                           padding=10)
        
        self.style.map('Delete.TButton',
                      background=[('active', '#c0392b')],  # Darker red on hover
                      foreground=[('active', 'white')])

    def create_header(self):
        header_frame = tk.Frame(self.app, height=60, bg=self.primary_color)
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Create gradient effect
        canvas = tk.Canvas(header_frame, height=60, bg=self.primary_color, highlightthickness=0)
        canvas.pack(fill='x')
        
        # Add title text
        canvas.create_text(40, 30, text="Library Management System",
                         font=self.title_font, fill='white', anchor='w')

    def create_sidebar(self):
        sidebar = ttk.Frame(self.main_container, style='Sidebar.TFrame')
        sidebar.pack(side="left", fill="y", padx=0, pady=0)

        # Navigation buttons
        buttons = [
            ("📚 View Books", self.show_books_view),
            ("➕ Add Book", self.show_add_book_view),
            ("📖 Borrow Book", self.show_borrow_view),
            ("↩️ Return Book", self.show_return_view),
            ("📋 Borrowed Books", self.show_borrowed_books_view),
            ("⏰ Overdue Books", self.show_overdue_view)
        ]

        for text, command in buttons:
            btn = ttk.Button(sidebar, text=text, command=command, style='Sidebar.TButton')
            btn.pack(pady=5, padx=10, fill="x")

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_books_view(self):
        self.clear_content()
        
        # Title
        title = ttk.Label(self.content_frame, text="Library Books", style='Title.TLabel')
        title.pack(pady=20)

        # Search frame
        search_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        search_frame.pack(fill='x', padx=20, pady=(0, 20))

        # Search entry
        search_entry = ttk.Entry(search_frame, width=40, style='Custom.TEntry')
        search_entry.pack(side="left", padx=10)
        search_entry.insert(0, "Search by title or author...")
        search_entry.bind('<FocusIn>', lambda e: search_entry.delete(0, 'end') if 
                         search_entry.get() == "Search by title or author..." else None)
        search_entry.bind('<FocusOut>', lambda e: search_entry.insert(0, "Search by title or author...") if 
                         search_entry.get() == "" else None)

        # Create table frame
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Create table
        columns = ('ID', 'Title', 'Author', 'Year', 'Status')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', style='Custom.Treeview')

        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')

        def update_table(search_term=""):
            # Clear current items
            for item in tree.get_children():
                tree.delete(item)

            # Filter and display books
            for book in self.books:
                if (search_term == "" or search_term.lower() in book['title'].lower() or 
                    search_term.lower() in book['author'].lower()):
                    status = "Available" if book['available'] else "Borrowed"
                    status_color = self.success_color if book['available'] else self.accent_color
                    tree.insert('', 'end', values=(book['id'], book['title'], book['author'], 
                                                book['publication_year'], status))

        def on_search():
            search_term = search_entry.get()
            if search_term == "Search by title or author...":
                search_term = ""
            update_table(search_term)

        # Search button
        search_btn = ttk.Button(search_frame, text="🔍 Search", command=on_search)
        search_btn.pack(side="left", padx=10)

        # Reset button
        reset_btn = ttk.Button(search_frame, text="🔄 Reset", command=lambda: (
            search_entry.delete(0, 'end'),
            search_entry.insert(0, "Search by title or author..."),
            update_table("")
        ))
        reset_btn.pack(side="left", padx=10)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Create delete button frame
        button_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        button_frame.pack(fill='x', padx=20, pady=10)

        def delete_selected():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a book to delete")
                return
            
            # Get the book ID from the selected item
            book_values = tree.item(selected_item)['values']
            book_id = book_values[0]
            
            # Confirm deletion
            if messagebox.askyesno("Confirm Deletion", 
                                f"Are you sure you want to delete the book '{book_values[1]}'?"):
                # Check if book is borrowed
                book = next((b for b in self.books if b['id'] == book_id), None)
                if book and not book['available']:
                    messagebox.showerror("Error", 
                                    "Cannot delete a borrowed book. Please wait for it to be returned.")
                    return
                
                # Remove from books list
                self.books = [b for b in self.books if b['id'] != book_id]
                # Remove from borrowed_books if present
                self.borrowed_books = [b for b in self.borrowed_books if b['book_id'] != book_id]
                
                # Save changes
                self.save_data()
                
                # Remove from treeview
                tree.delete(selected_item)
                messagebox.showinfo("Success", "Book deleted successfully!")

        # Add delete button
        delete_btn = ttk.Button(button_frame, text="🗑️ Delete Selected Book", 
                            command=delete_selected, style='Delete.TButton')
        delete_btn.pack(side='right', padx=5)
        
        # Pack elements
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Initial table population
        update_table()

    def show_add_book_view(self):
        self.clear_content()
        
        # Title
        title = ttk.Label(self.content_frame, text="Add New Book", style='Title.TLabel')
        title.pack(pady=20)

        # Form
        form_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        form_frame.pack(pady=20, padx=20)

        # Create a card-like effect
        form_canvas = tk.Canvas(form_frame, bg='white', highlightthickness=1,
                              highlightbackground=self.primary_color)
        form_canvas.pack(padx=20, pady=20, fill='both', expand=True)

        inner_frame = ttk.Frame(form_canvas, style='Content.TFrame')
        inner_frame.pack(padx=40, pady=40, fill='both', expand=True)

        # Title
        ttk.Label(inner_frame, text="Book Title", style='Subtitle.TLabel').pack(pady=(0, 5))
        title_entry = ttk.Entry(inner_frame, width=40, style='Custom.TEntry')
        title_entry.pack(pady=(0, 20))

        # Author
        ttk.Label(inner_frame, text="Author Name", style='Subtitle.TLabel').pack(pady=(0, 5))
        author_entry = ttk.Entry(inner_frame, width=40, style='Custom.TEntry')
        author_entry.pack(pady=(0, 20))

        # Year
        ttk.Label(inner_frame, text="Publication Year", style='Subtitle.TLabel').pack(pady=(0, 5))
        year_entry = ttk.Entry(inner_frame, width=40, style='Custom.TEntry')
        year_entry.pack(pady=(0, 20))

        def add_book():
            title = title_entry.get()
            author = author_entry.get()
            year = year_entry.get()

            if title and author and year:
                book = {
                    'id': len(self.books) + 1,
                    'title': title,
                    'author': author,
                    'publication_year': year,
                    'available': True
                }
                self.books.append(book)
                self.save_data()
                messagebox.showinfo("Success", f"Book '{title}' added successfully!")
                title_entry.delete(0, 'end')
                author_entry.delete(0, 'end')
                year_entry.delete(0, 'end')
            else:
                messagebox.showerror("Error", "Please fill all fields!")

        # Submit button
        submit_btn = ttk.Button(inner_frame, text="Add Book", command=add_book)
        submit_btn.pack(pady=20)

    def show_borrow_view(self):
        self.clear_content()
        
        # Title
        title = ttk.Label(self.content_frame, text="Borrow Book", style='Title.TLabel')
        title.pack(pady=20)

        # Form
        form_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        form_frame.pack(pady=20, padx=20)

        # Book ID
        ttk.Label(form_frame, text="Book ID", style='Subtitle.TLabel').pack(pady=(0, 5))
        book_id_entry = ttk.Entry(form_frame, width=40, style='Custom.TEntry')
        book_id_entry.pack(pady=(0, 20))

        # Student Name
        ttk.Label(form_frame, text="Student Name", style='Subtitle.TLabel').pack(pady=(0, 5))
        student_entry = ttk.Entry(form_frame, width=40, style='Custom.TEntry')
        student_entry.pack(pady=(0, 20))

        def borrow_book():
            try:
                book_id = int(book_id_entry.get())
                student_name = student_entry.get()

                if not student_name:
                    messagebox.showerror("Error", "Please enter student name!")
                    return

                for book in self.books:
                    if book['id'] == book_id and book['available']:
                        book['available'] = False
                        borrow_date = datetime.now()
                        due_date = borrow_date + timedelta(days=14)
                        
                        borrowed_info = {
                            'book_id': book_id,
                            'book_title': book['title'],
                            'student_name': student_name,
                            'borrow_date': borrow_date.strftime('%Y-%m-%d'),
                            'due_date': due_date.strftime('%Y-%m-%d')
                        }
                        
                        self.borrowed_books.append(borrowed_info)
                        self.save_data()
                        messagebox.showinfo("Success", 
                            f"Book '{book['title']}' has been borrowed by {student_name}.\n"
                            f"Due date: {due_date.strftime('%Y-%m-%d')}")
                        book_id_entry.delete(0, 'end')
                        student_entry.delete(0, 'end')
                        return

                messagebox.showerror("Error", "Book not available or invalid book ID!")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid book ID!")

        # Submit button
        submit_btn = ttk.Button(form_frame, text="Borrow Book", command=borrow_book)
        submit_btn.pack(pady=20)

    def show_return_view(self):
        self.clear_content()
        
        # Title
        title = ttk.Label(self.content_frame, text="Return Book", style='Title.TLabel')
        title.pack(pady=20)

        # Form
        form_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        form_frame.pack(pady=20, padx=20)

        # Book ID
        ttk.Label(form_frame, text="Book ID", style='Subtitle.TLabel').pack(pady=(0, 5))
        book_id_entry = ttk.Entry(form_frame, width=40, style='Custom.TEntry')
        book_id_entry.pack(pady=(0, 20))

        def return_book():
            try:
                book_id = int(book_id_entry.get())
                
                for book in self.books:
                    if book['id'] == book_id and not book['available']:
                        book['available'] = True
                        self.borrowed_books = [b for b in self.borrowed_books if b['book_id'] != book_id]
                        self.save_data()
                        messagebox.showinfo("Success", f"Book '{book['title']}' has been returned successfully!")
                        book_id_entry.delete(0, 'end')
                        return

                messagebox.showerror("Error", "Book not found or already returned!")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid book ID!")

        # Submit button
        submit_btn = ttk.Button(form_frame, text="Return Book", command=return_book)
        submit_btn.pack(pady=20)

    def show_overdue_view(self):
        self.clear_content()
        
        # Title
        title = ttk.Label(self.content_frame, text="Overdue Books", style='Title.TLabel')
        title.pack(pady=20)

        # Create table
        columns = ('Book Title', 'Student', 'Due Date', 'Days Overdue')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', style='Custom.Treeview')

        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Add data
        today = datetime.now()
        for borrowed in self.borrowed_books:
            due_date = datetime.strptime(borrowed['due_date'], '%Y-%m-%d')
            if today > due_date:
                days_overdue = (today - due_date).days
                tree.insert('', 'end', values=(borrowed['book_title'], borrowed['student_name'], 
                                             borrowed['due_date'], f"{days_overdue} days"))

        # Pack elements
        tree.pack(pady=20, padx=20, fill='both', expand=True, side='left')
        scrollbar.pack(pady=20, fill='y', side='right')

    def show_borrowed_books_view(self):
        self.clear_content()
        
        # Title
        title = ttk.Label(self.content_frame, text="Currently Borrowed Books", style='Title.TLabel')
        title.pack(pady=20)

        # Create table frame
        table_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        table_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Create table
        columns = ('Book ID', 'Book Title', 'Student Name', 'Borrow Date', 'Due Date', 'Status')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', style='Custom.Treeview')

        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor='center')

        # Add data
        today = datetime.now()
        for borrowed in self.borrowed_books:
            due_date = datetime.strptime(borrowed['due_date'], '%Y-%m-%d')
            status = "Overdue" if today > due_date else "On Time"
            status_color = self.accent_color if status == "Overdue" else self.success_color
            
            tree.insert('', 'end', values=(
                borrowed['book_id'],
                borrowed['book_title'],
                borrowed['student_name'],
                borrowed['borrow_date'],
                borrowed['due_date'],
                status
            ))

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Pack elements
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Add export button
        def export_borrowed_books():
            try:
                with open('borrowed_books_report.txt', 'w') as f:
                    f.write("LIBRARY BORROWED BOOKS REPORT\n")
                    f.write("Generated on: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\n")
                    f.write("-" * 100 + "\n")
                    
                    for borrowed in self.borrowed_books:
                        due_date = datetime.strptime(borrowed['due_date'], '%Y-%m-%d')
                        status = "Overdue" if today > due_date else "On Time"
                        
                        f.write(f"Book ID: {borrowed['book_id']}\n")
                        f.write(f"Title: {borrowed['book_title']}\n")
                        f.write(f"Borrowed by: {borrowed['student_name']}\n")
                        f.write(f"Borrow Date: {borrowed['borrow_date']}\n")
                        f.write(f"Due Date: {borrowed['due_date']}\n")
                        f.write(f"Status: {status}\n")
                        f.write("-" * 100 + "\n")
                
                messagebox.showinfo("Success", "Report exported to 'borrowed_books_report.txt'")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export report: {str(e)}")

        button_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        button_frame.pack(fill='x', padx=20, pady=10)
        
        export_btn = ttk.Button(button_frame, text="📄 Export Report", command=export_borrowed_books)
        export_btn.pack(side='right', padx=5)

    def load_data(self):
        # Load books data
        try:
            with open('books.json', 'r') as file:
                self.books = json.load(file)
        except FileNotFoundError:
            self.books = []

        # Load borrowed books data
        try:
            with open('borrowed_books.json', 'r') as file:
                self.borrowed_books = json.load(file)
        except FileNotFoundError:
            self.borrowed_books = []

    def save_data(self):
        # Save books data
        with open('books.json', 'w') as file:
            json.dump(self.books, file, indent=4)

        # Save borrowed books data
        with open('borrowed_books.json', 'w') as file:
            json.dump(self.borrowed_books, file, indent=4)

    def load_sample_data(self):
        sample_books = [
            {
                "id": 1,
                "title": "Harry Potter and the Philosopher's Stone",
                "author": "J.K. Rowling",
                "publication_year": "1997",
                "available": True
            },
            {
                "id": 2,
                "title": "The Lord of the Rings",
                "author": "J.R.R. Tolkien",
                "publication_year": "1954",
                "available": True
            },
            {
                "id": 3,
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "publication_year": "1960",
                "available": True
            },
            {
                "id": 4,
                "title": "1984",
                "author": "George Orwell",
                "publication_year": "1949",
                "available": True
            },
            {
                "id": 5,
                "title": "Pride and Prejudice",
                "author": "Jane Austen",
                "publication_year": "1813",
                "available": True
            },
            {
                "id": 6,
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "publication_year": "1925",
                "available": True
            },
            {
                "id": 7,
                "title": "The Hobbit",
                "author": "J.R.R. Tolkien",
                "publication_year": "1937",
                "available": True
            },
            {
                "id": 8,
                "title": "The Catcher in the Rye",
                "author": "J.D. Salinger",
                "publication_year": "1951",
                "available": True
            },
            {
                "id": 9,
                "title": "The Chronicles of Narnia",
                "author": "C.S. Lewis",
                "publication_year": "1950",
                "available": True
            },
            {
                "id": 10,
                "title": "Brave New World",
                "author": "Aldous Huxley",
                "publication_year": "1932",
                "available": True
            },
            {
                "id": 11,
                "title": "The Hunger Games",
                "author": "Suzanne Collins",
                "publication_year": "2008",
                "available": True
            },
            {
                "id": 12,
                "title": "The Da Vinci Code",
                "author": "Dan Brown",
                "publication_year": "2003",
                "available": True
            },
            {
                "id": 13,
                "title": "The Alchemist",
                "author": "Paulo Coelho",
                "publication_year": "1988",
                "available": True
            },
            {
                "id": 14,
                "title": "The Little Prince",
                "author": "Antoine de Saint-Exupéry",
                "publication_year": "1943",
                "available": True
            },
            {
                "id": 15,
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "publication_year": "1605",
                "available": True
            }
        ]

        # Add some borrowed books
        sample_borrowed = [
            {
                "book_id": 1,
                "book_title": "Harry Potter and the Philosopher's Stone",
                "student_name": "John Smith",
                "borrow_date": (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d'),
                "due_date": (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d')
            },
            {
                "book_id": 2,
                "book_title": "The Lord of the Rings",
                "student_name": "Emma Wilson",
                "borrow_date": (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d'),
                "due_date": (datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d')
            },
            {
                "book_id": 3,
                "book_title": "To Kill a Mockingbird",
                "student_name": "Michael Brown",
                "borrow_date": (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
                "due_date": (datetime.now() + timedelta(days=9)).strftime('%Y-%m-%d')
            }
        ]

        # Update availability for borrowed books
        for book in sample_books:
            if any(b["book_id"] == book["id"] for b in sample_borrowed):
                book["available"] = False

        # Confirm with user
        if messagebox.askyesno("Load Sample Data", 
                             "This will replace all current data with sample data. Continue?"):
            self.books = sample_books
            self.borrowed_books = sample_borrowed
            self.save_data()
            messagebox.showinfo("Success", "Sample data loaded successfully!")
            # Refresh the current view
            self.show_books_view()

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = LibraryGUI()
    app.run()
