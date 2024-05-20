import os
import sys

class UniqueInt:
    @staticmethod
    def processFile(inputFilePath, outputDir):
        unique_items = set()

        # Determine file type
        file_extension = os.path.splitext(inputFilePath)[1].lower()

        with open(inputFilePath, 'r') as inputFile:
            for line in inputFile:
                # Strip leading/trailing whitespaces and split by whitespace
                integers = UniqueInt.parse_line(line.strip())
                for integer in integers:
                    try:
                        num = int(integer)
                        if -1023 <= num <= 1023:
                            unique_items.add(num)
                    except ValueError:
                        # Skip non-integer inputs
                        pass


        # Sort unique items
        sorted_items = UniqueInt.custom_sort(list(unique_items))

        # Generate output file path
        outputFilePath = os.path.join(outputDir, os.path.basename(inputFilePath)[:-4] + "_results.txt")
        print("Output File Path:", outputFilePath)
        
        # Write to output file
        with open(outputFilePath, 'w') as outputFile:
            for item in sorted_items:
                outputFile.write(str(item) + '\n')

    @staticmethod
    def parse_line(line):
        integers = []
        num = ''
        # Split the line by whitespace characters (space or tab)
        parts = line.split()
        if len(parts) > 1:
            # If there are multiple parts, skip the line
            return integers
        for part in parts:
            if part.strip():
                # Check if the part contains only digits or a single '-' character
                if all(char.isdigit() or (char == '-' and part.count('-') == 1 and len(part) > 1 and part.index('-') == 0) for char in part):
                    num += part
                else:
                    # If the part contains non-integer characters or multiple '-', skip it
                    num = ''
            if num:
                # If num is not empty, append it to the list of integers
                integers.append(int(num))  # Convert num to integer before appending
                num = ''
        return integers

    @staticmethod
    def custom_sort(arr):
        # Bubble sort implementation
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python UniqueInt.py <input_file_path>")
        sys.exit(1)

    inputFilePath = sys.argv[1]
    outputDir = 'sample_results/'

    # Ensure input file exists
    if not os.path.exists(inputFilePath):
        print("Error: Input file not found.")
        sys.exit(1)

    # Ensure output directory exists, create if not
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    # Process file
    UniqueInt.processFile(inputFilePath, outputDir)
    print("File processed successfully.")
