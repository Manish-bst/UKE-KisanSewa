import tkinter as tk
from tkinter import messagebox, ttk
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import webbrowser
import json
API_KEY = 'bd8cf8c8e762bbdaa8de1c91d2deddf8'
districts = ['Dehradun', 'Almora', 'Nainital', 'Pauri', 'Rudraprayag', 'Tehri', 'UdhamSinghNagar', 'Pithoragarh', 'Bageshwar', 'Haridwar', 'Chamoli', 'Champawat']
# File paths
data_file = 'crop_data.json'
# Global variables
signup_username_var = None
signup_password_var = None
signup_confirm_password_var = None
# Load or initialize data
def load_data():
    if not os.path.exists(data_file):
        # Initialize data if file does not exist
        initial_data = {
            'crop_info': {
                'MarketPrice': {
                    'Bageshwar': {'Wheat': 2070,'Rice': 1790,'Barley': 1670,'Mustard': 1970,'Maize': 1480,'Potato': 1170,'Tomato': 1470,'Millet': 1570,'Peas': 1770,'Soybean': 1870,'Cucumber': 1370,'Ladyfinger': 1580,'Pumpkin': 1240,
                    },
                    'Chamoli': {'Wheat': 2100,'Rice': 1750,'Barley': 1690,'Mustard': 1980,'Maize': 1430,'Potato': 1160,'Tomato': 1360,'Millet': 1540,'Peas': 1730,'Soybean': 1830,'Cucumber': 1270,'Ladyfinger': 1570,'Pumpkin': 1280,
                    },
                    'Champawat': {'Wheat': 1980,'Rice': 1890,'Barley': 1600,'Mustard': 1990,'Maize': 1450,'Potato': 1270,'Tomato': 1420,'Millet': 1470,'Peas': 1790,'Soybean': 1890,'Cucumber': 1340,'Ladyfinger': 1520,'Pumpkin': 1210,
                    },
                    'Dehradun': {'Wheat': 2040,'Rice': 1760,'Barley': 1640,'Mustard': 1950,'Maize': 1500,'Potato': 1150,'Tomato': 1490,'Millet': 1540,'Peas': 1780,'Soybean': 1820,'Cucumber': 1400,'Ladyfinger': 1590,'Pumpkin': 1200,
                    },
                    'Haridwar': {'Wheat': 2100,'Rice': 1800,'Barley': 1650,'Mustard': 1970,'Maize': 1480,'Potato': 1140,'Tomato': 1590,'Millet': 1510,'Peas': 1760,'Soybean': 1850,'Cucumber': 1310,'Ladyfinger': 1560,'Pumpkin': 1100,
                    },
                    'Nainital': {'Wheat': 1960,'Rice': 1730,'Barley': 1690,'Mustard': 1960,'Maize': 1420,'Potato': 1170,'Tomato': 1430,'Millet': 1530,'Peas': 1790,'Soybean': 1870,'Cucumber': 1320,'Ladyfinger': 1570,'Pumpkin': 1210,
                    },
                    'Pauri': {'Wheat': 2060,'Rice': 1790,'Barley': 1630,'Mustard': 1800,'Maize': 1450,'Potato': 1100,'Tomato': 1500,'Millet': 1520,'Peas': 1740,'Soybean': 1850,'Cucumber': 1370,'Ladyfinger': 1590,'Pumpkin': 1300,
                    },
                    'Pithoragarh': {'Wheat': 2030,'Rice': 1700,'Barley': 1670,'Mustard': 1930,'Maize': 1510,'Potato': 1120,'Tomato': 1420,'Millet': 1550,'Peas': 1760,'Soybean': 1830,'Cucumber': 1320,'Ladyfinger': 1570,'Pumpkin': 1170,
                    },
                    'Rudraprayag': {'Wheat': 2100,'Rice': 1730,'Barley': 1690,'Mustard': 1870,'Maize': 1520,'Potato': 1170,'Tomato': 1470,'Millet': 1530,'Peas': 1750,'Soybean': 1800,'Cucumber': 1290,'Ladyfinger': 1540,'Pumpkin': 1280,
                    },
                    'Tehri': {'Wheat': 2080,'Rice': 1800,'Barley': 1590,'Mustard': 1920,'Maize': 1480,'Potato': 1200,'Tomato': 1490,'Millet': 1550,'Peas': 1600,'Soybean': 1870,'Cucumber': 1340,'Ladyfinger': 1490,'Pumpkin': 1270,
                    },
                    'UdhamSinghNagar': {'Wheat': 2030,'Rice': 1760,'Barley': 1700,'Mustard': 1970,'Maize': 1420,'Potato': 1130,'Tomato': 1470,'Millet': 1570,'Peas': 1770,'Soybean': 1900,'Cucumber': 1320,'Ladyfinger': 1550,'Pumpkin': 1270,
                    },
                    'Almora': {'Wheat': 2070,'Rice': 1780,'Barley': 1680,'Mustard': 1960,'Maize': 1480,'Potato': 1130,'Tomato': 1430,'Millet': 1470,'Peas': 1720,'Soybean': 1870,'Cucumber': 1340,'Ladyfinger': 1530,'Pumpkin': 1240,
                    },
                },
                'CropAdvisory': {
                    'Barley': {
                        'advisory': 'Best sown in September for winter harvest.',
                        'irrigation_time': '1 hour',
                        'harvesting_time': 'April',
                        'fertilization_time': 'Before sowing',
                        'fertilizer_recommendation': 'Urea, DAP',
                        'expected_diseases': 'Rust, Blight',
                        'disease_remedies': 'Fungicide A, Fungicide B',
                    },
                    'Cucumber': {
                        'advisory': 'Sow in April for summer crop.',
                        'irrigation_time': '1.5 hours',
                        'harvesting_time': 'July',
                        'fertilization_time': 'After 3 weeks of planting',
                        'fertilizer_recommendation': 'NPK',
                        'expected_diseases': 'Powdery Mildew, Cucumber Beetle',
                        'disease_remedies': 'Fungicide C, Insecticide D',
                    },
                    'Ladyfinger': {
                        'advisory': 'Best planted in May for summer yield.',
                        'irrigation_time': '1 hour',
                        'harvesting_time': 'August',
                        'fertilization_time': 'Before sowing',
                        'fertilizer_recommendation': 'Urea, NPK',
                        'expected_diseases': 'Yellow Vein Mosaic, Powdery Mildew',
                        'disease_remedies':'Insecticide E, Fungicide F',
                    },
                    'Maize': {
                        'advisory': 'Plant in April for summer crop.',
                        'irrigation_time': '2 hours',
                        'harvesting_time': 'September',
                        'fertilization_time': 'After 4 weeks of planting',
                        'fertilizer_recommendation': 'Urea, DAP',
                        'expected_diseases': 'Maize Weevil, Gray Leaf Spot',
                        'disease_remedies': 'Insecticide G, Fungicide H',
                    },
                    'Millet': {
                        'advisory': 'Sow in June for monsoon crop.',
                        'irrigation_time': '1 hour',
                        'harvesting_time': 'October',
                        'fertilization_time': 'Before sowing',
                        'fertilizer_recommendation': 'Urea, NPK',
                        'expected_diseases': 'Blast, Smuts',
                        'disease_remedies': 'Fungicide I, Fungicide J',
                    },
                    'Mustard': {
                        'advisory': 'Ideal planting time is October to November.',
                        'irrigation_time': '1 hour',
                        'harvesting_time': 'March',
                        'fertilization_time': 'Before sowing',
                        'fertil izer_recommendation': 'Urea, DAP',
                        'expected_diseases': 'White Rust, Alternaria',
                        'disease_remedies': 'Fungicide K, Fungicide L',
                    },
                    'Peas': {
                        'advisory': 'Best sown in November for winter harvest.',
                        'irrigation_time': '1 hour',
                        'harvesting_time': 'May',
                        'fertilization_time': 'Before sowing',
                        'fertilizer_recommendation': 'Urea, NPK',
                        'expected_diseases': 'Powdery Mildew, Root Rot',
                        'disease_remedies': 'Fungicide M, Fungicide N',
                    },
                    'Potato': {
                        'advisory': 'Plant in February for early harvest.',
                        'irrigation_time': '2 hours',
                        'harvesting_time': 'August',
                        'fertilization_time': 'After planting',
                        'fertilizer_recommendation': 'NPK, Potash',
                        'expected_diseases': 'Late Blight, Fusarium Wilt',
                        'disease_remedies': 'Fungicide O, Fungicide P',
                    },
                    'Pumpkin': {
                        'advisory': 'Sow in June for monsoon crop.',
                        'irrigation_time': '1.5 hours',
                        'harvesting_time': 'October',
                        'fertilization_time': 'After 2 weeks of planting',
                        'fertilizer_recommendation': 'NPK',
                        'expected_diseases': 'Powdery Mildew, Crown Rot',
                        'disease_remedies': 'Fungicide Q, Fungicide R',
                    },
                    'Rice': {
                        'advisory': 'Transplant seedlings in June for optimal growth.',
                        'irrigation_time': 'Continuous flooding',
                        'harvesting_time': 'September',
                        'fertilization_time': 'After 30 days of sowing',
                        'fertilizer_recommendation': 'Urea, Potash',
                        'expected_diseases': 'Blast, Sheath blight',
                        'disease_remedies': 'Fungicide C, Fungicide D',
                    },
                    'Soybean': {
                        'advisory': 'Plant in June for summer yield.',
                        'irrigation_time': '1 hour',
                        'harvesting_time': 'October',
                        'fertilization_time': 'Before sowing',
                        'fertilizer_recommendation': 'NPK',
                        'expected_diseases': 'Soybean Cyst Nematode, Powdery Mildew',
                        'disease_remedies': 'Insecticide S, Fungicide T',
                    },
                    'Tomato': {
                        'advisory': 'Transplant in March for summer crop.',
                        'irrigation_time': '1.5 hours',
                        'harvesting_time': 'July',
                        'fertilization_time': 'After 4 weeks of planting',
                        'fertilizer_recommendation': 'NPK, Calcium',
                        'expected_diseases': 'Blight, Wilt',
                        'disease_remedies': 'Fungicide U, Fungicide V',
                    },
                    'Wheat': {
                        'advisory': 'Sow in October for best yield.',
                        'irrigation_time': '2 hours',
                        'harvesting_time': 'June',
                        'fertilization_time': 'Before sowing',
                        'fertilizer_recommendation': 'Urea, DAP',
                        'expected_diseases': 'Rust, Blight',
                        'disease_remedies': 'Fungicide A, Fungicide B',
                    },
                },
            },
            'users': {},
            'crop_sales': []
        }
        with open(data_file, 'w') as f:
            json.dump(initial_data, f, indent=4)
    
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    return data

data = load_data()
crop_info = data['crop_info']
users = data['users']
crop_sales = data['crop_sales']

# Function to save data to the JSON file
def save_data():
    with open(data_file, 'w') as f:
        json.dump({
            'crop_info': crop_info,
            'users': users,
            'crop_sales': crop_sales
        }, f, indent=4)

# Validate password
def validate_password(password):
    # Check if password is at least 8 characters long
    if len(password) < 8:
        return False
    
    # Check if password contains at least one capital letter
    if not any(char.isupper() for char in password):
        return False
    
    # Check if password contains at least one special character
    if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/" for char in password):
        return False
    
    # Check if password contains at least one digit
    if not any(char.isdigit() for char in password):
        return False
    
    # If all checks pass, return True
    return True

# Function to signup a new user
def signup():
    global signup_username_var, signup_password_var, signup_confirm_password_var
    username = signup_username_var.get()
    password = signup_password_var.get()
    confirm_password = signup_confirm_password_var.get()
    
    # Check if username and password match with any existing users
    if username in users and users[username] == password:
        messagebox.showinfo("Success", "Login successful")
        signup_window.destroy()
        main_menu()  # Directly go to main menu if user exists and password matches
    else:
        # Validate password
        if not validate_password(password):
            messagebox.showerror("Error", "Password must contain at least 8 characters, one capital letter, one digit, and one special character.")
            return
        
        # Check if passwords match
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        
        # Create new user account
        users[username] = password
        messagebox.showinfo("Success", "Account created successfully")
        save_data()  # Save user data
        signup_window.destroy()
        main_menu()  # Directly go to main menu after signup

# Signup window
def signup_window():
    global signup_window, signup_username_var, signup_password_var, signup_confirm_password_var
    signup_window = tk.Tk()
    signup_window.title("Signup")
    signup_window.geometry("400x300")  
    signup_window.configure(bg="#f0f8ff")  
    tk.Label(signup_window, text="Username:", font=("Helvetica", 12), bg="#f0f8ff").pack(pady=5)
    signup_username_var = tk.StringVar()
    tk.Entry(signup_window, textvariable=signup_username_var).pack(pady=5)
    tk.Label(signup_window, text="Password:", font=("Helvetica", 12), bg="#f0f8ff").pack(pady=5)
    signup_password_var = tk.StringVar()
    tk.Entry(signup_window, textvariable=signup_password_var, show="*").pack(pady=5)
    tk.Label(signup_window, text="Confirm Password:", font=("Helvetica", 12), bg="#f0f8ff").pack(pady=5)
    signup_confirm_password_var = tk.StringVar()
    tk.Entry(signup_window, textvariable=signup_confirm_password_var, show="*").pack(pady=5)
    tk.Button(signup_window, text="Signup", command=signup, bg="#4CAF50", fg="white").pack(pady=10)
    signup_window.mainloop()

# Function to add crop for sale
def add_crop_for_sale():
    global crop_var, quantity_var, price_var, sale_window
    sale_window = tk.Toplevel(root)
    sale_window.title("Add Crop for Sale")
    sale_window.geometry("400x300")
    sale_window.configure(bg="#e6f7ff")
    tk.Label(sale_window, text="Select Crop:", bg="#e6f7ff").pack(pady=5)
    crop_var = tk.StringVar()
    crop_menu = ttk.Combobox(sale_window, textvariable=crop_var)
    crop_menu['values'] = list(crop_info['MarketPrice']['Bageshwar'].keys())  # Example for Bageshwar
    crop_menu.pack(pady=5)
    tk.Label(sale_window, text="Quantity:", bg="#e6f7ff").pack(pady=5)
    quantity_var = tk.StringVar()
    tk.Entry(sale_window, textvariable=quantity_var).pack(pady=5)
    tk.Label(sale_window, text="Price:", bg="#e6f7ff").pack(pady=5)
    price_var = tk.StringVar()
    tk.Entry(sale_window, textvariable=price_var).pack(pady=5)
    tk.Button(sale_window, text="Add Crop", command=process_sale, bg="#4CAF50", fg="white").pack(pady=10)

def process_sale():
    selected_crop = crop_var.get()
    quantity = quantity_var.get()
    price = price_var.get()
    username = signup_username_var.get()  # Accessing the global variable
    
    if not quantity.isdigit() or int(quantity) <= 0:
        messagebox.showerror("Error", "Please enter a valid quantity.")
        return
    
    try:
        price = float(price)
        if price <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid price.")
        return
    
    crop_sales.append({
        'user': username,
        'crop': selected_crop,
        'quantity': quantity,
        'price': price
    })
    
    save_data()  # Save crop sales data
    messagebox.showinfo("Success", f"Successfully added {quantity}kg of {selected_crop} for sale at ₹{price}.")
    sale_window.destroy()
def view_selling_crops():
    sold_crops_window = tk.Toplevel(root)
    sold_crops_window.title("Selling Crops")
    sold_crops_window.geometry("600x400")
    sold_crops_window.configure(bg="#e6f7ff")
    tk.Label(sold_crops_window, text="List of Selling Crops", font=("Helvetica", 16), bg="#e6f7ff").pack(pady=10)
    
    if not crop_sales:
        tk.Label(sold_crops_window, text="No crops sold yet.", bg="#e6f7ff").pack(pady=5)
        return
    
    for sale in crop_sales:
        tk.Label(sold_crops_window, text=f"User:  {sale['user']}, Crop: {sale['crop']}, Quantity: {sale['quantity']}kg, Price: ₹{sale['price']}", bg="#e6f7ff").pack(pady=5)

# Function to generate PDF with crop details
def generate_pdf_with_crop_details(username, district, crop):
    price = crop_info['MarketPrice'].get(district, {}).get(crop)
    advisory_info = crop_info['CropAdvisory'].get(crop)
    
    if price is None or advisory_info is None:
        messagebox.showerror("Error", "No data available for the selected district and crop.")
        return
    
    # Create PDF
    file_name = f"{username}_{district}_{crop}.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    c.drawString(100, 750, "Here are the details and recommendations for the crop you chose in your district")
    c.drawString(100, 720, f"User: {username}")
    c.drawString(100, 700, f"District: {district}")
    c.drawString(100, 680, f"Crop: {crop}")
    c.drawString(100, 660, f"Market Price: ₹{price}")
    c.drawString(100, 630, f"Advisory: {advisory_info['advisory']}")
    c.drawString(100, 610, f"Irrigation Time: {advisory_info['irrigation_time']}")
    c.drawString(100, 590, f"Harvesting Time: {advisory_info['harvesting_time']}")
    c.drawString(100, 570, f"Fertilization Time: {advisory_info['fertilization_time']}")
    c.drawString(100, 550, f"Fertilizer Recommendation: {advisory_info['fertilizer_recommendation']}")
    c.drawString(100, 530, f"Expected Diseases: {advisory_info['expected_diseases']}")
    c.drawString(100, 510, f"Disease Remedies: {advisory_info['disease_remedies']}")
    c.drawString(100, 470, "Thank you for trusting us")
    c.drawString(100, 450, "Hoping the best for your good harvest")
    c.save()
    pdf_path = os.path.abspath(file_name)
    messagebox.showinfo("Success", f"PDF generated successfully: {pdf_path}")
    webbrowser.open(pdf_path)  # Open the PDF in the default web browser

# Function to open the PDF generation window
def open_pdf_generation_window():
    pdf_window = tk.Toplevel(root)
    pdf_window.title("Generate PDF with Crop Details")
    pdf_window.geometry("400x300")
    pdf_window.configure(bg="#e6f7ff")
    tk.Label(pdf_window, text="Select Crop and District", font=("Helvetica", 14), bg="#e6f7ff").pack(pady=10)
    tk.Label(pdf_window, text="Select District:", bg="#e6f7ff").pack(pady=5)
    district_var = tk.StringVar()
    district_menu = ttk.Combobox(pdf_window, textvariable=district_var)
    district_menu['values'] = districts
    district_menu.pack(pady=5)
    tk.Label(pdf_window, text="Select Crop:", bg="#e6f7ff").pack(pady=5)
    crop_var = tk.StringVar()
    crop_menu = ttk.Combobox(pdf_window, textvariable=crop_var)
    crop_menu.pack(pady=5)

    def update_crops(event):
        selected_district = district_var.get()
        crop_menu['values'] = list(crop_info['MarketPrice'].get(selected_district, {}).keys())
        crop_menu.set('')

    district_menu.bind("<<ComboboxSelected>>", update_crops)

    def generate_pdf():
        selected_district = district_var.get()
        selected_crop = crop_var.get()
        generate_pdf_with_crop_details(signup_username_var.get(), selected_district, selected_crop)

    tk.Button(pdf_window, text="Generate PDF", command=generate_pdf, bg="#4CAF50", fg="white").pack(pady=10)

# Function to calculate profit
def calculate_profit():
    def calculate():
        try:
            investment_seeds = float(investment_seeds_var.get())
            investment_fertilizers = float(investment_fertilizers_var.get())
            investment_soil = float(investment_soil_var.get())
            net_yield = float(net_yield_var.get())
            profit = net_yield - (investment_seeds + investment_fertilizers + investment_soil)
            messagebox.showinfo("Profit Calculation", f"Your profit is: ₹{profit:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")

    profit_window = tk.Toplevel(root)
    profit_window.title("Profit Calculation")
    profit_window.geometry("600x500")
    profit_window.configure(bg="#e6f7ff")
    tk.Label(profit_window, text="Profit Calculation", font=("Helvetica", 16), bg="#e6f7ff").pack(pady=10)
    tk.Label(profit_window, text="Investment in Seeds (₹):", bg="#e6f7ff").pack(pady=5)
    investment_seeds_var = tk.StringVar()
    tk.Entry(profit_window, textvariable=investment_seeds_var).pack(pady=5)
    tk.Label(profit_window, text="Investment in Fertilizers (₹):", bg="#e6f7ff").pack(pady=5)
    investment_fertilizers_var = tk.StringVar()
    tk.Entry(profit_window, textvariable=investment_fertilizers_var).pack(pady=5)
    tk.Label(profit_window, text="Investment in Soil Preparation (₹):", bg="#e6f7ff").pack(pady=5)
    investment_soil_var = tk.StringVar()
    tk.Entry(profit_window, textvariable=investment_soil_var).pack(pady=5)
    tk.Label(profit_window, text="Net Yield (₹):", bg="#e6f7ff").pack(pady=5)
    net_yield_var = tk.StringVar()
    tk.Entry(profit_window, textvariable=net_yield_var).pack(pady=5)
    tk.Button(profit_window, text="Calculate Profit", command=calculate, bg="#4CAF50", fg="white").pack(pady=10)

# Main menu
def main_menu():
    global root
    root = tk.Tk()
    root.title("Uttarakhand E-Kisan Seva")
    root.geometry("800x500")  
    root .configure(bg="#f0f8ff")
    menu_frame = tk.Frame(root, borderwidth=2, relief="groove", bg="#ffffff")  
    menu_frame.pack(pady=20, padx=10)
    tk.Label(menu_frame, text="Main Menu", font=("Helvetica", 16), bg="#ffffff").pack(pady=10)

    def show_crop_management():
        crop_management_window = tk.Toplevel(root)
        crop_management_window.title("Crop Management")
        crop_management_window.geometry("400x300")  
        crop_management_window.configure(bg="#e6f7ff")
        tk.Label(crop_management_window, text="Crop Management", font=("Helvetica", 14), bg="#e6f7ff").pack(pady=10)
        crop_management_frame = tk.Frame(crop_management_window, bg="#ffffff")  
        crop_management_frame.pack(pady=10)
        tk.Label(crop_management_frame, text="Select Crop:", font=("Helvetica", 12), bg="#ffffff").pack(side=tk.LEFT, padx=5)
        crop_var = tk.StringVar()
        crop_menu = ttk.Combobox(crop_management_frame, textvariable=crop_var)
        crop_menu['values'] = list(crop_info['CropAdvisory'].keys())
        crop_menu.pack(side=tk.LEFT, padx=5)

        def show_advisory():
            selected_crop = crop_var.get()
            advisory_info = crop_info['CropAdvisory'].get(selected_crop)
            if advisory_info:
                advisory_window = tk.Toplevel(crop_management_window)
                advisory_window.title("Crop Advisory Details")
                advisory_window.geometry("400x400")
                advisory_window.configure(bg="#e6f7ff")
                tk.Label(advisory_window, text=f"Advisory for {selected_crop}", font=("Helvetica", 14), bg="#e6f7ff").pack(pady=10)
                tk.Label(advisory_window, text=f"Advisory: {advisory_info['advisory']}", wraplength=400, bg="#e6f7ff").pack(pady=5)
                tk.Label(advisory_window, text=f"Irrigation Time: {advisory_info['irrigation_time']}", bg="#e6f7ff").pack(pady=5)
                tk.Label(advisory_window, text=f"Harvesting Time: {advisory_info['harvesting_time']}", bg="#e6f7ff").pack(pady=5)
                tk.Label(advisory_window, text=f"Fertilization Time: {advisory_info['fertilization_time']}", bg="#e6f7ff").pack(pady=5)
                tk.Label(advisory_window, text=f"Fertilizer Recommendation: {advisory_info['fertilizer_recommendation']}", bg="#e6f7ff").pack(pady=5)
                tk.Label(advisory_window, text=f"Expected Diseases: {advisory_info['expected_diseases']}", bg="#e6f7ff").pack(pady=5)
                tk.Label(advisory_window, text=f"Disease Remedies: {advisory_info['disease_remedies']}", bg="#e6f7ff").pack(pady=5)
            else:
                messagebox.showinfo("Info", "No advisory details available for this crop.")

        tk.Button(crop_management_frame, text="Show Advisory", command=show_advisory, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)

    def show_weather_info():
        weather_info_window = tk.Toplevel(root)
        weather_info_window.title("Weather Information")
        weather_info_window.geometry("400x300")  
        weather_info_window.configure(bg="#e6f7ff")
        tk.Label(weather_info_window, text="Weather Information", font=("Helvetica", 14), bg="#e6f7ff").pack(pady=10)
        weather_info_frame = tk.Frame(weather_info_window, bg="#ffffff")  
        weather_info_frame.pack(pady=10)
        tk.Label(weather_info_window, text="Select District:", font=("Helvetica", 12), bg="#e6f7ff").pack(side=tk.LEFT, padx=5)
        district_combobox = ttk.Combobox(weather_info_window, values=districts)
        district_combobox.pack(side=tk.LEFT, padx=5)
        district_combobox.set("Select a district")

        def get_weather_info():
            district = district_combobox.get()
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={district},IN&appid={API_KEY}&units=metric"
                response = requests.get(url)
                data = response.json()

                if response.status_code == 200:
                    temp = data['main']['temp']
                    condition = data['weather'][0]['description']
                    humidity = data['main']['humidity']
                    weather_info = f"Weather in {district}:\nTemperature: {temp}°C\nCondition: {condition.capitalize()}\nHumidity: {humidity}%"
                    messagebox.showinfo("Weather Info", weather_info)
                else:
                    messagebox.showwarning("Weather Info", "District not found or invalid API key.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        tk.Button(weather_info_frame, text="Get Weather Info", command=get_weather_info, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)

    def show_market_prices():
        market_prices_window = tk.Toplevel(root)
        market_prices_window.title("Market Prices")
        market_prices_window.geometry("500x600")  
        market_prices_window.configure(bg="#e6f7ff")  
        tk.Label(market_prices_window, text="Market Prices", font=("Helvetica", 14), bg="#e6f7ff").pack(pady=10)
        market_prices_frame = tk.Frame(market_prices_window, bg="#ffffff")  
        market_prices_frame.pack(pady=10)
        tk.Label(market_prices_frame, text="Select District:", font=("Helvetica", 12), bg="#ffffff").pack(side=tk.LEFT, padx=5)
        district_var = tk.StringVar()
        district_menu = ttk.Combobox(market_prices_frame, textvariable=district_var)
        district_menu['values'] = list(crop_info['MarketPrice'].keys())
        district_menu.pack(side=tk.LEFT, padx=5)

        def show_prices():
            selected_district = district_var.get()
            prices_window = tk.Toplevel(market_prices_window)
            prices_window.title("Prices")
            prices_window.geometry("400x300") 
            prices_window.configure(bg="#e6f7ff") 
            tk.Label(prices_window, text="Prices", font=("Helvetica", 14), bg="#e6f7ff").pack(pady=10)
            for crop, price in crop_info['MarketPrice'].get(selected_district, {}).items():
                tk.Label(prices_window, text=f"{crop}: ₹{price}", wraplength=400, bg="#e6f7ff").pack(pady=10)

        tk.Button(market_prices_frame, text="Show Prices", command=show_prices, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)

    def show_profit_calculation_window():
        calculate_profit()

    def show_help():
        help_window = tk.Toplevel(root)
        help_window.title("Help")
        help_window.geometry("400x300") 
        help_window.configure(bg="#e6f7ff")  
        tk.Label(help_window, text="Help - How to Use the Application", font=("Helvetica", 14), bg="#e6f7ff").pack(pady=10)
        help_text = ("1. Signup: Create an account by entering a username and password.\n"
                      "2. Crop Management: Select a crop to view advisories and fertilizer recommendations.\n"
                      "3. Weather Info: Select a district to get the current weather information.\n"
                      "4. Market Prices: Select a district to view the current market prices for various crops.\n"
                      "5. Profit Calculation: Enter your investments and net yield to calculate profit.\n"
                      "6. Help: Access this help section for guidance on using the application.")
        tk.Label(help_window, text=help_text, wraplength=380, bg="#e6f7ff").pack(pady=10)

    def exit_application():
        root.quit()

    crop_button = tk.Button(menu_frame, text="Crop Management", command=show_crop_management, font=("Helvetica", 12), bg="#4CAF50", fg="white")
    crop_button.pack(pady=5, padx=10)

    weather_button = tk.Button(menu_frame, text="Weather Info", command=show_weather_info, font=("Helvetica", 12), bg="#4CAF50", fg="white")
    weather_button.pack(pady=5, padx=10)

    market_button = tk.Button(menu_frame, text="Market Prices", command=show_market_prices, font=("Helvetica", 12), bg="#4CAF50", fg="white")
    market_button.pack(pady=5, padx=10)

    profit_button = tk.Button(menu_frame, text="Profit Calculation", command=show_profit_calculation_window, font=("Helvetica", 12), bg="#4CAF50", fg="white")
    profit_button.pack(pady=5, padx=10)

    pdf_button = tk.Button(menu_frame, text="Generate PDF with Crop Details", command=open_pdf_generation_window, font=("Helvetica", 12), bg="#4CAF50", fg="white")
    pdf_button.pack(pady=5, padx=10)

    tk.Button(menu_frame, text="Add Crop for Sale", command=add_crop_for_sale, font=("Helvetica", 12), bg="#4CAF50", fg="white").pack(pady=5, padx=10)

    tk.Button(menu_frame, text="View Selling Crops", command=view_selling_crops, font=("Helvetica", 12), bg="#4CAF50", fg="white").pack(pady=5, padx=10)

    help_button = tk.Button(menu_frame, text="Help", command=show_help, font=("Helvetica", 12), bg="#4CAF50", fg="white")
    help_button.pack(pady=5, padx=10)

    exit_button = tk.Button(menu_frame, text="Exit", command=exit_application, font=("Helvetica", 12), bg="#4CAF50", fg="white")
    exit_button.pack(pady=5, padx=10)
    root.mainloop()
signup_window()
# Start the application
if __name__ == "__main__":
    signup_window()
    main_menu()
