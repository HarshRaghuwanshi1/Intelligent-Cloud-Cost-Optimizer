from src.discovery.ec2_discovery import EC2Discovery
from src.intelligence.tag_normalizer import TagNormalizer
from src.intelligence.cost_analyzer import CostAnalyzer
from src.decision_engine.decision_engine import DecisionEngine
from src.intelligence.recommendation_engine import RecommendationEngine


def main():
    discovery = EC2Discovery()
    normalizer = TagNormalizer()
    cost_analyzer = CostAnalyzer()
    decision_engine = DecisionEngine()
    recommender = RecommendationEngine()

    instances = discovery.discover_instances()

    print(f"\nDiscovered {len(instances)} EC2 instances\n")

    for inst in instances:
        normalized = normalizer.normalize(inst)
        cost = cost_analyzer.analyze(inst)
        decision = decision_engine.decide(normalized, cost)
        recommendation = recommender.generate(decision, inst)

        print({
            **normalized,
            **cost,
            **decision,
            **recommendation
        })


if __name__ == "__main__":
    main()


