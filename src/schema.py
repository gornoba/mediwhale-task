from pydantic import AnyUrl, BaseModel, Field

class URLModel(BaseModel):
    url: AnyUrl = Field(..., example="https://example.com")
