import argparse
import parseanalysis as pa
import dxpy


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'analysisID',
        help=
        'DNANexus analysis ID you want to compare to the Gold Standard Experiment.'
    )
    parser.add_argument(
        '--auth_token',
        type=str,
        default=None,
        help='DNANexus authentication token')
    parser.add_argument(
        '--assembly',
        type=str,
        default=None,
        required=True,
        help='Assembly code hg19/GRCh38')
    args = parser.parse_args()
    return args

def authenticate(auth_token):
    dxpy.set_security_context({
        'auth_token_type': 'bearer',
        'auth_token': auth_token
    })
    return None


def main():
    args = get_args()
    analysisID = args.analysisID
    token = args.auth_token
    assembly = args.assembly
    authenticate(token)
    analysis_info = dxpy.describe(analysisID)
    analysis_md5_data = pa.calculate_md5_for_analysis(
        pa.parseanalysis(analysis_info, assembly))
