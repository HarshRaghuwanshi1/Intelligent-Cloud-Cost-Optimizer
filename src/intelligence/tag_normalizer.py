from typing import Dict


class TagNormalizer:
    REQUIRED_TAGS = ["Environment", "AutoOptimize"]

    def normalize(self, instance: Dict) -> Dict:
        tags = instance.get("tags", {})

        environment = tags.get("Environment", "unknown").lower()
        auto_optimize = tags.get("AutoOptimize", "false").lower() == "true"

        # Safety logic
        is_protected = False
        reasons = []

        if environment == "unknown":
            is_protected = True
            reasons.append("missing Environment tag")

        if environment == "prod":
            is_protected = True
            reasons.append("production environment")

        if not auto_optimize:
            is_protected = True
            reasons.append("AutoOptimize not enabled")

        risk_level = "LOW"
        if is_protected and environment == "prod":
            risk_level = "HIGH"
        elif is_protected:
            risk_level = "MEDIUM"

        return {
            "instance_id": instance["instance_id"],
            "environment": environment,
            "auto_optimize": auto_optimize,
            "is_protected": is_protected,
            "risk_level": risk_level,
            "reason": ", ".join(reasons) if reasons else "safe to evaluate"
        }
