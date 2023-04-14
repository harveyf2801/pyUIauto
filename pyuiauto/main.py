from abc import ABC, abstractmethod
from platform import system

# import scipy.io as sio
# import os, sys
# import argparse

class FrameworkCreator(ABC):
    @staticmethod
    def build_framework() -> Framework:
        if system() == "Darwin":
            # pip installed modules
            try:
                    import atomacos
            except ImportError: # requires pip install
                    raise ModuleNotFoundError('To install the required modules use pip install atomacos (Mac ONLY)')
            
            return UIApplication()
        
        elif system() == "Windows":
            # pip installed modules
            try:
                    import pywinauto
            except ImportError: # requires pip install
                    raise ModuleNotFoundError('To install the required modules use pip install pywinauto (Windows ONLY)')
            
            return UIApplication()
        else:
            raise OSError("The current OS isn't supported with this framework")

mseedfile = 'example_2020-05-01_IN.RAGD..BHZ.mseed'

info_string = '''
Python utility program to convert mseed file to mat (by Utpal Kumar, IESAS, 2021/04)
'''

PARSER = argparse.ArgumentParser(description=info_string)

def main(args):
    mseedfile = args.input_mseed
    st = read(mseedfile)

    filename, _ = os.path.splitext(mseedfile)
    if not args.output_mat:
        outfilename = filename +".mat"
    else:
        outfilename = args.output_mat

    outdict = {}


    # st.plot(outfile=f"{filename}.png")
    
    outdict['stats'] = {}
    outdict['data'] = {}
    
    for ii,tr in enumerate(st):
        outdict['stats'][f'stats_{ii}'] = {}
        for val in tr.stats:
            if val in ['starttime', 'endtime']:
                outdict['stats'][f'stats_{ii}'][val] = str(tr.stats[val])
            else:
                outdict['stats'][f'stats_{ii}'][val] = tr.stats[val]
        outdict['data'][f"data_{ii}"] = tr.data
    
        
    # print(outdict)
    sio.savemat(
        outfilename, outdict
    )
    sys.stdout.write(f"Output file: {outfilename}\n")

if __name__ == '__main__':
    PARSER.add_argument("-inp",'--input_mseed', type=str, help="input mseed file, e.g. example_2020-05-01_IN.RAGD..BHZ.mseed", required=True)
    PARSER.add_argument("-out",'--output_mat', type=str, help="output mat file name, e.g. example_2020-05-01_IN.RAGD..BHZ.mat")
    

    args = PARSER.parse_args()
    main(args)