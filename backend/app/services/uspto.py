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

        # RapidAPI configuration for trademark search
        self.rapidapi_key = settings.RAPIDAPI_KEY
        self.rapidapi_host = settings.RAPIDAPI_HOST
        self.rapidapi_url = f"https://{self.rapidapi_host}/v1"

        self.headers = {
            "api_key": self.api_key,
            "Accept": "application/json"
        }

        self.rapidapi_headers = {
            "x-rapidapi-key": self.rapidapi_key,
            "x-rapidapi-host": self.rapidapi_host
        }

    async def search_trademarks(self, query: str, limit: int = 50) -> List[Trademark]:
        """
        Search for trademarks by text query using RapidAPI

        Args:
            query: Search term (trademark name, keyword)
            limit: Maximum number of results

        Returns:
            List of Trademark objects
        """
        # Use RapidAPI USPTO Trademark Search
        url = f"{self.rapidapi_url}/trademarkSearch/{query}/active"

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(
                    url,
                    headers=self.rapidapi_headers
                )
                response.raise_for_status()

                data = response.json()

                # Parse RapidAPI response into Trademark objects
                trademarks = self._parse_rapidapi_response(data, limit)
                return trademarks

            except httpx.HTTPStatusError as e:
                print(f"HTTP error searching trademarks: {e}")
                print(f"Response: {e.response.text}")
                return []
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

    def _parse_rapidapi_response(self, data: dict, limit: int) -> List[Trademark]:
        """
        Parse RapidAPI response into Trademark objects

        RapidAPI returns data in format:
        {
            "count": 123,
            "items": [
                {
                    "keyword": "TRADEMARK NAME",
                    "serial_number": "87654321",
                    "registration_number": "5123456",
                    "status_code": "REG",
                    "status_label": "Live/Registered",
                    "filing_date": "2018-01-15",
                    "registration_date": "2019-06-20",
                    "owner": "Company Name",
                    "description": "Goods and services description",
                    "class_codes": "009,035"
                },
                ...
            ]
        }
        """
        trademarks = []

        try:
            items = data.get("items", [])

            for item in items[:limit]:
                # Parse status
                status = self._parse_rapidapi_status(item.get("status_code", ""))

                # Parse dates
                filing_date = self._parse_date(item.get("filing_date"))
                registration_date = self._parse_date(item.get("registration_date"))

                # Parse international classes
                class_codes = item.get("class_codes", "")
                classes = [c.strip().zfill(3) for c in class_codes.split(",") if c.strip()]

                trademark = Trademark(
                    serial_number=item.get("serial_number", ""),
                    registration_number=item.get("registration_number"),
                    mark_text=item.get("keyword", ""),
                    owner_name=item.get("owner", "Unknown"),
                    status=status,
                    filing_date=filing_date,
                    registration_date=registration_date,
                    international_classes=classes,
                    goods_services_description=item.get("description", "")
                )

                trademarks.append(trademark)

        except Exception as e:
            print(f"Error parsing RapidAPI response: {e}")

        return trademarks

    def _parse_rapidapi_status(self, status_code: str) -> TrademarkStatus:
        """Map RapidAPI status code to TrademarkStatus enum"""
        if not status_code:
            return TrademarkStatus.UNKNOWN

        status_map = {
            "REG": TrademarkStatus.REGISTERED,
            "REGISTERED": TrademarkStatus.REGISTERED,
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

        return status_map.get(status_code.upper(), TrademarkStatus.UNKNOWN)
