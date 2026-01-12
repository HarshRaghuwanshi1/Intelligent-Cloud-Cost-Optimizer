import boto3
from typing import List, Dict


class EC2Discovery:
    def __init__(self, region_name: str = None):
        self.ec2_client = boto3.client("ec2", region_name=region_name)

    def discover_instances(self) -> List[Dict]:
        """
        Discover all EC2 instances and return
        normalized metadata for cost analysis.
        """
        instances = []
        paginator = self.ec2_client.get_paginator("describe_instances")

        for page in paginator.paginate():
            for reservation in page.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    instances.append(self._extract_instance(instance))

        return instances

    def _extract_instance(self, instance: Dict) -> Dict:
        tags = {t["Key"]: t["Value"] for t in instance.get("Tags", [])}

        return {
            "instance_id": instance["InstanceId"],
            "instance_type": instance["InstanceType"],
            "state": instance["State"]["Name"],
            "launch_time": instance["LaunchTime"].isoformat(),
            "availability_zone": instance["Placement"]["AvailabilityZone"],
            "tags": tags
        }
