import time

def wait_until_condition(conditional_func, timeout: float = 3, retry_interval: float = 0.01, *func_args, **func_kwargs) -> bool:
    '''Wait until condition function\n
    Returns True if the conditional function returns a value that is True before the Timeout is reached.\n
    However, returns False if the conditional function doesn't return a value that is True before the Timeout is reached.\n
    Args:
                    conditional_func: the function to perform on each iteration check
                    
                    (optional)
                    timeout: the timeout max (in seconds) of type float
                    retry_interval: the delay time (in seconds) of type float between each check
                    *func_args: the arguments to pass into the conditional function
                    **func_kwargs: the keyword arguments to pass into the conditional function

        Returns: 
                    result: value of type bool
    '''
    timeafter = time.time() + timeout
    while time.time() < timeafter:
        if conditional_func(*func_args, **func_kwargs): return True
        time.sleep(retry_interval)
    return False

def wait_until_raise(conditional_func, error: Exception = TimeoutError(), timeout: float = 3, retry_interval: float = 0.01, *func_args, **func_kwargs):
    '''Wait until raise function\n
    Returns the value if the conditional function returns a value that is True before the Timeout is reached.\n
    However, raises an error if the conditional function doesn't return a value that is True before the Timeout is reached.\n
    Args:
                    conditional_func: the function to perform on each iteration check
                    
                    (optional)
                    error: the error to raise if a timeout is reached of type exception
                    timeout: the timeout max (in seconds) of type float
                    retry_interval: the delay time (in seconds) of type float between each check
                    *func_args: the arguments to pass into the conditional function
                    **func_kwargs: the keyword arguments to pass into the conditional function

        Returns: 
                    result: value of type bool
    '''
    timeafter = time.time() + timeout
    while time.time() < timeafter:
        result = conditional_func(*func_args, **func_kwargs)
        if result: return result
        time.sleep(retry_interval)
    raise error