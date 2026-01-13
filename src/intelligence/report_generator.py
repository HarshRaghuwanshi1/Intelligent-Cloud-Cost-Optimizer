from typing import List, Dict


class ReportGenerator:
    PRICING = {
        "t3.micro": 7.49,
        "t3.small": 14.98,
    }

    def generate(self, results: List[Dict]) -> Dict:
        enriched = []

        totals = {
            "instances_analyzed": len(results),
            "provisioned_monthly_cost_usd": 0.0,
            "actual_monthly_cost_usd": 0.0,
            "wasted_monthly_cost_usd": 0.0,
        }

        for r in results:
            instance_type = r.get("instance_type")
            monthly_cost = self.PRICING.get(instance_type, 0.0)

            state = r.get("state")
            is_idle = r.get("is_idle", False)

            # Cost calculations
            provisioned_cost = monthly_cost
            actual_cost = monthly_cost if state == "running" else 0.0
            wasted_cost = monthly_cost if (state == "running" and is_idle) else 0.0

            totals["provisioned_monthly_cost_usd"] += provisioned_cost
            totals["actual_monthly_cost_usd"] += actual_cost
            totals["wasted_monthly_cost_usd"] += wasted_cost

            enriched.append({
                "instance_id": r["instance_id"],
                "name": r.get("tags", {}).get("Name", "unknown"),
                "environment": r.get("environment"),
                "state": state,
                "avg_cpu_7d": f'{r.get("avg_cpu_7d", "N/A")}%',
                "network_7d_mb": r.get("network_mb_7d", "N/A"),
                "monthly_cost_if_running_usd": provisioned_cost,
                "actual_monthly_cost_usd": actual_cost,
                "wasted_monthly_cost_usd": wasted_cost,
                "recommendation": r.get("recommendation"),
                "reason": r.get("message", r.get("reason")),
                "risk": self._risk_label(r),
            })

        # Round totals
        for k in totals:
            if k != "instances_analyzed":
                totals[k] = round(totals[k], 2)

        # Sort by wasted cost (most important first)
        enriched.sort(
            key=lambda x: x["wasted_monthly_cost_usd"], reverse=True
        )

        return {
            "summary": totals,
            "details": enriched,
        }

    def _risk_label(self, r: Dict) -> str:
        if r.get("environment") == "prod":
            return "HIGH"
        if r.get("is_protected"):
            return "MEDIUM"
        return "LOW"

