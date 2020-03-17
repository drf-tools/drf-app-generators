from enum import Enum


# ==============================================================================
# ChoiceEnum
# ==============================================================================
class BaseChoiceEnum(Enum):
    """
    The base class for choices enumeration. This enumeration is often uses with
    Django fields.
    """

    @classmethod
    def to_tuple(cls):
        """
        Parse enum to tuple.
        @return: Tuple
        """
        return [(data.name, data.value) for data in cls]

    @classmethod
    def to_json(cls):
        """
        Parse enum to json.
        @return: Json
        """
        return [{'name': data.name, 'value': data.value} for data in cls]

    @classmethod
    def values(cls):
        """
        Get values of enum.
        @return: List of value.
        """
        return [data.value for data in cls]

    @classmethod
    def names(cls):
        """
        Get names of enum.

        @return: List of name.
        """
        return [data.name for data in cls]

    @classmethod
    def get_value(cls, name):
        """
        Get value of enum by name.
        """
        return cls[name].value if name in cls.names() else -1


class MembershipLevelsEnum(BaseChoiceEnum):
    """
    Membership levels enum.
    """
    BASIC = 0
    SILVER = 1
    GOLD = 2


class CouponKindsEnum(BaseChoiceEnum):
    """
    Coupon kinds enum.
    """
    PERCENTAGE = 0
    MONEY = 1


class OrderStatusesEnum(BaseChoiceEnum):
    """
    Order statuses enum.
    """
    PAID = 0
    CANCEL = 1
    PENDING = 2


class UserRolesEnum(BaseChoiceEnum):
    """
    User roles enum.
    """
    ADMIN_ROLE = 0
    USER_ROLE = 1
    CUSTOMER_ROLE = 2


class GendersEnum(BaseChoiceEnum):
    """
    Genders enum.
    """
    NA = -1  # Not available
    MEN = 0
    WOMEN = 1


class ColorsEnum(BaseChoiceEnum):
    """
    Colors enum.
    """
    NA = -1  # Not available
    NAVY_BLUE = 0
    BLUE = 1
    SILVER = 2
    BLACK = 3
    GREY = 4
    GREEN = 5
    PURPLE = 6
    WHITE = 7
    BEIGE = 8
    BROWN = 9
    BRONZE = 10
    TEAL = 11
    COPPER = 12
    PINK = 13
    OFF_WHITE = 14
    MAROON = 15
    RED = 16
    KHAKI = 17
    ORANGE = 18
    COFFEE_BROWN = 19
    YELLOW = 20
    CHARCOAL = 21
    GOLD = 22
    STEEL = 23
    TAN = 24
    MULTI = 25
    MAGENTA = 26
    LAVENDER = 27
    SEA_GREEN = 28
    CREAM = 29
    PEACH = 30
    OLIVE = 31
    SKIN = 32
    BURGUNDY = 33
    GREY_MELANGE = 34
    RUST = 35
    ROSE = 36
    LIME_GREEN = 37
    MAUVE = 38
    TURQUOISE_BLUE = 39
    METALLIC = 40
    MUSTARD = 41
    TAUPE = 42
    NUDE = 43
    MUSHROOM_BROWN = 44
    FLUORESCENT_GREEN = 45


class SeasonsEnum(BaseChoiceEnum):
    """
    Seasons enum.
    """
    NA = -1  # Not available
    SPRING = 0
    SUMMER = 1
    AUTUMN = 2
    WINTER = 3


class UsagesEnum(BaseChoiceEnum):
    """
    Usages enum.
    """
    NA = -1  # Not available
    SPORT = 0
    CASUAL = 1
    ETHNIC = 2
