import pandas as pd
import datetime
import os
import argparse



class AnomalyDetector:
    """Analyze e-commerce data, detecting quality issues."""
    
    def __init__(self, data_path):
        """Inits AnomalyDetector.

        Args:
            data_path (string): path to csv e-commerce data file 
        """
        
        # Load the data
        df = pd.read_csv(data_path)
        self.df = df
        # Get the parent diectory of data
        parent_dir = os.path.dirname(data_path)
        # Open log file
        log_file = open(os.path.join(parent_dir, "Anomalies_report.txt"), "w")
        self.log_file = log_file
        
        
    def __missing_val(self,):
        """Identify and log missing values."""
        
        # check the columns that has NaNs
        col_isna_df = self.df.isna().sum()
        cols_na = col_isna_df[col_isna_df > 0].index.tolist()
        # Log the output
        self.log_file.write(f"Missing values detected in {cols_na} columns\n")
        self.log_file.write(f"Total number of missing values: {self.df[cols_na].isna().sum().sum()}\n")
        # Detailed NaNs for each column
        col_na_count_dict = dict(zip(cols_na, col_isna_df[col_isna_df > 0].tolist()))
        self.log_file.write(f"Missing values count: {col_na_count_dict}\n")
        
        # Log each record that has NaN 
        for col in cols_na:
            missing_indices = self.df[self.df[col].isna()].index.tolist()
            missing_indices = [i+1 for i in missing_indices]
            self.log_file.write(f"\nColumn '{col}' has missing values at record numbers : {missing_indices}\n")
            self.log_file.write("Record(s) with missing values:\n")
            self.log_file.write(self.df.iloc[missing_indices].to_string())
            self.log_file.write("\n")
            self.log_file.write("-"*100)
            self.log_file.write("\n")
            
            
    def __future_data(self,):
        """Flag future-dated entries in the OrderDate field."""
        
        # Parsing OrderDate to datetime type
        order_date = pd.to_datetime(self.df["OrderDate"], format="mixed")
        order_date = order_date.dt.date
        # Get today's date
        today = datetime.date.today()
        # Extract the future dates in the OrderDate
        future_dates = order_date[order_date > today]
        future_dates_indices = future_dates.index.tolist()
        # Log the output
        self.log_file.write("\n")
        self.log_file.write("*"*100)
        self.log_file.write("\n")
        self.log_file.write(f"\nNumber of records with future dates: {len(future_dates_indices)}\n")
        self.log_file.write(f"Records with future dates indices: {future_dates_indices}\n")
        self.log_file.write(f"Records with future dates:\n")
        self.log_file.write(self.df.iloc[future_dates_indices].to_string())
        
    
    def __quantity_outliers(self,):
        """Detect records with unusual Quantity values."""
        
        # Detect the unusal outliers in Quantity column
        unusual_high_quantity = (self.df["Quantity"] >= 100).sum()
        unusual_low_quantity = (self.df["Quantity"] <= 0).sum()
        # Log the output
        self.log_file.write("\n")
        self.log_file.write("*"*100)
        self.log_file.write("\n")
        self.log_file.write(f"\nNumber of records with unusual high quantity (>= 100): {unusual_high_quantity}\n")
        self.log_file.write(f"Number of records with unusual low quantity (<= 0): {unusual_low_quantity}\n")
        
        
    def __total_amount_validation(self,):
        """Validate TotalAmount by checking if it logically aligns with (Quantity * Price)."""
        
        # Check the TotalAmount values to match the result of (Quantity * Price)
        valid_total_amount = (self.df["TotalAmount"] == self.df["Quantity"] * self.df["Price"]).sum()
        if valid_total_amount < len(self.df):
            wrong_total_amount = len(self.df) - valid_total_amount
            self.log_file.write("\n")
            self.log_file.write("*"*100)
            self.log_file.write("\n")
            self.log_file.write("\nValidation (for TotalAmount) failed!\n")
            self.log_file.write("Records detected with no matching TotalAmount with (Quantity * Price)\n")
            self.log_file.write(f"Number of records with wrong total amount: {wrong_total_amount}\n")
        else:
            self.log_file.write("\n")
            self.log_file.write("*"*100)
            self.log_file.write("\n")
            self.log_file.write("\nValidation (for TotalAmount) passed successfully!")
            
    def run(self,):
        """Run the anomaly detection processes: 
            1. Detection missing values
            2. Identifying future dates
            3. Flag outliers in Quantity field
            4. Validate the TotalAmount field values
        """
        self.__missing_val()
        self.__future_data()
        self.__quantity_outliers()
        self.__total_amount_validation()
        
        # Close the logfile
        self.log_file.close()





if __name__ == "__main__":
    
    # Define the command line parser to get the data file path
    parser = argparse.ArgumentParser(description='Parse ecommerce data file for anomaly detection.')
    parser.add_argument('-f', '--ecommerce_data')
    args = parser.parse_args()
    # Extract the input
    data_path = args.ecommerce_data
    
    # Run anomaly detection process
    anomaly_detector_obj = AnomalyDetector(data_path=data_path)
    anomaly_detector_obj.run()
    