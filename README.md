## File Checksum Tool

A Python-based file checksum tool that supports multiple hashing algorithms, allowing you to verify file integrity by calculating and comparing checksums. This tool supports:
- **Multiple hashing algorithms:** md5, sha1, sha256, sha512
- **Recursive directory traversal:** to process a directory recursively
- **Checksum database:** To store and compare checksums with existing files.
- **Multiple file processing:** to process multiple files at once by using glob patterns or directories.
- **Progress indication:** To provide feedback on progress for hashing files.
- **Different output formats:** To output checksums in `hex` or `base64` format.

This application allows you to easily calculate and verify file checksums using a command-line interface (CLI).

### Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Calculate Checksum](#calculate-checksum)
  - [Verify Checksum](#verify-checksum)
  - [Compare with Database](#compare-with-database)
  - [Delete Checksum from Database](#delete-checksum-from-database)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

---

### Features

- **Multiple Hashing Algorithms**: Supports various hashing algorithms including `md5`, `sha1`, `sha256`, and `sha512`.
- **Recursive Directory Traversal**: Ability to process files within a directory and its subdirectories.
- **Checksum Database**: Save calculated checksums to an SQLite database for future verification.
- **Multiple File Processing**: Process multiple files using glob patterns or directories.
- **Progress Indication**: Shows a progress bar during checksum calculation for large files.
- **Different output formats:** Support for `hex` or `base64` output format for checksums.
- **Clear Screen**: Clear the console screen for a cleaner output.
- **Default Algorithm**: Set a default hashing algorithm to use if not specified.

---

### Installation

To run this app locally, follow these steps:

#### 1. Clone the Repository

```bash
git clone <REPOSITORY_LINK>
cd <REPOSITORY_FOLDER>
```

#### 2. Install Dependencies

Make sure you have **Python 3** installed. Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

The `requirements.txt` should contain the following:
```txt
tqdm
```

---

### Usage

Once installed, you can run the application from the command line using:

```bash
python checksum_tool.py
```

This will launch the CLI, where you can choose to calculate, verify checksums or compare with database.

---

#### Calculate Checksum

1.  **Calculate**: Calculates and prints the checksum of the specified file(s) or directory.
    - Enter the file path, directory, or a glob pattern (e.g. `*.txt`).
    - Optionally, provide a specific hashing algorithm (if not, `sha256` is used).
    - Optionally, provide output format either `hex` or `base64`(if not, `hex` is used).
     - The calculated checksums are also saved to a database.

Example:

```bash
python checksum_tool.py
...
Enter your choice (1/2/3/4/5/6/7): 1
Enter the file path, directory, or glob pattern (e.g., *.txt): myfile.txt
Enter hashing algorithm (e.g., md5, sha1, sha256, sha512. press enter for sha256): sha256
Enter checksum output format (hex or base64, press enter for hex): base64
Checksum (sha256, base64):  +tL5R550+G4uC1P9z78W07Wq0B0i29T031J5K645K0= - myfile.txt
```
---

#### Verify Checksum

1.  **Verify**: Verifies checksum of the specified file(s) or directory against a user-provided checksum value.
    - Enter the file path, directory, or a glob pattern (e.g. `*.txt`).
    - Optionally, provide a specific hashing algorithm (if not, `sha256` is used).
    - Optionally, provide output format either `hex` or `base64`(if not, `hex` is used).
    -  When processing files you will be prompted to enter expected checksum.

Example:

```bash
python checksum_tool.py
...
Enter your choice (1/2/3/4/5/6/7): 2
Enter the file path, directory, or glob pattern (e.g., *.txt): myfile.txt
Enter hashing algorithm (e.g., md5, sha1, sha256, sha512. press enter for sha256): sha256
Enter checksum output format (hex or base64, press enter for hex): base64
Enter expected checksum for myfile.txt:  +tL5R550+G4uC1P9z78W07Wq0B0i29T031J5K645K0=
Match: myfile.txt
```
---
#### Compare with Database

1.  **Compare**: Compares checksums of files with those stored in the database.
    - Enter the file path, directory, or a glob pattern (e.g. `*.txt`).
    - Optionally, provide a specific hashing algorithm (if not, `sha256` is used).
    - Optionally, provide output format either `hex` or `base64`(if not, `hex` is used).
     - The calculated checksums are compared with checksums saved in the database.

Example:

```bash
python checksum_tool.py
...
Enter your choice (1/2/3/4/5/6/7): 3
Enter the file path, directory, or glob pattern (e.g., *.txt): myfile.txt
Enter hashing algorithm (e.g., md5, sha1, sha256, sha512. press enter for sha256): sha256
Enter checksum output format (hex or base64, press enter for hex): base64
Match: myfile.txt
```
---
#### Delete Checksum from Database

1.  **Delete:** Deletes a checksum from the database.
     - Enter the file path of checksum to delete from database.
Example:
```bash
python checksum_tool.py
...
Enter your choice (1/2/3/4/5/6/7): 4
Enter the file path to delete checksum from database:myfile.txt
Checksum for 'myfile.txt' deleted.
```
---

### Project Structure

```
checksum-tool/
│
├── checksum_tool.py   # Main Python script for running the CLI app
├── README.md          # This README file
├── requirements.txt   # List of dependencies
└── checksums.db         # Sqlite database to store checksums
```

---

### Requirements

- **Python 3** or higher
- **Pip** to install dependencies
- Required Python libraries (in `requirements.txt`):
  - `tqdm`: To display progress bars during hashing.

To install the dependencies:

```bash
pip install -r requirements.txt
```

---

### Contributing

If you want to contribute to this project, feel free to submit a pull request or create an issue with a detailed description of the feature or bug you're addressing.

#### Steps to Contribute:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature-name`).
3. Make your changes.
4. Test your changes.
5. Commit your changes (`git commit -m 'Add some feature'`).
6. Push to your branch (`git push origin feature-name`).
7. Create a pull request.

---

### License

This project is open-source and available under the [MIT License](LICENSE).

---

### Future Improvements

- Add support for more output formats for checksums.
- Develop a GUI for non-command-line users.
- Add support for saving checksums to text or JSON files.

---

### Authors

- **CodeByKalvin** - *Initial work* - [GitHub Profile](https://github.com/codebykalvin)
