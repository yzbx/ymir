import logging
import os
import shutil
import unittest
from unittest import mock

from google.protobuf.json_format import MessageToDict, ParseDict

from common_utils import labels
from controller.utils.invoker_call import make_invoker_cmd_call
from controller.utils.invoker_mapping import RequestTypeToInvoker
from proto import backend_pb2
import tests.utils as test_utils

RET_ID = 'commit t000aaaabbbbbbzzzzzzzzzzzzzzz3\nabc'


class TestInvokerInit(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        # dir structure:
        # test_involer_CLSNAME_sandbox_root
        # ├── media_storage_root
        # └── test_user
        #     └── ymir-dvc-test
        super().__init__(methodName=methodName)
        self._user_name = "user"
        self._mir_repo_name = "repoid"
        self._storage_name = "media_storage_root"
        self._task_id = 't000aaaabbbbbbzzzzzzzzzzzzzzz5'
        self._base_task_id = 't000aaaabbbbbbzzzzzzzzzzzzzzz4'

        self._sandbox_root = test_utils.dir_test_root(self.id().split(".")[-3:])
        self._user_root = os.path.join(self._sandbox_root, self._user_name)
        self._mir_repo_root = os.path.join(self._user_root, self._mir_repo_name)
        self._storage_root = os.path.join(self._sandbox_root, self._storage_name)

    def setUp(self):
        test_utils.check_commands()
        self._prepare_dirs()
        labels.load_or_create_userlabels(label_storage_file=os.path.join(self._user_root, 'labels.yaml'),
                                         create_ok=True)
        labels.UserLabels.main_name_for_ids = mock.Mock(return_value=["person", "cat"])
        logging.info("preparing done.")

    def tearDown(self):
        if os.path.isdir(self._sandbox_root):
            shutil.rmtree(self._sandbox_root)
        pass

    # custom: env prepare
    def _prepare_dirs(self):
        if os.path.isdir(self._sandbox_root):
            logging.info("sandbox root exists, remove it first")
            shutil.rmtree(self._sandbox_root)
        os.makedirs(self._sandbox_root)
        os.mkdir(self._user_root)
        os.mkdir(self._storage_root)

    def _mock_run_func(*args, **kwargs):
        ret = type('', (), {})()
        ret.returncode = 0
        ret.stdout = RET_ID
        return ret

    @mock.patch("subprocess.run", side_effect=_mock_run_func)
    def test_invoker_init_00(self, mock_run):
        response = make_invoker_cmd_call(sandbox_root=self._sandbox_root,
                                         req_type=backend_pb2.CMD_INIT,
                                         invoker=RequestTypeToInvoker[backend_pb2.CMD_INIT],
                                         user_id=self._user_name,
                                         task_id=self._task_id,
                                         repo_id=self._mir_repo_name)
        print(MessageToDict(response))

        expected_cmd = (f"mir init --root {os.path.join(self._user_root, self._mir_repo_name)} "
                        f"--user-label-file {test_utils.user_label_file(self._sandbox_root, self._user_name)} "
                        f"--with-empty-rev {self._task_id}@{self._task_id}")
        mock_run.assert_called_once_with(expected_cmd.split(' '), capture_output=True, text=True)

        expected_ret = backend_pb2.GeneralResp()
        expected_dict = {'message': RET_ID}
        ParseDict(expected_dict, expected_ret)
        self.assertEqual(response, expected_ret)
