from enum import Enum
from logging import exception, basicConfig
from pprint import pprint
from typing import List, Optional

from dataclass_property import dataclass, field_property, field
import jsons


basicConfig()


# fully good
good = '''{
"herp": {"derp": "yarp", "narp": false},
"yes": {"whyNot": [{"Try": false, "Do": "DoNot"}]}
}'''

# there is no try (missing optional value)
stillgood = '''{
"herp": {"derp": "yarp", "narp": false},
"yes": {"whyNot": [{"Do": "DoNot"}]}
}'''

# missing mandatory property
missing = '''{
"herp": {"derp": "yarp"},
"yes": {"whyNot": [{"Try": false, "Do": "DoNot"}]}
}'''

# bad property value
invalid = '''{
"herp": {"derp": "yorp", "narp": false},
"yes": {"whyNot": [{"Try": false, "Do": "DoNot"}]}
}'''



@dataclass
class Root:
    herp: 'herp'
    yes: 'yes'

@dataclass
class herp:
    narp: bool

    @field_property(default=None)
    def derp(self) -> Optional[str]:
        return self._derp
    @derp.setter
    def derp(self, value):
        if value not in ['yarp', 'narp']:
            raise ValueError(value)
        self._derp = value


@dataclass
class yes:
    whyNot: List['yoda']


@dataclass
class yoda:
    Do: 'doIt'
    Try: Optional[bool] = None


class doIt(Enum):
    Do = 1
    DoNot = 2


for name, testcase in [('good', good), ('stillgood', stillgood), ('missing', missing), ('invalid', invalid)]:
    print(f'\n\n{name}\n')
    try:
        root = jsons.loads(testcase, Root, strict=True)
        pprint(root)
        outjson = jsons.dumps(root, strip_privates=True)
        pprint(outjson)
    except:
        exception('blowedup')
