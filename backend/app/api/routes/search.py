"""
Search API routes
"""
from fastapi import APIRouter, HTTPException
from typing import List

from app.models.trademark import SearchQuery, Trademark
from app.services.db_client import PostgreSQLClient

router = APIRouter()


@router.post("/", response_model=List[Trademark])
async def search_trademarks(query: SearchQuery):
    """
    Search USPTO trademark database

    Args:
        query: SearchQuery with search parameters

    Returns:
        List of matching trademarks
    """
    try:
        client = PostgreSQLClient()
        client.connect()
        results = client.search_trademarks(
            query=query.query,
            limit=query.limit
        )

        if not results:
            return []

        return results

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching trademarks: {str(e)}"
        )


@router.get("/{serial_number}", response_model=Trademark)
async def get_trademark(serial_number: str):
    """
    Get detailed trademark information by serial number

    Args:
        serial_number: USPTO serial number

    Returns:
        Trademark details
    """
    try:
        client = PostgreSQLClient()
        client.connect()
        trademark = client.get_trademark_by_serial(serial_number)

        if not trademark:
            raise HTTPException(
                status_code=404,
                detail=f"Trademark {serial_number} not found"
            )

        return trademark

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving trademark: {str(e)}"
        )
