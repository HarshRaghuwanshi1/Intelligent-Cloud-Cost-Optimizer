from typing import Dict


class RecommendationEngine:
    # Very rough on-demand pricing (can be improved later)
    INSTANCE_PRICING_USD = {
        "t3.micro": 0.0104,
        "t3.small": 0.0208,
    }

    def generate(self, decision: Dict, instance: Dict) -> Dict:
        decision_type = decision["decision"]

        if decision_type == "NO_ACTION":
            return {
                "instance_id": decision["instance_id"],
                "recommendation": "NO_ACTION",
                "message": "No action recommended",
                "estimated_monthly_savings_usd": 0.0
            }

        if decision_type == "RECOMMEND_STOP":
            savings = self._estimate_savings(instance)
            return {
                "instance_id": decision["instance_id"],
                "recommendation": "RECOMMEND_STOP",
                "message": "Instance appears idle. Enable AutoOptimize to allow auto-stop.",
                "estimated_monthly_savings_usd": savings
            }

        if decision_type == "ELIGIBLE_FOR_STOP":
            savings = self._estimate_savings(instance)
            return {
                "instance_id": decision["instance_id"],
                "recommendation": "AUTO_STOP_ELIGIBLE",
                "message": "Instance idle and eligible for automated stop (not executed).",
                "estimated_monthly_savings_usd": savings
            }

        return {
            "instance_id": decision["instance_id"],
            "recommendation": "UNKNOWN",
            "message": "Unhandled decision state",
            "estimated_monthly_savings_usd": 0.0
        }

    def _estimate_savings(self, instance: Dict) -> float:
        instance_type = instance.get("instance_type")
        hourly = self.INSTANCE_PRICING_USD.get(instance_type, 0.0)

        # Approx monthly hours
        return round(hourly * 24 * 30, 2)
