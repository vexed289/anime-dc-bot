def getTitle(media: dict) -> str:
    return (
            media["title"]["english"] or 
            media["title"]["romaji"] or 
            media["title"]["native"] or
            "Unknown Title"
            )

def formatDate(date: dict | None) -> str:
    if not date or not date.get("year"):
        return f"N/A"
    result = []
    day = date.get("day"); month = date.get("month"); year = date.get("year")
    if day and month: result.append(day)
    if month and year: result.append(month)
    if year: result.append(year)
    return '/'.join(result)
