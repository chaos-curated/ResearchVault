
from database import get_connection

try:
    connection = get_connection()

    print("ResearchVault connected to MySQL successfully!")

    connection.close()

except Exception as error:
    print("Connection failed:", error)
