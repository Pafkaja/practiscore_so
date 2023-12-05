import  requests

def get_match_data(match_uuid):
    match_def = requests.get(f'https://s3.amazonaws.com/ps-scores/production/{match_uuid}/match_def.json')
    results = requests.get(f'https://s3.amazonaws.com/ps-scores/production/{match_uuid}/results.json')
    match_scores = requests.get(f'https://s3.amazonaws.com/ps-scores/production/{match_uuid}/match_scores.json')
    return match_def.json(), results.json(), match_scores.json()

if __name__=="__main__":
    mdef, results, scores = get_match_data('576a8688-c515-43de-bb96-ebf75dd3f34c')

    print()