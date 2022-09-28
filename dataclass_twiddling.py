import json
import dacite

from dataclasses import dataclass, field, is_dataclass
from enum import Enum
from pprint import pprint
from typing import List, Optional


def asdict(obj):
    retval = dict()
    for k in obj.__dataclass_fields__:
        v = obj.__dict__.get(k)
        if v is not None:
            if is_dataclass(v):
                v = asdict(v)
            retval[k] = v
    return retval


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

# missing derp optional value
yetgood = '''{
"herp": {"narp": false},
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
    derp: Optional[str] = field()

    def __post_init__(self):
        if self.derp is not None and self.derp not in ['yarp', 'narp']:
            raise ValueError(self.derp)

@dataclass
class yes:
    whyNot: List['yoda']


@dataclass
class yoda:
    Do: 'doIt'
    Try: Optional[bool] = field()


class doIt(Enum):
    Do = 'Do'
    DoNot = 'DoNot'


class BetterEncoder(json.JSONEncoder):
    def default(self, o):
        # we got here because o wasn't serializable

        # if enum return the enum value instead
        if isinstance(o, Enum):
            return o.value

        # if dataclass return dataclass.asdict(), stripping nulls
        if is_dataclass(o):
            return {k: v for k, v in asdict(o).items() if v is not None}

        # give up and make the base class complain about it not being serializable
        return super().default(o)


for name, testcase in [('good', good), ('stillgood', stillgood), ('yetgood', yetgood), ('missing', missing), ('invalid', invalid)]:
    print(f'\n\n{name}\n')
    try:
        root = dacite.from_dict(
            data=json.loads(testcase),
            data_class=Root,
            config=dacite.Config(
                type_hooks={doIt: doIt}))
        pprint(root)
        outjson = json.dumps(root, cls=BetterEncoder)
        pprint(outjson)
    except Exception as exc:
        print(exc)
