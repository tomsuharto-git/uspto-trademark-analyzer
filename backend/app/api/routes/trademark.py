"""
Trademark detail API routes
"""
from fastapi import APIRouter, HTTPException
from app.models.trademark import Trademark
from app.services.db_client import PostgreSQLClient

router = APIRouter()


@router.get("/{serial_number}", response_model=Trademark)
async def get_trademark_details(serial_number: str):
    """
    Get complete trademark details by serial number

    Fetches full trademark information from PostgreSQL database including:
    - Owner name
    - Status and dates
    - International classes
    - Goods/services description
    - Attorney info
    - Correspondence address

    Args:
        serial_number: USPTO trademark serial number (e.g., "88234567")

    Returns:
        Trademark: Complete trademark details

    Raises:
        404: Trademark not found
        500: Error fetching trademark data
    """
    try:
        db_client = PostgreSQLClient()
        db_client.connect()
        trademark = db_client.get_trademark_by_serial(serial_number)

        if not trademark:
            raise HTTPException(
                status_code=404,
                detail=f"Trademark with serial number {serial_number} not found"
            )

        return trademark

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching trademark details: {str(e)}"
        )
