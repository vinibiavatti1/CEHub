from enum import Enum


class InstancePatchEnum(Enum):
    """
    CE patches enum
    """
    PATCH_133 = 'Patch v1.33'
    PATCH_141 = 'Patch v1.41'
    PATCH_142 = 'Patch v1.42 (SEB Fix)'
    PATCH_143 = 'Patch v1.43 (Dafoosa\'s Patch) (Recommended)'
