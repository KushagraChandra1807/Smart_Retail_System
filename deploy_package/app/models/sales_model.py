from pydantic import BaseModel

class SalesData(BaseModel):
    product_id: str
    date: str
    units_sold: int
    revenue: float
    store_location: str