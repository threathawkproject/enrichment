from mitreattack.stix20 import MitreAttackData

class CampaignsViaAttackPattern():
    def run(self, ioc, type, node_id):
        mitre_attack_data = MitreAttackData("./resources/enterprise-attack.json")
        groups = mitre_attack_data.get_campaigns_using_technique(node_id)
        data = []
        for group in groups:
            intrusion_set = group["object"].serialize()
            relationship = group["relationship"].serialize()
            data.append(intrusion_set)
            data.append(relationship)
        return data