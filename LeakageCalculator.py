import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

# Global variable to keep track of tab count
tab_count = 1

def classify_leakage(measured, L_values):
    if measured <= L_values[0]:
        return "L1"
    elif measured <= L_values[1]:
        return "L2"
    else:
        return "L3"

def calculate(tab):
    try:
        # Get entries from the current tab
        length = float(tab.length_entry.get())
        width = float(tab.width_entry.get())
        height = float(tab.height_entry.get())

        underpressure_leak = float(tab.underpressure_leak_entry.get())
        overpressure_leak = float(tab.overpressure_leak_entry.get())

        # Calculate section Area [m²]
        area = ((2 * (width + height)) * length) + (2 * (width * height))

        # Constants for Air Leakage Rate [dm³/sm²]
        leakage_rates = {
            "Underpressure": [0.15, 0.44, 1.32],
            "Overpressure": [0.22, 0.63, 1.9]
        }

        calculated_leakages = {}
        results = []

        for pressure_type, constants in leakage_rates.items():
            results.append(f"--- {pressure_type} Leakage Rate ---")
            calculated_leakages[pressure_type] = []

            for i, C in enumerate(constants, start=1):
                leakage = area * C
                calculated_leakages[pressure_type].append(leakage)
                results.append(f"Class L{i}: {leakage:.2f} l/s")

        # Classify measured values
        underpressure_class = classify_leakage(underpressure_leak, calculated_leakages["Underpressure"])
        overpressure_class = classify_leakage(overpressure_leak, calculated_leakages["Overpressure"])

        # Append classification results
        results.append("\n--- Classification Based on Measured Values ---")
        results.append(f"Measured Underpressure Leak: {underpressure_leak:.2f} l/s → Class {underpressure_class}")
        results.append(f"Measured Overpressure Leak: {overpressure_leak:.2f} l/s → Class {overpressure_class}")

        # Display results in the scrolled text box
        tab.result_output.config(state=tk.NORMAL)
        tab.result_output.delete("1.0", tk.END)  # Clear previous results
        tab.result_output.insert(tk.END, "\n".join(results))
        tab.result_output.config(state=tk.DISABLED)

    except ValueError:
        tab.result_output.config(state=tk.NORMAL)
        tab.result_output.delete("1.0", tk.END)
        tab.result_output.insert(tk.END, "❌ Please enter valid numeric values!")
        tab.result_output.config(state=tk.DISABLED)

def add_tab():
    global tab_count
    new_tab = ttk.Frame(notebook)
    
    
    # Ensure that the first tab is inserted normally if no other tabs exist
    if len(notebook.tabs()) > 0:
        notebook.insert(notebook.index("end") - 1, new_tab, text=f"Tab {tab_count}")
    else:
        notebook.add(new_tab, text=f"Tab {tab_count}")  # First tab is added normally

     #  **Title Label and Entry Field**
    tk.Label(new_tab, text="Measured Section:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    title_entry = tk.Entry(new_tab, width=20)
    title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")
    
    #  **Function to update the tab title dynamically**
    def update_tab_title(*args):
        new_title = title_entry.get().strip()
        if new_title:
            notebook.tab(new_tab, text=new_title)  # Update tab title

     # Bind the title entry to update tab title when text changes
    title_entry.bind("<KeyRelease>", update_tab_title)
    
    # Create input fields for dimensions
    input_labels = ["Length [m]:", "Width [m]:", "Height [m]:", "Underpressure Leak [l/s]:", "Overpressure Leak [l/s]:"]
    entries = []

    for i, label in enumerate(input_labels):
        tk.Label(new_tab, text=label).grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(new_tab, width=10)
        entry.grid(row=i+1, column=1, padx=5, pady=5, sticky="we")
        entries.append(entry)

    calculate_button = tk.Button(new_tab, text="Calculate", command=lambda: calculate(new_tab), bg="#4CAF50", fg="white")
    calculate_button.grid(row=len(input_labels)+1, column=0, columnspan=2, pady=10, sticky="we")

    result_output = scrolledtext.ScrolledText(new_tab, height=10, wrap=tk.WORD, state=tk.DISABLED)
    result_output.grid(row=len(input_labels) + 2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

    new_tab.length_entry, new_tab.width_entry, new_tab.height_entry, new_tab.underpressure_leak_entry, new_tab.overpressure_leak_entry = entries
    new_tab.title_entry = title_entry
    new_tab.result_output = result_output

    for i in range(2):  
        new_tab.columnconfigure(i, weight=1)
    new_tab.rowconfigure(len(input_labels) + 2, weight=1)  # Make results box expand

    tab_count += 1


# Initialize window
root = tk.Tk()
root.title("Leakage Calculator")
root.geometry("800x600")

# Allow window to be resized
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


# Create a notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Function to ensure "+" tab is at the end
def maintain_plus_tab():
    if notebook.tab(notebook.index("end") - 1, "text") != "+":
        plus_tab = ttk.Frame(notebook)
        notebook.add(plus_tab, text="+")
        notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

# Function to handle clicking the "+" tab
def on_tab_changed(event):
    if notebook.tab(notebook.select(), "text") == "+":
        add_tab()
        # Ensure "+" tab is always last
        notebook.add(notebook.tab(notebook.index("end") - 1, "text"), text="+", sticky="nsew")
        maintain_plus_tab()

add_tab()

# Add "+" tab first
plus_tab = ttk.Frame(notebook)
notebook.add(plus_tab, text="+")
notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

# Run the main event loop
test
test
test
root.mainloop()