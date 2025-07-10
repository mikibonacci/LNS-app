# utilities to inspect folders and files in the LNS-apps project
from pathlib import Path
from importlib.resources import files

def grep_hdf_files_informations(folder: Path) -> list:
    """
    Find all hdf files in the given folder and return a list of year and the number extracted from the filenames.
    
    the filename is camea2021n001388.hdf, where the year is 2021 and the number is 1388. So, 
    we need to extract the year number from the filename.
    This function searches for all files with the .hdf extension in the specified folder and extracts the year number
    from the filename. It returns a list of year numbers as strings.

    Args:
        folder (Path): The folder to search for hdf files.
        
    Returns:
        list: A list of year numbers as strings.
    """
    hdf_files = list(folder.glob('*.hdf'))
    year_numbers = []
    file_numbers = []

    for file in hdf_files:
        if file.is_file():
            # Extract the year number from the filename
            year_number = file.stem.split('n')[0].replace('camea', '')
            if year_number.isdigit():
                year_number = year_number[:4]
                if len(year_number) == 4:  # Ensure it's a valid year format
                    year_numbers.append(year_number)
            
            file_number = file.stem.split('n')[1].replace('hdf', '')
            if file_number.isdigit():
                # clean from leading zeros
                file_number = int(file_number.lstrip('0'))
                if file_number:  # Ensure it's not an empty string
                    file_numbers.append(file_number)
    
    # Remove duplicates and sort the year numbers
    year_numbers = sorted(set(year_numbers)) 
    file_numbers = [str(number) for number in sorted(set(file_numbers))]   

    return year_numbers, file_numbers