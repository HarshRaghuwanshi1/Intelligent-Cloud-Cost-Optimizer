import boto3
from datetime import datetime, timedelta
from typing import Dict


class CostAnalyzer:
    def __init__(self, region_name: str = None):
        self.cw = boto3.client("cloudwatch", region_name=region_name)

    def analyze(self, instance: Dict) -> Dict:
        if instance["state"] != "running":
            return {
                "instance_id": instance["instance_id"],
                "is_idle": False,
                "reason": "instance not running"
            }

        end = datetime.utcnow()
        start = end - timedelta(days=7)

        cpu = self._avg_cpu(instance["instance_id"], start, end)
        net = self._network_usage(instance["instance_id"], start, end)

        is_idle = cpu < 5 and net < 50

        return {
            "instance_id": instance["instance_id"],
            "avg_cpu_7d": round(cpu, 2),
            "network_mb_7d": round(net, 2),
            "is_idle": is_idle,
            "confidence": "HIGH" if is_idle else "LOW"
        }

    def _avg_cpu(self, instance_id: str, start, end) -> float:
        metrics = self.cw.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
            Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
            StartTime=start,
            EndTime=end,
            Period=86400,
            Statistics=["Average"],
        )

        datapoints = metrics.get("Datapoints", [])
        if not datapoints:
            return 0.0

        return sum(dp["Average"] for dp in datapoints) / len(datapoints)

    def _network_usage(self, instance_id: str, start, end) -> float:
        def get_sum(metric):
            res = self.cw.get_metric_statistics(
                Namespace="AWS/EC2",
                MetricName=metric,
                Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
                StartTime=start,
                EndTime=end,
                Period=86400,
                Statistics=["Sum"],
            )
            return sum(dp["Sum"] for dp in res.get("Datapoints", []))

        net_in = get_sum("NetworkIn")
        net_out = get_sum("NetworkOut")

        # Bytes → MB
        return (net_in + net_out) / (1024 * 1024)
