from typing import List, Dict


class ReportGenerator:
    def generate(self, results: List[Dict]) -> Dict:
        enriched = []
        total_cost = 0.0
        total_savings = 0.0

        for r in results:
            monthly_cost = self._estimate_monthly_cost(r)
            savings = r.get("estimated_monthly_savings_usd", 0.0)

            total_cost += monthly_cost
            total_savings += savings

            enriched.append({
                "instance_id": r["instance_id"],
                "name": r.get("tags", {}).get("Name", "unknown"),
                "environment": r.get("environment"),
                "state": r.get("state", "unknown"),
                "avg_cpu_7d": f'{r.get("avg_cpu_7d", "N/A")}%',
                "network_7d_mb": r.get("network_mb_7d", "N/A"),
                "monthly_cost_usd": round(monthly_cost, 2),
                "potential_savings_usd": savings,
                "recommendation": r.get("recommendation"),
                "reason": r.get("message", r.get("reason")),
                "risk": self._risk_label(r)
            })

        summary = {
            "instances_analyzed": len(results),
            "total_monthly_cost_usd": round(total_cost, 2),
            "total_potential_savings_usd": round(total_savings, 2),
            "safe_by_default": True
        }

        # Sort: savings first
        enriched.sort(key=lambda x: x["potential_savings_usd"], reverse=True)

        return {
            "summary": summary,
            "details": enriched
        }

    def _estimate_monthly_cost(self, r: Dict) -> float:
        pricing = {
            "t3.micro": 7.49,
            "t3.small": 14.98,
        }
        instance_type = r.get("instance_type")
        return pricing.get(instance_type, 0.0)

    def _risk_label(self, r: Dict) -> str:
        if r.get("environment") == "prod":
            return "HIGH"
        if r.get("is_protected"):
            return "MEDIUM"
        return "LOW"

