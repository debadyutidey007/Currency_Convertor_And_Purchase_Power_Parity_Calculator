# Currency Converter & Purchasing Power Parity Calculator

<div align="center">

[![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)](https://github.com/debadyutidey007/Currency_Convertor_And_Purchase_Power_Parity_Calculator)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Repo Size](https://img.shields.io/github/repo-size/debadyutidey007/Currency_Convertor_And_Purchase_Power_Parity_Calculator)](https://github.com/debadyutidey007/Currency_Convertor_And_Purchase_Power_Parity_Calculator)

**A modern desktop utility for real-time currency conversion and insightful Purchasing Power Parity (PPP) analysis.**

</div>

<p align="center">
  <img src="https://github.com/user-attachments/assets/71a6e70b-d2d7-4660-848e-f6362f6b8c9d" alt="Application Screenshot" width="700"/>
</p>

## 📜 Overview

This application provides a seamless, dual-function interface for essential economic calculations. It is designed for travelers, economists, students, and anyone interested in the true value of money across different countries. Go beyond simple market exchange rates and understand the real-world purchasing power of your currency.

The entire application is a standalone executable, requiring no installation, making it incredibly portable and easy to use.

## ✨ Key Features

-   **Real-Time Currency Conversion**: Get up-to-the-minute exchange rates for a vast selection of global currencies.
-   **Purchasing Power Parity (PPP) Analysis**: Calculate the equivalent amount needed in another country to maintain the same standard of living.
-   **Intuitive Dual-Mode UI**: A clean, tabbed interface allows you to switch effortlessly between the Converter and the PPP Calculator.
-   **Modern & Responsive Design**: Built with `customtkinter` for a sleek, contemporary look and feel that works flawlessly on your desktop.
-   **Zero Installation**: Runs as a single executable file (`main.exe`) with no need for Python or dependency installations.

## 🛠️ Technologies Used

This project is built with a focus on simplicity and modern aesthetics using the following technologies:

| Technology | Description |
| :--- | :--- |
| **Python** | The core programming language for the application logic. |
| **CustomTkinter** | A modern Python UI library based on Tkinter for creating visually appealing graphical interfaces. |
| **API Integration** | Connects to an external API (not specified) to fetch live currency exchange data. |

## 🚀 How to Use

There are two methods to run this application. The first is recommended for most users.

### Method 1: Direct Executable (Recommended)

This is the simplest way to get started.

1.  Navigate to the **[Releases](https://github.com/debadyutidey007/Currency_Convertor_And_Purchase_Power_Parity_Calculator/releases)** section of this repository.
2.  Download the `main.exe` file from the latest release.
3.  Save the file to a convenient location on your computer.
4.  **Double-click `main.exe`** to launch the application instantly.

### Method 2: From Source Code (For Developers)

If you wish to run the application from the source code or contribute to its development:

1.  **Prerequisites**: Ensure you have [Python 3](https://www.python.org/downloads/) installed on your system.
2.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/debadyutidey007/Currency_Convertor_And_Purchase_Power_Parity_Calculator.git](https://github.com/debadyutidey007/Currency_Convertor_And_Purchase_Power_Parity_Calculator.git)
    cd Currency_Convertor_And_Purchase_Power_Parity_Calculator
    ```
3.  **Set Up a Virtual Environment** (Recommended):
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate
    
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
4.  **Install Dependencies**:
    ```bash
    pip install customtkinter
    ```
5.  **Run the Application**:
    ```bash
    python main.py
    ```

## 📈 How PPP is Calculated

The Purchasing Power Parity calculation provides a more realistic comparison of economic well-being. The formula used is:

$$ \text{Equivalent Cost} = \text{Amount}_{\text{base}} \times \left( \frac{\text{PPP Index}_{\text{target}}}{\text{PPP Index}_{\text{base}}} \right) $$

This helps estimate the amount in the target currency required to buy the same "basket of goods" as the original amount in the base currency.

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  **Fork the Project**
2.  **Create your Feature Branch** (`git checkout -b feature/AmazingFeature`)
3.  **Commit your Changes** (`git commit -m 'feat: Add some AmazingFeature'`)
4.  **Push to the Branch** (`git push origin feature/AmazingFeature`)
5.  **Open a Pull Request**

## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for more information.

## 🙏 Acknowledgments

-   Data for PPP indices is sourced from reliable economic databases.
-   Exchange rates are provided by a third-party API.
-   Inspiration from the `customtkinter` library documentation and community.

---