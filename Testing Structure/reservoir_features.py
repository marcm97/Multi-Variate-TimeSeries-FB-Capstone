import numpy as np

class reservoir_features:
    '''
    creates an object associated with a multivariate dataset
    '''
    def __init__(self,data,num_features):
        '''
        data: Takes in a multidimensional array (x * y * z) - z>y
        Initializes it
        x: Timeseries
        y: Attributes for a given timeseries observation
        z: timestamped observations (features)
        
        num_features: you must specify the dimension you want to reduce it to
        
        '''
        self.features = []
        self.filters_used = []
        self.original_data = data.copy()
        self.data = data.copy()
        self.num_features = num_features
        self.x = data.shape[0]
        self.y = data.shape[1]
        self.z = data.shape[2]
        # perform checks 
        #1. 3d numpy array
        #2. Each time series should have same number of observations
        #3. num_features should be less than timestamped observations
    
    def normalize(self):
        '''
        Each attribute could potentially be on a different scale
        modifies the original data and performs a min max normalization
        '''
        for i in range(self.original_data.shape[0]):
            for j in range(self.original_data.shape[1]):
                self.data[i][j] = (self.original_data[i][j] - self.original_data[i][j].min())/(self.original_data[i][j].max()-self.original_data[i][j].min())
    
    def filters(self,stride_len = [1], num_filters = 1):
        '''
        stride_len: num of columns to skip after each filter multiplication
        num_filters: you can specify the number of filters you need; each filter will be of a differnt size
        size of filter = n*m 
        (n = # of rows = attribute size, 
        m = # of columns)
        '''
        #Have error check to make sure stride len is a list and value is <length of attributes
        n = self.y
        
        
        #Edge case vals is empty/smaller than num_filters
        
        for iteration in range(num_filters):
            m = self._get_m(stride_len[iteration])
            filter_a = np.random.random((n,m))
            print("filter of size ", str(n), "*", str(m), "was created\n")
            self.filters_used.append(filter_a)
            
            temp_features =[]
            for i in range(self.x):
                temp = []
                j = 0
                while j + m < self.data.shape[2]:
                    temp.append((filter_a*self.data[i,:,j:j+m]).mean())
                    j+=stride_len[iteration]
                temp_features.append(temp)
            self.features.append(temp_features)
     
    def _get_m(self,stride_len):
        '''
        stride_len: 
        based on stride length,& num_features, we calculate possible filter size 
        '''
        m = self.z -(self.num_features)*stride_len
        return m
    
    def result_features(self):
        '''
        if multiple filters were added, takes the average result
        '''
        ans =[]
        for timeseries in range(len(self.features[0])):
            temp =[]
            for feature in range(len(self.features[0][0])):
                val = np.mean([self.features[filter][timeseries][feature] for filter in range(len(self.features))])
                temp.append(val)
            ans.append(temp)
        return ans
        