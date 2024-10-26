import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class DataLoader:
    """Class to load data from a CSV file."""

    def __init__(self, file_path):
        """Initialize with the path to the CSV file."""
        self.file_path = file_path
        self.data = None
        self.load_data()

    def load_data(self):
        """Load data from the CSV file into a DataFrame."""
        try:
            # Load the CSV file, assuming headers
            self.data = pd.read_csv(self.file_path)

            # Drop rows where all columns are NaN (if any)
            self.data.dropna(how='all', inplace=True)

            # Convert data to numeric, coercing errors to NaN
            self.data = self.data.apply(pd.to_numeric, errors='coerce')

            print("Data loaded successfully.")
            # print(self.data.head())  # Print first few rows of the loaded data for verification
        except FileNotFoundError:
            print(f"Error: The file {self.file_path} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_data(self):
        """Return the loaded data."""
        return self.data.to_numpy()



class DataPlotter:
    """Class to plot data using Matplotlib."""

    def __init__(self, data):
        """Initialize with the data to be plotted."""
        self.data = data

    def plot(self, x_index, y_index, title='Signal Plot', x_label='Time', y_label='Amplitude'):
        """Plot the signal using specified column indices."""
        if self.data is not None:
            plt.figure(figsize=(12, 6))  # Wider figure

            # Create time axis (x_index can be either time or sample index)
            x_data = self.data.iloc[:, x_index]
            y_data = self.data.iloc[:, y_index]

            # Plot the data as a signal
            plt.plot(x_data, y_data, color='blue', linewidth=1)

            # Set the title and labels
            plt.title(title)
            plt.xlabel(x_label)
            plt.ylabel(y_label)

            # Set x and y limits to accommodate the signal range
            plt.xlim(x_data.min(), x_data.max())  # X-axis based on time or samples
            plt.ylim(y_data.min() - 1, y_data.max() + 1)  # Adjust y-limits as needed

            plt.grid(True)
            plt.show()
        else:
            print("Error: No data to plot.")



def main():
    """Main function to run the data loading and plotting."""
    # Replace 'your_file.csv' with the path to your CSV file
    csv_file_path = "D:\Faculty\SBE 24-25\DSP\Signal-Reconstructor\signals_data\ECG_Normal.csv"

    # Create a DataLoader instance and load data
    data_loader = DataLoader(csv_file_path)
    data_loader.load_data()

    # Get the loaded data
    data = data_loader.get_data()

    # Create a DataPlotter instance and plot the data
    if data is not None:
        data_plotter = DataPlotter(data)

        # Assuming the first column is Time and the second column is Value
        num_columns = data.shape[1]

        if num_columns >= 2:
            data_plotter.plot(x_index=0, y_index=1, title='Signal Plot', x_label='Time (s)', y_label='Amplitude')
        else:
            print("Error: The data does not have enough columns for plotting.")


if __name__ == '__main__':
    main()

