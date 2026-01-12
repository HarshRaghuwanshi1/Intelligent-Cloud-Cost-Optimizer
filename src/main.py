from src.discovery.ec2_discovery import EC2Discovery
from src.intelligence.tag_normalizer import TagNormalizer


def main():
    discovery = EC2Discovery()
    normalizer = TagNormalizer()

    instances = discovery.discover_instances()

    print(f"\nDiscovered {len(instances)} EC2 instances\n")

    for inst in instances:
        normalized = normalizer.normalize(inst)
        print(normalized)


if __name__ == "__main__":
    main()

