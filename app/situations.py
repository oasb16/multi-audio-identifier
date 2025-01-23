def situation_description(situation):
    descriptions = {
        "party": "Loud music and people talking.",
        "emergency": "Sirens and urgent noises.",
        "workplace": "Office chatter and keyboard typing.",
        "quiet": "Minimal or no sounds detected."
    }
    return descriptions.get(situation, "Unknown situation.")
