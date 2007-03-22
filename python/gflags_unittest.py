#!/usr/bin/env python

# Copyright (c) 2007, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"Unittest for flags.py module"

__pychecker__ = "no-local" # for unittest


import sys
import os
import shutil
import unittest

# We use the name 'flags' internally in this test, for historical reasons.
# Don't do this yourself! :-)  Just do 'import gflags; FLAGS=gflags.FLAGS; etc'
import gflags as flags
FLAGS=flags.FLAGS

class FlagsUnitTest(unittest.TestCase):
  "Flags Unit Test"

  def test_flags(self):
    
    ##############################################
    # Test normal usage with no (expected) errors.

    # Define flags
    number_test_framework_flags = len(FLAGS.RegisteredFlags())
    repeatHelp = "how many times to repeat (0-5)"
    flags.DEFINE_integer("repeat", 4, repeatHelp,
                         lower_bound=0, short_name='r')
    flags.DEFINE_string("name", "Bob", "namehelp")
    flags.DEFINE_boolean("debug", 0, "debughelp")
    flags.DEFINE_boolean("q", 1, "quiet mode")
    flags.DEFINE_boolean("quack", 0, "superstring of 'q'")
    flags.DEFINE_boolean("noexec", 1, "boolean flag with no as prefix")
    flags.DEFINE_integer("x", 3, "how eXtreme to be")
    flags.DEFINE_integer("l", 0x7fffffff00000000L, "how long to be")
    assert FLAGS.repeat == 4, "integer default values not set:" + FLAGS.repeat
    assert FLAGS.name == 'Bob', "default values not set:" + FLAGS.name
    assert FLAGS.debug == 0, "boolean default values not set:" + FLAGS.debug
    assert FLAGS.q == 1, "boolean default values not set:" + FLAGS.q
    assert FLAGS.x == 3, "integer default values not set:" + FLAGS.x
    assert FLAGS.l == 0x7fffffff00000000L, "integer default values not set:" + FLAGS.l
    
    flag_values = FLAGS.FlagValuesDict()
    assert flag_values['repeat'] == 4
    assert flag_values['name'] == 'Bob'
    assert flag_values['debug'] == 0
    assert flag_values['r'] == 4       # short for of repeat
    assert flag_values['q'] == 1
    assert flag_values['quack'] == 0
    assert flag_values['x'] == 3
    assert flag_values['l'] == 0x7fffffff00000000L

    # Verify string form of defaults
    assert FLAGS['repeat'].default_as_str == "'4'"
    assert FLAGS['name'].default_as_str == "'Bob'"
    assert FLAGS['debug'].default_as_str == "'false'"
    assert FLAGS['q'].default_as_str == "'true'"
    assert FLAGS['quack'].default_as_str == "'false'"
    assert FLAGS['noexec'].default_as_str == "'true'"
    assert FLAGS['x'].default_as_str == "'3'"
    assert FLAGS['l'].default_as_str == "'9223372032559808512'"

    # Verify that the iterator for flags yields all the keys
    keys = list(FLAGS)
    keys.sort()
    reg_flags = FLAGS.RegisteredFlags()
    reg_flags.sort()
    self.assertEqual(keys, reg_flags)
    
    # Parse flags
    # .. empty command line
    argv = ('./program',)
    argv = FLAGS(argv)
    assert len(argv) == 1, "wrong number of arguments pulled"
    assert argv[0]=='./program', "program name not preserved"

    # .. non-empty command line
    argv = ('./program', '--debug', '--name=Bob', '-q', '--x=8')
    argv = FLAGS(argv)
    assert len(argv) == 1, "wrong number of arguments pulled"
    assert argv[0]=='./program', "program name not preserved"
    assert FLAGS['debug'].present == 1
    FLAGS['debug'].present = 0 # Reset
    assert FLAGS['name'].present == 1
    FLAGS['name'].present = 0 # Reset
    assert FLAGS['q'].present == 1
    FLAGS['q'].present = 0 # Reset
    assert FLAGS['x'].present == 1
    FLAGS['x'].present = 0 # Reset

    # Flags list
    
    assert len(FLAGS.RegisteredFlags()) == 9 + number_test_framework_flags
    assert 'name' in FLAGS.RegisteredFlags()
    assert 'debug' in FLAGS.RegisteredFlags()
    assert 'repeat' in FLAGS.RegisteredFlags()
    assert 'r' in FLAGS.RegisteredFlags()
    assert 'q' in FLAGS.RegisteredFlags()
    assert 'quack' in FLAGS.RegisteredFlags()
    assert 'x' in FLAGS.RegisteredFlags()
    assert 'l' in FLAGS.RegisteredFlags()

    # has_key
    assert FLAGS.has_key('name')
    assert not FLAGS.has_key('name2')
    assert 'name' in FLAGS
    assert 'name2' not in FLAGS

    # try deleting a flag
    del FLAGS.r
    assert len(FLAGS.RegisteredFlags()) == 8 + number_test_framework_flags
    assert not 'r' in FLAGS.RegisteredFlags()

    # .. command line with extra stuff
    argv = ('./program', '--debug', '--name=Bob', 'extra')
    argv = FLAGS(argv)
    assert len(argv) == 2, "wrong number of arguments pulled"
    assert argv[0]=='./program', "program name not preserved"
    assert argv[1]=='extra', "extra argument not preserved"
    assert FLAGS['debug'].present == 1
    FLAGS['debug'].present = 0 # Reset
    assert FLAGS['name'].present == 1
    FLAGS['name'].present = 0 # Reset

    # Test reset
    argv = ('./program', '--debug')
    argv = FLAGS(argv)
    assert len(argv) == 1, "wrong number of arguments pulled"
    assert argv[0] == './program', "program name not preserved"
    assert FLAGS['debug'].present == 1
    assert FLAGS['debug'].value == True
    FLAGS.Reset()
    assert FLAGS['debug'].present == 0
    assert FLAGS['debug'].value == False

    # Test integer argument passing
    argv = ('./program', '--x', '0x12345')
    argv = FLAGS(argv)
    # 0x12345 == 74565
    self.assertEquals(FLAGS.x, 74565)
    self.assertEquals(type(FLAGS.x), int)

    argv = ('./program', '--x', '0x123456789A')
    argv = FLAGS(argv)
    # 0x123456789A == 78187493530L
    self.assertEquals(FLAGS.x, 78187493530L)
    self.assertEquals(type(FLAGS.x), long)

    # Treat 0-prefixed parameters as base-10, not base-8
    argv = ('./program', '--x', '012345')
    argv = FLAGS(argv)
    self.assertEquals(FLAGS.x, 12345)
    self.assertEquals(type(FLAGS.x), int)

    argv = ('./program', '--x', '0123459')
    argv = FLAGS(argv)
    self.assertEquals(FLAGS.x, 123459)
    self.assertEquals(type(FLAGS.x), int)

    argv = ('./program', '--x', '0x123efg')
    try:
      argv = FLAGS(argv)
      raise AssertionError("failed to detect invalid hex argument")
    except flags.IllegalFlagValue:
      pass

    argv = ('./program', '--x', '0X123efg')
    try:
      argv = FLAGS(argv)
      raise AssertionError("failed to detect invalid hex argument")
    except flags.IllegalFlagValue:
      pass

    # Test boolean argument parsing
    flags.DEFINE_boolean("test0", None, "test boolean parsing")
    argv = ('./program', '--notest0')
    argv = FLAGS(argv)
    assert FLAGS.test0 == 0

    flags.DEFINE_boolean("test1", None, "test boolean parsing")
    argv = ('./program', '--test1')
    argv = FLAGS(argv)
    assert FLAGS.test1 == 1

    FLAGS.test0 = None
    argv = ('./program', '--test0=false')
    argv = FLAGS(argv)
    assert FLAGS.test0 == 0

    FLAGS.test1 = None
    argv = ('./program', '--test1=true')
    argv = FLAGS(argv)
    assert FLAGS.test1 == 1

    FLAGS.test0 = None
    argv = ('./program', '--test0=0')
    argv = FLAGS(argv)
    assert FLAGS.test0 == 0

    FLAGS.test1 = None
    argv = ('./program', '--test1=1')
    argv = FLAGS(argv)
    assert FLAGS.test1 == 1

    # Test booleans that already have 'no' as a prefix
    FLAGS.noexec = None
    argv = ('./program', '--nonoexec', '--name', 'Bob')
    argv = FLAGS(argv)
    assert FLAGS.noexec == 0

    FLAGS.noexec = None
    argv = ('./program', '--name', 'Bob', '--noexec')
    argv = FLAGS(argv)
    assert FLAGS.noexec == 1

    # Test unassigned booleans
    flags.DEFINE_boolean("testnone", None, "test boolean parsing")
    argv = ('./program',)
    argv = FLAGS(argv)
    assert FLAGS.testnone == None

    # Test get with default
    flags.DEFINE_boolean("testget1", None, "test parsing with defaults")
    flags.DEFINE_boolean("testget2", None, "test parsing with defaults")
    flags.DEFINE_boolean("testget3", None, "test parsing with defaults")
    flags.DEFINE_integer("testget4", None, "test parsing with defaults")
    argv = ('./program','--testget1','--notestget2')
    argv = FLAGS(argv)
    assert FLAGS.get('testget1', 'foo') == 1
    assert FLAGS.get('testget2', 'foo') == 0
    assert FLAGS.get('testget3', 'foo') == 'foo'
    assert FLAGS.get('testget4', 'foo') == 'foo'

    # test list code
    lists = [['hello','moo','boo','1'],
             [],]
            
    flags.DEFINE_list('testlist', '', 'test lists parsing')
    flags.DEFINE_spaceseplist('testspacelist', '', 'tests space lists parsing')

    for name, sep in (('testlist', ','), ('testspacelist', ' '), 
                      ('testspacelist', '\n')):
      for lst in lists:
        argv = ('./program', '--%s=%s' % (name, sep.join(lst)))
        argv = FLAGS(argv)
        self.assertEquals(getattr(FLAGS, name), lst)
   
    # Test help text
    flagsHelp = str(FLAGS)
    assert flagsHelp.find("repeat") != -1, "cannot find flag in help"
    assert flagsHelp.find(repeatHelp) != -1, "cannot find help string in help"

    # Test flag specified twice
    argv = ('./program', '--repeat=4', '--repeat=2', '--debug', '--nodebug')
    argv = FLAGS(argv)
    self.assertEqual(FLAGS.get('repeat', None), 2)
    self.assertEqual(FLAGS.get('debug', None), 0)

    # Test MultiFlag with single default value
    flags.DEFINE_multistring('s_str', 'sing1',
                             'string option that can occur multiple times',
                             short_name='s')
    self.assertEqual(FLAGS.get('s_str', None), [ 'sing1', ])
    
    # Test MultiFlag with list of default values
    multi_string_defs = [ 'def1', 'def2', ]
    flags.DEFINE_multistring('m_str', multi_string_defs,
                             'string option that can occur multiple times',
                             short_name='m')
    self.assertEqual(FLAGS.get('m_str', None), multi_string_defs)
    
    # Test flag specified multiple times with a MultiFlag
    argv = ('./program', '--m_str=str1', '-m', 'str2')
    argv = FLAGS(argv)
    self.assertEqual(FLAGS.get('m_str', None), [ 'str1', 'str2', ])
    
    # Test single-letter flags; should support both single and double dash
    argv = ('./program', '-q', '-x8')
    argv = FLAGS(argv)
    self.assertEqual(FLAGS.get('q', None), 1)
    self.assertEqual(FLAGS.get('x', None), 8)

    argv = ('./program', '--q', '--x', '9', '--noqu')
    argv = FLAGS(argv)
    self.assertEqual(FLAGS.get('q', None), 1)
    self.assertEqual(FLAGS.get('x', None), 9)
    # --noqu should match '--noquack since it's a unique prefix
    self.assertEqual(FLAGS.get('quack', None), 0)

    argv = ('./program', '--noq', '--x=10', '--qu')
    argv = FLAGS(argv)
    self.assertEqual(FLAGS.get('q', None), 0)
    self.assertEqual(FLAGS.get('x', None), 10)
    self.assertEqual(FLAGS.get('quack', None), 1)

    ####################################
    # Test flag serialization code:

    oldtestlist = FLAGS.testlist
    oldtestspacelist = FLAGS.testspacelist
    
    argv = ('./program',
            FLAGS['test0'].Serialize(),
            FLAGS['test1'].Serialize(),
            FLAGS['testnone'].Serialize(),
            FLAGS['s_str'].Serialize())
    argv = FLAGS(argv)
    self.assertEqual(FLAGS['test0'].Serialize(), '--notest0')
    self.assertEqual(FLAGS['test1'].Serialize(), '--test1')
    self.assertEqual(FLAGS['testnone'].Serialize(), '')
    self.assertEqual(FLAGS['s_str'].Serialize(), '--s_str=sing1')

    testlist1 = ['aa', 'bb']
    testspacelist1 = ['aa', 'bb', 'cc']
    FLAGS.testlist = list(testlist1)
    FLAGS.testspacelist = list(testspacelist1)
    argv = ('./program',
            FLAGS['testlist'].Serialize(),
            FLAGS['testspacelist'].Serialize())    
    argv = FLAGS(argv)
    self.assertEqual(FLAGS.testlist, testlist1)
    self.assertEqual(FLAGS.testspacelist, testspacelist1)

    testlist1 = ['aa some spaces', 'bb']
    testspacelist1 = ['aa', 'bb,some,commas,', 'cc']
    FLAGS.testlist = list(testlist1)
    FLAGS.testspacelist = list(testspacelist1)
    argv = ('./program',
            FLAGS['testlist'].Serialize(),
            FLAGS['testspacelist'].Serialize())
    argv = FLAGS(argv)
    self.assertEqual(FLAGS.testlist, testlist1)
    self.assertEqual(FLAGS.testspacelist, testspacelist1)

    FLAGS.testlist = oldtestlist
    FLAGS.testspacelist = oldtestspacelist

    ####################################
    # Test flag-update:

    def ArgsString():
      flagnames = FLAGS.RegisteredFlags()
      flagnames.sort()
      nonbool_flags = ['--%s %s' % (name, FLAGS.get(name, None))
                      for name in flagnames
                      if not isinstance(FLAGS[name], flags.BooleanFlag)]

      truebool_flags = ['--%s' % (name)
                       for name in flagnames
                       if isinstance(FLAGS[name], flags.BooleanFlag) and
                          FLAGS.get(name, None)]
      falsebool_flags = ['--no%s' % (name)
                        for name in flagnames
                        if isinstance(FLAGS[name], flags.BooleanFlag) and
                           not FLAGS.get(name, None)]
      return ' '.join(nonbool_flags + truebool_flags + falsebool_flags)

    argv = ('./program', '--repeat=3', '--name=giants', '--nodebug')
    FLAGS(argv)
    self.assertEqual(FLAGS.get('repeat', None), 3)
    self.assertEqual(FLAGS.get('name', None), 'giants')
    self.assertEqual(FLAGS.get('debug', None), 0)
    self.assertEqual(ArgsString(),
      "--l 9223372032559808512 "
      "--m ['str1', 'str2'] --m_str ['str1', 'str2'] " 
      "--name giants " 
      "--repeat 3 " 
      "--s ['sing1'] --s_str ['sing1'] "
      "--testget4 None --testlist [] "
      "--testspacelist [] --x 10 "
      "--noexec --quack "
      "--test1 "
      "--testget1 --no? --nodebug --nohelp --nohelpshort "
      "--noq --notest0 --notestget2 "
      "--notestget3 --notestnone")

    argv = ('./program', '--debug', '--m_str=upd1', '-s', 'upd2')
    FLAGS(argv)
    self.assertEqual(FLAGS.get('repeat', None), 3)
    self.assertEqual(FLAGS.get('name', None), 'giants')
    self.assertEqual(FLAGS.get('debug', None), 1)

    # items appended to existing non-default value lists for --m/--m_str
    # new value overwrites default value (not appended to it) for --s/--s_str
    self.assertEqual(ArgsString(),
      "--l 9223372032559808512 "
      "--m ['str1', 'str2', 'upd1'] "
      "--m_str ['str1', 'str2', 'upd1'] "
      "--name giants " 
      "--repeat 3 " 
      "--s ['upd2'] --s_str ['upd2'] "
      "--testget4 None --testlist [] "
      "--testspacelist [] --x 10 "
      "--debug --noexec --quack "
      "--test1 "
      "--testget1 --no? --nohelp --nohelpshort "
      "--noq --notest0 --notestget2 "
      "--notestget3 --notestnone")


    ####################################
    # Test all kind of error conditions.
    
    # Duplicate flag detection
    try:
      flags.DEFINE_boolean("run", 0, "runhelp", short_name='q')
      raise AssertionError("duplicate flag detection failed")
    except flags.DuplicateFlag, e:
      pass

    try:
      flags.DEFINE_boolean("zoom1", 0, "runhelp z1", short_name='z')
      flags.DEFINE_boolean("zoom2", 0, "runhelp z2", short_name='z')
      raise AssertionError("duplicate flag detection failed")
    except flags.DuplicateFlag, e:
      pass

    # Make sure allow_override works
    try:
      flags.DEFINE_boolean("dup1", 0, "runhelp d11", short_name='u',
                           allow_override=0)
      flag = FLAGS.FlagDict()['dup1']
      self.assertEqual(flag.default, 0)

      flags.DEFINE_boolean("dup1", 1, "runhelp d12", short_name='u',
                           allow_override=1)
      flag = FLAGS.FlagDict()['dup1']
      self.assertEqual(flag.default, 1)
    except flags.DuplicateFlag, e:
      raise AssertionError("allow_override did not permit a flag duplication")

    # Make sure allow_override works
    try:
      flags.DEFINE_boolean("dup2", 0, "runhelp d21", short_name='u',
                           allow_override=1)
      flag = FLAGS.FlagDict()['dup2']
      self.assertEqual(flag.default, 0)

      flags.DEFINE_boolean("dup2", 1, "runhelp d22", short_name='u',
                           allow_override=0)
      flag = FLAGS.FlagDict()['dup2']
      self.assertEqual(flag.default, 1)
    except flags.DuplicateFlag, e:
      raise AssertionError("allow_override did not permit a flag duplication")

    # Make sure allow_override doesn't work with None default
    try:
      flags.DEFINE_boolean("dup3", 0, "runhelp d31", short_name='u',
                           allow_override=0)
      flag = FLAGS.FlagDict()['dup3']
      self.assertEqual(flag.default, 0)

      flags.DEFINE_boolean("dup3", None, "runhelp d32", short_name='u',
                           allow_override=1)
      raise AssertionError('Cannot override a flag with a default of None')
    except flags.DuplicateFlag, e:
      pass

    # Make sure that when we override, the help string gets updated correctly
    flags.DEFINE_boolean("dup3", 0, "runhelp d31", short_name='u',
                         allow_override=1)
    flags.DEFINE_boolean("dup3", 1, "runhelp d32", short_name='u',
                         allow_override=1)
    self.assert_(str(FLAGS).find('runhelp d31') == -1)
    self.assert_(str(FLAGS).find('runhelp d32') != -1)

    # Integer out of bounds
    try:
      argv = ('./program', '--repeat=-4')
      FLAGS(argv)
      raise AssertionError('integer bounds exception not thrown:'
                           + str(FLAGS.repeat))
    except flags.IllegalFlagValue:
      pass

    # Non-integer
    try:
      argv = ('./program', '--repeat=2.5')
      FLAGS(argv)
      raise AssertionError("malformed integer value exception not thrown")
    except flags.IllegalFlagValue:
      pass

    # Missing required arugment
    try:
      argv = ('./program', '--name')
      FLAGS(argv)
      raise AssertionError("Flag argument required exception not thrown")
    except flags.FlagsError:
      pass

    # Argument erroneously supplied for boolean
    try:
      argv = ('./program', '--debug=goofup')
      FLAGS(argv)
      raise AssertionError("No argument allowed exception not thrown")
    except flags.FlagsError:
      pass

    # Unknown argument --nosuchflag
    try:
      argv = ('./program', '--nosuchflag', '--name=Bob', 'extra')
      FLAGS(argv)
      raise AssertionError("Unknown argument exception not thrown")
    except flags.FlagsError:
      pass

    # Non-numeric argument for integer flag --repeat
    try:
      argv = ('./program', '--repeat', 'Bob', 'extra')
      FLAGS(argv)
      raise AssertionError("Illegal flag value exception not thrown")
    except flags.IllegalFlagValue:
      pass
      
  ################################################
  # Code to test the flagfile=<> loading behavior
  ################################################
  def _SetupTestFiles(self):  
    """ Creates and sets up some dummy flagfile files with bogus flags"""
    
    # Figure out where to create temporary files
    tmp_path = '/tmp/flags_unittest'
    if os.path.exists(tmp_path):
      shutil.rmtree(tmp_path)
    os.makedirs(tmp_path)

    try:
      tmp_flag_file_1 = open((tmp_path + '/UnitTestFile1.tst'), 'w') 
      tmp_flag_file_2 = open((tmp_path + '/UnitTestFile2.tst'), 'w')
      tmp_flag_file_3 = open((tmp_path + '/UnitTestFile3.tst'), 'w')
    except IOError, e_msg:
      print e_msg
      print 'FAIL\n File Creation problem in Unit Test' 
      sys.exit(1)
    
    # put some dummy flags in our test files
    tmp_flag_file_1.write('#A Fake Comment\n')
    tmp_flag_file_1.write('--UnitTestMessage1=tempFile1!\n')
    tmp_flag_file_1.write('\n')
    tmp_flag_file_1.write('--UnitTestNumber=54321\n')
    tmp_flag_file_1.write('--noUnitTestBoolFlag\n')
    file_list = [tmp_flag_file_1.name]
    # this one includes test file 1
    tmp_flag_file_2.write('//A Different Fake Comment\n')
    tmp_flag_file_2.write('--flagfile=%s\n' % tmp_flag_file_1.name)
    tmp_flag_file_2.write('--UnitTestMessage2=setFromTempFile2\n')
    tmp_flag_file_2.write('\t\t\n')
    tmp_flag_file_2.write('--UnitTestNumber=6789a\n')
    file_list.append(tmp_flag_file_2.name)
    # this file points to itself
    tmp_flag_file_3.write('--flagfile=%s\n' % tmp_flag_file_3.name)
    tmp_flag_file_3.write('--UnitTestMessage1=setFromTempFile3\n')
    tmp_flag_file_3.write('#YAFC\n')
    tmp_flag_file_3.write('--UnitTestBoolFlag\n')
    file_list.append(tmp_flag_file_3.name)
    
    tmp_flag_file_1.close() 
    tmp_flag_file_2.close()
    tmp_flag_file_3.close()

    return file_list # these are just the file names
  # end SetupFiles def
  
  def _RemoveTestFiles(self, tmp_file_list):
    """Closes the files we just created.  tempfile deletes them for us """
    for file_name in tmp_file_list: 
      try:
        os.remove(file_name) 
      except OSError, e_msg:
        print '%s\n, Problem deleting test file' % e_msg
  #end RemoveTestFiles def
  
  def __DeclareSomeFlags(self):
    flags.DEFINE_string('UnitTestMessage1', 'Foo!', 'You Add Here.')
    flags.DEFINE_string('UnitTestMessage2', 'Bar!', 'Hello, Sailor!')
    flags.DEFINE_boolean('UnitTestBoolFlag', 0, 'Some Boolean thing')
    flags.DEFINE_integer('UnitTestNumber', 12345, 'Some integer',
                         lower_bound=0)
  
  def _UndeclareSomeFlags(self): 
    FLAGS.__delattr__('UnitTestMessage1')
    FLAGS.__delattr__('UnitTestMessage2')
    FLAGS.__delattr__('UnitTestBoolFlag')
    FLAGS.__delattr__('UnitTestNumber')
    
  #### Flagfile Unit Tests ####  
  def testMethod_flagfiles_1(self):
    """ Test trivial case with no flagfile based options. """
    self.__DeclareSomeFlags()
    fake_cmd_line = 'fooScript --UnitTestBoolFlag'
    fake_argv = fake_cmd_line.split(' ')
    FLAGS(fake_argv)
    self.assertEqual( FLAGS.UnitTestBoolFlag, 1)
    self.assertEqual( fake_argv, FLAGS.ReadFlagsFromFiles(fake_argv))
    self._UndeclareSomeFlags()
  # end testMethodOne
  
  def testMethod_flagfiles_2(self):
    """Tests parsing one file + arguments off simulated argv"""
    self.__DeclareSomeFlags()
    tmp_files = self._SetupTestFiles()
    # specify our temp file on the fake cmd line
    fake_cmd_line = 'fooScript --q --flagfile=%s' % tmp_files[0]
    fake_argv = fake_cmd_line.split(' ')
    
    # We should see the original cmd line with the file's contents spliced in. 
    # Note that these will be in REVERSE order from order encountered in file
    # This is done so arguements we encounter sooner will have priority.
    expected_results = ['fooScript',
                          '--UnitTestMessage1=tempFile1!',
                          '--UnitTestNumber=54321',
                          '--noUnitTestBoolFlag',
                          '--q']
    test_results = FLAGS.ReadFlagsFromFiles(fake_argv)
    self.assertEqual(expected_results, test_results) 
    self._RemoveTestFiles(tmp_files)  
    self._UndeclareSomeFlags()
  # end testTwo def

  def testMethod_flagfiles_3(self):
    """Tests parsing nested files + arguments of simulated argv"""
    self.__DeclareSomeFlags()
    tmp_files = self._SetupTestFiles()
    # specify our temp file on the fake cmd line
    fake_cmd_line = ('fooScript --UnitTestNumber=77 --flagfile=%s'
                     % tmp_files[1])
    fake_argv = fake_cmd_line.split(' ')
    
    expected_results = ['fooScript',
                          '--UnitTestMessage1=tempFile1!',
                          '--UnitTestNumber=54321',
                          '--noUnitTestBoolFlag',
                          '--UnitTestMessage2=setFromTempFile2',
                          '--UnitTestNumber=6789a',
                          '--UnitTestNumber=77']
    test_results = FLAGS.ReadFlagsFromFiles(fake_argv)
    self.assertEqual(expected_results, test_results) 
    self._RemoveTestFiles(tmp_files)
    self._UndeclareSomeFlags()
  # end testThree def
    
  def testMethod_flagfiles_4(self):
    """Tests parsing self referetial files + arguments of simulated argv.
      This test should print a warning to stderr of some sort.
    """
    self.__DeclareSomeFlags()
    tmp_files = self._SetupTestFiles()
    # specify our temp file on the fake cmd line
    fake_cmd_line = ('fooScript --flagfile=%s --noUnitTestBoolFlag'
                     % tmp_files[2])
    fake_argv = fake_cmd_line.split(' ')
    expected_results = ['fooScript',
                          '--UnitTestMessage1=setFromTempFile3',
                          '--UnitTestBoolFlag',
                          '--noUnitTestBoolFlag' ]

    test_results = FLAGS.ReadFlagsFromFiles(fake_argv)
    self.assertEqual(expected_results, test_results) 
    self._RemoveTestFiles(tmp_files)  
    self._UndeclareSomeFlags()

  def test_flagfiles_user_path_expansion(self):
    """Test that user directory referenced paths (ie. ~/foo) are correctly 
      expanded.  This test depends on whatever account's running the unit test 
      to have read/write access to their own home directory, otherwise it'll 
      FAIL.
    """
    self.__DeclareSomeFlags()
    fake_flagfile_item_style_1 = '--flagfile=~/foo.file'
    fake_flagfile_item_style_2 = '-flagfile=~/foo.file'
    
    expected_results = os.path.expanduser('~/foo.file')

    test_results = FLAGS.ExtractFilename(fake_flagfile_item_style_1)
    self.assertEqual(expected_results, test_results)

    test_results = FLAGS.ExtractFilename(fake_flagfile_item_style_2)
    self.assertEqual(expected_results, test_results)

    self._UndeclareSomeFlags()

  # end testFour def

  def test_no_touchy_non_flags(self):
    """
    Test that the flags parser does not mutilate arguments which are
    not supposed to be flags
    """
    self.__DeclareSomeFlags()
    fake_argv = ['fooScript', '--UnitTestBoolFlag',
                 'command', '--command_arg1', '--UnitTestBoom', '--UnitTestB']
    argv = FLAGS(fake_argv)
    self.assertEqual(argv, fake_argv[:1] + fake_argv[2:])
    self._UndeclareSomeFlags()

  def test_SetDefault(self):
    """
    Test changing flag defaults.
    """
    self.__DeclareSomeFlags()
    # Test that SetDefault changes both the default and the value,
    # and that the value is changed when one is given as an option.
    FLAGS['UnitTestMessage1'].SetDefault('New value')
    self.assertEqual(FLAGS.UnitTestMessage1, 'New value')
    self.assertEqual(FLAGS['UnitTestMessage1'].default_as_str,"'New value'")
    FLAGS([ 'dummyscript', '--UnitTestMessage1=Newer value' ])
    self.assertEqual(FLAGS.UnitTestMessage1, 'Newer value')
    # Test that setting the default to None works correctly.
    FLAGS['UnitTestNumber'].SetDefault(None)
    self.assertEqual(FLAGS.UnitTestNumber, None)
    self.assertEqual(FLAGS['UnitTestNumber'].default_as_str, None)
    FLAGS([ 'dummyscript', '--UnitTestNumber=56' ])
    self.assertEqual(FLAGS.UnitTestNumber, 56)
    # Test that setting invalid defaults raises exceptions
    self.assertRaises(flags.IllegalFlagValue,
                      FLAGS['UnitTestNumber'].SetDefault, 'oops')
    self.assertRaises(flags.IllegalFlagValue,
                      FLAGS['UnitTestNumber'].SetDefault, -1)
    self.assertRaises(flags.IllegalFlagValue,
                      FLAGS['UnitTestBoolFlag'].SetDefault, 'oops')
    
    self._UndeclareSomeFlags()

  def testMethod_ShortestUniquePrefixes(self):
    """
    Test FlagValues.ShortestUniquePrefixes
    """
    flags.DEFINE_string('a', '', '')
    flags.DEFINE_string('abc', '', '')
    flags.DEFINE_string('common_a_string', '', '')
    flags.DEFINE_boolean('common_b_boolean', 0, '')
    flags.DEFINE_boolean('common_c_boolean', 0, '')
    flags.DEFINE_boolean('common', 0, '')
    flags.DEFINE_integer('commonly', 0, '')
    flags.DEFINE_boolean('zz', 0, '')
    flags.DEFINE_integer('nozz', 0, '')

    shorter_flags = FLAGS.ShortestUniquePrefixes(FLAGS.FlagDict())

    expected_results = {'nocommon_b_boolean': 'nocommon_b',
                        'common_c_boolean': 'common_c',
                        'common_b_boolean': 'common_b',
                        'a': 'a',
                        'abc': 'ab',
                        'zz': 'z',
                        'nozz': 'nozz',
                        'common_a_string': 'common_a',
                        'commonly': 'commonl',
                        'nocommon_c_boolean': 'nocommon_c',
                        'nocommon': 'nocommon',
                        'common': 'common'}

    for name, shorter in expected_results.iteritems():
      self.assertEquals(shorter_flags[name], shorter)

    FLAGS.__delattr__('a')
    FLAGS.__delattr__('abc')
    FLAGS.__delattr__('common_a_string')
    FLAGS.__delattr__('common_b_boolean')
    FLAGS.__delattr__('common_c_boolean')
    FLAGS.__delattr__('common')
    FLAGS.__delattr__('commonly')
    FLAGS.__delattr__('zz')
    FLAGS.__delattr__('nozz')


if __name__ == '__main__':
  unittest.main()
