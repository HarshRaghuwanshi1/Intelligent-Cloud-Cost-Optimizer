from src.discovery.ec2_discovery import EC2Discovery
from src.intelligence.tag_normalizer import TagNormalizer
from src.intelligence.cost_analyzer import CostAnalyzer
from src.decision_engine.decision_engine import DecisionEngine
from src.intelligence.recommendation_engine import RecommendationEngine
from src.intelligence.report_generator import ReportGenerator
from src.actions.ec2_actions import EC2ActionEngine

# Simulation imports
from src.intelligence.simulation import SIMULATION_MODE, SIMULATED_INSTANCES


def main():
    # Initialize components
    discovery = EC2Discovery()
    normalizer = TagNormalizer()
    cost_analyzer = CostAnalyzer()
    decision_engine = DecisionEngine()
    recommender = RecommendationEngine()
    reporter = ReportGenerator()

    # Always dry-run by default
    action_engine = EC2ActionEngine(dry_run=True)

    # Discover real EC2 instances
    instances = discovery.discover_instances()

    # Inject simulated instances ONLY in demo mode
    if SIMULATION_MODE:
        for sim_instance in SIMULATED_INSTANCES.values():
            instances.append(sim_instance)

    results = []

    # Core processing loop
    for inst in instances:
        normalized = normalizer.normalize(inst)
        cost = cost_analyzer.analyze(inst)
        decision = decision_engine.decide(normalized, cost)
        recommendation = recommender.generate(decision, inst)
        action = action_engine.stop_instance(decision)

        results.append({
            **inst,              # raw instance data
            **normalized,
            **cost,
            **decision,
            **recommendation,
            **action,
        })

    # Generate report
    report = reporter.generate(results)

    # Print report
    print("\n==== COST OPTIMIZATION REPORT ====\n")
    print("SUMMARY:")
    print(report["summary"])
    print("\nDETAILS:")
    for item in report["details"]:
        print(item)


if __name__ == "__main__":
    main()








