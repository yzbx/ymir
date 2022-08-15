PRODUCER_KEY = 'producer'
PRODUCER_NAME = 'ymir'
EXECUTOR_CONFIG_KEY = 'executor_config'
TASK_CONTEXT_KEY = 'task_context'
TASK_CONTEXT_PARAMETERS_KEY = 'task_parameters'
TASK_CONTEXT_PREPROCESS_KEY = 'preprocess'
EXECUTOR_OUTLOG_NAME = 'ymir-executor-out.log'

# about hists
BYTES_PER_MB = 1048576
QUALITY_DESC_LOWER_BNDS = [x / 10 for x in range(10, -1, -1)]
ANNO_AREA_DESC_LOWER_BNDS = [200000, 100000, 50000, 10000, 5000, 2500, 500, 50, 0]
ASSET_BYTES_DESC_LOWER_BNDS = [x * BYTES_PER_MB / 2 for x in range(10, -1, -1)]
ASSET_AREA_DESC_LOWER_BNDS = [8000000, 6000000, 4000000, 2000000, 1000000, 500000, 100000, 0]
ASSET_HW_RATIO_DESC_LOWER_BNDS = [x / 10 for x in range(15, -1, -1)]

# about evaluate default args
DEFAULT_EVALUATE_CONF_THR = 0.005
DEFAULT_EVALUATE_IOU_THR = '0.5'
