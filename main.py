import tkinter as tk
from tkinter import messagebox
import requests
import json
import webbrowser

class BINCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BIN/CC Checker")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Styling
        self.root.configure(bg="#f0f0f0")
        self.font = ("Arial", 10)
        self.title_font = ("Arial", 14, "bold")
        
        # Header
        tk.Label(root, text="BIN/CC Checker", font=self.title_font, bg="#f0f0f0").pack(pady=10)
        
        # Input Frame
        input_frame = tk.Frame(root, bg="#f0f0f0")
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Enter BIN (first 6-8 digits):", font=self.font, bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.bin_entry = tk.Entry(input_frame, font=self.font, width=20)
        self.bin_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Check BIN", command=self.check_bin, bg="#4CAF50", fg="white", font=self.font).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Clear", command=self.clear_fields, bg="#f44336", fg="white", font=self.font).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Exit", command=root.quit, bg="#607D8B", fg="white", font=self.font).grid(row=0, column=2, padx=5)
        
        # Results Frame
        self.results_frame = tk.LabelFrame(root, text="BIN Information", font=self.font, bg="#f0f0f0")
        self.results_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Result labels
        self.result_labels = {
            "BIN": tk.Label(self.results_frame, text="", font=self.font, bg="#f0f0f0"),
            "Brand": tk.Label(self.results_frame, text="", font=self.font, bg="#f0f0f0"),
            "Type": tk.Label(self.results_frame, text="", font=self.font, bg="#f0f0f0"),
            "Bank": tk.Label(self.results_frame, text="", font=self.font, bg="#f0f0f0"),
            "Country": tk.Label(self.results_frame, text="", font=self.font, bg="#f0f0f0"),
            "Website": tk.Label(self.results_frame, text="", font=self.font, bg="#f0f0f0", fg="blue", cursor="hand2")
        }
        
        for i, (text, label) in enumerate(self.result_labels.items()):
            tk.Label(self.results_frame, text=f"{text}:", font=self.font, bg="#f0f0f0").grid(row=i, column=0, sticky="e", padx=5, pady=2)
            label.grid(row=i, column=1, sticky="w", padx=5, pady=2)
        
        self.result_labels["Website"].bind("<Button-1>", self.open_website)
        
        # Footer
        tk.Label(root, text="https://lookup.binlist.net/45717360", font=("Arial", 8), bg="#f0f0f0").pack(side="bottom", pady=5)
    
    def check_bin(self):
        bin_number = self.bin_entry.get().strip()
        
        if not bin_number.isdigit() or len(bin_number) < 6 or len(bin_number) > 8:
            messagebox.showerror("Error", "Please enter a valid BIN (6-8 digits)")
            return
        
        try:
            response = requests.get(f"https://lookup.binlist.net/{bin_number}", 
                                  headers={"Accept-Version": "3"})
            
            if response.status_code == 200:
                data = response.json()
                self.display_results(bin_number, data)
            else:
                messagebox.showerror("Error", f"BIN not found (Status: {response.status_code})")
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to connect to API: {str(e)}")
    
    def display_results(self, bin_number, data):
        self.result_labels["BIN"].config(text=bin_number)
        self.result_labels["Brand"].config(text=data.get("scheme", "N/A"))
        self.result_labels["Type"].config(text=data.get("type", "N/A"))
        
        bank_info = data.get("bank", {})
        self.result_labels["Bank"].config(text=bank_info.get("name", "N/A"))
        
        country_info = data.get("country", {})
        country_name = country_info.get("name", "N/A")
        country_emoji = country_info.get("emoji", "")
        self.result_labels["Country"].config(text=f"{country_name} {country_emoji}")
        
        bank_url = bank_info.get("url")
        if bank_url:
            self.result_labels["Website"].config(text=bank_url)
            self.result_labels["Website"].config(fg="blue", cursor="hand2")
        else:
            self.result_labels["Website"].config(text="N/A")
            self.result_labels["Website"].config(fg="black", cursor="")
    
    def open_website(self, event):
        url = self.result_labels["Website"].cget("text")
        if url != "N/A":
            webbrowser.open_new_tab(url)
    
    def clear_fields(self):
        self.bin_entry.delete(0, tk.END)
        for label in self.result_labels.values():
            label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = BINCheckerApp(root)
    root.mainloop()
