
from database import get_connection


def add_paper(user_id, title, authors, year, abstract, url, topic, status):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO papers
            (user_id, title, authors, publication_year,
             abstract, paper_url, topic, reading_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            user_id, title, authors, year,
            abstract, url, topic, status
        ))

        connection.commit()
        return True, "Research paper saved successfully."

    except Exception as error:
        if connection:
            connection.rollback()
        return False, str(error)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def get_papers(user_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT paper_id, title, authors, publication_year,
                   abstract, paper_url, topic, reading_status,
                   created_at
            FROM papers
            WHERE user_id = %s
            ORDER BY created_at DESC
        """

        cursor.execute(query, (user_id,))
        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def update_paper(
    user_id, paper_id, title, authors, year,
    abstract, url, topic, status
):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            UPDATE papers
            SET title = %s,
                authors = %s,
                publication_year = %s,
                abstract = %s,
                paper_url = %s,
                topic = %s,
                reading_status = %s
            WHERE paper_id = %s AND user_id = %s
        """

        cursor.execute(query, (
            title, authors, year, abstract,
            url, topic, status, paper_id, user_id
        ))

        if cursor.rowcount == 0:
            connection.rollback()
            return False, "Paper not found or no changes made."

        connection.commit()
        return True, "Research paper updated successfully."

    except Exception as error:
        if connection:
            connection.rollback()
        return False, str(error)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def delete_paper(user_id, paper_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            DELETE FROM papers
            WHERE paper_id = %s AND user_id = %s
        """

        cursor.execute(query, (paper_id, user_id))

        if cursor.rowcount == 0:
            connection.rollback()
            return False, "Paper not found."

        connection.commit()
        return True, "Research paper deleted successfully."

    except Exception as error:
        if connection:
            connection.rollback()
        return False, str(error)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
