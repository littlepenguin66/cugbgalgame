import pandas as pd
import json
import sys

class DataProcessor:
    """
    A class to process data from a CSV file and convert it to JSON format.

    Attributes:
        csv_file_path (str): The path to the CSV file to read.
        json_file_path (str): The path to the JSON file to write.

    Methods:
        read_csv: Reads a CSV file and prints the DataFrame.
        to_json: Converts the DataFrame to a JSON format and writes it to a file.
        generate_variations: Generates variations of content for each row in the DataFrame.
    """

    def __init__(self, csv_file_path, json_file_path):
        self.csv_file_path = csv_file_path
        self.json_file_path = json_file_path

    def read_csv(self):
        """Reads a CSV file and prints the DataFrame."""
        df = pd.read_csv(self.csv_file_path, encoding='gbk')
        print(df)
        self.to_json(df)

    def to_json(self, df):
        """Converts the DataFrame to a JSON format and writes it to a file."""
        new_rows = self.generate_variations(df)
        new_df = pd.DataFrame(new_rows)
        data_dict = new_df.to_dict('records')

        with open(self.json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=4)

    def generate_variations(self, df):
        """
        Generates variations of content for each row in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to process.

        Returns:
            list of dict: A list of dictionaries with the new content variations.
        """
        new_rows = []
        for _, row in df.iterrows():
            content = row['content']
            summary = row['summary']
            variations = [
                f'什么是{content}',
                f'{content}是什么',
                f'{content}是什么意思',
                f'{content}的意思',
                f'介绍一下{content}',
                f'啥是{content}',
                f'{content}是啥',
                f'{content}是啥意思',
                f'{content}的意思是什么'
            ]
            for variation in variations:
                new_rows.append({'content': variation, 'summary': summary})
        return new_rows

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python read_csv.py <csv_file_path> <json_file_path>")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    json_file_path = sys.argv[2]

    processor = DataProcessor(csv_file_path, json_file_path)
    processor.read_csv()
