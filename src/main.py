from src.discovery.ec2_discovery import EC2Discovery
from src.intelligence.tag_normalizer import TagNormalizer
from src.intelligence.cost_analyzer import CostAnalyzer
from src.decision_engine.decision_engine import DecisionEngine
from src.intelligence.recommendation_engine import RecommendationEngine
from src.intelligence.report_generator import ReportGenerator
from src.actions.ec2_actions import EC2ActionEngine
from src.intelligence.simulation import SIMULATION_MODE, SIMULATED_INSTANCES


def main():
    discovery = EC2Discovery()
    normalizer = TagNormalizer()
    cost_analyzer = CostAnalyzer()
    decision_engine = DecisionEngine()
    recommender = RecommendationEngine()
    reporter = ReportGenerator()

    # DRY RUN MODE
    action_engine = EC2ActionEngine(dry_run=True)

    instances = discovery.discover_instances()
    results = []

    for inst in instances:
      if SIMULATION_MODE:
       sim = SIMULATED_INSTANCES.get(inst["instance_id"])
        if sim:
           inst.update(sim)

        normalized = normalizer.normalize(inst)
        cost = cost_analyzer.analyze(inst)
        decision = decision_engine.decide(normalized, cost)
        recommendation = recommender.generate(decision, inst)
        action = action_engine.stop_instance(decision)

        results.append({
            **inst,
            **normalized,
            **cost,
            **decision,
            **recommendation,
            **action
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








