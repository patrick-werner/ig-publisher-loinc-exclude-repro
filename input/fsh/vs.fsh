Alias: $loinc = http://loinc.org

// Filter include + explicit code excludes.
// tx.fhir.org: the include alone has 68 codes; with the excludes 64.
ValueSet: ReproExcludeCodes
Id: repro-exclude-codes
Title: "Repro: filter include, explicit code excludes"
* ^status = #draft
* include codes from system $loinc where METHOD_TYP = "LP6429-7" and SYSTEM = "LP7735-6" and PROPERTY = "LP6850-4" and STATUS = "ACTIVE"
* exclude $loinc#44851-4 "Mycobacterium sp # 2 identified in Specimen by Organism specific culture"
* exclude $loinc#44852-2 "Mycobacterium sp # 3 identified in Specimen by Organism specific culture"
* exclude $loinc#44854-8 "Mycobacterium sp # 4 identified in Specimen by Organism specific culture"
* exclude $loinc#44855-5 "Mycobacterium sp # 5 identified in Specimen by Organism specific culture"

// Filter include + filter exclude (component "Microscopic observation").
ValueSet: ReproExcludeFilter
Id: repro-exclude-filter
Title: "Repro: filter include, filter exclude"
* ^status = #draft
* include codes from system $loinc where CLASS = "LP7819-8" and PROPERTY = "LP6850-4" and METHOD_TYP = "LP6398-4" and STATUS = "ACTIVE"
* exclude codes from system $loinc where COMPONENT = "LP442509-8"
