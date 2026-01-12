from src.discovery.ec2_discovery import EC2Discovery
from src.intelligence.tag_normalizer import TagNormalizer
from src.intelligence.cost_analyzer import CostAnalyzer
from src.decision_engine.decision_engine import DecisionEngine
from src.intelligence.recommendation_engine import RecommendationEngine
from src.intelligence.report_generator import ReportGenerator


def main():
    discovery = EC2Discovery()
    normalizer = TagNormalizer()
    cost_analyzer = CostAnalyzer()
    decision_engine = DecisionEngine()
    recommender = RecommendationEngine()
    reporter = ReportGenerator()

    instances = discovery.discover_instances()
    results = []

    for inst in instances:
        normalized = normalizer.normalize(inst)
        cost = cost_analyzer.analyze(inst)
        decision = decision_engine.decide(normalized, cost)
        recommendation = recommender.generate(decision, inst)

        results.append({
            **normalized,
            **cost,
            **decision,
            **recommendation
        })

    report = reporter.generate(results)

    print("\n==== COST OPTIMIZATION REPORT ====\n")
    print("SUMMARY:")
    print(report["summary"])
    print("\nDETAILS:")
    for d in report["details"]:
        print(d)


if __name__ == "__main__":
    main()



