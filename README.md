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

## 🛠️ Setup Instructions

1. **Clone the Repo**
   ```bash
   git clone https://github.com/musicalScorpio/Rentalyze.git
   cd Rentalyze
Set Up Virtual Environment
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Configure Environment Variables
Create a .env file with keys such as:
ini
Copy
Edit
FRED_API_KEY=your_key_here
Run Backend APIs
bash
Copy
Edit
cd apis
python app.py  # or flask run
Launch the Streamlit App
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

🧾 License

MIT License. See LICENSE file for details.

