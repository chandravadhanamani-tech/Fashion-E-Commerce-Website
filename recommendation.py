from typing import Dict, Any, Optional

SIZES = ["XS", "S", "M", "L", "XL", "XXL"]

def calculate_size_recommendation(
    gender: str,
    height_cm: float,
    weight_kg: float,
    chest_cm: Optional[float] = None,
    waist_cm: Optional[float] = None,
    hip_cm: Optional[float] = None,
    category_name: Optional[str] = "Tops",
    fit_preference: Optional[str] = "regular"
) -> Dict[str, Any]:
    """
    Intelligent fashion size recommendation algorithm.
    Calculates estimated bodily proportions if missing, evaluates category specific metrics,
    applies fit preference adjustments, and produces a confidence score and breakdown.
    """
    gender_clean = (gender or "unisex").lower()
    cat_clean = (category_name or "Tops").lower()
    fit_pref = (fit_preference or "regular").lower()

    # Calculate BMI
    height_m = height_cm / 100.0
    bmi = weight_kg / (height_m * height_m)

    # Estimate missing body metrics if not supplied
    if gender_clean == "women":
        est_chest = chest_cm or (82 + (bmi - 21) * 2.8)
        est_waist = waist_cm or (64 + (bmi - 21) * 2.6)
        est_hip = hip_cm or (90 + (bmi - 21) * 3.0)
    else: # Men or Unisex
        est_chest = chest_cm or (90 + (bmi - 22.5) * 3.2)
        est_waist = waist_cm or (76 + (bmi - 22.5) * 3.0)
        est_hip = hip_cm or (94 + (bmi - 22.5) * 2.8)

    # Determine size index based on category and metrics
    if "bottom" in cat_clean or "pant" in cat_clean or "jean" in cat_clean:
        # Waist driven
        if est_waist < 68: size_idx = 0       # XS
        elif est_waist < 76: size_idx = 1     # S
        elif est_waist < 84: size_idx = 2     # M
        elif est_waist < 92: size_idx = 3     # L
        elif est_waist < 100: size_idx = 4    # XL
        else: size_idx = 5                   # XXL
    elif "dress" in cat_clean:
        # Hips & Chest driven
        ref_metric = (est_chest + est_hip) / 2.0
        if ref_metric < 85: size_idx = 0
        elif ref_metric < 92: size_idx = 1
        elif ref_metric < 99: size_idx = 2
        elif ref_metric < 107: size_idx = 3
        elif ref_metric < 115: size_idx = 4
        else: size_idx = 5
    else:
        # Tops / Outerwear - Chest driven
        if est_chest < 86: size_idx = 0       # XS
        elif est_chest < 94: size_idx = 1     # S
        elif est_chest < 102: size_idx = 2    # M
        elif est_chest < 110: size_idx = 3    # L
        elif est_chest < 118: size_idx = 4    # XL
        else: size_idx = 5                   # XXL

    # Adjust for fit preference
    if fit_pref == "tight" and size_idx > 0:
        size_idx -= 1
    elif fit_pref == "loose" and size_idx < len(SIZES) - 1:
        size_idx += 1

    recommended_size = SIZES[size_idx]

    # Calculate confidence percentage
    confidence = 94 if (chest_cm or waist_cm) else 86
    if 18.5 <= bmi <= 25:
        confidence += 4

    confidence = min(98, max(75, confidence))

    # Suggested alternative (adjacent size)
    alternative = None
    if size_idx > 0 and fit_pref == "loose":
        alternative = SIZES[size_idx - 1]
    elif size_idx < len(SIZES) - 1:
        alternative = SIZES[size_idx + 1]

    # Generate personalized summary text
    summary_notes = (
        f"Based on your height ({height_cm:.0f}cm), weight ({weight_kg:.0f}kg), "
        f"and estimated chest/waist measurements ({est_chest:.1f}cm / {est_waist:.1f}cm), "
        f"size '{recommended_size}' will offer an optimal {fit_pref} fit."
    )

    size_breakdown = {
        "calculated_bmi": round(bmi, 1),
        "estimated_chest_cm": round(est_chest, 1),
        "estimated_waist_cm": round(est_waist, 1),
        "estimated_hip_cm": round(est_hip, 1),
        "fit_preference": fit_pref,
        "primary_size": recommended_size,
        "alternative_size": alternative
    }

    return {
        "recommended_size": recommended_size,
        "confidence_percentage": confidence,
        "fit_summary": summary_notes,
        "size_breakdown": size_breakdown,
        "suggested_alternative": alternative
    }
