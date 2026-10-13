
import csv
import os
from collections import defaultdict


class RecurringReversalProcessor:

    def __init__(self, input_file, column_names, delimiter=","):
        self.input_file = input_file
        self.column_names = column_names
        self.delimiter = delimiter

        self.output_file = self._generate_output_file_name()

        self.original_sum = defaultdict(float)
        self.modified_sum = defaultdict(float)
        self.total_rows = 0

    def _generate_output_file_name(self):
        base, ext = os.path.splitext(self.input_file)
        return f"{base}_reversal{ext}"

    def read_and_process_file(self):
        print(f"Reading and processing file: {self.input_file}")

        try:
            with open(
                self.input_file, "r", newline="", encoding="utf-8-sig"
            ) as infile:

                reader = csv.DictReader(
                    infile, delimiter=self.delimiter
                )

                if reader.fieldnames is None:
                    raise ValueError("The input file is empty or has no header.")

                missing_columns = [
                    col for col in self.column_names
                    if col not in reader.fieldnames
                ]

                if missing_columns:
                    raise ValueError(
                        f"Columns not found in file: {missing_columns}. "
                        f"Available columns: {reader.fieldnames}"
                    )

                rows = []

                for row in reader:
                    for column_name in self.column_names:
                        try:
                            value = float(row[column_name])
                        except (ValueError, TypeError):
                            raise ValueError(
                                f"Invalid numeric value in column "
                                f"'{column_name}': {row[column_name]!r}, "
                                f"at data row {self.total_rows + 1}"
                            )

                        self.original_sum[column_name] += value

                        reversed_value = -value
                        row[column_name] = str(reversed_value)

                        self.modified_sum[column_name] += reversed_value

                    self.total_rows += 1
                    rows.append(row)

                print("File read successfully and data processed.")
                return rows

        except (OSError, csv.Error, ValueError) as e:
            print(f"Error reading or processing file: {e}")
            return []

    def write_processed_file(self, rows):
        print(f"Writing processed data to file: {self.output_file}")

        try:
            if not rows:
                print("No data rows available to write.")
                return

            with open(
                self.output_file, "w", newline="", encoding="utf-8"
            ) as outfile:

                writer = csv.DictWriter(
                    outfile,
                    fieldnames=rows[0].keys(),
                    delimiter=self.delimiter
                )

                writer.writeheader()
                writer.writerows(rows)

            print("Processed data written to file successfully.")

        except (OSError, csv.Error) as e:
            print(f"Error writing to file: {e}")

    def print_audit_info(self):
        print("\n--- Audit Information ---")
        print(f"Total rows processed: {self.total_rows}")

        for column_name in self.column_names:
            print(
                f"Original sum of '{column_name}': "
                f"{self.original_sum[column_name]:.2f}"
            )

            print(
                f"Modified sum of '{column_name}': "
                f"{self.modified_sum[column_name]:.2f}"
            )

    def process(self):
        rows = self.read_and_process_file()

        if rows:
            self.write_processed_file(rows)
            self.print_audit_info()


# Example usage
if __name__ == "__main__":

    input_file = r"C:\Users\Asus\Downloads\IDM_RECURRING_sample_ledger_data_25_rows-1.csv"

    if "SLTrans" in input_file:
        column_names = ["Transaction Amount"]
        delimiter = "\t"

    elif "IDM_RECURRING" in input_file:
        column_names = ["Amount"]

        # Change this to "\t" if the IDM file is tab-separated.
        delimiter = ","

    else:
        raise ValueError("Unrecognized input file type.")

    processor = RecurringReversalProcessor(
        input_file, column_names, delimiter
    )

    processor.process()
