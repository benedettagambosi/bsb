import unittest
from test_setup import skip_parallel


class TestCLI(unittest.TestCase):
    @skip_parallel
    def test_availability(self):
        import bsb, subprocess

        our_version = bytes(bsb.__version__, encoding="utf-8")
        # Split on newlines to ignore any prepended spammy output in case of environment
        # specific warnings when running BSB commands.
        cli_version = subprocess.check_output("bsb --version".split()).split(b"\n")[-2]
        # Remove \r on Windows
        cli_version = cli_version.replace(b"\r", b"")
        self.assertEqual(our_version, cli_version, "Could not access the BSB through CLI")

    def test_defaults(self):
        import bsb.options, bsb.exceptions

        # Test the default verbosity
        self.assertEqual(1, bsb.options.verbosity)
        # Test that an option without script descriptor isn't registered
        self.assertRaises(bsb.exceptions.OptionError, lambda: bsb.options.config)

    def test_env_descriptor(self):
        import os, bsb.options
        from bsb.option import BsbOption

        class TestOption(BsbOption, env=("GRZLGRK",), script=("GRZLGRK",)):
            pass

        TestOption.register()
        o = TestOption()

        # Assert that we start out clean
        self.assertEqual(o.get(), None)
        # Test env functionality
        os.environ["GRZLGRK"] = "Hello"
        self.assertEqual(o.get(), "Hello")
        # Test env removed functionality
        del os.environ["GRZLGRK"]
        self.assertEqual(o.get(), None)
        # Test env override by script
        bsb.options.GRZLGRK = "Bye"
        os.environ["GRZLGRK"] = "Hello"
        self.assertEqual(o.get(), "Bye")
        del os.environ["GRZLGRK"]


class TestOptions(unittest.TestCase):
    def test_get_cli_tags(self):
        from bsb.option import BsbOption

        class t1(BsbOption, cli=("a",)):
            pass

        class t2(BsbOption, cli=("a", "b")):
            pass

        class t3(BsbOption, cli=("a", "ave")):
            pass

        class t4(BsbOption, cli=("cC")):
            pass

        self.assertEqual(["-a"], t1.get_cli_tags())
        self.assertEqual(["-a", "-b"], t2.get_cli_tags())
        self.assertEqual(["-a", "--ave"], t3.get_cli_tags())
        self.assertEqual(["-c", "-C"], t4.get_cli_tags())

    def test_plugins(self):
        # Test that the plugins are loaded and their script options work
        pass

    def test_register(self):
        import bsb.options, bsb.exceptions
        from bsb.option import BsbOption

        # Test that registering an option into the module works
        class t1(BsbOption, script=("aaa",)):
            def get_default(self):
                return 5

        t1.register()
        self.assertEqual(5, bsb.options.aaa)
        t1._unregister()
        self.assertRaises(bsb.exceptions.OptionError, lambda: bsb.options.aaa)