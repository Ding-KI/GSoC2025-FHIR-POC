import json
from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from fhir.resources.bundle import Bundle
from pydantic import ValidationError

def validate_fhir_resources(json_file, resource_type):
    """Verify that FHIR resources conform to the standard."""
    try:
        # Read JSON file
        with open(json_file, 'r') as f:
            resources_dict = json.load(f)
        
        # Validate each resource
        valid_count = 0
        error_count = 0
        error_messages = []
        
        if isinstance(resources_dict, list):
            # If it's a list of resources
            for i, resource_dict in enumerate(resources_dict):
                try:
                    if resource_type == "Patient":
                        Patient.parse_obj(resource_dict)
                    elif resource_type == "Observation":
                        Observation.parse_obj(resource_dict)
                    valid_count += 1
                except ValidationError as e:
                    error_count += 1
                    error_messages.append(f"Source #{i+1} validation error: {str(e)}")
        else:
            # If it's a single Bundle
            try:
                Bundle.parse_obj(resources_dict)
                valid_count = 1
            except ValidationError as e:
                error_count = 1
                error_messages.append(f"Bundle validation error: {str(e)}")
        
        return {
            "valid_count": valid_count,
            "error_count": error_count,
            "error_messages": error_messages
        }
    
    except Exception as e:
        return {
            "valid_count": 0,
            "error_count": 1,
            "error_messages": [f"File processing error: {str(e)}"]
        }

def main():
    # Validate patient resources
    patient_result = validate_fhir_resources('patients.json', 'Patient')
    print(f"Patient resource validation results:")
    print(f"- Valid resources: {patient_result['valid_count']}")
    print(f"- Error resources: {patient_result['error_count']}")
    if patient_result['error_count'] > 0:
        for msg in patient_result['error_messages']:
            print(f"  * {msg}")
    
    # Validate observation resources
    obs_result = validate_fhir_resources('observations.json', 'Observation')
    print(f"\nObservation resource validation results:")
    print(f"- Valid resources: {obs_result['valid_count']}")
    print(f"- Error resources: {obs_result['error_count']}")
    if obs_result['error_count'] > 0:
        for msg in obs_result['error_messages']:
            print(f"  * {msg}")
    
    # Validate Bundle
    bundle_result = validate_fhir_resources('bundle.json', 'Bundle')
    print(f"\nBundle validation results:")
    print(f"- Valid: {bundle_result['valid_count'] > 0}")
    if bundle_result['error_count'] > 0:
        for msg in bundle_result['error_messages']:
            print(f"  * {msg}")

if __name__ == "__main__":
    main()