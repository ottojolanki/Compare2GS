import argparse
import parseanalysis
import dxpy
import json


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
        required=True,
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
    analysis_md5_data = parseanalysis.calculate_md5_for_analysis(
        parseanalysis.parse_analysis(analysis_info, assembly))
    reference_filename = '_'.join([analysis_md5_data.target, str(analysis_md5_data.unreplicated), analysis_md5_data.assembly]) + '.json'
    reference_filename = 'GS_Reference_jsons/' + reference_filename

    with open(reference_filename, 'r') as f:
        reference_json = json.load(f)[3]

    for key in analysis_md5_data.file_descriptions:
        if reference_json[key] == analysis_md5_data.file_descriptions[key]:
            print 'MD5 matches for %s' % key
        else:
            print 'MD5 does not match for %s' % key


if __name__ == "__main__":
    main()
