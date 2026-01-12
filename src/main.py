from src.discovery.ec2_discovery import EC2Discovery
from src.intelligence.tag_normalizer import TagNormalizer
from src.intelligence.cost_analyzer import CostAnalyzer


def main():
    discovery = EC2Discovery()
    normalizer = TagNormalizer()
    cost_analyzer = CostAnalyzer()

    instances = discovery.discover_instances()

    print(f"\nDiscovered {len(instances)} EC2 instances\n")

    for inst in instances:
        normalized = normalizer.normalize(inst)
        cost = cost_analyzer.analyze(inst)

        print({
            **normalized,
            **cost
        })


if __name__ == "__main__":
    main()


