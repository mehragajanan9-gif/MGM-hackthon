def classify_complaint(text):

    text = text.lower().strip()


    # ==========================
    # FIRE EMERGENCY
    # ==========================
    if any(word in text for word in [
        "fire",
        "burn",
        "burning",
        "smoke",
        "explosion"
    ]):

        return (
            "fire",
            "critical",
            "Fire Department",
            "AI detected a possible fire emergency requiring immediate attention.",
            True
        )


    # ==========================
    # ACCIDENT / MEDICAL EMERGENCY
    # ==========================
    elif any(word in text for word in [
        "accident",
        "injury",
        "injured",
        "ambulance",
        "medical emergency",
        "unconscious"
    ]):

        return (
            "health",
            "critical",
            "Emergency Medical Services",
            "AI detected a possible medical or accident emergency.",
            True
        )


    # ==========================
    # VIOLENCE / SECURITY EMERGENCY
    # ==========================
    elif any(word in text for word in [
        "violence",
        "attack",
        "fight",
        "assault",
        "crime",
        "danger",
        "threat"
    ]):

        return (
            "other",
            "critical",
            "Police Department",
            "AI detected a possible public safety emergency.",
            True
        )


    # ==========================
    # WATER / FLOOD
    # ==========================
    elif any(word in text for word in [
        "water",
        "flood",
        "flooding",
        "waterlogging",
        "drainage",
        "pipeline",
        "leakage"
    ]):

        return (
            "water",
            "high",
            "Water Supply Department",
            "AI detected a water supply, flooding, or drainage-related issue.",
            False
        )


    # ==========================
    # ROAD / INFRASTRUCTURE
    # ==========================
    elif any(word in text for word in [
        "road",
        "pothole",
        "street",
        "bridge",
        "footpath",
        "damaged road"
    ]):

        return (
            "road",
            "medium",
            "Public Works Department",
            "AI detected a road or infrastructure-related issue.",
            False
        )


    # ==========================
    # ELECTRICITY
    # ==========================
    elif any(word in text for word in [
        "electricity",
        "electric",
        "power",
        "electric pole",
        "wire",
        "short circuit",
        "transformer"
    ]):

        return (
            "electricity",
            "high",
            "Electricity Department",
            "AI detected an electricity-related issue.",
            False
        )


    # ==========================
    # WASTE MANAGEMENT
    # ==========================
    elif any(word in text for word in [
        "garbage",
        "waste",
        "trash",
        "dirty",
        "cleaning",
        "sewage",
        "dump"
    ]):

        return (
            "waste",
            "medium",
            "Waste Management Department",
            "AI detected a sanitation or waste-management issue.",
            False
        )


    # ==========================
    # HEALTHCARE
    # ==========================
    elif any(word in text for word in [
        "hospital",
        "doctor",
        "health",
        "disease",
        "medicine",
        "healthcare"
    ]):

        return (
            "health",
            "high",
            "Healthcare Department",
            "AI detected a healthcare-related public issue.",
            False
        )


    # ==========================
    # DEFAULT
    # ==========================
    else:

        return (
            "other",
            "medium",
            "General Administration Department",
            "AI could not determine a specific category. The complaint has been assigned for general review.",
            False
        )