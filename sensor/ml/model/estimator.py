class TargetValueMapping:
    """ 
    Custom code to encode the categorical column by assigning 1 for pos class and 0 for neg class
    """
    def __init__(self):
        self.pos = 1
        self.neg = 0
    
    def to_dict(self):
        """ Function to return self as dictionary """
        return self.__dict__

    def reverse_mapping(self):
        """ Reverse mapping the dictionary"""
        mapping_response = self.to_dict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))