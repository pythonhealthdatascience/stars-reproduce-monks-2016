'''
Contains data classes for simulation model
'''
from dataclasses import dataclass
from abc import ABC, abstractmethod
from numpy.random import RandomState


class Distribution(ABC):
    '''
    Abstract distribution object.

    Each distribution has its own random number steam
    used for sampling.
    '''
    def __init__(self, random_state):
        self._rand = RandomState(seed=random_state)

    @abstractmethod
    def sample(self, size=None):
        pass


class Normal(Distribution):
    '''
    Wraps a normal distribution and its parameters.
    Allows lower truncation of normal distribution.
    Allows control of random number stream.
    '''

    def __init__(self, mean=0.0, std=1.0, minimum=None, random_state=None):
        '''

        Constructor for Normal Distribution

        Parameters
        ----------
        mean : float, optional
            mean of the normal distribution. The default is 0.0
        std : float, optional
            stdev of the normal distribution. The default is 1.0
        minimum: float, optional
            lower truncation point of the normal dist. if None
            then distribution is not truncated.  Default is None.
        random_state : int, optional
            random_initial state to control the stream
            of random numbers generated by the distribution.
            The default is None.

        '''

        super().__init__(random_state)
        self.mean = mean
        self.std = std
        self.minimum = minimum

    def sample(self, size=None):
        '''
        Samples from the normal distribution with 
        specified parameters.

        Lower truncates values if self.trunc is set.

        Parameters
        ----------
        size : int, optional
            Number of samples to return. The default is None.

        Returns
        -------
        scalar or numpy.array of 
            normally distributed variates.

        '''
        sample = self._rand.normal(self.mean,
                                   self.std,
                                   size=size)

        if self.minimum is not None:
            if size is None:
                sample = max(sample, self.minimum)
            else:
                sample[sample < self.minimum] = self.minimum

        return sample


class Uniform(Distribution):
    '''
    Wraps a uniform distribution and its parameters
    Allows control of random number stream.
    '''

    def __init__(self, minimum, maximum, random_state=None):
        '''
        Constructor of the Uniform Distribution
        sampling object

        Parameters
        ----------
        minimum : float, optional
            Min of the uniform distribution. The default is 0.0.
        maximum : TYPE, optional
            Max of the uniform distribution. The default is 1.0.
        random_state : int, optional
            seed for random state and controlling the 
            random number stream of the distribution. The default is None.
        '''
        super().__init__(random_state)
        self.maximum = maximum
        self.minimum = minimum

    def sample(self, size=None):
        '''
        Samples from the uniform distribution with 
        specified parameters

        Parameters
        ----------
        size : int, optional
            Number of samples to return. The default is None.

        Returns
        -------
        scalar or numpy.array of 
            uniform distributed variates.
        '''

        return self._rand.uniform(self.minimum, 
                                  self.maximum, 
                                  size=size)


@dataclass(frozen=True)
class Scenario:
    '''
    Dataclass for DialysisSim

    Encapsulates all parameters for the simulation model.  

    Note the @dataclass decorator.  This takes
    a parameter call frozen which means the class
    is immutable.  That's nice for parameters!
    '''

    run_length: float = 200

    audit_interval: int = 1

    # Proportion of all people who will get infected (limited by herd immunity)
    # really this is init only...
    total_proportion_people_infected: float = 0.8

    # Proportion negative people who 'may' have COV
    prop_neg_patients_cov_query: float = 0.02

    # Infection distribution type (default = Normal)
    time_to_infection: Distribution = Normal(60, 15, 0.0)

    # Sampling distribution for time positive 
    time_positive: Distribution = Uniform(7, 14)

    # Proportion Cov+ requiring inpatient care
    proportion_pos_requiring_inpatient: float = 0.4
    requiring_inpatient_random: Distribution = Uniform(0.0, 1.0)
    time_pos_before_inpatient: Distribution = Uniform(3, 7)
    time_inpatient: Distribution = Uniform(7.0, 14.0)

    # Mortality rate
    mortality: float = 0.15

    # Mortality random number
    mortality_rand = Uniform(0.0, 1.0)

    # Add random positives at start; applies to negative patients
    random_positive_rate_at_start: float = 0.0

    # Restrict the maximum proportion of people who can be infected    
    will_be_infected_rand = Uniform(0.0, 1.0)

    # Strategies ---------------------------------

    open_all_sessions: bool = False
    drop_to_two_sessions: bool = False
    prop_patients_drop_to_two_sessions: float = 0.9
