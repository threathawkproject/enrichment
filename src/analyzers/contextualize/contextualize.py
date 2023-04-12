from mitreattack.stix20 import MitreAttackData


def get_mitre_data(attack_id, type):
    mitre_attack_data = MitreAttackData("./resources/enterprise-attack.json")
    ttp = mitre_attack_data.get_object_by_attack_id(attack_id, type)
    if ttp is not None:
        return ttp.serialize()
    return None


# class Contextualize():
#     def run(self, ioc, type, node_id):
        # mitre_attack_data = MitreAttackData("enterprise-attack.json")
