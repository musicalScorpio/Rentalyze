# 🏡 Rentalyze

**Rentalyze** is an AI-assisted real estate investment analysis tool that helps property investors make informed decisions by evaluating rental potential, estimating returns, and identifying key investment metrics based on address-level data.

---

## 🚀 Features

- 🔍 **Property Address Lookup**  
  Enter an address to retrieve surrounding rental rates, property tax estimates, and insurance costs.

- 📊 **ROI Calculator**  
  Instantly calculate Cash-on-Cash return, cap rate, and mortgage breakdown based on user inputs.

- 🌐 **County-Level Market Data**  
  Uses public and third-party APIs to gather fair market rents, tax rates, and regional benchmarks.

- 📍 **Radius-Based Rental Comparison**  
  Analyze nearby rental listings within a customizable radius to evaluate market competitiveness.

- 💰 **Custom Investment Strategy Modeling**  
  Allows inputs for offer price, down payment, interest rate, and more — tailored to your investment strategy.

---

## 🧠 Tech Stack

- **Frontend**: Streamlit  
- **Backend**: Flask APIs  
- **Data Sources**: RentData.org, County Tax APIs, FRED (for Treasury yields)  
- **Language**: Python  
- **Visualization**: Pydeck, Plotly, Folium  

---

## 🛠️ Setup Instructions (Step-by-Step)
```bash
**📥 Step 1: Clone the Repository**


git clone https://github.com/musicalScorpio/Rentalyze.git
cd Rentalyze

**🐍 Step 2: Create a Virtual Environment**
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # For Windows use: venv\Scripts\activate

**📦 Step 3: Install Dependencies**
bash
Copy
Edit
pip install -r requirements.txt

**🔐 Step 4: Create a .env File**
In the apis/ directory, create a .env file with your API keys:

env
Copy
Edit
FRED_API_KEY=your_fred_api_key_here

**🧠 Step 5: Start the Backend API**
bash
Copy
Edit
cd apis
python app.py  # or flask run

**💻 Step 6: Launch the Streamlit Frontend**
bash
Copy
Edit
cd ..
streamlit run ui/main.py
📌 Roadmap

 Integrate MLS or Zillow API for richer listing data
 Add map-based property selector
  Enable export of investment analysis to PDF
 User login and history tracking
  Monetization layer (premium features)
🙌 Contributing

Have a feature idea or want to fix a bug? Fork the repo and submit a PR. All contributors welcome!

**🧾 License**

MIT License. See LICENSE file for details.

**📫 Contact**

Created by Sam Mukherjee
For inquiries or collaborations, email: sam.mukherjee@gmail.com
