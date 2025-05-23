'''
Utility functions
'''

# Define required fields for each type
REQUIRED_FIELDS = {
    'experience': ['title', 'company', 'start_date', 'end_date', 'description', 'logo'],
    'education': ['course', 'school', 'start_date', 'end_date', 'grade', 'logo'],
    'skill': ['name', 'proficiency', 'logo']
}

def validate_data(data_type, data):
    '''
    Validates that all required fields are present in the data
    
    Parameters
    ----------
    data_type : str
        The type of data being validated ('experience', 'education', or 'skill')
    data : dict
        The data to validate
        
    Returns
    -------
    tuple
        (bool, str) - (is_valid, error_message)
    '''
    if data is None:
        return False, "Invalid data format"
        
    if not isinstance(data, dict):
        return False, "Invalid data format"
        
    missing_fields = [field for field in REQUIRED_FIELDS[data_type] if field not in data]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    return True, None 