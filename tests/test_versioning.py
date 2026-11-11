import importlib.util
import pathlib
import tempfile
import subprocess
import unittest
from concurrent.futures import ThreadPoolExecutor
spec=importlib.util.spec_from_file_location('versioning',pathlib.Path(__file__).parents[1]/'tools/versioning/manager.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class VersionTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=pathlib.Path(self.tmp.name)
  self.remote=self.root/'remote.git';subprocess.run(['git','init','--bare',str(self.remote)],check=True,capture_output=True)
  self.repo=self.root/'repo';self.repo.mkdir();self.m=mod.VersionManager(self.repo)
  self.m.git('init');self.m.git('config','user.name','Ujian');self.m.git('config','user.email','test@example.invalid');self.m.git('commit','--allow-empty','-m','checkpoint');self.m.git('remote','add','origin',str(self.remote))
 def tearDown(self):self.tmp.cleanup()
 def test_sequence_idempotent_and_failed_not_reused(self):
  a=self.m.reserve('first','Ujian pertama');b=self.m.reserve('second','Ujian kedua');self.assertEqual([a['build'],b['build']],[1,2]);self.assertEqual(self.m.reserve('first','nama berubah'),a)
  # Reservation tidak dipadam walaupun task gagal; task berikut dapat nombor baharu.
  self.assertEqual(self.m.reserve('after-failed','Ketiga')['build'],3)
 def test_parallel_branches_unique(self):
  def reserve(i):return mod.VersionManager(self.repo).reserve('job'+str(i),'Serentak')['build']
  with ThreadPoolExecutor(max_workers=4) as pool:result=list(pool.map(reserve,range(4)))
  self.assertEqual(sorted(result),[1,2,3,4])
 def test_restore_source_never_overwrites(self):
  sha=self.m.checkpoint('v0.0.0.1-draft');dest=self.root/'recovered';self.assertEqual(self.m.restore_source(sha,dest),sha)
  with self.assertRaises(ValueError):self.m.restore_source(sha,dest)
  with self.assertRaises(subprocess.CalledProcessError):self.m.checkpoint('v0.0.0.1-draft')

class ReleaseStateTests(unittest.TestCase):
 def test_failed_is_never_stable_and_old_record_immutable(self):
  with tempfile.TemporaryDirectory() as d:
   record={'display':'v0.0.0.1'}
   old=mod.record_result(d,record,'FAILED',{'unit':'FAIL'},'sha');raw=old.read_bytes()
   with self.assertRaises(ValueError):mod.record_result(d,record,'STABLE',{'unit':'PASS'},'sha',True)
   mod.record_result(d,record,'DRAFT',{},'next');self.assertEqual(old.read_bytes(),raw)
