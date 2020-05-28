from basetest import *
import time

class TestZfsAutobackup(unittest2.TestCase):
    
    def setUp(self):
        prepare_zpools()

    def  test_defaults(self):

        with self.subTest("defaults with full verbose and debug"):

            with patch('time.strftime', return_value="20101111000000"):
                self.assertFalse(ZfsAutobackup("test test_target1 --verbose --debug".split(" ")).run())

            r=shelltest("zfs list -H -o name -r -t all")
            self.assertMultiLineEqual(r,"""
test_source1
test_source1/fs1
test_source1/fs1@test-20101111000000
test_source1/fs1/sub
test_source1/fs1/sub@test-20101111000000
test_source2
test_source2/fs2
test_source2/fs2/sub
test_source2/fs2/sub@test-20101111000000
test_source2/fs3
test_source2/fs3/sub
test_target1
test_target1/test_source1
test_target1/test_source1/fs1
test_target1/test_source1/fs1@test-20101111000000
test_target1/test_source1/fs1/sub
test_target1/test_source1/fs1/sub@test-20101111000000
test_target1/test_source2
test_target1/test_source2/fs2
test_target1/test_source2/fs2/sub
test_target1/test_source2/fs2/sub@test-20101111000000
""")

        with self.subTest("bare defaults, allow empty"):
            with patch('time.strftime', return_value="20101111000001"):
                self.assertFalse(ZfsAutobackup("test test_target1 --allow-empty".split(" ")).run())

        
            r=shelltest("zfs list -H -o name -r -t all")
            self.assertMultiLineEqual(r,"""
test_source1
test_source1/fs1
test_source1/fs1@test-20101111000000
test_source1/fs1@test-20101111000001
test_source1/fs1/sub
test_source1/fs1/sub@test-20101111000000
test_source1/fs1/sub@test-20101111000001
test_source2
test_source2/fs2
test_source2/fs2/sub
test_source2/fs2/sub@test-20101111000000
test_source2/fs2/sub@test-20101111000001
test_source2/fs3
test_source2/fs3/sub
test_target1
test_target1/test_source1
test_target1/test_source1/fs1
test_target1/test_source1/fs1@test-20101111000000
test_target1/test_source1/fs1@test-20101111000001
test_target1/test_source1/fs1/sub
test_target1/test_source1/fs1/sub@test-20101111000000
test_target1/test_source1/fs1/sub@test-20101111000001
test_target1/test_source2
test_target1/test_source2/fs2
test_target1/test_source2/fs2/sub
test_target1/test_source2/fs2/sub@test-20101111000000
test_target1/test_source2/fs2/sub@test-20101111000001
""")

        with self.subTest("verify holds"):

            r=shelltest("zfs get -r userrefs test_source1 test_source2 test_target1")
            self.assertMultiLineEqual(r,"""
NAME                                                   PROPERTY  VALUE     SOURCE
test_source1                                           userrefs  -         -
test_source1/fs1                                       userrefs  -         -
test_source1/fs1@test-20101111000000                   userrefs  0         -
test_source1/fs1@test-20101111000001                   userrefs  1         -
test_source1/fs1/sub                                   userrefs  -         -
test_source1/fs1/sub@test-20101111000000               userrefs  0         -
test_source1/fs1/sub@test-20101111000001               userrefs  1         -
test_source2                                           userrefs  -         -
test_source2/fs2                                       userrefs  -         -
test_source2/fs2/sub                                   userrefs  -         -
test_source2/fs2/sub@test-20101111000000               userrefs  0         -
test_source2/fs2/sub@test-20101111000001               userrefs  1         -
test_source2/fs3                                       userrefs  -         -
test_source2/fs3/sub                                   userrefs  -         -
test_target1                                           userrefs  -         -
test_target1/test_source1                              userrefs  -         -
test_target1/test_source1/fs1                          userrefs  -         -
test_target1/test_source1/fs1@test-20101111000000      userrefs  0         -
test_target1/test_source1/fs1@test-20101111000001      userrefs  1         -
test_target1/test_source1/fs1/sub                      userrefs  -         -
test_target1/test_source1/fs1/sub@test-20101111000000  userrefs  0         -
test_target1/test_source1/fs1/sub@test-20101111000001  userrefs  1         -
test_target1/test_source2                              userrefs  -         -
test_target1/test_source2/fs2                          userrefs  -         -
test_target1/test_source2/fs2/sub                      userrefs  -         -
test_target1/test_source2/fs2/sub@test-20101111000000  userrefs  0         -
test_target1/test_source2/fs2/sub@test-20101111000001  userrefs  1         -
""")




    def  test_ignore_othersnaphots(self):

        r=shelltest("zfs snapshot test_source1/fs1@othersimple")
        r=shelltest("zfs snapshot test_source1/fs1@otherdate-20001111000000")

        with patch('time.strftime', return_value="20101111000000"):
            self.assertFalse(ZfsAutobackup("test test_target1 --verbose".split(" ")).run())

            r=shelltest("zfs list -H -o name -r -t all")
            self.assertMultiLineEqual(r,"""
test_source1
test_source1/fs1
test_source1/fs1@othersimple
test_source1/fs1@otherdate-20001111000000
test_source1/fs1@test-20101111000000
test_source1/fs1/sub
test_source1/fs1/sub@test-20101111000000
test_source2
test_source2/fs2
test_source2/fs2/sub
test_source2/fs2/sub@test-20101111000000
test_source2/fs3
test_source2/fs3/sub
test_target1
test_target1/test_source1
test_target1/test_source1/fs1
test_target1/test_source1/fs1@test-20101111000000
test_target1/test_source1/fs1/sub
test_target1/test_source1/fs1/sub@test-20101111000000
test_target1/test_source2
test_target1/test_source2/fs2
test_target1/test_source2/fs2/sub
test_target1/test_source2/fs2/sub@test-20101111000000
""")

    def  test_othersnaphots(self):

        r=shelltest("zfs snapshot test_source1/fs1@othersimple")
        r=shelltest("zfs snapshot test_source1/fs1@otherdate-20001111000000")

        with patch('time.strftime', return_value="20101111000000"):
            self.assertFalse(ZfsAutobackup("test test_target1 --verbose --other-snapshots".split(" ")).run())

            r=shelltest("zfs list -H -o name -r -t all")
            self.assertMultiLineEqual(r,"""
test_source1
test_source1/fs1
test_source1/fs1@othersimple
test_source1/fs1@otherdate-20001111000000
test_source1/fs1@test-20101111000000
test_source1/fs1/sub
test_source1/fs1/sub@test-20101111000000
test_source2
test_source2/fs2
test_source2/fs2/sub
test_source2/fs2/sub@test-20101111000000
test_source2/fs3
test_source2/fs3/sub
test_target1
test_target1/test_source1
test_target1/test_source1/fs1
test_target1/test_source1/fs1@othersimple
test_target1/test_source1/fs1@otherdate-20001111000000
test_target1/test_source1/fs1@test-20101111000000
test_target1/test_source1/fs1/sub
test_target1/test_source1/fs1/sub@test-20101111000000
test_target1/test_source2
test_target1/test_source2/fs2
test_target1/test_source2/fs2/sub
test_target1/test_source2/fs2/sub@test-20101111000000
""")

