import boto3
from typing import Dict


class EC2ActionEngine:
    def __init__(self, dry_run: bool = True, region_name: str = None):
        self.ec2 = boto3.client("ec2", region_name=region_name)
        self.dry_run = dry_run

    def stop_instance(self, decision: Dict) -> Dict:
        instance_id = decision["instance_id"]

        if not decision.get("action_allowed", False):
            return {
                "instance_id": instance_id,
                "action": "SKIPPED",
                "reason": "action not allowed by policy"
            }

        if self.dry_run:
            return {
                "instance_id": instance_id,
                "action": "DRY_RUN",
                "reason": "dry-run mode enabled"
            }

        self.ec2.stop_instances(InstanceIds=[instance_id])

        return {
            "instance_id": instance_id,
            "action": "STOPPED",
            "reason": "instance stopped by policy engine"
        }
