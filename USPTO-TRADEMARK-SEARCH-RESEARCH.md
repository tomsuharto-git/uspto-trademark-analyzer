# USPTO Trademark Search Tool - Research Findings

## Overview
Research on the USPTO trademark database APIs and existing tools for building a trademark search application.

## Official USPTO APIs

### 1. TSDR (Trademark Status & Document Retrieval) API
- **Primary API** for trademark status, documents, and images
- Requires API key registration at https://account.uspto.gov/api-manager/
- **Rate Limits:**
  - 60 requests per API key per minute (general)
  - 4 requests per API key per minute (PDF, ZIP, multi-case downloads)
- **Documentation:** [TSDR Data API](https://developer.uspto.gov/api-catalog/tsdr-data-api)
- **User Guide:** [PDF Guide](https://www.uspto.gov/sites/default/files/documents/tm-enterprise-api-user-guide-v2.pdf)

### 2. Trademark Assignment Search Data API
- Retrieves trademark assignment information
- Generates XML files with search results
- **Documentation:** [Trademark Assignment Search](https://developer.uspto.gov/api-catalog/trademark-assignment-search-data)

### 3. Open Data Portal
- Main data platform: https://developer.uspto.gov/
- API Catalog: https://developer.uspto.gov/api-catalog
- Bulk Data: https://www.uspto.gov/trademarks/apply/check-status-view-documents/trademark-bulk-data

## Recommended GitHub Repositories to Clone/Study

### Python Implementations

#### 1. **Plumage-py** ⭐ RECOMMENDED
- **Repo:** [codingatty/Plumage-py](https://github.com/codingatty/Plumage-py)
- **Language:** Python
- **Purpose:** Obtain trademark status information from USPTO's TSDR system
- **Status:** Mature, well-maintained
- **Why Clone:** Clean Python implementation, good starting point

#### 2. **TSDR2JSON**
- **Repo:** [codingatty/TSDR2JSON](https://github.com/codingatty/TSDR2JSON)
- **Language:** Python (Windows CLI)
- **Purpose:** Get trademark info in JSON format
- **Output:** Easy-to-parse JSON format
- **Why Clone:** Good for understanding TSDR response parsing

#### 3. **uspto-opendata-python**
- **Repo:** [ip-tools/uspto-opendata-python](https://github.com/ip-tools/uspto-opendata-python)
- **Language:** Python
- **Package:** Available on [PyPI](https://pypi.org/project/uspto-opendata-python/)
- **Documentation:** https://docs.ip-tools.org/uspto-opendata-python/
- **Purpose:** Client library for USPTO Open Data APIs
- **Note:** Primarily patent-focused, but shows API patterns
- **Why Clone:** Professional implementation, good architecture reference

### Other Language Implementations

#### 4. **USPTO-Trademark-API**
- **Repo:** [Ethan3600/USPTO-Trademark-API](https://github.com/Ethan3600/USPTO-Trademark-API)
- **Language:** PHP
- **Purpose:** Grabs status data from TSDR system
- **Why Study:** Different language approach, API integration patterns

#### 5. **trademark-marker**
- **Repo:** [null-none/trademark-marker](https://github.com/null-none/trademark-marker)
- **Language:** Python
- **Purpose:** Trademark search API wrapper
- **Features:** Simple search interface
- **Why Study:** Simplified API abstraction

#### 6. **uspto-crawler-mcp** 🆕
- **Repo:** [YobieBen/uspto-crawler-mcp](https://github.com/YobieBen/uspto-crawler-mcp)
- **Purpose:** USPTO Patent & Trademark Web Crawler
- **Features:** Real-time application status via PAIR and TSDR
- **Why Study:** Modern approach with web crawling + API

### Data Analysis Tools

#### 7. **uspto (jlroo/uspto)**
- **Repo:** [jlroo/uspto](https://github.com/jlroo/uspto)
- **Purpose:** Parse and analyze trademark data from USPTO
- **Features:** Handles bulk XML data
- **Why Clone:** Good for bulk data processing

## Key Technical Considerations

### Authentication
- API key required for TSDR APIs
- Register at https://account.uspto.gov/api-manager/

### Rate Limits
- **Standard:** 60 requests/minute per API key
- **Downloads:** 4 requests/minute for PDFs/ZIPs
- Plan for throttling/queuing in your implementation

### Data Formats
- **TSDR API:** XML responses (most repos convert to JSON)
- **Bulk Data:** Large XML files available for download
- Consider caching and local database for performance

## Recommended Approach

### Option 1: Python Web Application (RECOMMENDED)
**Stack:**
- Backend: Python + Flask/FastAPI
- TSDR Integration: Fork/adapt **Plumage-py**
- Frontend: React/Next.js with clean search interface
- Database: PostgreSQL for caching results

**Why:**
- Plumage-py is mature and well-tested
- Python ecosystem has good USPTO tools
- Easy to extend and customize

### Option 2: Modern Full-Stack
**Stack:**
- Clone **uspto-crawler-mcp** as starting point
- Extend with custom search UI
- Add features like:
  - Saved searches
  - Alerts for trademark status changes
  - Bulk search capabilities

### Option 3: Simple Search Tool
**Stack:**
- Fork **TSDR2JSON** for backend
- Build lightweight web UI
- Focus on single trademark lookups
- Quick to deploy

## Next Steps

1. **Clone Plumage-py** - Best starting point for Python
   ```bash
   git clone https://github.com/codingatty/Plumage-py.git
   ```

2. **Clone TSDR2JSON** - Study JSON conversion
   ```bash
   git clone https://github.com/codingatty/TSDR2JSON.git
   ```

3. **Register for API Key**
   - Visit https://account.uspto.gov/api-manager/
   - Get credentials for testing

4. **Review Official Docs**
   - Read [TSDR User Guide PDF](https://www.uspto.gov/sites/default/files/documents/tm-enterprise-api-user-guide-v2.pdf)
   - Study API endpoints and parameters

5. **Prototype**
   - Start with simple serial number lookup
   - Test rate limits
   - Build search interface
   - Add caching layer

## Additional Resources

- [USPTO Developer Portal](https://developer.uspto.gov/)
- [Bulk Data Downloads](https://www.uspto.gov/trademarks/apply/check-status-view-documents/trademark-bulk-data)
- [Postman Collection](https://www.postman.com/api-evangelist/united-states-patent-and-trademark-office-uspto/documentation/37kbms4/uspto-data-set-api)

## Sources

- [USPTO API Catalog](https://developer.uspto.gov/api-catalog)
- [TSDR Data API](https://developer.uspto.gov/api-catalog/tsdr-data-api)
- [Plumage-py GitHub](https://github.com/codingatty/Plumage-py)
- [TSDR2JSON GitHub](https://github.com/codingatty/TSDR2JSON)
- [uspto-opendata-python](https://github.com/ip-tools/uspto-opendata-python)
- [trademark-marker GitHub](https://github.com/null-none/trademark-marker)
- [USPTO-Trademark-API GitHub](https://github.com/Ethan3600/USPTO-Trademark-API)
- [uspto-crawler-mcp GitHub](https://github.com/YobieBen/uspto-crawler-mcp)
