import json
import pandas as pd
from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from fhir.resources.bundle import Bundle

def extract_patients_from_bundle(bundle_file):
    """Extract Patient resources from bundle"""
    with open(bundle_file, 'r') as f:
        bundle_dict = json.load(f)
    
    bundle = Bundle.parse_obj(bundle_dict)
    patients = []
    
    for entry in bundle.entry:
        if entry.resource.__resource_type__ == "Patient":
            patients.append(entry.resource)
    
    return patients

def extract_observations_from_bundle(bundle_file):
    """Extract Observation resources from bundle"""
    with open(bundle_file, 'r') as f:
        bundle_dict = json.load(f)
    
    bundle = Bundle.parse_obj(bundle_dict)
    observations = []
    
    for entry in bundle.entry:
        if entry.resource.__resource_type__ == "Observation":
            observations.append(entry.resource)
    
    return observations

def patients_to_csv(patients, output_file):
    """Convert FHIR Patient resources to CSV format"""
    data = []
    
    for patient in patients:
        # Extract necessary fields
        patient_data = {
            'id': patient.id,
            'family_name': patient.name[0].family if patient.name and len(patient.name) > 0 else '',
            'given_name': patient.name[0].given[0] if patient.name and len(patient.name) > 0 and patient.name[0].given else '',
            'gender': patient.gender,
            'birth_date': patient.birthDate,
            'address': patient.address[0].line[0] if patient.address and len(patient.address) > 0 and patient.address[0].line else '',
            'city': patient.address[0].city if patient.address and len(patient.address) > 0 else '',
            'country': patient.address[0].country if patient.address and len(patient.address) > 0 else '',
            'phone': next((t.value for t in patient.telecom if t.system == "phone"), '') if patient.telecom else ''
        }
        data.append(patient_data)
    
    # Create DataFrame and save as CSV
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    return len(data)

def observations_to_csv(observations, output_file):
    """Convert FHIR Observation resources to CSV format"""
    data = []
    
    for obs in observations:
        # Extract patient ID from subject
        patient_id = ''
        if obs.subject and obs.subject.reference:
            # Format usually "Patient/123"
            parts = obs.subject.reference.split('/')
            if len(parts) > 1:
                patient_id = parts[1]
        
        # Extract coding information
        code = ''
        code_system = ''
        display = ''
        if obs.code and obs.code.coding and len(obs.code.coding) > 0:
            code = obs.code.coding[0].code
            code_system = obs.code.coding[0].system
            display = obs.code.coding[0].display
        
        # Extract value
        value = ''
        unit = ''
        if obs.valueQuantity:
            value = obs.valueQuantity.value
            unit = obs.valueQuantity.unit
        
        # Create observation data
        obs_data = {
            'id': obs.id,
            'patient_id': patient_id,
            'observation_date': obs.effectiveDateTime,
            'code': code,
            'code_system': code_system,
            'display': display,
            'value': value,
            'unit': unit
        }
        data.append(obs_data)
    
    # Create DataFrame and save as CSV
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    return len(data)

def main():
    # Extract resources from bundle
    patients = extract_patients_from_bundle('bundle.json')
    observations = extract_observations_from_bundle('bundle.json')
    
    # Convert resources to CSV
    patient_count = patients_to_csv(patients, 'patients_reversed.csv')
    obs_count = observations_to_csv(observations, 'observations_reversed.csv')
    
    print(f"Converted {patient_count} patient records to CSV")
    print(f"Converted {obs_count} observation records to CSV")

if __name__ == "__main__":
    main()