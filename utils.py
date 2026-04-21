def get_k4_max(info: dict) -> float:
    return max(info["к4"].values())


def calculate_kb(info, ukr, math, history, choice_subject, choice_score):
    k1 = info["к1"]
    k2 = info["к2"]
    k3 = info["к3"]
    k4 = info["к4"][choice_subject]
    k4_max = get_k4_max(info)
    gk = info.get("гк", 1.0)

    numerator = k1 * ukr + k2 * math + k3 * history + k4 * choice_score
    denominator = k1 + k2 + k3 + (k4_max + k4) / 2

    kb_base = numerator / denominator
    kb_final = min(kb_base * gk, 200)

    return {
        "kb_base": round(kb_base, 3),
        "kb_final": round(kb_final, 3),
        "k1": k1,
        "k2": k2,
        "k3": k3,
        "k4": k4,
        "k4_max": k4_max,
        "denominator": round(denominator, 3),
        "gk": gk,
    }


def is_valid_score(text: str) -> bool:
    return text.isdigit() and 100 <= int(text) <= 200

