from . import block_params

def parse_block_params(input_block_params_str,blockparamsclass=block_params.BlockParams):
    if input_block_params_str is not None:
        input_vec = input_block_params_str.split(',')
        size = int(input_vec[0])
        overlap = int(input_vec[1])

        if size > 0 and overlap >= 0:
            return blockparamsclass(size=size, overlap=overlap), ''
        else:
            return blockparamsclass.default(), 'Invalid block size or overlap'
    else:
        return blockparamsclass.default(), 'Invalid block size or overlap'