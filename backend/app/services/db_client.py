"""
Supabase PostgreSQL Client for USPTO Trademark Database
"""
import psycopg2
import psycopg2.extras
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
from datetime import datetime

from app.models.trademark import Trademark, TrademarkStatus

load_dotenv()


class PostgreSQLClient:
    """PostgreSQL client for database operations (Railway, Supabase, or any PostgreSQL)"""

    def __init__(self):
        """Initialize connection to PostgreSQL database (Railway or Supabase)"""
        # Database connection details
        # Format: postgresql://postgres:[PASSWORD]@[HOST]:[PORT]/[DATABASE]
        self.connection_string = os.getenv('DATABASE_URL') or os.getenv('SUPABASE_DB_URL')

        if not self.connection_string:
            raise ValueError(
                "DATABASE_URL environment variable not set.\n"
                "Add your PostgreSQL connection string to scripts/.env file"
            )

        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    self.connection_string,
                    cursor_factory=psycopg2.extras.RealDictCursor
                )
                self.conn.autocommit = True
                self.cursor = self.conn.cursor()
                print("✅ Connected to PostgreSQL database")
            except Exception as e:
                print(f"❌ Failed to connect to Supabase: {e}")
                raise

    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Disconnected from PostgreSQL database")

    def execute_sql_file(self, file_path: str):
        """Execute SQL from file (e.g., schema.sql)"""
        if not self.conn:
            self.connect()

        with open(file_path, 'r') as f:
            sql = f.read()

        try:
            self.cursor.execute(sql)
            print(f"✅ Executed SQL file: {file_path}")
        except Exception as e:
            print(f"❌ Error executing SQL file: {e}")
            raise

    def insert_trademark(self, trademark_data: Dict) -> bool:
        """Insert single trademark record"""
        if not self.conn:
            self.connect()

        try:
            self.cursor.execute(
                """
                INSERT INTO trademarks (
                    serial_number, mark_text, owner_name, status,
                    filing_date, registration_date, registration_number,
                    international_classes, goods_services
                ) VALUES (
                    %(serial_number)s, %(mark_text)s, %(owner_name)s, %(status)s,
                    %(filing_date)s, %(registration_date)s, %(registration_number)s,
                    %(international_classes)s, %(goods_services)s
                )
                ON CONFLICT (serial_number) DO UPDATE SET
                    mark_text = EXCLUDED.mark_text,
                    owner_name = EXCLUDED.owner_name,
                    status = EXCLUDED.status,
                    filing_date = EXCLUDED.filing_date,
                    registration_date = EXCLUDED.registration_date,
                    registration_number = EXCLUDED.registration_number,
                    international_classes = EXCLUDED.international_classes,
                    goods_services = EXCLUDED.goods_services,
                    updated_at = NOW()
                """,
                trademark_data
            )
            return True
        except Exception as e:
            print(f"❌ Error inserting trademark {trademark_data.get('serial_number')}: {e}")
            return False

    def bulk_insert_from_csv(self, csv_file_path: str, table_name: str = 'trademarks'):
        """Bulk insert from CSV using COPY (fastest method)"""
        if not self.conn:
            self.connect()

        try:
            with open(csv_file_path, 'r') as f:
                # Use COPY FROM for fast bulk insert
                self.cursor.copy_expert(
                    f"""
                    COPY {table_name} (
                        serial_number, mark_text, owner_name, status,
                        filing_date, registration_date, registration_number,
                        international_classes, goods_services
                    )
                    FROM STDIN WITH CSV HEADER DELIMITER ','
                    """,
                    f
                )
            print(f"✅ Bulk inserted from {csv_file_path}")
            return True
        except Exception as e:
            print(f"❌ Error bulk inserting from CSV: {e}")
            raise

    def search_trademarks(self, query: str, limit: int = 50) -> List[Trademark]:
        """Search trademarks using full-text search"""
        if not self.conn:
            self.connect()

        try:
            self.cursor.execute(
                """
                SELECT
                    serial_number, mark_text, owner_name, status,
                    filing_date, registration_date, registration_number,
                    international_classes, goods_services,
                    ts_rank(search_vector, query) AS rank
                FROM trademarks, to_tsquery('english', %s) query
                WHERE search_vector @@ query
                ORDER BY rank DESC
                LIMIT %s
                """,
                (query, limit)
            )
            results = self.cursor.fetchall()
            return [self._dict_to_trademark(dict(row)) for row in results]
        except Exception as e:
            print(f"❌ Error searching trademarks: {e}")
            return []

    def search_exact_match(self, mark_text: str) -> Optional[Dict]:
        """Search for exact trademark match (case-insensitive)"""
        if not self.conn:
            self.connect()

        try:
            self.cursor.execute(
                """
                SELECT * FROM trademarks
                WHERE UPPER(mark_text) = UPPER(%s)
                LIMIT 1
                """,
                (mark_text,)
            )
            result = self.cursor.fetchone()
            return dict(result) if result else None
        except Exception as e:
            print(f"❌ Error searching for exact match: {e}")
            return None

    def get_trademark_by_serial(self, serial_number: str) -> Optional[Trademark]:
        """Get trademark by serial number"""
        if not self.conn:
            self.connect()

        try:
            self.cursor.execute(
                "SELECT * FROM trademarks WHERE serial_number = %s",
                (serial_number,)
            )
            result = self.cursor.fetchone()
            return self._dict_to_trademark(dict(result)) if result else None
        except Exception as e:
            print(f"❌ Error getting trademark by serial: {e}")
            return None

    def count_trademarks(self, status_filter: Optional[str] = None) -> int:
        """Count trademarks, optionally filtered by status"""
        if not self.conn:
            self.connect()

        try:
            if status_filter:
                self.cursor.execute(
                    "SELECT COUNT(*) as count FROM trademarks WHERE status = %s",
                    (status_filter,)
                )
            else:
                self.cursor.execute("SELECT COUNT(*) as count FROM trademarks")

            result = self.cursor.fetchone()
            return result['count'] if result else 0
        except Exception as e:
            print(f"❌ Error counting trademarks: {e}")
            return 0

    def log_import(self, file_name: str, records_imported: int, records_failed: int, status: str, error_message: Optional[str] = None):
        """Log import results"""
        if not self.conn:
            self.connect()

        try:
            self.cursor.execute(
                """
                INSERT INTO import_log (file_name, records_imported, records_failed, status, error_message, completed_at)
                VALUES (%s, %s, %s, %s, %s, NOW())
                """,
                (file_name, records_imported, records_failed, status, error_message)
            )
            print(f"📝 Logged import: {file_name} - {records_imported} imported, {records_failed} failed")
        except Exception as e:
            print(f"❌ Error logging import: {e}")

    def _dict_to_trademark(self, row: Dict) -> Trademark:
        """Convert database row dictionary to Trademark model"""
        # Parse status string to TrademarkStatus enum
        status_str = row.get('status', '').upper()
        status_map = {
            'REGISTERED': TrademarkStatus.REGISTERED,
            'REG': TrademarkStatus.REGISTERED,
            'LIVE': TrademarkStatus.REGISTERED,
            'PENDING': TrademarkStatus.PENDING,
            'PUB': TrademarkStatus.PENDING,
            'PUBLISHED': TrademarkStatus.PENDING,
            'ABANDONED': TrademarkStatus.ABANDONED,
            'DEAD': TrademarkStatus.ABANDONED,
            'CANCELLED': TrademarkStatus.CANCELLED,
            'CANCELED': TrademarkStatus.CANCELLED,
            'EXPIRED': TrademarkStatus.EXPIRED,
        }
        status = status_map.get(status_str, TrademarkStatus.UNKNOWN)

        # Parse international classes (stored as array in PostgreSQL)
        classes = row.get('international_classes', [])
        if isinstance(classes, str):
            classes = [c.strip() for c in classes.split(',') if c.strip()]
        elif not isinstance(classes, list):
            classes = []

        # Convert date objects to ISO format strings
        filing_date = row.get('filing_date')
        if isinstance(filing_date, datetime):
            filing_date = filing_date.date().isoformat()
        elif hasattr(filing_date, 'isoformat'):
            filing_date = filing_date.isoformat()

        registration_date = row.get('registration_date')
        if isinstance(registration_date, datetime):
            registration_date = registration_date.date().isoformat()
        elif hasattr(registration_date, 'isoformat'):
            registration_date = registration_date.isoformat()

        return Trademark(
            serial_number=row.get('serial_number', ''),
            registration_number=row.get('registration_number'),
            mark_text=row.get('mark_text', ''),
            owner_name=row.get('owner_name', 'Unknown'),
            status=status,
            filing_date=filing_date,
            registration_date=registration_date,
            international_classes=classes,
            goods_services_description=row.get('goods_services')
        )


# For backwards compatibility
SupabaseClient = PostgreSQLClient

# Example usage
if __name__ == "__main__":
    client = PostgreSQLClient()
    client.connect()

    # Test: Count trademarks
    count = client.count_trademarks()
    print(f"Total trademarks in database: {count}")

    # Test: Search for Nike
    results = client.search_trademarks("Nike")
    print(f"Found {len(results)} trademarks matching 'Nike'")

    client.disconnect()
