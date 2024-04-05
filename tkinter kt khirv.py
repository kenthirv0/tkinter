# K.Hirv
# 05.04.24
# 05.03.24 tkinter töö

import tkinter as tk
from tkinter import messagebox
import csv
import os

class LibrarySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Raamatukogu Laenutussüsteem")

        # Raamatute andmete sisestamise osa
        self.frame_books = tk.LabelFrame(root, text="Raamatute andmed")
        self.frame_books.pack(fill="both", expand="yes", padx=20, pady=10)

        tk.Label(self.frame_books, text="Pealkiri:").grid(row=0, column=0)
        tk.Label(self.frame_books, text="Autor:").grid(row=1, column=0)
        tk.Label(self.frame_books, text="Väljaandeaasta:").grid(row=2, column=0)

        self.title_entry = tk.Entry(self.frame_books)
        self.title_entry.grid(row=0, column=1)
        self.author_entry = tk.Entry(self.frame_books)
        self.author_entry.grid(row=1, column=1)
        self.year_entry = tk.Entry(self.frame_books)
        self.year_entry.grid(row=2, column=1)

        self.add_book_button = tk.Button(self.frame_books, text="Lisa raamat", command=self.add_book)
        self.add_book_button.grid(row=3, columnspan=2, pady=5)

        # Lugejate andmete sisestamise osa
        self.frame_readers = tk.LabelFrame(root, text="Lugejate andmed")
        self.frame_readers.pack(fill="both", expand="yes", padx=20, pady=10)

        tk.Label(self.frame_readers, text="Nimi:").grid(row=0, column=0)
        tk.Label(self.frame_readers, text="Kontaktandmed:").grid(row=1, column=0)

        self.name_entry = tk.Entry(self.frame_readers)
        self.name_entry.grid(row=0, column=1)
        self.contact_entry = tk.Entry(self.frame_readers)
        self.contact_entry.grid(row=1, column=1)

        self.add_reader_button = tk.Button(self.frame_readers, text="Lisa lugeja", command=self.add_reader)
        self.add_reader_button.grid(row=2, columnspan=2, pady=5)

        # Raamatute ja lugejate kuvamine
        self.listbox_books = tk.Listbox(root)
        self.listbox_books.pack(padx=20, pady=10)
        self.listbox_books.bind("<Double-Button-1>", self.edit_selected_book)

        self.listbox_readers = tk.Listbox(root)
        self.listbox_readers.pack(padx=20, pady=10)
        self.listbox_readers.bind("<Double-Button-1>", self.edit_selected_reader)

        # Kustutamise nupud
        self.delete_book_button = tk.Button(root, text="Kustuta raamat", command=self.delete_selected_book)
        self.delete_book_button.pack()
        
        self.delete_reader_button = tk.Button(root, text="Kustuta lugeja", command=self.delete_selected_reader)
        self.delete_reader_button.pack()

        # Raamatute ja lugejate andmete salvestamine
        self.books = []
        self.readers = []
        self.load_data()

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()
        self.books.append({"Pealkiri": title, "Autor": author, "Väljaandeaasta": year})
        self.save_data("books.csv", self.books)
        self.update_books_listbox()

    def add_reader(self):
        name = self.name_entry.get()
        contact = self.contact_entry.get()
        self.readers.append({"Nimi": name, "Kontaktandmed": contact})
        self.save_data("readers.csv", self.readers)
        self.update_readers_listbox()

    def delete_selected_book(self):
        selected_index = self.listbox_books.curselection()
        if selected_index:
            index = selected_index[0]
            del self.books[index]
            if self.books:  # Kontroll, kas nimekiri on tühi
                self.save_data("books.csv", self.books)
            else:
                # Kui nimekiri on tühi, salvestamist pole vaja teha
                os.remove("books.csv")
            self.update_books_listbox()
        else:
            messagebox.showwarning("Hoiatus", "Palun vali raamat, mida soovid kustutada.")

    def delete_selected_reader(self):
        selected_index = self.listbox_readers.curselection()
        if selected_index:
            index = selected_index[0]
            del self.readers[index]
            if self.readers:  # Kontroll, kas nimekiri on tühi
                self.save_data("readers.csv", self.readers)
            else:
                # Kui nimekiri on tühi, salvestamist pole vaja teha
                os.remove("readers.csv")
            self.update_readers_listbox()
        else:
            messagebox.showwarning("Hoiatus", "Palun vali lugeja, keda soovid kustutada.")

    def edit_selected_book(self, event):
        selected_index = self.listbox_books.curselection()
        if selected_index:
            index = selected_index[0]
            book = self.books[index]
            self.edit_book_window(book, index)

    def edit_selected_reader(self, event):
        selected_index = self.listbox_readers.curselection()
        if selected_index:
            index = selected_index[0]
            reader = self.readers[index]
            self.edit_reader_window(reader, index)

    def edit_book_window(self, book, index):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Raamatu muutmine")

        tk.Label(edit_window, text="Pealkiri:").grid(row=0, column=0)
        tk.Label(edit_window, text="Autor:").grid(row=1, column=0)
        tk.Label(edit_window, text="Väljaandeaasta:").grid(row=2, column=0)

        title_entry = tk.Entry(edit_window)
        title_entry.grid(row=0, column=1)
        title_entry.insert(0, book["Pealkiri"])

        author_entry = tk.Entry(edit_window)
        author_entry.grid(row=1, column=1)
        author_entry.insert(0, book["Autor"])

        year_entry = tk.Entry(edit_window)
        year_entry.grid(row=2, column=1)
        year_entry.insert(0, book["Väljaandeaasta"])

        save_button = tk.Button(edit_window, text="Salvesta", command=lambda: self.save_book_changes(title_entry.get(), author_entry.get(), year_entry.get(), index))
        save_button.grid(row=3, columnspan=2, pady=5)

    def edit_reader_window(self, reader, index):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Lugeja muutmine")

        tk.Label(edit_window, text="Nimi:").grid(row=0, column=0)
        tk.Label(edit_window, text="Kontaktandmed:").grid(row=1, column=0)

        name_entry = tk.Entry(edit_window)
        name_entry.grid(row=0, column=1)
        name_entry.insert(0, reader["Nimi"])

        contact_entry = tk.Entry(edit_window)
        contact_entry.grid(row=1, column=1)
        contact_entry.insert(0, reader["Kontaktandmed"])

        save_button = tk.Button(edit_window, text="Salvesta", command=lambda: self.save_reader_changes(name_entry.get(), contact_entry.get(), index))
        save_button.grid(row=2, columnspan=2, pady=5)

    def save_book_changes(self, new_title, new_author, new_year, index):
        self.books[index]["Pealkiri"] = new_title
        self.books[index]["Autor"] = new_author
        self.books[index]["Väljaandeaasta"] = new_year
        self.save_data("books.csv", self.books)
        self.update_books_listbox()

    def save_reader_changes(self, new_name, new_contact, index):
        self.readers[index]["Nimi"] = new_name
        self.readers[index]["Kontaktandmed"] = new_contact
        self.save_data("readers.csv", self.readers)
        self.update_readers_listbox()

    def save_data(self, filename, data):
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def load_data(self):
        if os.path.exists("books.csv"):
            with open("books.csv") as file:
                reader = csv.DictReader(file)
                self.books = [row for row in reader]
                self.update_books_listbox()

        if os.path.exists("readers.csv"):
            with open("readers.csv") as file:
                reader = csv.DictReader(file)
                self.readers = [row for row in reader]
                self.update_readers_listbox()

    def update_books_listbox(self):
        self.listbox_books.delete(0, tk.END)
        for book in self.books:
            self.listbox_books.insert(tk.END, f"{book['Pealkiri']} - {book['Autor']} ({book['Väljaandeaasta']})")

    def update_readers_listbox(self):
        self.listbox_readers.delete(0, tk.END)
        for reader in self.readers:
            self.listbox_readers.insert(tk.END, f"{reader['Nimi']} - {reader['Kontaktandmed']}")

root = tk.Tk()
app = LibrarySystem(root)
root.mainloop()
