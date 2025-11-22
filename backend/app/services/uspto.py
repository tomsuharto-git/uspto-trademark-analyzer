"""
USPTO API Client - Interfaces with the USPTO Open Data Portal
"""
import httpx
from typing import List, Optional
import xml.etree.ElementTree as ET
from datetime import datetime

from app.config import settings
from app.models.trademark import Trademark, TrademarkStatus


class USPTOClient:
    """Client for USPTO Trademark APIs"""

    def __init__(self):
        self.api_key = settings.USPTO_API_KEY
        self.base_url = settings.USPTO_BASE_URL
        self.tsdr_url = settings.USPTO_TSDR_URL
        self.headers = {
            "api_key": self.api_key,
            "Accept": "application/json"
        }

    async def search_trademarks(self, query: str, limit: int = 50) -> List[Trademark]:
        """
        Search for trademarks by text query

        Args:
            query: Search term (trademark name, keyword)
            limit: Maximum number of results

        Returns:
            List of Trademark objects
        """
        # For MVP, we'll use the TSDR API with serial number lookups
        # In production, integrate with the full-text search API

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                # This is a simplified implementation
                # Real implementation would use the search API endpoint
                results = await self._mock_search(query, limit)
                return results
            except Exception as e:
                print(f"Error searching trademarks: {e}")
                return []

    async def get_trademark_by_serial(self, serial_number: str) -> Optional[Trademark]:
        """
        Get detailed trademark information by serial number using TSDR API

        Args:
            serial_number: USPTO serial number

        Returns:
            Trademark object or None
        """
        url = f"{self.tsdr_url}/{serial_number}"

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(
                    url,
                    headers=self.headers
                )
                response.raise_for_status()

                # Parse XML response
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

            # Extract trademark data from XML
            # This is a simplified parser - real implementation needs full XML parsing
            trademark_data = {
                "serial_number": self._get_xml_text(root, ".//SerialNumber"),
                "registration_number": self._get_xml_text(root, ".//RegistrationNumber"),
                "mark_text": self._get_xml_text(root, ".//MarkVerbalElementText"),
                "owner_name": self._get_xml_text(root, ".//ApplicantName"),
                "status": self._parse_status(self._get_xml_text(root, ".//MarkCurrentStatusCode")),
                "filing_date": self._parse_date(self._get_xml_text(root, ".//ApplicationDate")),
                "registration_date": self._parse_date(self._get_xml_text(root, ".//RegistrationDate")),
                "international_classes": self._get_classes(root),
                "goods_services_description": self._get_xml_text(root, ".//GoodsServicesDescription"),
            }

            return Trademark(**trademark_data)

        except Exception as e:
            print(f"Error parsing TSDR XML: {e}")
            return None

    def _get_xml_text(self, root: ET.Element, path: str) -> Optional[str]:
        """Safely get text from XML element"""
        element = root.find(path)
        return element.text if element is not None else None

    def _get_classes(self, root: ET.Element) -> List[str]:
        """Extract international classification codes"""
        classes = []
        for class_elem in root.findall(".//ClassNumber"):
            if class_elem.text:
                classes.append(class_elem.text.zfill(3))  # Pad to 3 digits
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

    async def _mock_search(self, query: str, limit: int) -> List[Trademark]:
        """
        Mock search for development/testing
        TODO: Replace with actual USPTO search API integration
        """
        # Return mock data for testing
        mock_trademarks = [
            Trademark(
                serial_number="88234567",
                registration_number="5678901",
                mark_text=f"{query.upper()} BRAND",
                owner_name="Example Corporation",
                status=TrademarkStatus.REGISTERED,
                filing_date=datetime(2020, 1, 15).date(),
                registration_date=datetime(2021, 6, 30).date(),
                international_classes=["009", "035"],
                goods_services_description="Computer software and hardware"
            ),
            Trademark(
                serial_number="88234568",
                mark_text=f"{query.upper()} PRO",
                owner_name="Another Company LLC",
                status=TrademarkStatus.PENDING,
                filing_date=datetime(2023, 3, 10).date(),
                international_classes=["009"],
                goods_services_description="Mobile applications"
            ),
            Trademark(
                serial_number="88234569",
                mark_text=f"{query.upper()}TECH",
                owner_name="Tech Innovations Inc",
                status=TrademarkStatus.REGISTERED,
                filing_date=datetime(2019, 5, 20).date(),
                registration_date=datetime(2020, 11, 15).date(),
                international_classes=["042"],
                goods_services_description="Software development services"
            ),
        ]

        return mock_trademarks[:limit]
