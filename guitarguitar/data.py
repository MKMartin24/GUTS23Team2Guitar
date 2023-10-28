"""
Data loading and deserialisation

Main entrypoints are the .load_api() methods of Customer, Product and Order
"""


from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Type, TypeVar
import requests


class ApiError(Exception):
    """An error when trying to read from the API"""

    pass


ExpT = TypeVar("ExpT")


def get_typed(
    obj: Dict, key: str, exp_type: Type[ExpT], context: str
) -> Optional[ExpT]:
    """Try read a field from a dict, and check its type if successful"""

    # Attempt to get field
    try:
        val = obj.pop(key)
    except KeyError:
        return None

    # Validate field type
    if not isinstance(val, exp_type) and val is not None:
        raise ApiError(f"{context}: field {key} is of type {type(val)} not {exp_type}")

    return val


def try_get(obj: Dict, key: str, exp_type: Type[ExpT], context: str) -> ExpT:
    """Read a field from a dict with validation. Throws ApiError if failing"""

    # Attempt to get field
    val = get_typed(obj, key, exp_type, context)

    # Check not None
    if val is None:
        raise ApiError(f"{context}: field {key} not found")

    return val


class Colour(Enum):
    """Enum for API Product colours"""

    Red = 1
    Orange = 2
    Yellow = 3
    Green = 4
    Blue = 5
    Purple = 6
    Pink = 7
    Brown = 8
    Gold = 9
    Silver = 10
    Grey = 11
    Black = 12
    White = 13
    Natural = 14
    Multicolor = 15

    UNKNOWN = -1

    @staticmethod
    def from_json(val: int) -> "Colour":
        """Deserialise the json representation of the object"""

        if 1 <= val <= 15:
            return Colour(val)
        else:
            return Colour.UNKNOWN


class Pickup(Enum):
    """Enum for API Product pickup types"""

    ElectroAcoustic = 1
    SS = 2
    SSS = 3
    HH = 4
    HHH = 5
    HS = 6
    HSS = 7
    HSH = 8
    P90 = 9
    S = 10
    H = 11

    UNKNOWN = -1

    @staticmethod
    def from_json(val: int) -> "Pickup":
        """Deserialise the json representation of the object"""

        if 1 <= val <= 11:
            return Pickup(val)
        else:
            return Pickup.UNKNOWN


class BodyShape(Enum):
    """Enum for API Product shapes"""

    SStyle = 1
    TStyle = 2
    DoubleCut = 3
    Offset = 4
    HollowBody = 5
    VStyle = 6
    SmallBody = 7
    Orchestral = 8
    GrandAuditorium = 9
    Dreadnought = 10
    Jumbo = 11
    Explorer = 12
    SingleCut = 13
    Combo = 14
    Head = 15
    Cabinet = 16

    UNKNOWN = -1

    @staticmethod
    def from_json(val: int) -> "BodyShape":
        """Deserialise the json representation of the object"""

        if 1 <= val <= 16:
            return BodyShape(val)
        else:
            return BodyShape.UNKNOWN


class OrderStatus(Enum):
    """Enum for API Order statuses"""

    Placed = 1
    Dispatched = 2
    Delivering = 3
    Delivered = 4
    Completed = 5
    Cancelled = 6

    UNKNOWN = -1

    @staticmethod
    def from_json(val: int) -> "OrderStatus":
        """Deserialise the json representation of the object"""

        if 1 <= val <= 6:
            return OrderStatus(val)
        else:
            return OrderStatus.UNKNOWN


@dataclass(frozen=True)
class Address:
    """Accessor for API Address object"""

    city: str
    street_name: str
    street_address: str
    zip_code: str
    country: str

    @staticmethod
    def from_json(data: Dict, context: str) -> "Address":
        """Deserialise the json representation of the object"""

        data = data.copy()
        ctx = f"{context}:Address"
        ret = Address(
            try_get(data, "city", str, ctx),
            try_get(data, "street_name", str, ctx),
            try_get(data, "street_address", str, ctx),
            try_get(data, "zip_code", str, ctx),
            try_get(data, "country", str, ctx),
        )
        assert len(data) == 0, f"Leftover data {data}"

        return ret


@dataclass(frozen=True)
class Customer:
    """Accessor for API Customer object"""

    Id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    avatar: str
    address: Address
    LoyaltyLevel: int
    Orders: Any

    @staticmethod
    def from_json(data: Dict) -> "Customer":
        """Deserialise the json representation of the object"""

        data = data.copy()
        ctx = "Customer"
        ret = Customer(
            try_get(data, "Id", int, ctx),
            try_get(data, "first_name", str, ctx),
            try_get(data, "last_name", str, ctx),
            try_get(data, "email", str, ctx),
            try_get(data, "phone_number", str, ctx),
            try_get(data, "avatar", str, ctx),
            Address.from_json(try_get(data, "address", dict, ctx), ctx),
            get_typed(data, "LoyaltyLevel", int, ctx) or 0,  # Not always present
            get_typed(data, "Orders", object, ctx),  # Not always present
        )
        assert len(data) == 0, f"Leftover data {data}"

        return ret

    @staticmethod
    def load_api() -> List["Customer"]:
        """Load the customer list from the server"""

        response = requests.get("https://www.guitarguitar.co.uk/hackathon/customers/")

        if response.status_code != 200:
            raise ApiError(
                f"Couldn't contact server for customers: {response.status_code} {response.content}"
            )

        data = response.json()

        if not type(data) == list:
            raise ApiError("Customers response was not json list")

        return [Customer.from_json(entry) for entry in data]


@dataclass(frozen=True)
class Product:
    """Accessor for API Product object"""

    SKU_ID: str
    ASN: str
    Category: str
    Online: bool
    ItemName: str
    Title: str
    BrandName: str
    Description: str
    ProductDetail: str
    SalesPrice: float
    PictureMain: str
    QtyInStock: int
    QtyOnOrder: int
    Colour: Colour
    Pickup: Pickup
    BodyShape: BodyShape
    CreatedOn: str
    ImageUrls: Any  # Not sure what this is?

    @staticmethod
    def from_json(data: Dict, context=None) -> "Product":
        """Deserialise the json representation of the object"""

        data = data.copy()
        if context is None:
            ctx = f"{context}:Product"
        else:
            ctx = "Product"
        ret = Product(
            try_get(data, "SKU_ID", str, ctx),
            try_get(data, "ASN", str, ctx),
            try_get(data, "Category", str, ctx),
            try_get(data, "Online", bool, ctx),
            try_get(data, "ItemName", str, ctx),
            try_get(data, "Title", str, ctx),
            try_get(data, "BrandName", str, ctx),
            get_typed(data, "Description", str, ctx) or "",
            try_get(data, "ProductDetail", str, ctx),
            try_get(data, "SalesPrice", float, ctx),
            try_get(data, "PictureMain", str, ctx),
            try_get(data, "QtyInStock", int, ctx),
            try_get(data, "QtyOnOrder", int, ctx),
            Colour.from_json(try_get(data, "Colour", int, ctx)),
            Pickup.from_json(try_get(data, "Pickup", int, ctx)),
            BodyShape.from_json(try_get(data, "BodyShape", int, ctx)),
            try_get(data, "CreatedOn", str, ctx),
            get_typed(data, "ImageUrls", object, ctx),
        )
        assert len(data) == 0, f"Leftover data {data}"
        return ret

    @staticmethod
    def load_api() -> List["Product"]:
        """Load the product list from the server"""

        response = requests.get("https://www.guitarguitar.co.uk/hackathon/products/")

        if response.status_code != 200:
            raise ApiError(
                f"Couldn't contact server for products: {response.status_code} {response.content}"
            )

        data = response.json()

        if not type(data) == list:
            raise ApiError("Products response was not json list")

        return [Product.from_json(entry) for entry in data]


@dataclass(frozen=True)
class Order:
    """Accessor for the API Order object"""

    Id: int
    CustomerId: int
    ShippingAddress: Address
    Products: List[Product]
    DateCreated: str
    OrderTotal: float
    OrderStatus: OrderStatus

    @staticmethod
    def from_json(data: Dict) -> "Order":
        """Deserialise the json representation of the object"""

        data = data.copy()
        ctx = "Order"
        ret = Order(
            try_get(data, "Id", int, ctx),
            try_get(data, "CustomerId", int, ctx),
            Address.from_json(try_get(data, "ShippingAddress", dict, ctx), "Order"),
            [
                Product.from_json(entry, "Order")
                for entry in try_get(data, "Products", list, ctx)
            ],
            try_get(data, "DateCreated", str, ctx),
            try_get(data, "OrderTotal", float, ctx),
            OrderStatus(try_get(data, "OrderStatus", int, ctx)),
        )
        assert len(data) == 0, f"Leftover data {data}"
        return ret

    @staticmethod
    def load_api() -> List["Order"]:
        """Load the order lsit from the server"""

        response = requests.get("https://www.guitarguitar.co.uk/hackathon/orders/")

        if response.status_code != 200:
            raise ApiError(
                f"Couldn't contact server for orders: {response.status_code} {response.content}"
            )

        data = response.json()

        if not type(data) == list:
            raise ApiError("Orders response was not json list")

        return [Order.from_json(entry) for entry in data]
