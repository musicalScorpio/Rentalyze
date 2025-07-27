"""

author : Sam Mukherjee

"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

def getChart (sales_prices, contract_amount):
    mean = np.mean(sales_prices)
    std_dev = np.std(sales_prices)

    # Generate bell curve data
    x = np.linspace(mean - 4 * std_dev, mean + 4 * std_dev, 1000)
    y = stats.norm.pdf(x, mean, std_dev)

    # Plot with matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y, label='Sales Price Distribution')
    ax.axvline(contract_amount, color='red', linestyle='--', label='contract_amount (Target)')
    ax.set_title('Bell Curve of Sales Prices')
    ax.set_xlabel('Sales Price ($)')
    ax.set_ylabel('Probability Density')
    ax.legend()
    ax.grid(True)
    # Display in Streamlit
    #st.pyplot(fig)

    return fig

"""
# Use the previously extracted sales prices
sales_prices = [220000.0, 113800.0, 245000.0, 240000.0, 232000.0, 269000.0, 155000.0]

# Calculate mean and standard deviation
mean = np.mean(sales_prices)
std_dev = np.std(sales_prices)

# Generate bell curve data
x = np.linspace(mean - 4 * std_dev, mean + 4 * std_dev, 1000)
y = stats.norm.pdf(x, mean, std_dev)

# Plot the bell curve
plt.figure(figsize=(10, 6))
plt.plot(x, y, label="Sales Price Distribution")
plt.axvline(225000, color='red', linestyle='--', label='225000 (Target)')
plt.title('Bell Curve of Sales Prices')
plt.xlabel('Sales Price ($)')
plt.ylabel('Probability Density')
plt.legend()
plt.grid(True)
plt.show()

"""