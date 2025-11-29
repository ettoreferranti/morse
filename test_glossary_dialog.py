#!/usr/bin/env python3
"""
Quick test to verify the abbreviation glossary dialog works.

This script launches just the glossary dialog for visual testing.
"""

import tkinter as tk
from tkinter import ttk
from qso_data import ABBREVIATIONS, ABBREVIATION_CATEGORIES


def show_abbreviation_glossary(root):
    """Display searchable glossary of amateur radio abbreviations"""
    glossary_window = tk.Toplevel(root)
    glossary_window.title("Amateur Radio Abbreviations")
    glossary_window.geometry("700x600")

    # Header
    header_frame = ttk.Frame(glossary_window)
    header_frame.pack(fill=tk.X, padx=10, pady=10)

    ttk.Label(header_frame,
             text="Amateur Radio Abbreviations",
             font=('TkDefaultFont', 14, 'bold')).pack()

    ttk.Label(header_frame,
             text=f"{len(ABBREVIATIONS)} abbreviations used in QSO practice",
             font=('TkDefaultFont', 9)).pack()

    # Search bar
    search_frame = ttk.Frame(glossary_window)
    search_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

    ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_frame, textvariable=search_var, width=30)
    search_entry.pack(side=tk.LEFT, padx=(0, 10))

    # Category filter
    ttk.Label(search_frame, text="Category:").pack(side=tk.LEFT, padx=(10, 5))
    category_var = tk.StringVar(value="All")
    category_combo = ttk.Combobox(search_frame,
                                  textvariable=category_var,
                                  values=["All"] + list(ABBREVIATION_CATEGORIES.keys()),
                                  state='readonly',
                                  width=20)
    category_combo.pack(side=tk.LEFT)

    # Results area with scrollbar
    results_frame = ttk.Frame(glossary_window)
    results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    # Create Treeview for organized display
    tree_scroll = ttk.Scrollbar(results_frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(results_frame,
                       columns=('Abbr', 'Meaning', 'Category'),
                       show='headings',
                       yscrollcommand=tree_scroll.set,
                       height=20)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    tree_scroll.config(command=tree.yview)

    # Configure columns
    tree.heading('Abbr', text='Abbreviation')
    tree.heading('Meaning', text='Meaning')
    tree.heading('Category', text='Category')

    tree.column('Abbr', width=120, anchor=tk.W)
    tree.column('Meaning', width=350, anchor=tk.W)
    tree.column('Category', width=150, anchor=tk.W)

    # Find category for each abbreviation
    def get_category(abbr):
        for category, abbrs in ABBREVIATION_CATEGORIES.items():
            if abbr in abbrs:
                return category
        return "Other"

    # Populate tree
    def update_display(*args):
        # Clear tree
        for item in tree.get_children():
            tree.delete(item)

        search_text = search_var.get().upper()
        selected_category = category_var.get()

        # Filter and display abbreviations
        count = 0
        for abbr, meaning in sorted(ABBREVIATIONS.items()):
            category = get_category(abbr)

            # Apply filters
            if selected_category != "All" and category != selected_category:
                continue

            if search_text:
                if search_text not in abbr.upper() and search_text not in meaning.upper():
                    continue

            # Add to tree
            tree.insert('', tk.END, values=(abbr, meaning, category))
            count += 1

        # Update status
        status_label.config(text=f"Showing {count} of {len(ABBREVIATIONS)} abbreviations")

    # Status bar
    status_frame = ttk.Frame(glossary_window)
    status_frame.pack(fill=tk.X, padx=10, pady=(0, 5))

    status_label = ttk.Label(status_frame, text="")
    status_label.pack(side=tk.LEFT)

    # Bind search updates
    search_var.trace('w', update_display)
    category_var.trace('w', update_display)

    # Initial display
    update_display()

    # Close button
    button_frame = ttk.Frame(glossary_window)
    button_frame.pack(fill=tk.X, padx=10, pady=(5, 10))

    ttk.Button(button_frame,
              text="Close",
              command=glossary_window.destroy).pack(side=tk.RIGHT)

    # Focus on search entry
    search_entry.focus()


def main():
    """Test the glossary dialog"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    print("Opening abbreviation glossary dialog...")
    print("Test the following features:")
    print("  1. Search for abbreviations (e.g., 'QSO', 'signal')")
    print("  2. Filter by category")
    print("  3. Verify all 62 abbreviations appear")
    print("  4. Check sorting and display")
    print("\nClose the dialog window to exit.")

    show_abbreviation_glossary(root)
    root.mainloop()


if __name__ == '__main__':
    main()
