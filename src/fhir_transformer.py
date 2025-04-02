import pandas as pd
import json
import datetime
from datetime import date, datetime
from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.address import Address
from fhir.resources.observation import Observation
from fhir.resources.reference import Reference
from fhir.resources.quantity import Quantity
from fhir.resources.coding import Coding
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.bundle import Bundle, BundleEntry

def csv_to_fhir_patients(csv_file):
    """Convert CSV patient data to FHIR Patient resources"""
    patients_df = pd.read_csv(csv_file)
    patients = []
    
    for _, row in patients_df.iterrows():
        # Create a Patient resource
        patient = Patient(
            id=str(row['id']),
            name=[
                HumanName(
                    family=row['family_name'],
                    given=[row['given_name']]
                )
            ],
            gender=row['gender'],
            birthDate=row['birth_date'],
            address=[
                Address(
                    line=[row['address']],
                    city=row['city'],
                    country=row['country']
                )
            ],
            telecom=[
                ContactPoint(
                    system="phone",
                    value=row['phone']
                )
            ]
        )
        patients.append(patient)
    
    return patients

def csv_to_fhir_observations(csv_file, patient_refs=None):
    """Convert CSV observation data to FHIR Observation resources"""
    obs_df = pd.read_csv(csv_file)
    observations = []
    
    for _, row in obs_df.iterrows():
        # Coding
        coding = Coding(
            system=row['code_system'],
            code=row['code'],
            display=row['display']
        )
        
        # CodeableConcept
        code = CodeableConcept(
            coding=[coding],
            text=row['display']
        )
        
        # ValueQuantity
        value_quantity = Quantity(
            value=float(row['value']),
            unit=row['unit'],
            system="http://unitsofmeasure.org",
            code=row['unit']
        )
        
        # Create Observation resource
        observation = Observation(
            id=str(row['id']),
            status="final",
            code=code,
            subject=Reference(reference=f"Patient/{row['patient_id']}"),
            effectiveDateTime=row['observation_date'],
            valueQuantity=value_quantity
        )
        
        observations.append(observation)
    
    return observations

def create_bundle(patients, observations):
    """Create a FHIR Bundle containing patients and observations"""
    entries = []
    
    # Add patient entries
    for patient in patients:
        entry = BundleEntry(
            fullUrl=f"Patient/{patient.id}",
            resource=patient
        )
        entries.append(entry)
    
    # Add observation entries
    for obs in observations:
        entry = BundleEntry(
            fullUrl=f"Observation/{obs.id}",
            resource=obs
        )
        entries.append(entry)
    
    # Create Bundle
    bundle = Bundle(
        type="collection",
        entry=entries
    )
    
    return bundle

def save_resources_to_json(resources, output_file):
    """Save FHIR resources to a JSON file"""
    # Convert resources to dictionary
    resources_dict = [resource.dict() for resource in resources]
    
    # Save as JSON
    with open(output_file, 'w') as f:
        json.dump(resources_dict, f, indent=2)

def save_bundle_to_json(bundle, output_file):
    """Save FHIR Bundle to a JSON file"""
    # Convert Bundle to dictionary
    bundle_dict = bundle.dict()
    
    # Custom JSON encoder to handle date types
    class DateEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (date, datetime)):
                return obj.isoformat()
            return super().default(obj)
    
    # Save as JSON, using custom encoder
    with open(output_file, 'w') as f:
        json.dump(bundle_dict, f, indent=2, cls=DateEncoder)

def main():
    # Convert patient data
    patients = csv_to_fhir_patients('sample_patients.csv')
    print(f"Converted {len(patients)} patient records")
    
    # Convert observation data
    observations = csv_to_fhir_observations('sample_observations.csv')
    print(f"Converted {len(observations)} observation records")
    
    # Save individual resources
    save_resources_to_json(patients, 'patients.json')
    save_resources_to_json(observations, 'observations.json')
    
    # Create and save Bundle
    bundle = create_bundle(patients, observations)
    save_bundle_to_json(bundle, 'bundle.json')
    print(f"Created a Bundle with {len(bundle.entry)} entries")

if __name__ == "__main__":
    main()