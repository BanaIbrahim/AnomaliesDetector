# AnomaliesDetector

A command-line tool to detect anomalies in eCommerce data according to Clarity company standards.

## How to Use

To run the tool:

1.	Clone the repository to your local machine.
2.	Install pandas if it is not already installed by running:

`pip install pandas`


3.	Run the tool from the terminal:
* Navigate to the repository directory.
* Execute the following command: 

`python analysis.py -f <file_path>`

* Replace `<file_path>` with the path to the input data file.

4.	An anomaly detection log file **Anomalies_report.txt** will be saved in the same directory as the input data file.

## Output

The output of the anomaly detection analysis is a simple, self-explanatory log file providing a detailed report of anomalies, including:

1.	Detection of missing values
2.	Flagging of future dates
3.	Identification of outliers in the Quantity field
4.	Validation of the TotalAmount field to ensure it matches `Quantity * Price`

An example log file, log_example.txt, is provided in the repository for reference.

## Additional Resources

The repository also includes a Jupyter notebook **Clarity_data_quality_analysis.ipynb** that performs data quality analysis on a sample dataset following Clarity’s standards. This notebook serves as an example of how the tool works with Clarity’s data and provides additional insights into data quality checks and anomaly detection.