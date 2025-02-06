import hashlib
import os
import glob
import sqlite3
import base64
from tqdm import tqdm

TITLE = """
***************************
*      ChkSum             *
*    CodebyKalvin         *
***************************
"""
DATABASE_NAME = "checksums.db"
DEFAULT_OUTPUT_FORMAT = "hex"
DEFAULT_ALGORITHM = "sha256"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def calculate_checksum(filepath, algorithm=DEFAULT_ALGORITHM, block_size=65536, output_format=DEFAULT_OUTPUT_FORMAT):
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return None
    try:
        hasher = hashlib.new(algorithm)
        file_size = os.path.getsize(filepath)
        with open(filepath, 'rb') as file, tqdm(total=file_size, unit='B', unit_scale=True, desc=f"Hashing {os.path.basename(filepath)}") as pbar:
            while chunk := file.read(block_size):
                hasher.update(chunk)
                pbar.update(len(chunk))
        if output_format == "hex":
            return hasher.hexdigest()
        elif output_format == "base64":
            return base64.b64encode(hasher.digest()).decode('utf-8')
        return None
    except Exception as e:
        print(f"Error calculating hash: {e}")
        return None

def verify_checksum(filepath, expected_checksum, algorithm=DEFAULT_ALGORITHM, output_format=DEFAULT_OUTPUT_FORMAT):
    calculated_checksum = calculate_checksum(filepath, algorithm, output_format)
    return calculated_checksum and calculated_checksum.lower() == expected_checksum.lower()

def create_checksum_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS checksums (
            filepath TEXT PRIMARY KEY,
            algorithm TEXT NOT NULL,
            checksum TEXT NOT NULL,
            output_format TEXT NOT NULL
        )
    """)
    conn.commit()

def save_checksum_to_db(conn, filepath, algorithm, checksum, output_format):
    try:
        conn.execute("INSERT OR REPLACE INTO checksums (filepath, algorithm, checksum, output_format) VALUES (?, ?, ?, ?)", (filepath, algorithm, checksum, output_format))
        conn.commit()
    except Exception as e:
        print(f"Error saving checksum to database: {e}")

def load_checksums_from_db(conn):
    cursor = conn.execute("SELECT filepath, algorithm, checksum, output_format FROM checksums")
    return cursor.fetchall()

def delete_checksum_from_db(conn, filepath):
    try:
        conn.execute("DELETE FROM checksums WHERE filepath = ?", (filepath,))
        conn.commit()
        print(f"Checksum for '{filepath}' deleted.")
    except Exception as e:
        print(f"Error deleting checksum: {e}")

def get_checksum_count_from_db(conn):
    return conn.execute("SELECT COUNT(*) FROM checksums").fetchone()[0]

def compare_checksums_with_db(conn, file_pattern, algorithm, output_format):
    files = []
    if os.path.isdir(file_pattern):
        files = [os.path.join(root, filename) for root, _, filenames in os.walk(file_pattern) for filename in filenames]
    else:
        files = glob.glob(file_pattern)

    if not files:
        print("No files matched.")
        return

    db_checksums = {row[0]: row for row in load_checksums_from_db(conn)}
    for file in files:
        calculated_checksum = calculate_checksum(file, algorithm, output_format)
        if calculated_checksum is None:
            continue
        if file in db_checksums:
            db_algo, db_checksum, db_format = db_checksums[file][1:]
            if db_algo == algorithm and db_format == output_format and calculated_checksum.lower() == db_checksum.lower():
                print(f"Match: {file}")
            else:
                print(f"Mismatch: {file}")
        else:
            print(f"Not in DB: {file}, Checksum: {calculated_checksum}")

def process_files(file_pattern, algorithm, operation, output_format):
    conn = sqlite3.connect(DATABASE_NAME)
    create_checksum_table(conn)

    files = []
    if os.path.isdir(file_pattern):
        files = [os.path.join(root, filename) for root, _, filenames in os.walk(file_pattern) for filename in filenames]
    else:
        files = glob.glob(file_pattern)

    if not files:
        print("No files matched.")
        return
    for file in files:
      if operation == "calculate":
         checksum = calculate_checksum(file, algorithm, output_format)
         if checksum:
            print(f"Checksum ({algorithm}, {output_format}): {checksum} - {file}")
            save_checksum_to_db(conn, file, algorithm, checksum, output_format)
      elif operation == "verify":
        expected = input(f"Enter expected checksum for {file}: ")
        if verify_checksum(file, expected, algorithm, output_format):
          print(f"Match: {file}")
        else:
          print(f"Mismatch: {file}")
    conn.close()

def main():
    global DEFAULT_ALGORITHM
    clear_screen()
    print(TITLE)

    conn = sqlite3.connect(DATABASE_NAME)
    create_checksum_table(conn)  # Ensure the table exists
    conn.close()

    while True:
        conn = sqlite3.connect(DATABASE_NAME)
        count = get_checksum_count_from_db(conn)
        conn.close()

        print(f"\nDefault algorithm: {DEFAULT_ALGORITHM} | Checksums in database: {count}")
        print("1. Calculate checksums and save")
        print("2. Verify checksums (manual)")
        print("3. Compare with database")
        print("4. Delete checksum from database")
        print("5. Set default algorithm")
        print("6. Clear Screen")
        print("7. Exit")
        choice = input("Enter choice (1-7): ")

        if choice == '1':
            file_pattern = input("Enter file(s)/path (e.g., *.txt, dir/): ")
            print(f"Processing files: {file_pattern}")
            algo = input(f"Algorithm (press enter for {DEFAULT_ALGORITHM}): ").strip() or DEFAULT_ALGORITHM
            while True:
                fmt = input(f"Output format (hex/base64, press enter for {DEFAULT_OUTPUT_FORMAT}): ").strip() or DEFAULT_OUTPUT_FORMAT
                if fmt.lower() in ["hex", "base64"]:
                  break
                else:
                  print("Invalid format. Use 'hex' or 'base64'.")
            process_files(file_pattern, algo, "calculate", fmt)

        elif choice == '2':
            file_pattern = input("Enter file(s)/path: ")
            print(f"Processing files: {file_pattern}")
            algo = input(f"Algorithm (press enter for {DEFAULT_ALGORITHM}): ").strip() or DEFAULT_ALGORITHM
            while True:
              fmt = input(f"Output format (hex/base64, press enter for {DEFAULT_OUTPUT_FORMAT}): ").strip() or DEFAULT_OUTPUT_FORMAT
              if fmt.lower() in ["hex", "base64"]:
                  break
              else:
                  print("Invalid format. Use 'hex' or 'base64'.")
            process_files(file_pattern, algo, "verify", fmt)
        elif choice == '3':
            file_pattern = input("Enter file(s)/path: ")
            print(f"Comparing with DB: {file_pattern}")
            algo = input(f"Algorithm (press enter for {DEFAULT_ALGORITHM}): ").strip() or DEFAULT_ALGORITHM
            while True:
              fmt = input(f"Output format (hex/base64, press enter for {DEFAULT_OUTPUT_FORMAT}): ").strip() or DEFAULT_OUTPUT_FORMAT
              if fmt.lower() in ["hex", "base64"]:
                  break
              else:
                  print("Invalid format. Use 'hex' or 'base64'.")
            conn = sqlite3.connect(DATABASE_NAME)
            compare_checksums_with_db(conn, file_pattern, algo, fmt)
            conn.close()
        elif choice == '4':
            filepath = input("Enter file path to delete: ")
            conn = sqlite3.connect(DATABASE_NAME)
            delete_checksum_from_db(conn, filepath)
            conn.close()
        elif choice == '5':
            DEFAULT_ALGORITHM = input("Enter new default algorithm: ").strip()
            print(f"Default algorithm set to: {DEFAULT_ALGORITHM}")
        elif choice == '6':
            clear_screen()
            print(TITLE)
        elif choice == '7':
            if input("Are you sure? (y/n): ").lower() == 'y':
              print("Exiting...")
              break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
