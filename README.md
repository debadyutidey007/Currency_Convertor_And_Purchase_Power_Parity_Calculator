# Currency Converter & Purchasing Power Parity Calculator

<div align="center">

[![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)](https://github.com/debadyutidey007/Currency_Convertor_And_Purchase_Power_Parity_Calculator)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Repo Size](https://img.shields.io/github/repo-size/debadyutidey007/Currency_Convertor_And_Purchase_Power_Parity_Calculator)](https://github.com/debadyutidey007/Currency_Convertor_And_Purchase_Power_Parity_Calculator)

**A modern, intuitive desktop utility for real-time currency conversion and insightful Purchasing Power Parity (PPP) analysis, designed for economic understanding and practical application.**

</div>

<p align="center">
  <img src="https://github.com/user-attachments/assets/71a6e70b-d2d7-4660-848e-f6362f6b8c9d" alt="Application Screenshot" width="700"/>
</p>

---

## 📜 Overview

The **Currency Converter & Purchasing Power Parity Calculator** is a robust desktop application engineered to demystify global economics for everyone from casual travelers to dedicated economists. It offers a seamless, dual-function interface, allowing users to effortlessly switch between precise **real-time currency conversions** and nuanced **Purchasing Power Parity (PPP) analysis**.

This application goes beyond typical market exchange rates, providing a deeper understanding of the true value of money across various international economies. Whether you're planning international travel, conducting economic research, or simply curious about global financial comparisons, this tool offers the insights you need. Its **standalone executable** nature means zero installation hassles, making it exceptionally portable and user-friendly.

---

## ✨ Key Features

This application is packed with features designed to provide both utility and a smooth user experience:

* **Real-Time Currency Conversion**: Access up-to-the-minute exchange rates for a comprehensive selection of global currencies. This feature relies on a robust external API to ensure data accuracy and reliability for all your conversion needs.
* **Purchasing Power Parity (PPP) Analysis**: Gain a deeper economic perspective by calculating the equivalent amount of money needed in a target country to afford the same standard of living or basket of goods as in a base country. This helps in understanding the true purchasing power, independent of volatile market exchange rates.
* **Intuitive Dual-Mode User Interface**: Navigate effortlessly between the "Currency Converter" and "PPP Calculator" functionalities using a clean, tabbed interface. This design ensures a streamlined workflow and an uncluttered user experience.
* **Modern & Responsive Design**: Crafted with `customtkinter`, the application boasts a sleek, contemporary aesthetic. Its responsive design ensures optimal performance and visual appeal across various desktop environments.
* **Zero Installation & Portable**: Distributed as a single executable file (`main.exe`), the application requires no complex installation processes, Python environment setups, or dependency management. Simply download and run, making it ideal for on-the-go use.

---

## 🛠️ Technologies Used

This project leverages a powerful combination of technologies to deliver a high-performance and visually appealing desktop application:

| Technology         | Description                                                                                                                                                                                                                                           |
| :----------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Python** | The foundational programming language, chosen for its readability, extensive libraries, and efficiency in handling application logic, data processing, and API integrations.                                                                          |
| **CustomTkinter** | A modern, open-source Python UI library that builds upon Tkinter to provide a significantly enhanced visual experience with contemporary widgets and themes. It enables the creation of elegant and responsive graphical user interfaces.            |
| **API Integration** | The application seamlessly integrates with an **external financial API** (details regarding the specific API used are maintained internally for security and rate limiting purposes) to fetch accurate, real-time currency exchange rates and relevant economic data. |

---

## 🚀 How to Use

Getting started with the Currency Converter & PPP Calculator is straightforward. Choose the method that best suits your needs:

### Method 1: Direct Executable (Recommended for All Users)

This is the simplest and most convenient way to run the application, requiring no technical setup.

1.  Visit the **[Releases](https://github.com/debadyutidey007/Currency_Convertor_And_Purchase_Power_Parity_Calculator/releases)** section on this GitHub repository.
2.  Locate the latest release and download the `main.exe` file.
3.  Save the executable to any preferred location on your computer (e.g., your Desktop or a dedicated applications folder).
4.  **Double-click `main.exe`** to launch the application immediately.

### Method 2: From Source Code (For Developers & Contributors)

If you're a developer, prefer to run the application from its source, or wish to contribute, follow these steps:

1.  **Prerequisites**: Ensure you have **[Python 3.x](https://www.python.org/downloads/)** installed on your system. Python 3.8 or newer is recommended for optimal compatibility.
2.  **Clone the Repository**: Open your terminal or command prompt and execute the following commands to clone the project:
    ```bash
    git clone [https://github.com/debadyutidey007/Currency_Convertor_And_Purchase_Power_Parity_Calculator.git](https://github.com/debadyutidey007/Currency_Convertor_And_Purchase_Power_Parity_Calculator.git)
    cd Currency_Convertor_And_Purchase_Power_Parity_Calculator
    ```
3.  **Set Up a Virtual Environment** (Highly Recommended): Creating a virtual environment isolates project dependencies, preventing conflicts with other Python projects.
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
4.  **Install Dependencies**: With your virtual environment activated, install the required libraries:
    ```bash
    pip install customtkinter
    # If the application uses other specific libraries for API calls or data,
    # you might need to add them here, e.g., pip install requests
    ```
5.  **Run the Application**: Finally, execute the main script:
    ```bash
    python main.py
    ```

---

## 📈 How PPP is Calculated

The Purchasing Power Parity (PPP) calculation is a fundamental economic concept that allows for a more accurate comparison of living standards and purchasing power between different countries, bypassing misleading market exchange rate fluctuations. The application utilizes the following core formula for its PPP analysis:

<p align="center">

$$
\displaystyle
\mathrm{Equivalent\ Cost}
= \mathrm{Amount}_{\mathrm{base}}
\times
\left(
  \frac{\mathrm{PPP\ Index}_{\mathrm{target}}}
       {\mathrm{PPP\ Index}_{\mathrm{base}}}
\right)
$$

</p>

**Explanation:**
* $\textbf{Amount}_{\textbf{base}}$: The original monetary amount in the starting (base) currency.
* $\textbf{PPP Index}_{\textbf{target}}$: The Purchasing Power Parity index for the target country. This index reflects the general price level of a "basket of goods" in that country relative to a reference (often the US dollar or a global average).
* $\textbf{PPP Index}_{\textbf{base}}$: The Purchasing Power Parity index for the base country.

By applying this formula, the calculator estimates the amount in the target currency that would be required to purchase the same "basket of goods and services" as the initial amount in the base currency, thereby offering a more realistic measure of comparative value.

---

## 🤝 Contributing

Contributions are genuinely what fuel the open-source community, transforming ideas into remarkable tools. Your input, whether through feature suggestions, bug reports, or code contributions, is highly valued and greatly appreciated.

If you have an idea for an enhancement or spot an issue, please consider contributing:

1.  **Fork the Project**: Click the "Fork" button at the top right of this repository.
2.  **Create your Feature Branch**:
    ```bash
    git checkout -b feature/AmazingFeature
    ```
    (e.g., `feature/add-new-currency-api`)
3.  **Commit your Changes**:
    ```bash
    git commit -m 'feat: Add an Amazing Feature'
    ```
    (Use descriptive commit messages!)
4.  **Push to the Branch**:
    ```bash
    git push origin feature/AmazingFeature
    ```
5.  **Open a Pull Request**: Navigate to your forked repository on GitHub and open a Pull Request to the `main` branch of this original repository. Please ensure your PR includes a clear description of the changes.

Alternatively, you can simply open an issue with the tag "enhancement" or "bug" to suggest improvements or report problems.

---

## 📄 License

This project is distributed under the **MIT License**. This permissive open-source license allows for wide usage, modification, and distribution. For complete details, please refer to the `LICENSE` file within the repository.

---

## 🙏 Acknowledgments

We extend our gratitude to the following resources and communities that made this project possible:

* **PPP Data Sources**: Data for Purchasing Power Parity indices are meticulously sourced from reputable international economic databases (e.g., World Bank, OECD), ensuring accuracy and consistency.
* **Exchange Rate API Provider**: Real-time exchange rates are provided by a reliable third-party API. Specific provider details are withheld for security and service stability.
* **CustomTkinter Community**: Inspiration, guidance, and invaluable resources from the `customtkinter` library documentation and its vibrant open-source community.

---