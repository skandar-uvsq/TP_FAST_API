import sqlite3


def _create_tables_if_not_exist(cursor):
    """
    Create tables if they do not exist in the database.
    """
    # Table for personal information
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS PersonalInformation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone_number TEXT
        )
        """
    )

    # Table for property details with a foreign key to personal information
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS PropertyDetails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            personal_id INTEGER,
            address TEXT,
            loan_amount INTEGER,
            surface INTEGER,
            description TEXT,
            region TEXT,
            FOREIGN KEY (personal_id) REFERENCES PersonalInformation (id) ON DELETE CASCADE
        )
        """
    )


def load_data(data: dict):
    """
    Load the extracted data into the SQLite database.

    :param data: Dictionary containing 'personal_information' and 'property_details'.
    """
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect("TP_FAST_API/real_estate.db")
    cursor = conn.cursor()

    # Create tables if they don't exist
    _create_tables_if_not_exist(cursor)

    # Extract personal information and property details from the data
    personal_info = data.get("personal_information", {})
    property_info = data.get("property_details", {})

    # Insert data into the PersonalInformation table
    cursor.execute(
        """
        INSERT INTO PersonalInformation (name, email, phone_number)
        VALUES (?, ?, ?)
        """,
        (
            personal_info.get("name", None),
            personal_info.get("email", None),
            personal_info.get("phone_number", None),
        ),
    )

    # Get the id of the newly inserted personal information record
    personal_id = cursor.lastrowid

    # Check if there was an insertion into PersonalInformation
    if personal_id:
        # Prepare the property description as a comma-separated string
        description_str = ", ".join(property_info.get("description", []))

        # Insert data into the PropertyDetails table
        cursor.execute(
            """
            INSERT INTO PropertyDetails (personal_id, address, loan_amount, surface, description, region)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                personal_id,
                property_info.get("address", None),
                property_info.get("loan_amount", None),
                property_info.get("surface", None),
                description_str,
                property_info.get("region", None),
            ),
        )

    # Commit changes and close the connection
    conn.commit()
    conn.close()
