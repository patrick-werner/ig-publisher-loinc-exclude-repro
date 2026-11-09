# IG Publisher: compose.exclude ignored for LOINC value sets

Minimal test case: the expansion that the FHIR IG Publisher renders for a
ValueSet with LOINC filter includes and an exclude still contains the excluded
codes. [HL7/fhir-ig-publisher#1310](https://github.com/HL7/fhir-ig-publisher/issues/1310)
fixed excludes for THO and for code systems defined in the IG; LOINC, whose
includes the publisher has tx.fhir.org expand, is still affected.

Validation is not affected: tx.fhir.org expands the same ValueSets correctly,
and `$validate-code` rejects the excluded codes.

## Value sets

[`input/fsh/vs.fsh`](input/fsh/vs.fsh) defines two ValueSets:

| ValueSet | include | exclude |
|---|---|---|
| `repro-exclude-codes` | LOINC filter (organism specific culture, system XXX, PrId) | four explicit codes, 44851-4, 44852-2, 44854-8, 44855-5 |
| `repro-exclude-filter` | LOINC filter (class MICRO, PrId, light microscopy) | LOINC filter `COMPONENT = LP442509-8` (Microscopic observation) |

## Reproduce

```
sushi .
java -jar publisher.jar -ig ig.ini -no-sushi
python3 check.py
```

## Result

FHIR IG Publisher 3.0.3 (Git# 15bda2b32db8, built 2026-11-06), FHIR R4,
tx.fhir.org, LOINC 2.83:

| ValueSet | publisher expansion (`output/expansions.json`, ValueSet page) | tx.fhir.org `$expand` | only in the publisher's expansion |
|---|---|---|---|
| `repro-exclude-codes` | 68 | 64 | 44851-4, 44852-2, 44854-8, 44855-5 |
| `repro-exclude-filter` | 37 | 36 | 33270-0 |

## Where it goes wrong

The publisher does not send the ValueSet to tx.fhir.org as a whole. The
txcache (`input-cache/txcache/loinc.cache`) shows that it has each include and
each filter exclude expanded separately, and tx.fhir.org answers each request
correctly:

| request | response |
|---|---|
| include of `repro-exclude-codes` | 68 codes, including 44851-4 |
| include of `repro-exclude-filter` | 37 codes, including 33270-0 |
| filter exclude `COMPONENT = LP442509-8`, as an expansion of its own | 502 codes, including 33270-0 |

The exclude is not subtracted when the publisher assembles the expansion. For
the explicit code excludes no request is made, and the codes remain as well.
The expansion parameters of the publisher's expansion contain `used-valueset`
with the value `null` and `excludeNested` twice, and no `total`; the ValueSet
page nevertheless says "Expansion from tx.fhir.org".

## Expected

The rendered expansion equals the tx.fhir.org expansion, without the excluded
codes.

## Seen in

The HL7 Europe Laboratory IG, branch Microbiology, e.g.
[ValueSet-micro-cultureSpecificCode-eu-lab](https://build.fhir.org/ig/hl7-eu/laboratory/branches/Microbiology/ValueSet-micro-cultureSpecificCode-eu-lab.html),
which lists the excluded codes 44851-4 to 44855-5, and six further ValueSets
with explicit or filter excludes.

The content of this repository is dedicated to the public domain (CC0 1.0).
