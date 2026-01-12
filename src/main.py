from src.discovery.ec2_discovery import EC2Discovery


def main():
    discovery = EC2Discovery()
    instances = discovery.discover_instances()

    print(f"\nDiscovered {len(instances)} EC2 instances\n")

    for instance in instances:
        print(instance)


if __name__ == "__main__":
    main()
