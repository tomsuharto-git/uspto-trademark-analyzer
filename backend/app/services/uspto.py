"""
USPTO API Client - Uses RapidAPI for real-time trademark searches
"""
import httpx
from typing import List, Optional
import xml.etree.ElementTree as ET
from datetime import datetime

from app.config import settings
from app.models.trademark import Trademark, TrademarkStatus


class USPTOClient:
    """Client for USPTO Trademark Database via RapidAPI"""

    def __init__(self):
        # RapidAPI credentials for trademark search
        self.rapidapi_key = settings.RAPIDAPI_KEY
        self.rapidapi_host = settings.RAPIDAPI_HOST
        self.rapidapi_headers = {
            "X-RapidAPI-Key": self.rapidapi_key,
            "X-RapidAPI-Host": self.rapidapi_host
        }

        # TSDR API for detailed trademark lookups
        self.tsdr_api_key = settings.USPTO_API_KEY
        self.tsdr_url = settings.USPTO_TSDR_URL
        self.tsdr_headers = {
            "USPTO-API-KEY": self.tsdr_api_key,
            "Accept": "application/json"
        }

    async def search_trademarks(self, query: str, limit: int = 50) -> List[Trademark]:
        """
        Search for trademarks using RapidAPI

        Args:
            query: Search term (trademark name)
            limit: Maximum number of results

        Returns:
            List of Trademark objects
        """
        print(f"\n🔍 RapidAPI search for '{query}' (limit: {limit})")

        url = f"https://{self.rapidapi_host}/v1/trademarkSearch/{query}"
        params = {"searchKeyword": query}

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(
                    url,
                    headers=self.rapidapi_headers,
                    params=params
                )
                response.raise_for_status()
                data = response.json()

                if not data or "items" not in data:
                    print(f"   No results found")
                    return []

                # Parse results
                trademarks = []
                items = data["items"][:limit]  # Limit results

                print(f"   Found {len(items)} results from RapidAPI")

                for item in items:
                    trademark = self._parse_rapidapi_result(item)
                    if trademark:
                        trademarks.append(trademark)

                print(f"✅ Parsed {len(trademarks)} valid trademarks")
                return trademarks

            except httpx.HTTPStatusError as e:
                print(f"❌ HTTP error searching RapidAPI: {e}")
                print(f"   Response: {e.response.text if hasattr(e, 'response') else 'N/A'}")
                return []
            except Exception as e:
                print(f"❌ Error searching RapidAPI: {e}")
                return []

    def _parse_rapidapi_result(self, item: dict) -> Optional[Trademark]:
        """Parse RapidAPI search result into Trademark model"""
        try:
            # Extract fields from RapidAPI response
            serial_number = item.get("serialNumber", "")
            registration_number = item.get("registrationNumber")
            mark_text = item.get("markIdentification", "")
            owner_name = item.get("ownerName", "Unknown")

            # Parse status
            status_text = item.get("status", "")
            status = self._parse_status_string(status_text)

            # Parse dates
            filing_date = self._parse_date(item.get("filingDate"))
            registration_date = self._parse_date(item.get("registrationDate"))

            # Parse international classes
            classes_raw = item.get("internationalClasses", [])
            classes = []
            if isinstance(classes_raw, list):
                classes = [str(c).zfill(3) for c in classes_raw if c]
            elif isinstance(classes_raw, str):
                classes = [c.strip().zfill(3) for c in classes_raw.split(",") if c.strip()]

            # Goods/services description
            goods_services = item.get("goodsAndServices")

            return Trademark(
                serial_number=serial_number,
                registration_number=registration_number,
                mark_text=mark_text,
                owner_name=owner_name,
                status=status,
                filing_date=filing_date,
                registration_date=registration_date,
                international_classes=classes,
                goods_services_description=goods_services
            )

        except Exception as e:
            print(f"Error parsing RapidAPI result: {e}")
            return None

    def _parse_status_string(self, status_str: str) -> TrademarkStatus:
        """Map status string to TrademarkStatus enum"""
        if not status_str:
            return TrademarkStatus.UNKNOWN

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
        Get detailed trademark information by serial number using TSDR API

        Args:
            serial_number: USPTO serial number

        Returns:
            Trademark object or None
        """
        print(f"📡 Fetching trademark {serial_number} from TSDR API...")
        return await self._fetch_from_tsdr(serial_number)

    async def _fetch_from_tsdr(self, serial_number: str) -> Optional[Trademark]:
        """Fetch trademark from TSDR API"""
        url = f"{self.tsdr_url}/sn{serial_number}/info.xml"

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url, headers=self.tsdr_headers)
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
            # Try multiple date formats
            for fmt in ["%Y-%m-%d", "%Y%m%d", "%m/%d/%Y"]:
                try:
                    return datetime.strptime(date_str, fmt).date()
                except ValueError:
                    continue
            return None
        except:
            return None
