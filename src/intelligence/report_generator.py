from typing import List, Dict


class ReportGenerator:
    def generate(self, results: List[Dict]) -> Dict:
        summary = {
            "total_instances": len(results),
            "no_action": 0,
            "recommend_stop": 0,
            "auto_stop_eligible": 0,
            "total_potential_savings_usd": 0.0
        }

        detailed = []

        for r in results:
            rec = r.get("recommendation")

            if rec == "NO_ACTION":
                summary["no_action"] += 1
            elif rec == "RECOMMEND_STOP":
                summary["recommend_stop"] += 1
            elif rec == "AUTO_STOP_ELIGIBLE":
                summary["auto_stop_eligible"] += 1

            summary["total_potential_savings_usd"] += r.get(
                "estimated_monthly_savings_usd", 0.0
            )

            detailed.append({
                "instance_id": r["instance_id"],
                "recommendation": rec,
                "message": r.get("message"),
                "estimated_monthly_savings_usd": r.get(
                    "estimated_monthly_savings_usd", 0.0
                )
            })

        summary["total_potential_savings_usd"] = round(
            summary["total_potential_savings_usd"], 2
        )

        return {
            "summary": summary,
            "details": detailed
        }
