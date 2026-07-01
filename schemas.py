from pydantic import BaseModel, Field
from typing import List

class MarketingSEOOutput(BaseModel):
    title: str = Field(description="SEO optimized title, maximum 140 characters.")
    tags: List[str] = Field(description="List of exactly 13 unique tags, each under 20 characters.")
    initial_description: str = Field(description="A comprehensive product description including features.")
    taxonomy_id: int = Field(description="Etsy Taxonomy ID. Choose the best match based on image/text: 165 for Keychains, 6764 for Dangle & Drop Earrings, 1217 for Necklaces.")

class CriticOutput(BaseModel):
    approved: bool = Field(description="True if title, tags, and description meet all Etsy rules. False otherwise.")
    feedback: str = Field(description="Detailed feedback if rejected, or 'Looks perfect' if approved.")
    corrected_tags: List[str] = Field(description="The list of 13 tags after validation/correction.")

class FinalListingOutput(BaseModel):
    title: str = Field(description="The final, approved Etsy title.")
    tags: List[str] = Field(description="The final list of 13 approved tags.")
    description: str = Field(description="The final polished description formatted with clean line breaks, no HTML.")
    taxonomy_id: int = Field(description="The final approved Etsy Taxonomy ID as an integer: 165 (Keychains), 6764 (Dangle Earrings), or 1217 (Necklaces).")

