import os
import sys
import time

try:
    import resource
    RESOURCE_MODULE_AVAILABLE = True
except ImportError:
    RESOURCE_MODULE_AVAILABLE = False


class UniqueInt:
    @staticmethod
    def processFile(inputFilePath, outputDir):
        """
        Process the input file to find unique integers and write them to the output file.

        Args:
            inputFilePath (str): Path to the input file.
            outputDir (str): Path to the output directory.
        """

        start_time = time.time()  # Start time measurement
        start_memory = UniqueInt.get_memory_usage() if RESOURCE_MODULE_AVAILABLE else None  # Start memory measurement

        unique_items = {}
        unique_count = 0

        # Determine file type
        file_extension = os.path.splitext(inputFilePath)[1].lower()

        with open(inputFilePath, 'r') as inputFile:
            for line in inputFile:
                if UniqueInt.validate_line(line.strip()):
                    integers = UniqueInt.parse_line(line.strip())
                    for integer in integers:
                        if UniqueInt.is_proper_number(integer) and UniqueInt.is_in_range(integer):
                            if integer not in unique_items:
                                unique_items[integer] = True
                                unique_count += 1

        # Convert dictionary keys to list for sorting
        unique_items_list = list(unique_items.keys())

        # Sort unique items
        sorted_items = UniqueInt.merge_sort(unique_items_list)

        # Generate output file path
        outputFilePath = os.path.join(outputDir, os.path.basename(inputFilePath)[:-4] + "_results.txt")
        print(f"Output file path: {outputFilePath}")


        # Write to output file
        with open(outputFilePath, 'w') as outputFile:
            for item in sorted_items:
                outputFile.write(str(item) + '\n')
        
        end_time = time.time()  # End time measurement
        end_memory = UniqueInt.get_memory_usage() if RESOURCE_MODULE_AVAILABLE else None  # End memory measurement

        # Print memory usage and runtime
        if RESOURCE_MODULE_AVAILABLE:
            print(f"Memory used: {end_memory - start_memory} Bytes")
        print(f"Runtime: {(end_time - start_time) * 1000} milliseconds")


        def get_memory_usage():
            """
            Get the current memory usage.
            """
            return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * resource.getpagesize()

    @staticmethod
    def validate_line(line):
        """
        Validate if a line contains a single valid number and doesn't contain two hyphens.

        Args:
            line (str): Line of text to validate.
        """
        if line.strip() == '':
            return False
        parts = line.split()
        if len(parts) != 1:
            return False
        if '--' in line:
            return False
        return True

    @staticmethod
    def parse_line(line):
        """
        Parse a line of text to extract integers.

        Args:
            line (str): Line of text to parse.
        """
        integers = []
        for part in UniqueInt.split_line(line):
            if UniqueInt.is_valid_integer(part):
                integers.append(int(part))
        return integers

    @staticmethod
    def split_line(line):
        """
        Split a line of text by whitespace characters (space or tab).

        Args:
            line (str): Line of text to split.
        """
        return line.split()

    @staticmethod
    def is_valid_integer(part):
        """
        Check if a part of text represents a valid integer.

        Args:
            part (str): Part of text to check.
        """
        return part.strip().isdigit() or (part.strip().startswith('-') and part.strip().count('-') == 1 and part.strip().lstrip('-').isdigit())

    @staticmethod
    def is_proper_number(num):
        """
        Check if a string represents a proper number.

        Args:
            num (str): String to check.
        """
        try:
            int(num)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_in_range(num):
        """
        Check if a number is within the range of -1023 to 1023.

        Args:
            num (int): Number to check.
        """
        return -1023 <= num <= 1023

    @staticmethod
    def merge_sort(arr):
        """
        Perform merge sort algorithm to sort a list of integers.

        Args:
            arr (list): List of integers to sort.
        """
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        left_half = UniqueInt.merge_sort(left_half)
        right_half = UniqueInt.merge_sort(right_half)
        return UniqueInt.merge(left_half, right_half)

    @staticmethod
    def merge(left_half, right_half):
        """
        Merge two sorted lists into one sorted list.

        Args:
            left_half (list): First sorted list.
            right_half (list): Second sorted list.
        """
        merged = []
        left_index, right_index = 0, 0
        while left_index < len(left_half) and right_index < len(right_half):
            if left_half[left_index] < right_half[right_index]:
                merged.append(left_half[left_index])
                left_index += 1
            else:
                merged.append(right_half[right_index])
                right_index += 1
        merged.extend(left_half[left_index:])
        merged.extend(right_half[right_index:])
        return merged


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
