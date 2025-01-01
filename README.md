
<h1 align="center">
    <img alt="project" title="#About" src="Readme/main.gif" />
</h1>

<h1 align="center">ReSigni</h1>
<h3 align="center">Real time signal reconstructor</h3>

<h4 align="center"> 
	 Status: Finished
</h4>

<p align="center">
 <a href="#about">About</a> •
 <a href="#features">Features</a> •
 <a href="#how-it-works">How it works</a> • 
 <a href="#tech-stack">Tech Stack</a> •  
 <a href="#developers">Developers</a>
</p>

# About
**Resigni** is a Python-based desktop application built with PyQt5 that reconstructs a given signal using the Nyquist Principle. The application provides intuitive visualization of the reconstructed signal, its frequency components, and an error graph to evaluate reconstruction accuracy.

---

## Features

- **Signal Sampling & Signal Mixer**: Mix multiple sinusoidal signals with different frequencies and magnitude and recover the original signal.
![task2 2](https://github.com/user-attachments/assets/decfe128-3838-4026-9b43-0697383671d5)
  
- **Interpolation Methods**: Reconstruct the original signal using different interpolation methods.
  ![task2 3](https://github.com/user-attachments/assets/a7757437-87b6-47d6-b596-4d116c321ff9)
  
- **Adding Noise**: adding noise to the original signal with differnet SNR values.
![task2 4](https://github.com/user-attachments/assets/8a31f909-dd5f-499a-8976-c8f071c4407a)


## Tech Stack

The following tools were used in the construction of the project:

- **[Python](https://www.python.org/)**
- **[PyQt5](https://riverbankcomputing.com/software/pyqt/intro)**
- **[PyQtGraph](https://www.pyqtgraph.org/)**
- **[NumPy](https://numpy.org/)**

---


## How it Works

The application is built with **Python** and **PyQt5**. It allows the user to add different signals using the composer and change the value of the sampling frequency to see real time sampling.


### Pre-requisites

Before running the application, make sure you have **Python** installed on your system. You will also need **pip** for installing dependencies.

---

## How to Run the Project Locally

To run the project locally, follow these steps:

### Steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/Signal-Reconstructor.git]
   ```

2. **Navigate to the project folder:**
   ```bash
   Signal-Reconstructor
   ```


3. **Install the required dependencies:**
   ```bash
   pyqt5
   pyqtgraph
   numpy
   ```

5. **Run the application:**
   ```bash
   python main.py
   ```

This will start the **ReSigni** application locally.

---

## Developers

| [**Talal Emara**](https://github.com/TalalEmara) | [**Meram Mahmoud**](https://github.com/Meram-Mahmoud) | [**Maya Mohammed**](https://github.com/Mayamohamed207) | [**Nouran Hani**](https://github.com/Nouran-Hani) | [**Nariman Ahmed**](https://github.com/nariman-ahmed) |
|:------------------------------------------:|:------------------------------------------:|:------------------------------------------:|:------------------------------------------:|:------------------------------------------:|


---


## Learn More

To learn more about PyQt5 and PyQtGraph, check out their official documentation:

- [PyQt5 Documentation](https://riverbankcomputing.com/software/pyqt/intro)
- [PyQtGraph Documentation](https://www.pyqtgraph.org/)
