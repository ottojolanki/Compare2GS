from collections import namedtuple
import dxpy
import hashlib
import copy


def calculate_md5_for_analysis(analysis):
    '''
    input: Analysis object from parse_analysis
    output: Analysis object with fileIDs replaced
            with md5sums
    '''
    analysis_cp = copy.deepcopy(analysis)

    for key in analysis_cp.file_descriptions:
        analysis_cp.file_descriptions[key] = calculatemd5_from_fileID(
            analysis_cp.file_descriptions[key])

    return analysis_cp


def parse_analysis(description, assembly):
    '''
    input: output from dxpy.describe(analysis-xyz)
    output: namedtuple with fields:
    -target_type: string histone/tf
    -unreplicated: boolean
    -assembly: hg19/GRCh38
    -file_descriptions: dict {filename:file DNAnexus fileID}
    '''

    Analysis = namedtuple('Analysis', [
        'target', 'unreplicated', 'assembly', 'file_descriptions'
    ])
    properties = description['properties']
    output_all = description['output']
    output_fileIDs = [
        output_all[key].values()[0] for key in output_all
        if isinstance(output_all[key], dict)
    ]
    file_info_dict = {}

    for fileID in output_fileIDs:
        file_info_dict.update(get_file_info(dxpy.describe(fileID)))

    return Analysis(properties['target_type'],
                    true_or_false(properties['unreplicated_experiment']),
                    assembly, file_info_dict)


def get_file_info(description):
    '''input: dict from dxpy.describe(fileID)
       output: dict {filename:fileID}
    '''
    return {description['name']: description['id']}


def true_or_false(token):
    return token.lower().startswith('t')


def calculatemd5_from_fileID(fileID, chunksize=4096):
    '''input: DNAnexus fileID
       output: corresponding md5 sum
    '''
    hash_md5 = hashlib.md5()
    filehandle = dxpy.DXFile(fileID)
    with filehandle as f:
        for chunk in iter(lambda: f.read(chunksize), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
