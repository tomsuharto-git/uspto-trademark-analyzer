"""
USPTO API Client - Interfaces with Railway PostgreSQL Database
"""
import httpx
from typing import List, Optional
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import quote

from app.config import settings
from app.models.trademark import Trademark, TrademarkStatus
from app.services.db_client import PostgreSQLClient


class USPTOClient:
    """Client for USPTO Trademark Database (Railway PostgreSQL)"""

    def __init__(self):
        # Database client for trademark search
        self.db_client = PostgreSQLClient()
        self.db_client.connect()

        # TSDR API for detailed trademark lookups (fallback/enrichment)
        self.api_key = settings.USPTO_API_KEY
        self.tsdr_url = settings.USPTO_TSDR_URL
        self.headers = {
            "USPTO-API-KEY": self.api_key,
            "Accept": "application/json"
        }

    async def search_trademarks(self, query: str, limit: int = 50) -> List[Trademark]:
        """
        Search for trademarks by text query using Railway PostgreSQL

        Strategy: Exact matches first, then full-text search
        1. Search for exact phrase (critical for trademark clearance)
        2. Search using PostgreSQL full-text search (broader coverage)
        3. Combine and deduplicate, prioritizing exact matches

        Args:
            query: Search term (trademark name, keyword)
            limit: Maximum number of results

        Returns:
            List of Trademark objects
        """
        print(f"\n🔍 Database search for '{query}':")

        # Dictionary to deduplicate results by serial number
        # Value is (trademark, priority) where priority: 0=exact match, 1=full-text match
        all_trademarks = {}

        # STEP 1: Exact match search (highest priority)
        print(f"   1. Exact match search: '{query}'")
        exact_match = self.db_client.search_exact_match(query)
        if exact_match:
            trademark = self._db_row_to_trademark(exact_match)
            all_trademarks[trademark.serial_number] = (trademark, 0)  # Priority 0 = exact match
            print(f"      ✅ Found exact match: {exact_match['mark_text']}")
        else:
            print(f"      No exact match found")

        # STEP 2: Full-text search (broader coverage)
        print(f"   2. Full-text search")
        search_results = self.db_client.search_trademarks(query, limit=limit)
        for row in search_results:
            trademark = self._db_row_to_trademark(row)
            if trademark.serial_number not in all_trademarks:
                all_trademarks[trademark.serial_number] = (trademark, 1)  # Priority 1 = full-text
        print(f"      Found {len(search_results)} full-text matches")

        # STEP 3: Sort by priority (exact matches first), then limit
        sorted_trademarks = sorted(all_trademarks.values(), key=lambda x: x[1])
        trademarks_list = [tm for tm, _ in sorted_trademarks[:limit]]

        exact_count = sum(1 for _, priority in all_trademarks.values() if priority == 0)
        print(f"\n✅ Combined results: {len(trademarks_list)} trademarks ({exact_count} exact, {len(trademarks_list)-exact_count} related)")
        return trademarks_list

    def _db_row_to_trademark(self, row: dict) -> Trademark:
        """Convert database row to Trademark object"""
        # Parse status
        status = self._parse_status_string(row.get('status', 'UNKNOWN'))

        # Parse dates
        filing_date = row.get('filing_date')
        registration_date = row.get('registration_date')

        # Handle international classes (comes as array from PostgreSQL)
        classes = row.get('international_classes', [])
        if isinstance(classes, str):
            # Handle string format if needed
            classes = [c.strip() for c in classes.strip('{}').split(',') if c.strip()]

        return Trademark(
            serial_number=row.get('serial_number', ''),
            registration_number=row.get('registration_number'),
            mark_text=row.get('mark_text', ''),
            owner_name=row.get('owner_name') or 'Unknown',
            status=status,
            filing_date=filing_date,
            registration_date=registration_date,
            international_classes=classes,
            goods_services_description=row.get('goods_services')
        )

    def _parse_status_string(self, status_str: str) -> TrademarkStatus:
        """Map status string to TrademarkStatus enum"""
        status_map = {
            "REGISTERED": TrademarkStatus.REGISTERED,
            "REG": TrademarkStatus.REGISTERED,
            "LIVE": TrademarkStatus.REGISTERED,
            "PENDING": TrademarkStatus.PENDING,
            "PUB": TrademarkStatus.PENDING,
            "PUBLISHED": TrademarkStatus.PENDING,
            "ABANDONED": TrademarkStatus.ABANDONED,
            "DEAD": TrademarkStatus.ABANDONED,
            "CANCELLED": TrademarkStatus.CANCELLED,
            "CANCELED": TrademarkStatus.CANCELLED,
            "EXPIRED": TrademarkStatus.EXPIRED,
        }
        return status_map.get(status_str.upper(), TrademarkStatus.UNKNOWN)

    async def get_trademark_by_serial(self, serial_number: str) -> Optional[Trademark]:
        """
        Get detailed trademark information by serial number

        First tries database, then falls back to TSDR API if needed

        Args:
            serial_number: USPTO serial number

        Returns:
            Trademark object or None
        """
        # Try database first (fastest)
        db_result = self.db_client.get_trademark_by_serial(serial_number)
        if db_result:
            return self._db_row_to_trademark(db_result)

        # Fall back to TSDR API if not in database
        print(f"Trademark {serial_number} not in database, trying TSDR API...")
        return await self._fetch_from_tsdr(serial_number)

    async def _fetch_from_tsdr(self, serial_number: str) -> Optional[Trademark]:
        """Fetch trademark from TSDR API"""
        url = f"{self.tsdr_url}/sn{serial_number}/info.xml"

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                trademark = self._parse_tsdr_xml(response.text)
                return trademark
            except httpx.HTTPStatusError as e:
                print(f"HTTP error getting trademark {serial_number}: {e}")
                return None
            except Exception as e:
                print(f"Error getting trademark {serial_number}: {e}")
                return None

    def _parse_tsdr_xml(self, xml_content: str) -> Optional[Trademark]:
        """Parse TSDR XML response into Trademark model"""
        try:
            root = ET.fromstring(xml_content)

            # Define XML namespaces used by USPTO TSDR API
            ns = {
                'ns1': 'http://www.wipo.int/standards/XMLSchema/ST96/Common',
                'ns2': 'http://www.wipo.int/standards/XMLSchema/ST96/Trademark'
            }

            # Extract trademark data from XML
            trademark_data = {
                "serial_number": self._get_xml_text(root, ".//ns1:ApplicationNumberText", ns),
                "registration_number": self._get_xml_text(root, ".//ns1:RegistrationNumber", ns),
                "mark_text": self._get_xml_text(root, ".//ns2:MarkVerbalElementText", ns),
                "owner_name": self._get_xml_text(root, ".//ns1:OrganizationStandardName", ns) or "Unknown",
                "status": self._parse_status(self._get_xml_text(root, ".//ns2:MarkCurrentStatusCode", ns)),
                "filing_date": self._parse_date(self._get_xml_text(root, ".//ns2:ApplicationDate", ns)),
                "registration_date": self._parse_date(self._get_xml_text(root, ".//ns1:RegistrationDate", ns)),
                "international_classes": self._get_classes(root, ns),
                "goods_services_description": self._get_xml_text(root, ".//ns2:GoodsServicesDescriptionText", ns),
            }

            return Trademark(**trademark_data)

        except Exception as e:
            print(f"Error parsing TSDR XML: {e}")
            return None

    def _get_xml_text(self, root: ET.Element, path: str, namespaces: dict = None) -> Optional[str]:
        """Safely get text from XML element"""
        element = root.find(path, namespaces=namespaces)
        return element.text if element is not None else None

    def _get_classes(self, root: ET.Element, namespaces: dict = None) -> List[str]:
        """Extract international classification codes (Nice Classification)"""
        classes = []
        for class_elem in root.findall(".//ns2:GoodsServicesClassification", namespaces=namespaces):
            kind_code = class_elem.find(".//ns2:ClassificationKindCode", namespaces=namespaces)
            if kind_code is not None and kind_code.text == "Nice":
                class_num = class_elem.find(".//ns2:ClassNumber", namespaces=namespaces)
                if class_num is not None and class_num.text:
                    classes.append(class_num.text.zfill(3))  # Pad to 3 digits
        return classes

    def _parse_status(self, status_code: Optional[str]) -> TrademarkStatus:
        """Map USPTO status code to TrademarkStatus enum"""
        if not status_code:
            return TrademarkStatus.UNKNOWN

        status_map = {
            "REGISTERED": TrademarkStatus.REGISTERED,
            "NEW APPLICATION FILED": TrademarkStatus.PENDING,
            "ABANDONED": TrademarkStatus.ABANDONED,
            "CANCELLED": TrademarkStatus.CANCELLED,
            "EXPIRED": TrademarkStatus.EXPIRED,
        }

        return status_map.get(status_code.upper(), TrademarkStatus.UNKNOWN)

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string to datetime"""
        if not date_str:
            return None

        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            return None
