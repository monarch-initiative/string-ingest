import uuid
from typing import Dict, List

import koza
from biolink_model.datamodel.pydanticmodel_v2 import AgentTypeEnum, KnowledgeLevelEnum, PairwiseGeneToGeneInteraction
from loguru import logger

# Mapping of STRING evidence type score fields to ECO codes
EVIDENCE_CODE_MAPPINGS = {
    "neighborhood": "ECO:0000044",
    "fusion": "ECO:0000124",
    "cooccurence": "ECO:0000080",
    "coexpression": "ECO:0000075",
    "experimental": "ECO:0000006",
    "database": "ECO:0007636",
    "textmining": "ECO:0007833",
}


def map_evidence_codes(row: Dict) -> List[str]:
    eco_mappings: List[str] = list()
    for evidence_type in EVIDENCE_CODE_MAPPINGS.keys():
        if int(row[evidence_type]) > 0:
            eco_mappings.append(EVIDENCE_CODE_MAPPINGS[evidence_type])
    return eco_mappings


def sorted_id_pair(row) -> str:
    return tuple(sorted([row['protein1'], row['protein2']]))


@koza.transform_record()
def transform_record(koza_transform, row):

    row_key = sorted_id_pair(row)

    # Initialize seen_rows on the transform object if not present
    if not hasattr(koza_transform, 'seen_rows'):
        koza_transform.seen_rows = set()

    # Skip if we've already seen this row (duplicate check)
    if row_key in koza_transform.seen_rows:
        return []

    koza_transform.seen_rows.add(row_key)

    pid_a = row['protein1']

    gene_ids_a = koza_transform.lookup(pid_a, 'entrez', 'entrez_2_string')
    if not gene_ids_a:
        logger.debug(f"protein1 PID '{str(pid_a)}' has no Entrez mappings?")

    pid_b = row['protein2']
    gene_ids_b = koza_transform.lookup(pid_b, 'entrez', 'entrez_2_string')
    if not gene_ids_b:
        logger.debug(f"protein2 PID '{str(pid_b)}' has no Entrez mappings?")

    # Some proteins may not have gene Entrez ID mappings.
    # Only process the record if both gene id's are found
    if gene_ids_a and gene_ids_b:

        entities = []

        has_evidence: List[str] = map_evidence_codes(row)

        for gid_a in gene_ids_a.split("|"):

            for gid_b in gene_ids_b.split("|"):

                gene_id_a = 'NCBIGene:' + gid_a

                gene_id_b = 'NCBIGene:' + gid_b

                association = PairwiseGeneToGeneInteraction(
                    id="uuid:" + str(uuid.uuid1()),
                    subject=gene_id_a,
                    object=gene_id_b,
                    predicate="biolink:interacts_with",
                    # sanity check: set to 'None' if empty list
                    has_evidence=has_evidence if has_evidence else None,
                    aggregator_knowledge_source=["infores:monarchinitiative"],
                    primary_knowledge_source="infores:string",
                    knowledge_level=KnowledgeLevelEnum.knowledge_assertion,
                    agent_type=AgentTypeEnum.not_provided,
                )
                entities.append(association)

        return entities
    # No gene id mapping for one or both proteins, skip this row
    return []
