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
    day = str(date.get("day")); month = str(date.get("month")); year = str(date.get("year"))
    if day and month: result.append(day)
    if month and year: result.append(month)
    if year: result.append(year)
    return '/'.join(result)

