"""Compare the IG Publisher's expansions with tx.fhir.org.

Run after the IG Publisher: python3 check.py
For each ValueSet in fsh-generated/resources, it expands the whole ValueSet on
tx.fhir.org and lists the codes that only the publisher's expansion
(output/expansions.json) contains.
"""
import glob
import json
import urllib.request

TX = "https://tx.fhir.org/r4/ValueSet/$expand"

published = {
    entry["resource"]["url"]: entry["resource"]
    for entry in json.load(open("output/expansions.json")).get("entry", [])
}

for path in sorted(glob.glob("fsh-generated/resources/ValueSet-*.json")):
    vs = json.load(open(path))
    body = json.dumps({
        "resourceType": "Parameters",
        "parameter": [
            {"name": "count", "valueInteger": 5000},
            {"name": "valueSet", "resource": vs},
        ],
    }).encode()
    request = urllib.request.Request(TX, data=body, headers={
        "Content-Type": "application/fhir+json",
        "Accept": "application/fhir+json",
    })
    tx = json.load(urllib.request.urlopen(request))
    tx_codes = {c["code"] for c in tx["expansion"].get("contains", [])}
    pub_codes = {c["code"] for c in published[vs["url"]]["expansion"].get("contains", [])}
    print(f"{vs['id']}: publisher {len(pub_codes)}, tx.fhir.org {len(tx_codes)}, "
          f"only in the publisher's expansion: {sorted(pub_codes - tx_codes)}")
