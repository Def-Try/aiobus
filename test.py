# import tests.cog_utils
from tests import cog_utils
from tests import cog_basic
from tests import core

core.add_tests(cog_utils.tests)
core.add_tests(cog_basic.tests)
core.run()
